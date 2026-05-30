# md2wechat 📱

**Markdown → WeChat Official Account Article Converter**

将Markdown格式文章一键转换为完美的微信公众号文章HTML。适合自媒体人、技术博主、运营编辑使用。

## 🎯 它能帮你什么？

如果你经常写公众号文章，但：
- ❌ 厌倦了在公众号编辑器里手动排版
- ❌ 想把博客/笔记直接发到公众号
- ❌ 需要保持代码高亮的排版效果

**md2wechat** 一键帮你搞定！

## ✨ 功能特点

| 功能 | 效果 |
|------|------|
| 代码高亮 | ✅ 完美的 `<pre><code>` 格式 |
| 微信公众号样式 | ✅ 自动内联CSS，直接粘贴可用 |
| Markdown表格 | ✅ 带边框和表头样式 |
| 引用块 | ✅ 左侧灰色竖线样式 |
| 图片 | ✅ 自动居中 |
| 浏览器预览 | ✅ `--preview` 实时查看效果 |
| 剪贴板 | ✅ `--copy` 一键复制 |

## 🚀 一分钟上手

```bash
# 1. 准备你的Markdown文章
# 2. 转换为微信公众号HTML
python md2wechat.py article.md -o article.html

# 3. 预览效果
python md2wechat.py article.md --preview

# 4. 复制到剪贴板
python md2wechat.py article.md --copy

# 5. 打开 article.html，全选复制到公众号编辑器即可！
```

## 📝 示例对比

### 输入 (article.md)
```markdown
# 我的第一篇公众号文章

今天我们来聊聊 **Python编程**。

## 代码示例

\`\`\`python
def hello():
    print("Hello WeChat!")
\`\`\`

> 这是一段引用
```

### 输出
自动生成带微信风格的完美HTML，打开直接复制到公众号后台即可。

## 📦 安装

```bash
# 方式一：直接下载
git clone https://github.com/chengjunhua465-create/md2wechat.git
cd md2wechat

# 方式二：pip安装（即将支持）
pip install md2wechat
```

## 🛠 命令行选项

| 选项 | 说明 |
|------|------|
| `input.md` | 输入的Markdown文件 |
| `-o output.html` | 输出HTML文件 |
| `--preview` | 在浏览器中预览 |
| `--copy` | 复制到剪贴板 |
| `--version` | 显示版本号 |

## ☕ 支持我

如果这个工具帮到了你，欢迎请我喝杯咖啡 ☕
- [GitHub Sponsors](https://github.com/sponsors/chengjunhua465-create)
- 微信打赏：联系作者

## 📄 License

MIT © ChengJunhua
