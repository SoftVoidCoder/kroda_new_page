<?php
declare(strict_types=1);
require __DIR__ . '/common.php';

enforce_post();
check_honeypot();
$lock = throttle('questionnaire');

$type = clean_text($_POST['questionnaire_type'] ?? '', 40);
$object = clean_text($_POST['object_name'] ?? '', 200);
$contact = clean_text($_POST['contacts'][0]['name'] ?? '', 100);
$phone = clean_text($_POST['contacts'][0]['phone'] ?? '', 40);
$email = clean_text($_POST['contacts'][0]['email'] ?? '', 150);
if (($type === '') || $object === '' || $contact === '' || ($phone === '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) || ($_POST['consent'] ?? '') !== 'on') {
    json_reply(422, ['ok' => false, 'error' => 'Заполните объект, контакт, телефон или e-mail и согласие']);
}

$labels = ['pipelines' => 'трубопроводам', 'tanks' => 'резервуарам', 'roof' => 'кровле', 'open-areas' => 'открытым площадям'];
if (!isset($labels[$type])) json_reply(422, ['ok' => false, 'error' => 'Неизвестный тип опросного листа']);
$fields = $_POST;
unset($fields['website'], $fields['consent']);
$lines = ['Опросный лист по ' . $labels[$type]];
array_push($lines, ...flatten_fields($fields));
$files = uploaded_files('attachments');
if (!send_message('Опросный лист КОРДА: ' . $object, $lines, $files)) {
    json_reply(500, ['ok' => false, 'error' => 'Почтовый сервер не принял опросный лист']);
}
touch($lock);
header('Location: ../spasibo.html?source=questionnaire', true, 303);
exit;
