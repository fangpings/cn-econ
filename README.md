# 中国宏观经济：从经济数字到运行机制

以 us-econ 为前置的中国经济进阶对照教材。主体是中国的制度、数据生成和中美差异；共通基础知识通过章节开头的前置阅读衔接。

从[教材目录](textbook/README.md)开始阅读。九个模块均已完成，最后更新于 2026-10-03：统计与账户入口、实体经济、价格、货币融资、财政与市场、开放经济、股票市场、房地产、综合实践。

股票模块（30—35）从指数、财报和融资制度讲到长期股东回报，检验“三千点与基本面”叙事；房地产模块（36—41）连续解释开发交付、房价、按揭、土地财政、项目风险及宏观再平衡。综合实践（42—44）包含历史诊断、可运行的数据版本练习、月报材料与完整参考分析。[研究工具箱](textbook/appendix-research-kit.md)提供中美指标映射、时间线、注册表及报告模板。

章节以美国篇为前置，含中国原始资料带读、算例和折叠答案。历史数据、制度版本和教学假设分别标明。原第 11 章迁入第 36 章，旧链接保留跳转；其他已发布章节路径不变。

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

首页复用 `textbook/README.md`；侧栏按文件编号自动分组，仅显示已有章节。新增第 01—44 章范围内的章节会自动纳入相应模块。发布前运行 `npm run build` 检查站内链接。

## 数据练习

需要 Python 3，仅使用标准库：

```sh
python3 tools/econ_lab.py --as-of 2025-06-30
python3 -m unittest discover -s tests -v
```

数据与版本说明见 [data/README.md](data/README.md)。网页第 43 章提供完整离线下载包。
