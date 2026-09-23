import { readFileSync, readdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vitepress'

const root = fileURLToPath(new URL('../', import.meta.url))
const files = readdirSync(root).filter(file => file.endsWith('.md')).sort()
const page = (file: string) => ({
  text: (readFileSync(`${root}${file}`, 'utf8').match(/^# (.+)$/m)?.[1] ?? file),
  link: file === 'README.md' ? '/' : `/${file.replace(/\.md$/, '')}`
})
const chapters = (from: number, to: number) => files
  .filter(file => /^\d{2}[a-z]?-.+\.md$/.test(file) && Number(file.slice(0, 2)) >= from && Number(file.slice(0, 2)) <= to)
  .map(page)

// Use word segmentation for Chinese phrases and preserve English tickers/acronyms.
// The function is serialized by VitePress and runs in both indexing and querying.
function tokenize(text: string) {
  return Array.from(new Intl.Segmenter('zh-CN', { granularity: 'word' }).segment(text))
    .filter(part => part.isWordLike)
    .map(part => part.segment)
}

export default defineConfig({
  base: '/cn-econ/',
  lang: 'zh-CN',
  title: '中国宏观经济',
  description: '从经济数字到运行机制 · 与美国对照理解',
  rewrites: { 'README.md': 'index.md' },
  themeConfig: {
    siteTitle: '中国宏观经济',
    nav: [
      { text: '学习指南', link: '/' },
      { text: '开始阅读', link: '/01-economic-map' }
    ],
    sidebar: [
      { text: '课程介绍', items: [{ text: '学习指南与全书目录', link: '/' }] },
      ...([
        ['01—04 · 基础与统计口径', 1, 4],
        ['05—12 · 实体经济', 5, 12],
        ['13—15 · 价格', 13, 15],
        ['16—21 · 货币与融资', 16, 21],
        ['22—26 · 财政与市场', 22, 26],
        ['27—29 · 开放经济', 27, 29],
        ['30—32 · 综合分析与实践', 30, 32]
      ] as const).map(([text, from, to]) => ({ text, collapsed: false, items: chapters(from, to) })).filter(group => group.items.length),
      ... (files.some(file => file.startsWith('appendix-')) ? [{ text: '配套资料', collapsed: false, items: files.filter(file => file.startsWith('appendix-')).map(page) }] : [])
    ],
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一节', next: '下一节' },
    sidebarMenuLabel: '章节目录',
    darkModeSwitchLabel: '切换外观',
    lightModeSwitchTitle: '切换为浅色',
    darkModeSwitchTitle: '切换为深色',
    returnToTopLabel: '回到顶部',
    search: {
      provider: 'local',
      options: {
        miniSearch: { options: { tokenize } },
        translations: {
          button: { buttonText: '搜索教材', buttonAriaLabel: '搜索教材' },
          modal: {
            displayDetails: '显示详情',
            resetButtonTitle: '清除搜索',
            backButtonTitle: '返回',
            noResultsText: '没有找到相关内容',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
          }
        }
      }
    }
  }
})
