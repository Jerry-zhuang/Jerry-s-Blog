<?php
/**
 * Theme player setting function file
 * @package Louie
 * @since Theme version 1.0.8
 */

/**
 * 添加组件
 */
add_action( 'init', 'BGMjson' );
add_action( 'init', 'BGMdata_search' );
add_action( 'init', 'BGMdata' );
add_action( 'admin_init', 'BGMoptions' );
add_action( 'admin_enqueue_scripts', 'BGMscripts', 9999999 );
if ( object('extension_player') ) add_action( 'admin_menu', 'BGMsetting' );
function BGMscripts() {
    wp_enqueue_style( 'player-setting', THEME_URL . '/assets/css/player-setting.css', array(), THEME_VERSION, 'all' );
    wp_enqueue_script( 'init', THEME_URL . '/assets/js/init.js', array(), THEME_VERSION, true );
    wp_enqueue_script( 'setting', THEME_URL . '/assets/js/setting.js', array(), THEME_VERSION, true );
}
function BGMsetting() {
    add_menu_page('Inspire Player', 'Inspire Player', 'manage_options', __FILE__, 'BGMSettingpage');
}
function BGMoptions() {
    register_setting('bgm_setting_group', 'bgm_options');
}
function BGMjson() {
    if($_GET['action'] == 'music_json_get' && 'GET' == $_SERVER['REQUEST_METHOD']) {
        echo 'var playlist = ['.json($_GET["id"], $_GET['type'], $_GET['source']).'];';
        die();
    }

    return;
}
function BGMdata() {
    if($_GET['action'] == 'music_list_get' && 'GET' == $_SERVER['REQUEST_METHOD']) {
        $bgm = get_option('bgm_options');
        echo 'var playlist = ['.json($bgm["mid"], $bgm['type'], $bgm['source'], $bgm['num']).'];';
        die();
    }
    return;
}
function BGMdata_search() {
    if($_GET['action'] == 'music_search_get' && 'GET' == $_SERVER['REQUEST_METHOD']) {
        echo 'var playlist = ['.search($_GET["name"], $_GET['source'], $_GET['page']).'];';
        die();
    }
    return;
}
add_action( 'init', 'delete_music_data' );
function delete_music_data() {
    if($_GET['action'] == 'music_data_delete' && 'GET' == $_SERVER['REQUEST_METHOD']) {
        delete_option('bgm_options');
    }
}

/**
 * 设置页
 */
function BGMSettingpage() {
    $bgm = get_option('bgm_options');
    ?>
    <section class="setting">
        <div class="setting-inner">
            <div class="bgm-guide">
                <a href="javascript:;" id="help-btn">帮助</a>
                <a href="http://music.163.com/#/user/home?id=48486192" target="_blank">关注</a>
            </div>
            <h2 class="title">Inspire Player</h2>
            <form method="post" action="options.php" class="sava-setting">
                <select id="music-type" name="bgm_options[type]">
                    <?php if($bgm['type'] == 0) : ?>
                        <option value="0">歌单</option>
                        <option value="1">专辑</option>
                    <?php else : ?>
                        <option value="1">专辑</option>
                        <option value="0">歌单</option>
                    <?php endif; ?>
                </select> 
                <input type="text" name="bgm_options[mid]" id="mid" value="<?php echo $bgm['mid']; ?>"  placeholder="曲单ID" required />
                <input type="number" name="bgm_options[num]" id="mnum" value="<?php echo $bgm['num']; ?>"  placeholder="单曲数量" />
                <div class="checkbox-source">
                    <label><input type="radio" name="bgm_options[source]" class="source" value="netease" checked <?php checked('netease',$bgm['source']); ?> />网易云</label>
                    <label><input type="radio" name="bgm_options[source]" class="source" value="tencent" <?php checked('tencent',$bgm['source']); ?> />QQ音乐</label>
                    <label><input type="radio" name="bgm_options[source]" class="source" value="xiami" <?php checked('xiami',$bgm['source']); ?> />虾米音乐</label>
                    <label><input type="radio" name="bgm_options[source]" class="source" value="kugou" <?php checked('kugou',$bgm['source']); ?> />酷狗音乐</label>
                    <label><input type="radio" name="bgm_options[source]" class="source" value="baidu" <?php checked('baidu',$bgm['source']); ?> />百度音乐</label>
                </div>
                <p class="checkbox-menu">
                    <label><input type="checkbox" name="bgm_options[autoplay]" class="autoplay" value="on" <?php checked('on',$bgm['autoplay']); ?> />自动播放</label>
                    <label><input type="checkbox" name="bgm_options[shuffle]" class="shuffle" value="on" <?php checked('on',$bgm['shuffle']); ?> />随机播放</label>
                    <label><input type="checkbox" name="bgm_options[search]" class="search" value="on" <?php checked('on',$bgm['search']); ?> />音乐搜索(beta)</label>
                    <label><input type="checkbox" name="bgm_options[lrc]" class="lrc" value="on" <?php checked('on',$bgm['lrc']); ?> />显示歌词</label>
                    <input type="text" name="bgm_options[netease_cookies]" class="netease-cookies" value="<?php echo $bgm['netease_cookies']; ?>" placeholder="网易云音乐权限账号Cookies，不懂请不要填写"/>
                    <span>单曲数量如果留空则加载全部，由于缓存原因，修改单曲数量可能需要等待15分钟后才可生效。</span>
                    <input type="submit" name="save" class="button" value="保存设置" style="background: #1e949e;" />
                    <input type="submit" name="delete" id="deleteBgmData" class="button" value="清除数据" style="background: #ca3382;" />
                </p>
                <?php settings_fields('bgm_setting_group'); ?>
            </form>
            <?php if ( isset($_REQUEST['settings-updated']) ){
                echo '<div id="message" class="updated"><p>设置更新成功。</p></div>';
            }?>
        </div>
        <div id="music-help">
            <div id="help-close">关闭</div>
            <div class="inner">
                <h3>音乐源的ID识别</h3>
                <p>黑色背景的字符串即为曲单ID</p>
                <span>网易云音乐</span>
                <ul class="items">
                    <li class="item">歌单 http://music.163.com/#/playlist?id=<code>888657769</code></li>
                    <li class="item">专辑 http://music.163.com/#/album?id=<code>34887005</code></li>
                </ul>
                <span>QQ音乐</span>
                <ul class="items">
                    <li class="item">歌单 https://y.qq.com/n/yqq/playlist/<code>2975376768</code>.html</li>
                    <li class="item">专辑 https://y.qq.com/n/yqq/album/<code>003mSJct34FWhh</code>.html</li>
                </ul>
                <span>虾米音乐</span>
                <ul class="items">
                    <li class="item">歌单 http://www.xiami.com/collect/<code>8977607</code>?spm=a1z1s.3065917.6862697.13.rigQ7h</li>
                    <li class="item">专辑 http://www.xiami.com/album/<code>nnemr26a9ec</code>?spm=a1z1s.3057849.6862609.7.so6XxM</li>
                </ul>
                <span>酷狗音乐</span>
                <ul class="items">
                    <li class="item">歌单 http://www.kugou.com/yy/special/single/<code>26430</code>.html</li>
                    <li class="item">专辑 http://www.kugou.com/yy/album/single/<code>1917859</code>.html</li>
                </ul>
                <span>百度音乐</span>
                <ul class="items">
                    <li class="item">歌单 http://music.baidu.com/songlist/<code>504891154</code></li>
                    <li class="item">专辑 http://music.baidu.com/album/<code>332131573</code>?pst=music</li>
                </ul>
            </div>
        </div>
    </section>
<?php
}