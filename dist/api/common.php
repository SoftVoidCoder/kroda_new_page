<?php
declare(strict_types=1);

const MAIL_TO = 'zayavka@korda.spb.ru';
const MAIL_FROM = 'korda57627@bitrix400.timeweb.ru';
const MAX_FILE_SIZE = 10 * 1024 * 1024;
const MAX_TOTAL_SIZE = 20 * 1024 * 1024;
const FILE_MIME = [
    'pdf' => ['application/pdf'],
    'doc' => ['application/msword', 'application/CDFV2', 'application/octet-stream'],
    'docx' => ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/zip', 'application/octet-stream'],
    'xls' => ['application/vnd.ms-excel', 'application/CDFV2', 'application/octet-stream'],
    'xlsx' => ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/zip', 'application/octet-stream'],
    'jpg' => ['image/jpeg'],
    'jpeg' => ['image/jpeg'],
    'png' => ['image/png'],
    'webp' => ['image/webp'],
];

date_default_timezone_set('Europe/Moscow');

function clean_text(mixed $value, int $max = 1500): string
{
    $text = trim((string)$value);
    $text = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $text) ?? '';
    return mb_substr($text, 0, $max);
}

function json_reply(int $status, array $payload): never
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    exit;
}

function enforce_post(): void
{
    if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
        json_reply(405, ['ok' => false, 'error' => 'Метод не поддерживается']);
    }
}

function check_honeypot(): void
{
    if (clean_text($_POST['website'] ?? '', 100) !== '') {
        json_reply(200, ['ok' => true]);
    }
}

function throttle(string $form): string
{
    $ip = clean_text($_SERVER['REMOTE_ADDR'] ?? 'unknown', 80);
    $lock = sys_get_temp_dir() . '/korda_' . $form . '_' . hash('sha256', $ip) . '.lock';
    if (is_file($lock) && time() - (int)filemtime($lock) < 20) {
        json_reply(429, ['ok' => false, 'error' => 'Заявка уже отправлена. Подождите немного']);
    }
    return $lock;
}

function flatten_fields(mixed $value, string $prefix = ''): array
{
    if (!is_array($value)) {
        $text = clean_text($value);
        return $text === '' ? [] : [$prefix . ': ' . $text];
    }
    $lines = [];
    foreach ($value as $key => $item) {
        $name = $prefix === '' ? (string)$key : $prefix . '.' . $key;
        array_push($lines, ...flatten_fields($item, $name));
    }
    return $lines;
}

function uploaded_files(string $field): array
{
    if (!isset($_FILES[$field])) return [];
    $source = $_FILES[$field];
    $names = is_array($source['name']) ? $source['name'] : [$source['name']];
    $tmp = is_array($source['tmp_name']) ? $source['tmp_name'] : [$source['tmp_name']];
    $sizes = is_array($source['size']) ? $source['size'] : [$source['size']];
    $errors = is_array($source['error']) ? $source['error'] : [$source['error']];
    $files = [];
    $total = 0;
    foreach ($names as $index => $name) {
        if (($errors[$index] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) continue;
        $size = (int)($sizes[$index] ?? 0);
        $path = (string)($tmp[$index] ?? '');
        if (($errors[$index] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK || $size <= 0 || $size > MAX_FILE_SIZE || !is_uploaded_file($path)) {
            json_reply(422, ['ok' => false, 'error' => 'Один из файлов не загрузился или превышает 10 МБ']);
        }
        $total += $size;
        if ($total > MAX_TOTAL_SIZE) json_reply(422, ['ok' => false, 'error' => 'Общий размер файлов превышает 20 МБ']);
        $ext = strtolower(pathinfo((string)$name, PATHINFO_EXTENSION));
        $mime = (new finfo(FILEINFO_MIME_TYPE))->file($path);
        if (!isset(FILE_MIME[$ext]) || $mime === false || !in_array($mime, FILE_MIME[$ext], true)) {
            json_reply(422, ['ok' => false, 'error' => 'Недопустимый тип вложения']);
        }
        $data = file_get_contents($path);
        if ($data === false) json_reply(500, ['ok' => false, 'error' => 'Не удалось прочитать вложение']);
        $files[] = ['name' => 'attachment-' . (count($files) + 1) . '.' . $ext, 'mime' => $mime, 'data' => $data];
    }
    return $files;
}

function send_message(string $subject, array $lines, array $files = []): bool
{
    $text = implode("\n", $lines) . "\n\nОтправлено с сайта КОРДА: " . date('d.m.Y H:i');
    $headers = [
        'From: =?UTF-8?B?' . base64_encode('Сайт КОРДА') . '?= <' . MAIL_FROM . '>',
        'MIME-Version: 1.0',
    ];
    if ($files) {
        $boundary = 'korda_' . bin2hex(random_bytes(12));
        $headers[] = 'Content-Type: multipart/mixed; boundary="' . $boundary . '"';
        $body = '--' . $boundary . "\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
            . chunk_split(base64_encode($text));
        foreach ($files as $file) {
            $body .= '--' . $boundary . "\r\nContent-Type: {$file['mime']}; name=\"{$file['name']}\"\r\n"
                . "Content-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename=\"{$file['name']}\"\r\n\r\n"
                . chunk_split(base64_encode($file['data']));
        }
        $body .= '--' . $boundary . '--';
    } else {
        $headers[] = 'Content-Type: text/plain; charset=UTF-8';
        $headers[] = 'Content-Transfer-Encoding: base64';
        $body = chunk_split(base64_encode($text));
    }
    if (getenv('KORDA_MAIL_DRY_RUN') === '1') return true;
    return mail(MAIL_TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers));
}
