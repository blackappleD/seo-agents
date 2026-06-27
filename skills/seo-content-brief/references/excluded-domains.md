# 排除的竞争对手域

> 本文件是 `seo-agents` 的中文详细参考，已按当前项目能力边界适配。命令名、API 名、Schema 类型、JSON 字段和专用 SEO 术语按需保留英文。

## 来源说明

- 原始注释：Updated: 2026-04-17

在分析 SERP 的竞争对手评分时，请过滤掉这些域。即使他们对目标关键词进行排名，他们也不是真正的商业竞争对手。

## 百科全书和参考网站
- wikipedia.org、britannica.com、investopedia.com、dictionary.com、merriam-webster.com、webmd.com、healthline.com、mayoclinic.org

## 社交媒体平台
- facebook.com、instagram.com、twitter.com、x.com、linkedin.com、pinterest.com、tiktok.com、youtube.com、reddit.com、quora.com、threads.net

## 内容平台和博客
-medium.com、substack.com、blogger.com、wordpress.com、wix.com、squarespace.com、hubpages.com、tumblr.com

## 搜索引擎
- google.com、bing.com、yahoo.com、duckduckgo.com、baidu.com

## 市场和电子商务聚合商
- amazon.com、amazon.com.au、amazon.co.uk、ebay.com、ebay.com.au、etsy.com、shopify.com、alibaba.com、gumtree.com.au、kogan.com

## 论坛和问答
- stackoverflow.com、stackexchange.com、whirlpool.net.au、superuser.com、serverfault.com

## 新闻和媒体
- bbc.com、bbc.co.uk、cnn.com、news.com.au、abc.net.au、theguardian.com、forbes.com、techcrunch.com、theverge.com、mashable.com、huffpost.com、nytimes.com、washingtonpost.com

## 数据和研究平台
- statista.com、ibisworld.com、similarweb.com

## 目录、评论和列表
-maps.google.com、tripadvisor.com、yelp.com、trustpilot.com、yellowpages.com.au、bark.com、thumbtack.com、angi.com、homeadvisor.com、truelocal.com.au、hotfrog.com.au、productreview.com.au

## 比较和聚合网站
- finder.com.au、canstar.com.au、iselect.com.au、mozo.com.au、comparethemarket.com.au、cmsmarket.com

## 求职板
-seek.com.au、indeed.com、glassdoor.com、jora.com、linkedin.com/jobs

## SEO 和营销工具页面
- semrush.com、ahrefs.com、moz.com、neilpatel.com、backlinko.com、searchengineland.com、searchenginejournal.com、yoast.com、尖叫青蛙.co.uk、majestic.com

## 人工智能平台
- chat.openai.com、chatgpt.com、claude.ai、perplexity.ai、gemini.google.com、copilot.microsoft.com

## 政府域名
- 任何以 .gov、.gov.au、.gov.uk、.gov.nz、.gc.ca 结尾的域名

## 学术领域
- 任何以 .edu、.edu.au、.ac.uk、.ac.nz 结尾的域名

## 要排除的 URL 路径模式

即使在其他有效的竞争对手域上，也要排除包含以下内容的 URL：
- `/tag/`、`/tags/`、`/author/`、`/category/`、`/archive/`
- `/feed/`、`/rss/`、`/wp-json/`、`/wp-admin/`
- `/login`、`/signup`、`/register`、`/cart`、`/checkout`
- `/terms`、`/privacy`、`/cookie-policy`、`/disclaimer`
- `/sitemap`、`/robots.txt`

## 如何使用此列表

1. 获取 SERP 结果后，根据这些域检查每个 URL
2. 在为竞争对手评分之前删除所有匹配项
3. 如果剩下的真正竞争对手少于 3 个，请注意竞争格局的薄弱
4. 切勿将已过滤的域名计入竞争对手分析表中

## 本项目适配边界

- 当前 `seo-agents backlinks ...` 是离线占位，不抓取真实外链。
- 没有用户导出或 provider 数据时，不要编造 referring domains、spam score、toxic ratio 或链接来源。
