#!/usr/bin/env python3
"""
pdf_chapter_extractor.py - PDF 章节定位与内容提取工具

功能：
  1. extract-toc    : 提取 PDF 目录（书签/TOC），输出结构化 JSON
  2. find-chapter   : 根据关键词定位章节，输出该章节的页码范围
  3. extract-pages  : 提取指定页码范围的内容（文本 + 图片）
  4. extract-images : 提取指定页码范围内的所有图片
  5. full-pipeline  : 一键完成：提取目录 → 定位章节 → 提取内容 → 保存

使用示例：
  python3 pdf_chapter_extractor.py extract-toc     /path/to/book.pdf
  python3 pdf_chapter_extractor.py find-chapter    /path/to/book.pdf "集合"
  python3 pdf_chapter_extractor.py extract-pages   /path/to/book.pdf 5 12
  python3 pdf_chapter_extractor.py extract-images  /path/to/book.pdf 5 12 ./output_imgs/
  python3 pdf_chapter_extractor.py full-pipeline   /path/to/book.pdf "集合" ./output/

依赖：pip install pymupdf pdfplumber
"""

import sys
import os
import json
import re
import fitz  # PyMuPDF


def extract_toc(pdf_path):
    """
    提取 PDF 的书签/目录结构，返回结构化列表。
    每个条目包含：level, title, page_number(1-based)
    """
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()  # 返回 [[level, title, page_number], ...]

    result = []
    for level, title, page_num in toc:
        result.append({
            "level": level,
            "title": title,
            "page_number": page_num,  # 1-based
        })

    doc.close()
    return result


def find_chapter(pdf_path, keyword, fuzzy=True):
    """
    根据关键词在目录中查找匹配的章节。
    返回匹配到的章节列表，每个包含 title, start_page, end_page(推断), level。

    fuzzy=True 时支持模糊匹配（如 "集合" 匹配 "1.1 集合"）。
    """
    toc = extract_toc(pdf_path)

    matches = []
    for i, entry in enumerate(toc):
        title = entry["title"]
        if fuzzy:
            if keyword in title:
                # 推断 end_page：取下一个同级或更高级条目的 start_page - 1
                end_page = _infer_end_page(toc, i)
                matches.append({
                    "title": title,
                    "level": entry["level"],
                    "start_page": entry["page_number"],
                    "end_page": end_page,
                })
        else:
            if keyword == title.strip():
                end_page = _infer_end_page(toc, i)
                matches.append({
                    "title": title,
                    "level": entry["level"],
                    "start_page": entry["page_number"],
                    "end_page": end_page,
                })

    return matches


def _infer_end_page(toc, current_index):
    """
    推断当前目录条目的结束页码。
    规则：找到下一个同级或更高级(level<=current)的条目，其 start_page - 1 即为 end_page。
    如果没有后续条目，则返回 -1（表示到文件末尾）。
    """
    current_level = toc[current_index]["level"]

    for j in range(current_index + 1, len(toc)):
        if toc[j]["level"] <= current_level:
            return toc[j]["page_number"] - 1

    return -1  # 到文件末尾


def extract_pages_content(pdf_path, start_page, end_page):
    """
    提取指定页码范围（1-based, 闭区间）的文本内容。
    返回纯文本字符串。
    """
    doc = fitz.open(pdf_path)
    text_parts = []

    # 确保页码范围合法
    total_pages = len(doc)
    start = max(1, start_page)
    end = min(total_pages, end_page) if end_page > 0 else total_pages

    for page_num in range(start, end + 1):
        page = doc[page_num - 1]  # 0-based index
        text = page.get_text("text")
        text_parts.append(f"--- 第 {page_num} 页 ---\n{text}")

    doc.close()
    return "\n\n".join(text_parts)


def extract_pages_with_layout(pdf_path, start_page, end_page):
    """
    提取指定页码范围的文本，保留更好的排版信息（使用 pdfplumber）。
    返回纯文本字符串。
    """
    import pdfplumber

    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        start = max(1, start_page)
        end = min(total_pages, end_page) if end_page > 0 else total_pages

        for page_num in range(start, end + 1):
            page = pdf.pages[page_num - 1]
            text = page.extract_text() or ""
            text_parts.append(f"--- 第 {page_num} 页 ---\n{text}")

    return "\n\n".join(text_parts)


