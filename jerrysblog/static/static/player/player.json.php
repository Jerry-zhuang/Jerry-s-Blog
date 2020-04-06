<?php
/**
 * Theme player api analysis function file
 * @package Louie
 * @since Theme version 1.0.8
 */
require 'api.php';

/**
 * jsonFormat
 */
function jsonFormat( $data, $indent = null ) {
    array_walk_recursive($data, 'jsonFormatProtect');
    $data = json_encode($data);
    $data = urldecode($data);
    $ret = '';
    $pos = 0;
    $length = strlen($data);
    $indent = isset($indent)? $indent : '    ';
    $newline = "\n";
    $prevchar = '';
    $outofquotes = true;
    for($i=0; $i<=$length; $i++){
        $char = substr($data, $i, 1);
        if($char=='"' && $prevchar!='\\'){
            $outofquotes = !$outofquotes;
        }elseif(($char=='}' || $char==']') && $outofquotes){
            $ret .= $newline;
            $pos --;
            for($j=0; $j<$pos; $j++){
                $ret .= $indent;
            }
        }
        $ret .= $char;
        if(($char==',' || $char=='{' || $char=='[') && $outofquotes){
            $ret .= $newline;
            if($char=='{' || $char=='['){
                $pos ++;
            }
            for($j=0; $j<$pos; $j++){
                $ret .= $indent;
            }
        }
        $prevchar = $char;
    }
    return $ret;
}  
  
/**
 * 数组urlencode
 */
function jsonFormatProtect( $val ){
    if($val!==true && $val!==false && $val!==null){
        $val = urlencode($val);
    }
}

/**
* MP3链接
* 返回 url
*/
function song( $id, $source ) {
    $cacheKey = "/$source/song_url/$id";
    $url = get_cache($cacheKey);
    if ($url) {
        return $url;
    }

    $API = new \Metowolf\Meting($source);

    $cookies = get_option('bgm_options')['netease_cookies'];
    if (!empty($cookies) && $source == "netease") $API->cookie($cookies);

    $url = json_decode($API->format(true)->url($id), true)['url'];
    if ($source == 'netease') {
        $url = str_replace('http://m7.', 'http://m9.', $url);
        $url = str_replace('http://m7c.', 'http://m9.', $url);
        $url = str_replace('http://m8c.', 'http://m9.', $url);
        $url = str_replace('http://m8.', 'http://m9.', $url);
        $url = str_replace('http://m9.', 'https://m9.', $url);
        $url = str_replace('http://m10', 'https://m10', $url);
    }
    if ($source == 'xiami' || $site == 'tencent') {
        $url = str_replace('http://', 'https://', $url);
    }
    if ($source == 'baidu') {
        $url = str_replace('http://zhangmenshiting.qianqian.com', 'https://gss3.baidu.com/y0s1hSulBw92lNKgpU_Z2jR7b2w6buu', $url);
    }
    
    set_cache($cacheKey, $url, 0.25);
    return $url;
}

/**
* 专辑图片
* 返回 url
*/
function cover( $id, $source ) {
    $cacheKey = "/$source/cover_url/$id";
    $url = get_cache($cacheKey);
    if ($url) {
        return $url;
    }

    $API = new \Metowolf\Meting($source);
    $cookies = get_option('bgm_options')['netease_cookies'];
    if (!empty($cookies) && $source == "netease") $API->cookie($cookies);

    $url = json_decode($API->format(true)->pic($id), true)['url'];

    set_cache($cacheKey, $url, 168);
    return $url;
}

/**
* 搜索功能
* 返回 id, name, artist, pic_id
*/
function search( $msg, $source, $page ) {
    $API = new \Metowolf\Meting($source);
    $data = json_decode($API->format(true)->search($msg,$page), true); // page = 1, limit = 30
    if ($data) {
        foreach ($data as $key => $song) {
            $json .= jsonFormat(array(
                'title' =>$song['name'],
                'artist' => $song['artist'][0],
                'pid' => $song['pic_id'],
                'mid' => $song['id'],
                'source' => $song['source']
                )
            );
            $json .=',';
        }

        return $json;
    }
}

