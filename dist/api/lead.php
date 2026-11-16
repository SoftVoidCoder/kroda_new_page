<?php
declare(strict_types=1);
require __DIR__ . '/common.php';

enforce_post();
$payload = json_decode((string)file_get_contents('php://input'), true);
if (!is_array($payload)) json_reply(400, ['ok' => false, 'error' => 'Некорректный запрос']);
$_POST = $payload;
check_honeypot();
$lock = throttle('lead');

$name = clean_text($payload['name'] ?? '', 100);
$phone = clean_text($payload['phone'] ?? '', 40);
$message = clean_text($payload['message'] ?? '');
$requestType = clean_text($payload['requestType'] ?? 'Заявка с сайта', 120);
if ($name === '' || strlen(preg_replace('/\D/', '', $phone) ?? '') < 7 || ($payload['consent'] ?? '') !== 'on') {
    json_reply(422, ['ok' => false, 'error' => 'Заполните имя, телефон и согласие']);
}

$lines = ['Тип заявки: ' . $requestType, 'Имя: ' . $name, 'Телефон: ' . $phone, 'Комментарий: ' . ($message ?: '—')];
if (!send_message('Новая заявка с сайта КОРДА', $lines)) {
    json_reply(500, ['ok' => false, 'error' => 'Почтовый сервер не принял заявку']);
}
touch($lock);
json_reply(200, ['ok' => true]);