def extract_images(pdf_path, start_page, end_page, output_dir):
    """
    提取指定页码范围内的所有图片，保存到 output_dir。
    返回提取的图片路径列表。
    """
    doc = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)

    total_pages = len(doc)
    start = max(1, start_page)
    end = min(total_pages, end_page) if end_page > 0 else total_pages

    image_paths = []
    img_index = 0

    for page_num in range(start, end + 1):
        page = doc[page_num - 1]
        image_list = page.get_images(full=True)

        for img_info in image_list:
            xref = img_info[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                # 如果是 CMYK，转换为 RGB
                if pix.n > 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                img_filename = f"page{page_num}_img{img_index}.png"
                img_path = os.path.join(output_dir, img_filename)
                pix.save(img_path)

                image_paths.append(img_path)
                img_index += 1
            except Exception as e:
                print(f"⚠️ 提取图片失败 (xref={xref}): {e}", file=sys.stderr)

    doc.close()
    return image_paths


def extract_page_images_as_pil(pdf_path, start_page, end_page, output_dir, dpi=200):
    """
    将指定页码范围整页渲染为图片（用于视觉模型识别）。
    返回图片路径列表。
    """
    doc = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)

    total_pages = len(doc)
    start = max(1, start_page)
    end = min(total_pages, end_page) if end_page > 0 else total_pages

    image_paths = []
    zoom = dpi / 72  # 72 是 PDF 默认 DPI
    mat = fitz.Matrix(zoom, zoom)

    for page_num in range(start, end + 1):
        page = doc[page_num - 1]
        pix = page.get_pixmap(matrix=mat)

        img_filename = f"page_{page_num}.png"
        img_path = os.path.join(output_dir, img_filename)
        pix.save(img_path)

        image_paths.append(img_path)

    doc.close()
    return image_paths


