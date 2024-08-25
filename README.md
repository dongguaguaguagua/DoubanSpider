# DoubanSpider

## 原理

使用豆瓣的“快速记录我看过的影视”功能，模拟豆瓣请求，快速抓取数据。

但是豆瓣不会把所有影视给你，顶多2万条。爬取的数据将存入SQLite数据库中。

## 如何构建

本项目使用[rye](https://rye.astral.sh/)作为虚拟环境管理系统。因此需预装rye：

```bash
curl -sSf https://rye.astral.sh/get | bash
```

安装全局python，可根据喜好调节python版本

```bash
rye toolchain fetch cpython@3.12.3
```

安装虚拟环境
```bash
rye sync
```

在`config.json`中填入你的`access_token`和`udid`(这些是由登陆产生的，每人账号都不一样)

这两个值可以对豆瓣进行抓包获得。

运行主程序:

```bash
python src/recommend_movies.py
```

