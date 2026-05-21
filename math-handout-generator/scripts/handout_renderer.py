#!/usr/bin/env python3
"""
handout_renderer.py - 数学讲义 Markdown → HTML 渲染器

功能：
  1. render-html : 将 Markdown 讲义渲染为带 KaTeX 的 HTML 文件
  2. render-pdf  : 将 Markdown 讲义渲染为 PDF（通过 HTML 中转）

使用示例：
  python3 handout_renderer.py render-html ./1.1_集合.md
  python3 handout_renderer.py render-html ./1.1_集合.md --output ./output.html
  python3 handout_renderer.py render-pdf  ./1.1_集合.md
"""

import sys
import os
import re
import argparse


HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<!-- KaTeX 渲染库 -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{
    delimiters:[
      {{left:'$$',right:'$$',display:true}},
      {{left:'$',right:'$',display:false}},
      {{left:'\\(',right:'\\)',display:false}},
      {{left:'\\[',right:'\\]',display:true}}
    ],
    throwOnError:false
  }})"></script>
<style>
  :root {{
    --bg: #ffffff;
    --fg: #1a1a2e;
    --accent: #e94560;
    --accent2: #0f3460;
    --border: #e0e0e0;
    --light-bg: #f8f9fa;
    --code-bg: #f1f3f5;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #1a1a2e;
      --fg: #e0e0e0;
      --accent: #ff6b81;
      --accent2: #7bed9f;
      --border: #333;
      --light-bg: #252540;
      --code-bg: #2a2a45;
    }}
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: "PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;
    font-size: 15px;
    line-height: 1.8;
    color: var(--fg);
    background: var(--bg);
    max-width: 860px;
    margin: 0 auto;
    padding: 40px 24px;
  }}
  h1 {{
    font-size: 28px;
    text-align: center;
    color: var(--accent2);
    margin-bottom: 8px;
    border-bottom: 3px solid var(--accent);
    padding-bottom: 12px;
  }}
  h2 {{
    font-size: 22px;
    color: var(--accent2);
    margin: 32px 0 16px;
    padding: 8px 12px;
    border-left: 4px solid var(--accent);
    background: var(--light-bg);
    border-radius: 0 8px 8px 0;
  }}
  h3 {{
    font-size: 18px;
    color: var(--accent);
    margin: 24px 0 12px;
  }}
  h4 {{
    font-size: 16px;
    color: var(--accent2);
    margin: 16px 0 8px;
  }}
  p {{ margin: 8px 0; }}
  hr {{
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--accent), transparent);
    margin: 28px 0;
  }}
  ul, ol {{ margin: 8px 0 8px 24px; }}
  li {{ margin: 4px 0; }}
  strong {{ color: var(--accent); }}
  blockquote {{
    border-left: 4px solid var(--accent);
    background: var(--light-bg);
    padding: 12px 16px;
    margin: 12px 0;
    border-radius: 0 8px 8px 0;
  }}
  blockquote p {{ margin: 4px 0; }}
  code {{
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
    font-family: "JetBrains Mono","Fira Code","Consolas",monospace;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 14px;
  }}
  th {{
    background: var(--accent2);
    color: #fff;
    padding: 10px 12px;
    text-align: center;
    font-weight: 600;
  }}
  td {{
    padding: 8px 12px;
    border: 1px solid var(--border);
    text-align: center;
  }}
  tr:nth-child(even) {{ background: var(--light-bg); }}
  tr:hover {{ background: rgba(233,69,96,0.1); }}
  .katex-display {{
    margin: 16px 0;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 8px 0;
  }}
  .katex {{ font-size: 1.1em; }}
  /* 易错点标记 */
  .emoji {{ font-style: normal; }}
  /* 打印优化 */
  @media print {{
    body {{ max-width: 100%; padding: 20px; }}
    h2 {{ break-after: avoid; }}
    table {{ break-inside: avoid; }}
    .katex-display {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
{content}
</body>
</html>
'''


def markdown_to_html_content(md_text):
    """
    将 Markdown 文本转换为 HTML body 内容。
    这是一个轻量级转换器，主要处理：标题、分割线、列表、表格、
    加粗、引用块等。LaTeX 公式交给 KaTeX 在浏览器端渲染。
    """
    lines = md_text.split('\n')
    html_lines = []
    in_table = False
    in_blockquote = False
    in_list = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 空行
        if not stripped:
            if in_table:
                html_lines.append('</tbody></table>')
                in_table = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append('')
            i += 1
            continue

        # 标题
        heading_match = re.match(r'^(#{1,4})\s+(.*)', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            content = _inline_format(heading_match.group(2))
            html_lines.append(f'<h{level}>{content}</h{level}>')
            i += 1
            continue

        # 分割线
        if re.match(r'^---+\s*$', stripped):
            html_lines.append('<hr>')
            i += 1
            continue

        # 表格
        if '|' in stripped and stripped.startswith('|'):
            if not in_table:
                # 表头行
                cells = [c.strip() for c in stripped.split('|')[1:-1]]
                header_html = ''.join(f'<th>{_inline_format(c)}</th>' for c in cells)
                html_lines.append(f'<table><thead><tr>{header_html}</tr></thead>')
                in_table = True
                i += 1
                # 跳过分隔行 (|:---:|:---|...)
                if i < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i].strip()):
                    html_lines.append('<tbody>')
                    i += 1
                continue
            else:
                # 表体行
                cells = [c.strip() for c in stripped.split('|')[1:-1]]
                row_html = ''.join(f'<td>{_inline_format(c)}</td>' for c in cells)
                html_lines.append(f'<tr>{row_html}</tr>')
                i += 1
                continue

        if in_table:
            html_lines.append('</tbody></table>')
            in_table = False

        # 引用块
        if stripped.startswith('>'):
            content = _inline_format(stripped.lstrip('> ').lstrip('>'))
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            html_lines.append(f'<p>{content}</p>')
            i += 1
            continue

        if in_blockquote:
            html_lines.append('</blockquote>')
            in_blockquote = False

        # 无序列表
        list_match = re.match(r'^[-*]\s+(.*)', stripped)
        if list_match:
            content = _inline_format(list_match.group(1))
            html_lines.append(f'<li>{content}</li>')
            i += 1
            continue

        # 普通段落
        content = _inline_format(stripped)
        html_lines.append(f'<p>{content}</p>')
        i += 1

    # 关闭未闭合的标签
    if in_table:
        html_lines.append('</tbody></table>')
    if in_blockquote:
        html_lines.append('</blockquote>')

    return '\n'.join(html_lines)


def _inline_format(text):
    """处理行内格式：加粗、行内代码"""
    # 加粗
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # 行内代码
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # <br>
    text = text.replace('<br>', '<br>')
    return text


def render_html(md_path, output_path=None):
    """将 Markdown 讲义渲染为 HTML 文件"""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 提取标题（第一个 # 开头的行）
    title_match = re.search(r'^#\s+(.+)', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(md_path).replace('.md', '')

    # 转换内容
    html_content = markdown_to_html_content(md_text)

    # 填充模板
    html = HTML_TEMPLATE.format(title=title, content=html_content)

    # 输出路径
    if output_path is None:
        output_path = md_path.replace('.md', '.html')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML 已生成: {output_path}")
    return output_path


def render_pdf(md_path, output_path=None):
    """将 Markdown 讲义渲染为 PDF（通过 HTML 中转 + 浏览器打印）"""
    html_path = render_html(md_path)
    if output_path is None:
        output_path = md_path.replace('.md', '.pdf')

    # 尝试使用 wkhtmltopdf
    import subprocess
    try:
        result = subprocess.run(
            ['wkhtmltopdf', '--enable-local-file-access', html_path, output_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print(f"✅ PDF 已生成: {output_path}")
            return output_path
    except FileNotFoundError:
        pass

    # 回退方案：提示用户手动打印
    print(f"⚠️ wkhtmltopdf 未安装，请用浏览器打开 HTML 文件后 Ctrl+P 打印为 PDF")
    print(f"   HTML 文件: {html_path}")
    print(f"   💡 安装 wkhtmltopdf: brew install wkhtmltopdf")
    return None


def main():
    parser = argparse.ArgumentParser(description="数学讲义 Markdown → HTML/PDF 渲染器")
    parser.add_argument('command', choices=['render-html', 'render-pdf'],
                       help='渲染命令')
    parser.add_argument('md_path', help='Markdown 讲义文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')

    args = parser.parse_args()

    if args.command == 'render-html':
        render_html(args.md_path, args.output)
    elif args.command == 'render-pdf':
        render_pdf(args.md_path, args.output)


if __name__ == "__main__":
    main()

