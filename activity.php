<?php

require_once('./vendor/autoload.php');
require_once('./key.php');

$client = new \Goutte\Client();

$url_login = 'https://marco.ms.dendai.ac.jp/PTDU79130R/AX0301.aspx';
$page_login = $client->request('GET', $url_login);
echo $page_login->filter('title', 0)->text();

