#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号草稿助手 - WeChat Official Account Draft Helper
基于微信公众号 API，实现文章自动创建草稿功能

注意：本工具只创建草稿，不自动发布。用户需要手动在公众号后台发布。

Usage:
    python publisher.py --appid "YOUR_APPID" --secret "YOUR_SECRET" --article article.md
    python publisher.py --appid "YOUR_APPID" --secret "YOUR_SECRET" --title "标题" --content "内容"

Example:
    python publisher.py --appid "wx36ba9f59df0d6313" --secret "ae71bf50f7217042e639b44fb57d5529" \
        --article ml-article.md --author "昌哥" --no-cover
"""

import argparse
import json
import os
import sys
import tempfile
import re
from datetime import datetime
from typing import Optional

import requests
import markdown
from PIL import Image, ImageDraw, ImageFont


class WeChatPublisher:
    """
    微信公众号草稿助手
    
    功能：
    - 获取 Access Token
    - 上传封面图片
    - 创建草稿到草稿箱
    - Markdown 转微信 HTML
    
    注意：只创建草稿，不自动发布
    """
    
    def __init__(self, appid: str, secret: str):
        """
        初始化发布助手
        
        Args:
            appid: 微信公众号 AppID
            secret: 微信公众号 AppSecret
        """
        self.appid = appid
        self.secret = secret
        self.access_token: Optional[str] = None
        self.base_url = "https://api.weixin.qq.com/cgi-bin"
    
    def get_access_token(self) -> Optional[str]:
        """
        获取微信公众号 Access Token
        
        Returns:
            access_token 字符串，失败返回 None
        """
        print("🔑 正在获取 access_token...")
        
        url = f"{self.base_url}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if "access_token" in data:
                self.access_token = data["access_token"]
                expires_in = data.get("expires_in", 7200)
                print(f"✅ access_token 获取成功（有效期 {expires_in//60} 分钟）")
                return self.access_token
            else:
                error_code = data.get("errcode", "Unknown")
                error_msg = data.get("errmsg", "Unknown error")
                print(f"❌ access_token 获取失败：{error_code} - {error_msg}")
                return None
                
        except requests.RequestException as e:
            print(f"❌ 网络请求失败：{e}")
            return None
        except Exception as e:
            print(f"❌ 未知错误：{e}")
            return None
    
    def upload_draft(self, title: str, content: str, author: str = None, 
                     digest: str = "", thumb_media_id: str = None) -> Optional[str]:
        """
        上传文章到草稿箱
        
        Args:
            title: 文章标题（≤64 字）
            content: 文章内容（HTML 格式，微信内联样式）
            author: 作者名
            digest: 摘要（≤120 字，默认空字符串）
            thumb_media_id: 封面图片 media_id
            
        Returns:
            media_id: 上传成功返回 media_id，失败返回 None
        """
        if not self.access_token:
            print("❌ 请先获取 access_token")
            return None
        
        print(f"📝 正在上传草稿：{title}")
        
        url = f"{self.base_url}/draft/add?access_token={self.access_token}"
        
        # 构建文章数据（digest 限制 120 字，title 限制 64 字）
        safe_title = title[:64] if len(title) > 64 else title
        # digest 可以为空，避免超限
        safe_digest = digest[:120] if digest and len(digest) > 120 else (digest or "")
        
        articles = {
            "articles": [
                {
                    "title": safe_title,
                    "author": author or "LucianaiB",
                    "digest": safe_digest,
                    "content": content,
                    "content_source_url": "",
                    "thumb_media_id": thumb_media_id,  # 必须提供有效的 media_id
                    "show_cover_pic": 1,  # 显示封面图
                    "need_open_comment": 0,  # 关闭评论
                    "only_fans_can_comment": 0  # 所有人可评论
                }
            ]
        }
        
        try:
            # 使用 json.dumps 确保中文正确编码（ensure_ascii=False）
            import json
            response = requests.post(
                url, 
                data=json.dumps(articles, ensure_ascii=False).encode('utf-8'),
                headers={'Content-Type': 'application/json; charset=utf-8'},
                timeout=30
            )
            data = response.json()
            
            # 微信草稿箱 API 成功时返回 media_id，不一定有 errcode
            if data.get("media_id"):
                media_id = data.get("media_id")
                print(f"✅ 草稿上传成功！media_id: {media_id}")
                return media_id
            elif data.get("errcode") == 0:
                media_id = data.get("media_id")
                print(f"✅ 草稿上传成功！media_id: {media_id}")
                return media_id
            else:
                error_code = data.get("errcode", "Unknown")
                error_msg = data.get("errmsg", "Unknown error")
                print(f"❌ 草稿上传失败：{error_code} - {error_msg}")
                
                # 封面裁剪失败时，尝试上传默认封面
                if error_code == 53402 and not thumb_media_id:
                    print("💡 尝试上传默认封面后重试...")
                    default_media_id = self.upload_default_cover()
                    if default_media_id:
                        articles["articles"][0]["thumb_media_id"] = default_media_id
                        return self.upload_draft(title, content, author, digest, default_media_id)
                
                # 常见错误处理
                if error_code == 40001:
                    print("💡 提示：AppSecret 可能不正确")
                elif error_code == 40014:
                    print("💡 提示：access_token 已过期，请重新获取")
                elif error_code == 45009:
                    print("💡 提示：API 调用频率超限，请稍后再试")
                elif error_code == 53402:
                    print("💡 提示：封面裁剪失败，请提供有效的封面图片")
                
                return None
                
        except Exception as e:
            print(f"❌ 请求失败：{e}")
            return None
    
    # 注意：publish_article 方法已移除
    # 原因：freepublish/submit 接口需要群发权限，个人订阅号默认不支持
    # 用户需要手动在微信公众号后台发布草稿
    
    def upload_image(self, image_path: str) -> Optional[str]:
        """
        上传封面图片（使用 material/add_material 接口获取 media_id）
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            media_id: 上传成功返回 media_id，失败返回 None
        """
        if not self.access_token:
            print("❌ 请先获取 access_token")
            return None
        
        print(f"🖼️ 正在上传封面图片：{image_path}")
        
        # 使用 material/add_material 接口获取 media_id（草稿箱需要）
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.access_token}&type=image"
        
        try:
            with open(image_path, 'rb') as f:
                files = {"media": f}
                response = requests.post(url, files=files, timeout=30)
                data = response.json()
            
            if "media_id" in data:
                media_id = data["media_id"]
                print(f"✅ 封面图片上传成功！media_id: {media_id}")
                return media_id
            else:
                error_code = data.get("errcode", "Unknown")
                error_msg = data.get("errmsg", "Unknown error")
                print(f"❌ 封面图片上传失败：{error_code} - {error_msg}")
                return None
                
        except Exception as e:
            print(f"❌ 请求失败：{e}")
            return None
    
    def delete_draft(self, media_id: str) -> bool:
        """
        删除草稿
        
        Args:
            media_id: 草稿的 media_id
            
        Returns:
            bool: 删除成功返回 True，失败返回 False
        """
        if not self.access_token:
            print("❌ 请先获取 access_token")
            return False
        
        print(f"🗑️ 正在删除草稿：{media_id}")
        
        url = f"{self.base_url}/draft/delete?access_token={self.access_token}"
        
        data = {"media_id": media_id}
        
        try:
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            if result.get("errcode") == 0:
                print(f"✅ 草稿删除成功")
                return True
            else:
                error_code = result.get("errcode", "Unknown")
                error_msg = result.get("errmsg", "Unknown error")
                print(f"❌ 草稿删除失败：{error_code} - {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ 请求失败：{e}")
            return False
    
    def get_article_url(self, article_id: str) -> str:
        """
        生成文章链接
        
        Args:
            article_id: 文章 ID
            
        Returns:
            str: 文章链接
        """
        # 微信公众号文章链接格式
        return f"https://mp.weixin.qq.com/s/{article_id}"
    
    def publish_from_markdown(self, markdown_file: str, title: str = None, 
                              author: str = "LucianaiB", thumb_media_id: str = None) -> Optional[str]:
        """
        从 Markdown 文件创建草稿
        
        流程：
        1. 读取 Markdown 文件
        2. 提取标题（如果没有提供）
        3. Markdown 转 HTML
        4. 上传草稿到草稿箱
        
        Args:
            markdown_file: Markdown 文件路径
            title: 文章标题（可选，默认从文件提取）
            author: 作者名
            thumb_media_id: 封面图片 media_id（可选）
            
        Returns:
            media_id: 草稿创建成功返回 media_id，失败返回 None
        """
        print(f"📄 正在读取 Markdown 文件：{markdown_file}")
        
        # 检查文件是否存在
        if not os.path.exists(markdown_file):
            print(f"❌ 文件不存在：{markdown_file}")
            return None
        
        # 读取 Markdown 内容
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果没有指定标题，从文件内容提取
        if not title:
            for line in content.split('\n'):
                if line.startswith('# '):
                    title = line[2:].strip()
                    break
            if not title:
                title = os.path.basename(markdown_file).replace('.md', '')
        
        print(f"📝 文章标题：{title}")
        
        # Markdown 转 HTML（简单转换）
        html_content = self._markdown_to_html(content)
        
        # 获取 access_token
        self.get_access_token()
        if not self.access_token:
            return None
        
        # 上传草稿（digest 限制 120 字，直接传空字符串避免超限）
        media_id = self.upload_draft(
            title=title,
            content=html_content,
            author=author,
            digest="",  # 空摘要，避免超限
            thumb_media_id=thumb_media_id
        )
        
        if media_id:
            print(f"\n✅ 文章已保存到草稿箱！")
            print(f"   Media ID: {media_id}")
            print(f"\n💡 提示：请前往微信公众号后台 (https://mp.weixin.qq.com/) 查看并发布。\n")
            return media_id
        
        return None
    
    def _markdown_to_html(self, md_text: str) -> str:
        """
        Markdown 转微信兼容 HTML（纯内联样式）
        
        使用 markdown 库做基础转换，再通过正则做微信样式适配。
        支持：标题、段落、粗体、斜体、引用、列表、代码块、链接、图片、表格。
        
        Args:
            md_text: Markdown 格式字符串
            
        Returns:
            微信兼容的 HTML 字符串（纯内联样式）
        """
        # 1. 用 markdown 库做基础转换（带扩展）
        html = markdown.markdown(md_text, extensions=[
            'fenced_code',    # ``` 代码块
            'codehilite',     # 代码高亮
            'tables',         # 表格
            'toc',            # 目录
            'nl2br',          # 换行转 br
            'sane_lists',     # 更安全的列表解析
        ])
        
        # 2. 标题样式化（兼容带 id 属性的 h 标签）
        html = re.sub(
            r'<h1[^>]*>(.*?)</h1>',
            r'<section style="font-size:20px;font-weight:bold;margin:20px 0 10px;color:#333;">\1</section>',
            html
        )
        html = re.sub(
            r'<h2[^>]*>(.*?)</h2>',
            r'<section style="font-size:18px;font-weight:bold;margin:16px 0 8px;color:#333;">\1</section>',
            html
        )
        html = re.sub(
            r'<h3[^>]*>(.*?)</h3>',
            r'<section style="font-size:16px;font-weight:bold;margin:12px 0 6px;color:#333;">\1</section>',
            html
        )
        
        # 3. 段落样式化
        html = re.sub(
            r'<p>(.*?)</p>',
            r'<section style="font-size:17px;line-height:1.75;color:#333;margin:12px 0;word-break:break-word;">\1</section>',
            html,
            flags=re.DOTALL
        )
        
        # 4. 引用块样式化
        html = re.sub(
            r'<blockquote>(.*?)</blockquote>',
            r'<section style="border-left:4px solid #ddd;padding:8px 12px;margin:12px 0;color:#666;font-style:italic;background:#f9f9f9;">\1</section>',
            html,
            flags=re.DOTALL
        )
        
        # 5. 代码块样式化（兼容 codehilite 扩展输出）
        # codehilite 会在 <pre> 内插 <span></span>
        html = re.sub(
            r'<div class="codehilite"><pre>(?:<span></span>)?<code[^>]*>(.*?)</code></pre></div>',
            r'<section style="background:#f6f8fa;padding:12px;border-radius:6px;margin:12px 0;overflow-x:auto;font-size:14px;"><pre style="margin:0;">\1</pre></section>',
            html,
            flags=re.DOTALL
        )
        html = re.sub(
            r'<pre><code( class="[^"]*")?>(.*?)</code></pre>',
            r'<section style="background:#f6f8fa;padding:12px;border-radius:6px;margin:12px 0;overflow-x:auto;font-size:14px;"><pre style="margin:0;">\2</pre></section>',
            html,
            flags=re.DOTALL
        )
        
        # 6. 行内代码样式化
        html = re.sub(
            r'<code>(.*?)</code>',
            r'<code style="background:#f6f8fa;padding:2px 6px;border-radius:3px;font-size:14px;color:#e83e8c;">\1</code>',
            html
        )
        
        # 7. 列表样式化
        html = re.sub(
            r'<ul>',
            r'<section style="margin:12px 0;padding-left:20px;">',
            html
        )
        html = re.sub(
            r'</ul>',
            r'</section>',
            html
        )
        html = re.sub(
            r'<li>',
            r'<section style="margin:6px 0;">• ',
            html
        )
        html = re.sub(
            r'</li>',
            r'</section>',
            html
        )
        
        # 8. 链接样式化
        html = re.sub(
            r'<a href="(.*?)"\s*>(.*?)</a>',
            r'<a href="\1" style="color:#576b95;text-decoration:none;">\2</a>',
            html
        )
        
        # 9. 图片适配微信
        html = re.sub(
            r'<img src="(.*?)"\s*(alt="[^"]*")?\s*/?>',
            r'<section style="text-align:center;margin:12px 0;"><img src="\1" style="max-width:100%;height:auto;border-radius:4px;" /></section>',
            html
        )
        
        # 10. 表格样式化
        html = re.sub(
            r'<table>',
            r'<section style="overflow-x:auto;margin:12px 0;"><table style="width:100%;border-collapse:collapse;font-size:14px;">',
            html
        )
        html = re.sub(
            r'</table>',
            r'</table></section>',
            html
        )
        html = re.sub(
            r'<th>',
            r'<th style="border:1px solid #ddd;padding:8px;background:#f6f8fa;font-weight:bold;">',
            html
        )
        html = re.sub(
            r'<td>',
            r'<td style="border:1px solid #ddd;padding:8px;">',
            html
        )
        
        return html
    
    def upload_default_cover(self, title: str = "") -> Optional[str]:
        """
        上传默认封面图（900x500 像素，微信要求最小 200x200）
        
        策略：使用 Pillow 生成渐变背景 + 标题文字的精美 JPG 封面。
        
        Returns:
            media_id: 上传成功返回 media_id，失败返回 None
        """
        try:
            width, height = 900, 500
            
            # 1. 创建渐变背景
            img = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(img)
            
            # 渐变：深蓝 -> 紫
            for y in range(height):
                r = int(30 + (100 - 30) * y / height)
                g = int(40 + (60 - 40) * y / height)
                b = int(80 + (140 - 80) * y / height)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # 2. 绘制标题文字
            title_text = title[:20] if title else "Article"
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            except (IOError, OSError):
                font = ImageFont.load_default()
            
            # 文字居中
            bbox = draw.textbbox((0, 0), title_text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            text_x = (width - text_w) // 2
            text_y = (height - text_h) // 2
            
            # 文字阴影
            draw.text((text_x + 2, text_y + 2), title_text, fill=(0, 0, 0, 128), font=font)
            draw.text((text_x, text_y), title_text, fill=(255, 255, 255, 255), font=font)
            
            # 3. 保存为 JPG
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
                img.save(f.name, 'JPEG', quality=90)
                temp_path = f.name
            
            media_id = self.upload_image(temp_path)
            os.unlink(temp_path)
            return media_id
            
        except Exception as e:
            print(f"❌ 默认封面生成失败：{e}")
            return None
    
    def print_config(self):
        """打印配置信息"""
        print("\n" + "=" * 60)
        print("📱 微信公众号发布助手")
        print("=" * 60)
        print(f"AppID: {self.appid[:10]}...{self.appid[-6:]}")
        print(f"Secret: {self.secret[:6]}...{self.secret[-6:]}")
        print("=" * 60 + "\n")


def main():
    """
    主函数 - 解析命令行参数并执行相应操作
    
    支持两种模式：
    1. Markdown 文件模式：--article article.md
    2. 直接输入模式：--title "标题" --content "内容"
    """
    parser = argparse.ArgumentParser(
        description='微信公众号草稿助手 - 一键创建草稿到草稿箱',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python publisher.py --appid "YOUR_APPID" --secret "YOUR_SECRET" --article article.md --author "昌哥" --no-cover
  python publisher.py --appid "YOUR_APPID" --secret "YOUR_SECRET" --title "标题" --content "内容" --no-cover
        '''
    )
    parser.add_argument('--appid', type=str, required=True,
                        help='微信公众号 AppID（必填）')
    parser.add_argument('--secret', type=str, required=True,
                        help='微信公众号 AppSecret（必填）')
    parser.add_argument('--article', type=str, metavar='FILE',
                        help='Markdown 文章文件路径')
    parser.add_argument('--title', type=str, metavar='TITLE',
                        help='文章标题（与 --content 配合使用）')
    parser.add_argument('--content', type=str, metavar='CONTENT',
                        help='文章内容（HTML 格式，与 --title 配合使用）')
    parser.add_argument('--author', type=str, default='昌哥',
                        help='作者名（默认：昌哥）')
    parser.add_argument('--image', type=str, metavar='IMAGE_FILE',
                        help='自定义封面图片路径')
    parser.add_argument('--no-cover', action='store_true',
                        help='跳过封面生成，使用默认封面（推荐）')
    
    args = parser.parse_args()
    
    # 创建发布助手
    publisher = WeChatPublisher(args.appid, args.secret)
    publisher.print_config()
    
    # 获取 access_token
    publisher.get_access_token()
    if not publisher.access_token:
        return
    
    # 提取标题（用于封面生成）
    cover_title = args.title or ""
    if args.article and not cover_title:
        try:
            with open(args.article, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('# '):
                        cover_title = line[2:].strip()
                        break
        except Exception:
            pass
    
    # 上传封面图（如果有）
    thumb_media_id = None
    if args.image and os.path.exists(args.image):
        thumb_media_id = publisher.upload_image(args.image)
    elif args.no_cover:
        print("📌 使用默认封面...")
        thumb_media_id = publisher.upload_default_cover(title=cover_title)
    
    # 如果有 Markdown 文件
    if args.article:
        publisher.publish_from_markdown(
            markdown_file=args.article,
            title=args.title,
            author=args.author,
            thumb_media_id=thumb_media_id
        )
    # 如果有标题和内容
    elif args.title and args.content:
        # 上传草稿
        media_id = publisher.upload_draft(
            title=args.title,
            content=args.content,
            author=args.author,
            thumb_media_id=thumb_media_id
        )
        if media_id:
            print(f"\n✅ 文章已保存到草稿箱！")
            print(f"   Media ID: {media_id}")
            print(f"\n💡 提示：请前往微信公众号后台 (https://mp.weixin.qq.com/) 查看并发布。\n")
    else:
        print("❌ 请提供文章内容（--article 或 --title + --content）")
        parser.print_help()


if __name__ == '__main__':
    main()
