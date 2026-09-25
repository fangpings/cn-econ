# 中国宏观经济：从经济数字到运行机制

以 us-econ 为前置的中国经济进阶对照教材。主体是中国的制度、数据生成和中美差异；共通基础知识通过章节开头的前置阅读衔接。

从[教材目录](textbook/README.md)开始阅读。第一、二模块（第 01—12 章）已于 2026-09-23 按上述定位重写，包含正文、逐步算例、官方资料带读、练习及折叠参考答案。第二模块另附中美对照简报审计作业。第三模块（第 13—15 章）已于 2026-09-24 完成，聚焦中国 CPI、工业 PPI 与低通胀传导，附中美价格简报审计作业。其余模块保留总体规划。

在线阅读：<https://fangpings.github.io/cn-econ/>。

阅读站使用 VitePress，提供中文全文搜索、章节导航、页内目录、深浅色模式与窄屏布局。教材源文件位于 `textbook/`。

## 本地阅读与构建

安装 Node.js 22 后，在项目目录运行：

```sh
npm ci
npm run dev
```

打开 <http://127.0.0.1:5173/cn-econ/>。若 us-econ 已占用该端口，可运行 `npm run dev -- --port 5174`。

```sh
npm run build
npm run preview
```

静态预览默认地址为 <http://127.0.0.1:4173/cn-econ/>。构建产物位于 `textbook/.vitepress/dist/`，不提交到仓库。

## 更新与发布

修改 `textbook/*.md` 后推送到 `main`，GitHub Actions 会自动构建并发布 GitHub Pages。也可从 Actions 手动运行发布工作流。Pages 使用 GitHub Actions 作为构建来源。

首页复用 `textbook/README.md`；侧栏按文件编号自动分组，仅显示已有章节。新增第 01—32 章范围内的章节会自动纳入相应模块。发布前运行 `npm run build` 检查站内链接。
