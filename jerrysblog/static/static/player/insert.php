<section id="insert-music">
	<div class="insert-music-content">
		<h3>添加文章歌单</h3>
		<div class="help-text">* 使用该功能必须开启播放器。</div>
		<div id="text-input">
			<p class="music-id">
				<span>ID号：</span><input type="text" name="musicID" id="musicID" value="" size="30" placeholder="必填，填写歌单或专辑的ID" />
			</p>
			<p class="music-title">
				<span>标题：</span><input type="text" name="musicTitle" id="musicTitle" value="" size="55" placeholder="必填，填写歌单或专辑的名称" />
			</p>
			<p class="music-tags">
				<span>风格：</span><input type="text" name="musicTags" id="musicTags" value="" size="55" placeholder="可选，如 摇滚、电子、古典等" />
			</p>
			<p class="music-cover">
				<span>封面：</span><input type="text" size="55" value="" name="musicCover_upload" id="musicCover" placeholder="必填，填写图片地址" /><button id="musicCover_upload" class="cover_upload_button button" href="#">添加封面</button>
			</p>
			<p class="music-num">
				<span>数量：</span><input type="number" name="musicNum" id="musicNum" value="" size="20" placeholder="必填，歌曲数量" />
			</p>
		</div>
		<p class="music-type">
			<span class="music-content-title">类型：</span>
			<label><input type="radio" name="type" value="playlist" checked="checked" />歌单</label>
			<label><input type="radio" name="type" value="album" />专辑</label>
		</p>
		<p class="music-source">
			<span class="music-content-title">来源：</span>
			<label><input type="radio" name="source" value="netease" checked="checked" />网易云</label>
            <label><input type="radio" name="source" value="tencent" />QQ音乐</label>
            <label><input type="radio" name="source" value="xiami" />虾米音乐</label>
            <label><input type="radio" name="source" value="kugou" />酷狗音乐</label>
            <label><input type="radio" name="source" value="baidu" />百度音乐</label>
		</p>
		<p class="postdata">
			<button id="insert-data-close" class="button">取消</button>
			<button id="insert-data" class="button">插入文章</button>
		</p>
	</div>
</section>