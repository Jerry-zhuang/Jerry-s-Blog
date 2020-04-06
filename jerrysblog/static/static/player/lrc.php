<?php
/**
 * Theme player api analysis function file
 * @package Louie
 * @since Theme version 1.1.6
 */
require 'api.php';
error_reporting(0);

$action = $_GET['action'];
$source = $_GET['source'];
$id = $_GET['id'];

if ( $action == 'lyric' && !empty($id) ) {
	header("Content-Type: text/html;charset=UTF-8");
	// json_encode($data, JSON_UNESCAPED_UNICODE);
	//$lrc = preg_replace("#\\\u([0-9a-f]{4})#ie", "iconv('UCS-2BE', 'UTF-8', pack('H4', '\\1'))", lyric($id, $source));
	$API = new \Metowolf\Meting($source);
    $result = $API->format(true)->lyric($id);
	preg_match('|"lyric":"(.+)"|U', $result, $matches);
	$lrc = $matches[1];
	$lrc = str_replace('\n', "\n", $lrc);
	$lrc = str_replace('\r', "\r", $lrc);
	$lrc = stripslashes($lrc);
	if (strpos($lrc,']') === false) {
		echo '[ti:暂无歌词]';
	} else {
		echo $lrc;
	}
} else {
	echo '404';
}