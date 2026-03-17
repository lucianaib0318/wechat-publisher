<p align="center">
  <h1 align="center">WeChat Publisher</h1>
  <p align="center">
    Markdown to WeChat Official Account Drafts in One Click.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skills-blue?style=flat-square" alt="OpenClaw Skills" />
  <img src="https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/License-MIT-brightgreen?style=flat-square" alt="License MIT" />
  <img src="https://img.shields.io/badge/Platform-WeChat%20MP-orange?style=flat-square" alt="WeChat MP" />
  <img src="https://img.shields.io/badge/Status-Draft✅-success?style=flat-square" alt="Status" />
</p>

> ✅ **Verified**: Successfully creates drafts in WeChat Official Account

---

## What It Does

**WeChat Publisher** converts Markdown documents into WeChat-compatible HTML format (pure inline styles) and automatically creates drafts to the WeChat Official Account draft box via the official API.

```
Markdown ──▶ HTML ──▶ WeChat Draft Box
```

## Features

- ✅ **One-Click Draft Creation** — Markdown input, draft box output
- ✅ **Chinese Support** — Perfect Chinese character support, no garbled text
- ✅ **Auto Cover** — Supports automatic 900x500 cover generation
- ✅ **Inline Styles** — All CSS inline, compatible with WeChat rendering
- ✅ **Length Limits** — Auto-handles title (≤64 chars) and digest (≤120 chars)
- ✅ **MacOS Code Blocks** — Supports code block styling

---

## Quick Start

### Requirements

- Python 3.8+
- WeChat Official Account AppID and AppSecret

### Installation

```bash
git clone https://github.com/lucianaib0318/wechat-publisher.git
cd wechat-publisher
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Get WeChat AppID and AppSecret

1. Login to [WeChat MP Platform](https://mp.weixin.qq.com/)
2. Go to **Development** → **Basic Configuration**
3. Find **AppID** (Application ID)
4. Click **Generate** button next to **AppSecret**
5. Copy AppSecret immediately (shown only once)

> **Important**: If running on a cloud server, add the server IP to the **IP Whitelist**.

---

## Usage

### Method 1: From Markdown File (Recommended)

```bash
python3 publisher.py \
  --appid "wx36ba9f59df0d6313" \
  --secret "ae71bf50f7217042e639b44fb57d5529" \
  --article article.md \
  --author "YourName" \
  --no-cover
```

### Method 2: Direct Title and Content

```bash
python3 publisher.py \
  --appid "YOUR_APPID" \
  --secret "YOUR_SECRET" \
  --title "Article Title" \
  --content "<section>Article Content</section>" \
  --author "YourName" \
  --no-cover
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--appid` | Yes | WeChat Official Account AppID |
| `--secret` | Yes | WeChat Official Account AppSecret |
| `--article` | No | Markdown article file path |
| `--title` | No | Article title (use with --content) |
| `--content` | No | Article content (HTML format) |
| `--author` | No | Author name (default: YourName) |
| `--image` | No | Custom cover image path |
| `--no-cover` | No | Use default cover (recommended) |

---

## Testing Status

| Test Item | Status | Notes |
|-----------|--------|-------|
| **Draft Creation** | ✅ Pass | Verified 2026-03-17 |
| **Cover Upload** | ✅ Pass | Auto-generated 900x500 |
| **Markdown Render** | ✅ Pass | WeChat inline styles |
| **Chinese Encoding** | ✅ Pass | No garbled text |
| **Title/Digest** | ✅ Pass | Auto-trimmed to limits |
| **Long Article (2900 words)** | ✅ Pass | Long-form test passed |

> 💡 **Note**: After creating a draft, you need to manually publish it in the WeChat Official Account backend.

---

## Project Structure

```
wechat-publisher/
├── publisher.py           # Main program
├── requirements.txt       # Python dependencies
├── README.md              # English documentation
├── README_CN.md           # Chinese documentation
├── SKILL.md               # OpenClaw skill definition
├── LICENSE                # MIT License
└── examples/              # Example files
    ├── article.md         # Example article
    └── test-article.md    # Test article
```

---

## Markdown Syntax Support

### Headings

```markdown
# Heading 1
## Heading 2
### Heading 3
```

### Text Formatting

```markdown
**Bold text**
*Italic text*
> Blockquote
```

### Lists

```markdown
- List item 1
- List item 2
- List item 3
```

### Code Blocks

````markdown
```python
print("Hello, WeChat!")
```
````

---

## FAQ

### Q: Why only create drafts, not auto-publish?

A: Auto-publish requires the "Mass Send API" permission, which personal subscription accounts don't have by default. After creating a draft, you need to manually publish it in the MP backend.

### Q: Chinese text shows as garbled?

A: Chinese encoding issue has been fixed (v1.1.0+). Please ensure you're using the latest version. The tool automatically handles UTF-8 encoding.

### Q: What are the cover image requirements?

A: Recommended size is 900x500 pixels (16:9), minimum 200x200 pixels. You can use `--no-cover` to auto-generate a default cover.

### Q: What if title or digest is too long?

A: The tool automatically truncates: title ≤64 chars, digest ≤120 chars.

### Q: How to view drafts?

A: Login to [WeChat MP Backend](https://mp.weixin.qq.com/) → Draft Box to see created drafts.

---

## Changelog

### v1.1.0 (2026-03-17)

- 🐛 Fix Chinese garbled text (ensure_ascii=False)
- ✨ Code optimization and refactoring
- 📝 Improve documentation and type hints
- 📦 Better error handling

### v1.0.0 (2026-03-16)

- ✨ Initial release
- ✅ Markdown to WeChat HTML
- ✅ Auto cover generation
- ✅ Draft box creation

---

## License

[MIT](./LICENSE)

---

## Author

**LucianaiB** ([@lucianaib0318](https://github.com/lucianaib0318))

---

<div align="center">

**If this project helps you, please give it a ⭐️ Star!**

Made with ❤️ by LucianaiB

</div>