def full_pipeline(pdf_path, keyword, output_dir):
    """
    一键流水线：
    1. 提取目录
    2. 根据关键词定位章节
    3. 提取该章节的文本内容
    4. 提取该章节的图片
    5. 渲染该章节的整页图片（供视觉模型使用）
    6. 保存所有结果到 output_dir
    """
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: 提取目录
    print("📖 Step 1: 提取 PDF 目录...")
    toc = extract_toc(pdf_path)
    toc_path = os.path.join(output_dir, "toc.json")
    with open(toc_path, "w", encoding="utf-8") as f:
        json.dump(toc, f, ensure_ascii=False, indent=2)
    print(f"   ✅ 目录已保存: {toc_path} ({len(toc)} 个条目)")

    # Step 2: 定位章节
    print(f"\n🔍 Step 2: 搜索关键词 '{keyword}'...")
    matches = find_chapter(pdf_path, keyword)

    if not matches:
        # 如果目录中没有匹配，尝试全文搜索关键词
        print("   ⚠️ 目录中未找到匹配，尝试全文搜索...")
        matches = _fulltext_search(pdf_path, keyword)

    if not matches:
        print(f"   ❌ 未找到包含 '{keyword}' 的章节")
        return None

    # 保存匹配结果
    matches_path = os.path.join(output_dir, "chapter_matches.json")
    with open(matches_path, "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)

    print(f"   ✅ 找到 {len(matches)} 个匹配章节:")
    for m in matches:
        end_str = str(m["end_page"]) if m["end_page"] > 0 else "末尾"
        print(f"      - {m['title']} (第 {m['start_page']}-{end_str} 页)")

    # 使用第一个匹配
    best_match = matches[0]
    start_page = best_match["start_page"]
    end_page = best_match["end_page"]

    # Step 3: 提取文本内容
    print(f"\n📝 Step 3: 提取第 {start_page}-{end_page if end_page > 0 else '末尾'} 页的文本...")
    text = extract_pages_content(pdf_path, start_page, end_page)
    text_path = os.path.join(output_dir, "chapter_text.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"   ✅ 文本已保存: {text_path}")

    # Step 3.5: 用 pdfplumber 提取带排版的文本
    print(f"\n📝 Step 3.5: 用 pdfplumber 提取带排版的文本...")
    try:
        text_layout = extract_pages_with_layout(pdf_path, start_page, end_page)
        text_layout_path = os.path.join(output_dir, "chapter_text_layout.txt")
        with open(text_layout_path, "w", encoding="utf-8") as f:
            f.write(text_layout)
        print(f"   ✅ 带排版文本已保存: {text_layout_path}")
    except Exception as e:
        print(f"   ⚠️ pdfplumber 提取失败: {e}")

    # Step 4: 提取嵌入图片
    print(f"\n🖼️ Step 4: 提取嵌入图片...")
    img_dir = os.path.join(output_dir, "images")
    image_paths = extract_images(pdf_path, start_page, end_page, img_dir)
    print(f"   ✅ 提取了 {len(image_paths)} 张图片 → {img_dir}/")

    # Step 5: 渲染整页为图片（供视觉模型识别）
    print(f"\n📸 Step 5: 渲染整页为高清图片（供视觉模型使用）...")
    pages_img_dir = os.path.join(output_dir, "page_screenshots")
    page_images = extract_page_images_as_pil(pdf_path, start_page, end_page, pages_img_dir, dpi=200)
    print(f"   ✅ 渲染了 {len(page_images)} 页 → {pages_img_dir}/")

    # Step 6: 输出摘要
    summary = {
        "pdf_path": pdf_path,
        "keyword": keyword,
        "matched_chapter": best_match,
        "all_matches": matches,
        "extracted_text_file": text_path,
        "extracted_images_dir": img_dir,
        "page_screenshots_dir": pages_img_dir,
        "page_range": f"{start_page}-{end_page if end_page > 0 else 'end'}",
        "total_pages_rendered": len(page_images),
        "total_images_extracted": len(image_paths),
    }
    summary_path = os.path.join(output_dir, "extraction_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"🎉 提取完成！所有文件保存在: {output_dir}")
    print(f"{'='*60}")
    print(f"   📄 文本内容: {text_path}")
    print(f"   🖼️ 嵌入图片: {img_dir}/ ({len(image_paths)} 张)")
    print(f"   📸 整页截图: {pages_img_dir}/ ({len(page_images)} 页)")
    print(f"   📋 提取摘要: {summary_path}")

    return summary


def _fulltext_search(pdf_path, keyword):
    """
    当目录中没有匹配时，全文搜索关键词出现的页码，
    推断章节范围。
    """
    doc = fitz.open(pdf_path)
    hits = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if keyword in text:
            hits.append(page_num + 1)  # 1-based

    doc.close()

    if not hits:
        return []

    # 推断章节范围：取连续页码的首尾，前后各扩展1页
    start = max(1, hits[0] - 1)
    end = hits[-1] + 1

    return [{
        "title": f"全文搜索匹配: '{keyword}' (出现在第 {hits[0]}-{hits[-1]} 页)",
        "level": 1,
        "start_page": start,
        "end_page": end,
        "matched_pages": hits,
    }]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "extract-toc":
        if len(sys.argv) < 3:
            print("用法: pdf_chapter_extractor.py extract-toc <pdf_path>")
            sys.exit(1)
        toc = extract_toc(sys.argv[2])
        print(json.dumps(toc, ensure_ascii=False, indent=2))

    elif command == "find-chapter":
        if len(sys.argv) < 4:
            print("用法: pdf_chapter_extractor.py find-chapter <pdf_path> <keyword>")
            sys.exit(1)
        matches = find_chapter(sys.argv[2], sys.argv[3])
        print(json.dumps(matches, ensure_ascii=False, indent=2))

    elif command == "extract-pages":
        if len(sys.argv) < 5:
            print("用法: pdf_chapter_extractor.py extract-pages <pdf_path> <start_page> <end_page>")
            sys.exit(1)
        text = extract_pages_content(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        print(text)

    elif command == "extract-images":
        if len(sys.argv) < 6:
            print("用法: pdf_chapter_extractor.py extract-images <pdf_path> <start_page> <end_page> <output_dir>")
            sys.exit(1)
        paths = extract_images(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
        for p in paths:
            print(p)

    elif command == "full-pipeline":
        if len(sys.argv) < 5:
            print("用法: pdf_chapter_extractor.py full-pipeline <pdf_path> <keyword> <output_dir>")
            sys.exit(1)
        result = full_pipeline(sys.argv[2], sys.argv[3], sys.argv[4])
        if result is None:
            sys.exit(1)

    else:
        print(f"未知命令: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()

