#!/bin/bash

# pdf_compressor.sh - PDF 高效压缩工具
# 基于 Ghostscript 将高清扫描版 PDF 压缩到适合 GitHub 上传的大小

if [ "$#" -lt 1 ]; then
    echo "用法: $0 <输入文件.pdf> [输出文件.pdf] [压缩等级]"
    echo ""
    echo "压缩等级选项:"
    echo "  screen  - 屏幕级，分辨率最低，体积最小 (默认)"
    echo "  ebook   - 电子书级，约 150 dpi，体积适中"
    echo "  printer - 打印级，约 300 dpi，质量较好，体积较大"
    echo "  prepress- 印刷级，最高质量，体积最大"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
COMPRESS_LEVEL="${3:-screen}" # 默认使用 screen 级别压缩

# 如果没有提供输出文件名，则在原文件名前加 compressed_
if [ -z "$OUTPUT_FILE" ]; then
    BASENAME=$(basename "$INPUT_FILE")
    DIRNAME=$(dirname "$INPUT_FILE")
    OUTPUT_FILE="$DIRNAME/compressed_$BASENAME"
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "错误: 找不到文件 '$INPUT_FILE'"
    exit 1
fi

echo "⏳ 正在使用 [$COMPRESS_LEVEL] 级别压缩: $INPUT_FILE"
echo "👉 输出至: $OUTPUT_FILE"
echo "..."

# 调用 ghostscript 进行压缩
# -dUseCIEColor 避免部分图片变黑白
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/${COMPRESS_LEVEL} \
   -dNOPAUSE \
   -dQUIET \
   -dBATCH \
   -dUseCIEColor \
   -sOutputFile="$OUTPUT_FILE" \
   "$INPUT_FILE"

if [ $? -eq 0 ]; then
    ORIGINAL_SIZE=$(ls -lh "$INPUT_FILE" | awk '{print $5}')
    NEW_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
    echo "✅ 压缩完成！"
    echo "📊 体积变化: $ORIGINAL_SIZE -> $NEW_SIZE"
else
    echo "❌ 压缩失败！"
fi

