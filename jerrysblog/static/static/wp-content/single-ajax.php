
<main id="main" class="overlay-main width-full" role="main" itemprop="mainContentOfPage" itemscope itemtype="http://schema.org/Blog">
	<div id="primary" class="content">
		<?php while ( have_posts() ) : the_post(); $cats = get_the_category(); ?>
		<?php $meta = get_post_meta( get_the_ID(), 'standard_post_options', true );
			if (!empty($meta)) {
				$shadow = $meta['img_shadow'] ? 'shadow' : '';
				$max = $meta['img_normal'] ? 'normal' : '';
			} ?>
		<article id="post-<?php the_ID(); ?>" <?php post_class(); ?> itemscope itemtype="http://schema.org/BlogPosting" itemprop="blogPost">
			<header class="entry-header">
				<?php the_title( '<h1 class="title" itemprop="name">', '</h1>' ); ?>
				<div class="meta">发布于 <time itemprop="datePublished" datetime="<?php echo get_the_date('c');?>"><?php echo get_post_time('Y-m-d H:i'); ?></time> / <a href="<?php echo esc_url( get_category_link( $cats[0]->term_id ) );?>"><?php echo $cats[0]->name; ?></a> / <?php comments_popup_link('0 条评论', '1 条评论', '% 条评论'); ?></div>
			</header>
			<div class="entry-content <?php echo $shadow.' ' .$max; ?>" itemprop="articleBody">
				<?php the_content(); ?>
			</div>
			<?php post_tags(); ?>
			<footer class="entry-footer">
				<?php share(); set_like(); ?>
				<div class="trends">
					<ul class="items state">
						<li class="item views">
							<span class="state-title">浏览</span>
							<span class="state-count"><?php echo get_views(get_the_ID()); ?></span>
						</li>
						<li class="item likes">
							<span class="state-title">喜欢</span>
							<span class="state-count"><?php echo get_like(); ?></span>
						</li>
					</ul>
					<ul class="items tourist">
						<?php comment_tourist(get_the_ID()); ?>
					</ul>
				</div>
			</footer>
			<?php post_copyright(); ?>
		</article>
		<?php endwhile; wp_reset_query(); ?>
	</div>
	<?php comments_template(); ?>
</main>