/**
* 歌单
* 返回 id, name, artist, pic_id
*/
function data_playlist( $id, $source ) {
    $API = new \Metowolf\Meting($source);
    $result = json_decode( $API->format(true)->playlist($id) );
    return $result;
}

/**
* 专辑
* 返回 id, name, artist, pic_id
*/
function data_album( $id, $source ) {
    $API = new \Metowolf\Meting($source);
    $result = json_decode( $API->format(true)->album($id) );
    return $result;
}

/**
 * 输出JSON
 */  
function json( $id, $type, $source, $num ) {
    $cacheKey = "/$source/$type/$id";
    $json = get_cache($cacheKey);
    if ($json) {
        return $json;
    }
    switch ( $type ) {
        case 0:
            $data = data_playlist($id, $source);
            break;
        case 1:
            $data = data_album($id, $source);
            break;
    }
    if ( !empty($data) ) {
        $count = 0;
        foreach ($data as $key => $song) {
            ++$count;
            $json .= jsonFormat(
                array(
                'title' =>$song->name,
                'artist' => $song->artist[0],
                'pid' => $song->pic_id,
                'mid' => $song->id,
                'tid' => $song->lyric_id,
                'source' => $song->source
                )
            );
            $json .=',';
            if ($count == $num && $num > 0) break;
        }
        set_cache($cacheKey, $json, 0.25);
        return $json;
    }
}

/**
* 曲库源转中文
* 返回 source
*/
function source_switch( $source ) {
    switch ($source) {
        case 'netease':
            $source = '网易云音乐';
            break;
        case 'tencent':
            $source = 'QQ音乐';
            break;
        case 'xiami':
            $source = '虾米音乐';
            break;
        case 'kugou':
            $source = '酷狗音乐';
            break;
        case 'baidu':
            $source = '百度音乐';
            break;
    }

    return $source;
}

/**
* 曲库源链接
* 返回 link
*/
function official_link( $id, $source, $type ) {
    $sheet = 'playlist';
    if ($source == 'netease') {
        if ($type == $sheet)
            $link = 'https://music.163.com/#/playlist?id='.$id;
        else
            $link = 'https://music.163.com/#/album?id='.$id;
    }
    elseif ($source == 'tencent') {
        if ($type == $sheet)
            $link = 'https://y.qq.com/n/yqq/playlist/'.$id.'.html';
        else
            $link = 'https://y.qq.com/n/yqq/album/'.$id.'.html';
    }
    elseif ($source == 'xiami') {
        if ($type == $sheet)
            $link = 'https://www.xiami.com/collect/'.$id;
        else
            $link = 'https://www.xiami.com/album/'.$id;
    }
    elseif ($source == 'kugou') {
        if ($type == $sheet)
            $link = 'http://www.kugou.com/yy/special/single/'.$id.'.html';
        else
            $link = 'http://www.kugou.com/yy/album/single/'.$id.'.html';
    }
    elseif ($source == 'baidu') {
        if ($type == $sheet)
            $link = 'http://music.baidu.com/songlist/'.$id;
        else
            $link = 'http://music.baidu.com/album/'.$id;
    }

    return $link;
}

/**
 * music ajax json
 */
add_action( 'init', 'ajax_music_info' );
function ajax_music_info() {
    if ( $_GET['action'] == 'ajax_music_info' && 'GET' == $_SERVER['REQUEST_METHOD'] ) : 
        $mid = $_GET['mid'];
        $pid = $_GET['pid'];
        $source = $_GET['source'];
        $song_url = song($mid, $source);
        $cover_url = cover($pid, $source);
        if ($source) {
            echo '{"song_url":"'.$song_url.'","cover_url":"'.$cover_url.'"}';
        }
        die();
    endif;
}

function get_cache($key) {
    $cache = get_transient($key);
    return $cache === false ? false : json_decode($cache, true);
}

function set_cache($key, $value, $hour = 0.1) {
    $value = json_encode($value);
    set_transient($key, $value, 60 * 60 * $hour);
}

function clear_cache($key) {
    //delete_transient($key);
}