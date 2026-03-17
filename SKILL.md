# 微信公众号草稿助手

Markdown 一键转微信公众号草稿，直达草稿箱。

## 功能

- ✅ 从 Markdown 文件创建草稿
- ✅ 直接输入标题和内容创建草稿
- ✅ 自动上传封面图片
- ✅ Markdown 转微信 HTML（内联样式）
- ✅ 中文编码支持（无乱码）
- ✅ 自动处理标题和摘要长度限制

## 安装

```bash
git clone https://github.com/lucianaib0318/wechat-publisher.git
cd wechat-publisher
pip install -r requirements.txt
```

## 配置

在微信公众号后台获取 AppID 和 AppSecret：
1. 登录 https://mp.weixin.qq.com/
2. 开发 → 基本配置
3. 获取 AppID 和 AppSecret

## 使用方法

### 从 Markdown 文件创建草稿

```bash
python3 publisher.py \
  --appid "YOUR_APPID" \
  --secret "YOUR_SECRET" \
  --article article.md \
  --author "昌哥" \
  --no-cover
```

### 直接输入标题和内容

```bash
python3 publisher.py \
  --appid "YOUR_APPID" \
  --secret "YOUR_SECRET" \
  --title "文章标题" \
  --content "<section>文章内容</section>" \
  --author "昌哥" \
  --no-cover
```

## 参数说明

- `--appid` - 微信公众号 AppID（必填）
- `--secret` - 微信公众号 AppSecret（必填）
- `--article` - Markdown 文章文件路径
- `--title` - 文章标题（与 --content 配合使用）
- `--content` - 文章内容（HTML 格式）
- `--author` - 作者名（默认：昌哥）
- `--image` - 自定义封面图片路径
- `--no-cover` - 使用默认封面（推荐）

## 示例

### 示例 1：发布 Markdown 文章

```bash
python3 publisher.py \
  --appid "wx36ba9f59df0d6313" \
  --secret "ae71bf50f7217042e639b44fb57d5529" \
  --article ml-article.md \
  --author "昌哥" \
  --no-cover
```

### 示例 2：发布短内容

```bash
python3 publisher.py \
  --appid "wx36ba9f59df0d6313" \
  --secret "ae71bf50f7217042e639b44fb57d5529" \
  --title "测试文章" \
  --content "<section>这是一篇测试文章</section>" \
  --author "昌哥" \
  --no-cover
```

## 输出示例

```
============================================================
📱 微信公众号发布助手
============================================================

🔑 正在获取 access_token...
✅ access_token 获取成功（有效期 120 分钟）

📌 使用默认封面...
🖼️ 正在上传封面图片...
✅ 封面图片上传成功！media_id: Zvbj7IqjbzDCDvX2j_jMA...

📝 正在上传草稿：机器学习入门指南
✅ 草稿上传成功！media_id: Zvbj7IqjbzDCDvX2j_jMA...

✅ 文章已保存到草稿箱！
   Media ID: Zvbj7IqjbzDCDvX2j_jMA...

💡 提示：请前往微信公众号后台 (https://mp.weixin.qq.com/) 查看并发布。
```

## 注意事项

1. **草稿发布**：本工具只创建草稿，不自动发布。需手动在公众号后台发布。
2. **封面尺寸**：建议 900x500 像素（16:9），最小 200x200 像素。
3. **标题限制**：≤64 字，超长自动截断。
4. **摘要限制**：≤120 字，超长自动截断。
5. **IP 白名单**：云服务器需添加 IP 到微信白名单。

## 常见问题

### Q: 中文显示为乱码？
A: 请确保使用 v1.1.0+ 版本，已修复中文编码问题。

### Q: 为什么只创建草稿？
A: 自动发布需要群发接口权限，个人订阅号默认不支持。

### Q: 如何查看草稿？
A: 登录微信公众号后台 → 草稿箱。

## 许可证

MIT License

## 作者

LucianaiB - https://github.com/lucianaib0318
