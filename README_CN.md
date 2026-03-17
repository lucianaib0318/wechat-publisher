<p align="center">
  <h1 align="center">WeChat Publisher</h1>
  <p align="center">
    Markdown 一键转微信公众号草稿，直达草稿箱。
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skills-blue?style=flat-square" alt="OpenClaw Skills" />
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/License-MIT-brightgreen?style=flat-square" alt="License MIT" />
  <img src="https://img.shields.io/badge/Platform-WeChat%20MP-orange?style=flat-square" alt="WeChat MP" />
  <img src="https://img.shields.io/badge/Status-草稿箱✅-success?style=flat-square" alt="Status" />
</p>

> ✅ **已验证**：可正常发布到微信公众号草稿箱

---

## 简介

**WeChat Publisher** 是一个微信公众号草稿创建工具，将 Markdown 文档自动转换为微信公众号兼容的 HTML 格式（纯内联样式），并通过微信官方 API 创建草稿到草稿箱。

```
Markdown ──▶ HTML ──▶ 微信公众号草稿箱
```

## 特性

- ✅ **一键创建草稿** — Markdown 输入，草稿箱输出
- ✅ **中文支持** — 完美支持中文字符，无乱码
- ✅ **自动封面** — 支持自动生成 900x500 封面图
- ✅ **内联样式** — 所有 CSS 内联，兼容微信渲染引擎
- ✅ **长度限制** — 自动处理标题（≤64 字）和摘要（≤120 字）限制
- ✅ **MacOS 代码块** — 支持代码块样式渲染

---

## 快速开始

### 环境要求

- Python 3.8+
- 微信公众号 AppID 和 AppSecret

### 安装

```bash
git clone https://github.com/lucianaib0318/wechat-publisher.git
cd wechat-publisher
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 获取微信公众号 AppID 和 AppSecret

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入 **开发** → **基本配置**
3. 找到 **AppID**（应用ID）
4. 点击 **AppSecret**（应用密钥）旁边的 **生成** 按钮
5. 立即复制 AppSecret（仅显示一次）

> **重要**：如果在云服务器上运行，需要将服务器 IP 添加到 **IP 白名单**。

---

## 使用方法

### 方式 1：从 Markdown 文件发布（推荐）

```bash
python3 publisher.py \
  --appid "wx36ba9f59df0d6313" \
  --secret "ae71bf50f7217042e639b44fb57d5529" \
  --article article.md \
  --author "昌哥" \
  --no-cover
```

### 方式 2：直接输入标题和内容

```bash
python3 publisher.py \
  --appid "YOUR_APPID" \
  --secret "YOUR_SECRET" \
  --title "文章标题" \
  --content "<section>文章内容</section>" \
  --author "昌哥" \
  --no-cover
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--appid` | 是 | 微信公众号 AppID |
| `--secret` | 是 | 微信公众号 AppSecret |
| `--article` | 否 | Markdown 文章文件路径 |
| `--title` | 否 | 文章标题（与 --content 配合使用） |
| `--content` | 否 | 文章内容（HTML 格式） |
| `--author` | 否 | 作者名（默认：昌哥） |
| `--image` | 否 | 自定义封面图片路径 |
| `--no-cover` | 否 | 使用默认封面（推荐） |

---

## 测试状态

| 测试项目 | 状态 | 备注 |
|----------|------|------|
| **草稿创建** | ✅ 正常 | 2026-03-17 验证 |
| **封面上传** | ✅ 正常 | 支持自动生成 900x500 封面 |
| **Markdown 渲染** | ✅ 正常 | 微信兼容内联样式 |
| **中文编码** | ✅ 正常 | 无乱码 |
| **标题/摘要** | ✅ 正常 | 自动处理长度限制 |
| **长文测试** | ✅ 正常 | 2900 字文章测试通过 |

> 💡 **提示**：文章创建草稿后，需手动在微信公众号后台发布。

---

## 项目结构

```
wechat-publisher/
├── publisher.py           # 主程序
├── requirements.txt       # Python 依赖
├── README.md              # 英文文档
├── README_CN.md           # 中文文档
├── SKILL.md               # OpenClaw 技能定义
├── LICENSE                # MIT 许可证
└── examples/              # 示例文件
    ├── article.md         # 示例文章
    └── test-article.md    # 测试文章
```

---

## Markdown 语法支持

### 标题

```markdown
# 一级标题
## 二级标题
### 三级标题
```

### 文本格式

```markdown
**粗体文本**
*斜体文本*
> 引用文本
```

### 列表

```markdown
- 列表项 1
- 列表项 2
- 列表项 3
```

### 代码块

````markdown
```python
print("Hello, WeChat!")
```
````

---

## 常见问题

### Q: 为什么只显示创建草稿，不自动发布？

A: 自动发布需要微信公众号的"群发接口"权限，个人订阅号默认没有此权限。创建草稿后，需手动在公众号后台发布。

### Q: 中文显示为乱码怎么办？

A: 已修复中文编码问题（v1.1.0+）。请确保使用最新版本，工具会自动处理 UTF-8 编码。

### Q: 封面图有什么要求？

A: 建议尺寸 900x500 像素（16:9），最小 200x200 像素。可以使用 `--no-cover` 参数自动生成默认封面。

### Q: 标题或摘要太长怎么办？

A: 工具会自动截断：标题≤64 字，摘要≤120 字。

### Q: 如何查看草稿？

A: 登录 [微信公众号后台](https://mp.weixin.qq.com/) → 草稿箱，即可看到创建的草稿。

---

## 更新日志

### v1.1.0 (2026-03-17)

- 🐛 修复中文乱码问题（ensure_ascii=False）
- ✨ 代码优化与重构
- 📝 完善文档和类型提示
- 📦 改进错误处理

### v1.0.0 (2026-03-16)

- ✨ 初始版本发布
- ✅ 支持 Markdown 转微信 HTML
- ✅ 支持自动封面生成
- ✅ 支持草稿箱创建

---

## 许可证

[MIT](./LICENSE)

---

## 作者

**LucianaiB** ([@lucianaib0318](https://github.com/lucianaib0318))

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by LucianaiB

</div>
