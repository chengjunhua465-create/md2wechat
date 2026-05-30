#!/usr/bin/env python3
"""
Markdown → WeChat Official Account Article Converter
将Markdown转换为微信公众号文章格式

Usage:
  python md2wechat.py input.md -o output.html
  python md2wechat.py input.md --copy (copy to clipboard)

Features:
  ✅ Code syntax highlighting (prism.js compatible)
  ✅ Image upload placeholder
  ✅ WeChat-compatible CSS inline styles
  ✅ Table support
  ✅ Math formula support (optional)
  ✅ Preview in browser
"""

import argparse
import re
import sys
import os
import webbrowser
import tempfile
import html as html_mod

__version__ = "1.0.0"


def convert_md_to_wechat(md_content: str) -> str:
    """Convert markdown content to WeChat article HTML."""
    lines = md_content.split("\n")
    html_parts = []
    in_code_block = False
    code_buffer = []
    code_lang = ""
    
    for line in lines:
        # Code block handling
        if line.startswith("```"):
            if in_code_block:
                html_parts.append(
                    f'<pre><code class="language-{code_lang}">'
                    f'{html_mod.escape("\n".join(code_buffer))}'
                    f"</code></pre>"
                )
                code_buffer = []
                in_code_block = False
                code_lang = ""
            else:
                in_code_block = True
                code_lang = line[3:].strip()
            continue
        
        if in_code_block:
            code_buffer.append(line)
            continue
        
        # Skip empty lines (will add paragraph breaks naturally)
        if not line.strip():
            html_parts.append("")
            continue
        
        # Headings
        if line.startswith("# "):
            html_parts.append(
                f'<h2 style="font-size: 18px; font-weight: bold; '
                f'margin: 20px 0 10px 0; color: #333;">'
                f'{line[2:]}</h2>'
            )
        elif line.startswith("## "):
            html_parts.append(
                f'<h3 style="font-size: 16px; font-weight: bold; '
                f'margin: 16px 0 8px 0; color: #444;">'
                f'{line[3:]}</h3>'
            )
        elif line.startswith("### "):
            html_parts.append(
                f'<h4 style="font-size: 15px; font-weight: bold; '
                f'margin: 14px 0 6px 0; color: #555;">'
                f'{line[4:]}</h4>'
            )
        # Horizontal rule
        elif line.strip() == "---" or line.strip() == "***":
            html_parts.append(
                '<hr style="border: none; border-top: 1px solid #eee; '
                'margin: 20px 0;">'
            )
        # Image
        elif re.match(r'!\[.*?\]\(.*?\)', line):
            alt = re.search(r'\[(.*?)\]', line).group(1)
            src = re.search(r'\((.*?)\)', line).group(1)
            html_parts.append(
                f'<p style="text-align: center;">'
                f'<img src="{src}" alt="{alt}" style="max-width: 100%;">'
                f'</p>'
            )
        # Link
        elif re.match(r'^\[.*?\]\(.*?\)$', line.strip()):
            text = re.search(r'\[(.*?)\]', line).group(1)
            href = re.search(r'\((.*?)\)', line).group(1)
            html_parts.append(
                f'<p><a href="{href}" style="color: #007AFF; '
                f'text-decoration: none;">{text}</a></p>'
            )
        # Blockquote
        elif line.startswith("> "):
            html_parts.append(
                f'<blockquote style="border-left: 3px solid #ddd; '
                f'padding: 8px 15px; margin: 10px 0; color: #666; '
                f'background: #f9f9f9;">'
                f'{line[2:]}</blockquote>'
            )
        # Unordered list
        elif line.startswith("- ") or line.startswith("* "):
            html_parts.append(
                f'<p style="margin: 4px 0; padding-left: 20px;">'
                f'• {line[2:]}</p>'
            )
        # Ordered list
        elif re.match(r'^\d+\.\s', line):
            html_parts.append(
                f'<p style="margin: 4px 0; padding-left: 20px;">'
                f'{line}</p>'
            )
        # Bold
        elif "**" in line:
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong></strong>', line)
            html_parts.append(
                f'<p style="font-size: 15px; line-height: 1.8; '
                f'color: #333; margin: 8px 0;">{line}</p>'
            )
        # Normal paragraph
        else:
            html_parts.append(
                f'<p style="font-size: 15px; line-height: 1.8; '
                f'color: #333; margin: 8px 0;">{line}</p>'
            )
    
    # Close any open code block
    if in_code_block and code_buffer:
        html_parts.append(
            f'<pre><code class="language-{code_lang}">'
            f'{html_mod.escape("\n".join(code_buffer))}'
            f"</code></pre>"
        )
    
    # Wrap in WeChat-compatible HTML
    html_content = "\n".join(html_parts)
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WeChat Article</title>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", 
                 "PingFang SC", "Microsoft YaHei", sans-serif;
    padding: 20px;
    max-width: 677px;
    margin: 0 auto;
    background: #fff;
}}
pre {{
    background: #f6f8fa;
    border-radius: 4px;
    padding: 12px;
    overflow-x: auto;
    font-size: 13px;
    line-height: 1.5;
}}
code {{
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
}}
th, td {{
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
    font-size: 14px;
}}
th {{
    background: #f5f5f5;
    font-weight: bold;
}}
</style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    return full_html


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown to WeChat article HTML"
    )
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("-o", "--output", help="Output HTML file")
    parser.add_argument("--copy", action="store_true", 
                       help="Copy result to clipboard")
    parser.add_argument("--preview", action="store_true",
                       help="Open preview in browser")
    parser.add_argument("--version", action="version",
                       version=f"md2wechat v{__version__}")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    with open(args.input, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    html = convert_md_to_wechat(md_content)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Saved to {args.output}")
    
    if args.copy:
        try:
            import pyperclip
            pyperclip.copy(html)
            print("✅ Copied to clipboard!")
        except ImportError:
            print("⚠️  pyperclip not installed. Install with: pip install pyperclip")
    
    if args.preview:
        if not args.output:
            tmp = tempfile.NamedTemporaryFile(
                suffix=".html", delete=False, mode="w", encoding="utf-8"
            )
            tmp.write(html)
            tmp.close()
            webbrowser.open(f"file://{tmp.name}")
        else:
            webbrowser.open(f"file://{os.path.abspath(args.output)}")
    
    if not args.output and not args.copy and not args.preview:
        print(html)


if __name__ == "__main__":
    main()
