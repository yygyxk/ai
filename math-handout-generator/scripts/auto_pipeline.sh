#!/bin/bash

# ==============================================================================
# auto_pipeline.sh - 基于 GitHub 的自动化教研流水线 (CI/CD)
#
# 功能：
# 1. 自动同步 math-materials 素材仓库
# 2. 自动根据关键词提取目标章节内容 (切片/图片/文字)
# 3. 提供清晰的下一步指引给 AI 进行生成
# 4. (讲义生成后) 自动渲染 HTML 并推送到 math 讲义仓库
#
# 用法：
# 阶段一 (提取)：./auto_pipeline.sh extract <PDF文件名> "<章节关键词>"
# 阶段二 (发布)：./auto_pipeline.sh publish <生成的讲义名.md>
# ==============================================================================

set -e

# --- 配置路径 ---
BASE_DIR="$HOME/IdeaProjects"
MATERIALS_REPO="$BASE_DIR/math-materials"
AI_REPO="$BASE_DIR/ai"
MATH_REPO="$BASE_DIR/math"
EXTRACT_SCRIPT="$AI_REPO/math-handout-generator/scripts/pdf_chapter_extractor.py"
RENDER_SCRIPT="$AI_REPO/math-handout-generator/scripts/handout_renderer.py"
TEMP_OUT_DIR="/tmp/handout_workspace"

COMMAND=$1

if [ "$COMMAND" = "extract" ]; then
    PDF_NAME=$2
    KEYWORD=$3

    if [ -z "$PDF_NAME" ] || [ -z "$KEYWORD" ]; then
        echo "❌ 用法: $0 extract <PDF文件名> \"<章节关键词>\""
        echo "示例: $0 extract 53_compressed.pdf \"基本不等式\""
        exit 1
    fi

    echo "🔄 [1/3] 正在同步 math-materials 仓库..."
    if [ ! -d "$MATERIALS_REPO" ]; then
        cd "$BASE_DIR"
        git clone https://github.com/yygyxk/math-materials.git
    else
        cd "$MATERIALS_REPO"
        git pull origin main
    fi

    PDF_PATH="$MATERIALS_REPO/$PDF_NAME"
    if [ ! -f "$PDF_PATH" ]; then
        echo "❌ 错误: 找不到 PDF 文件: $PDF_PATH"
        exit 1
    fi

    echo "✂️  [2/3] 开始提取章节内容..."
    rm -rf "$TEMP_OUT_DIR"
    python3 "$EXTRACT_SCRIPT" full-pipeline "$PDF_PATH" "$KEYWORD" "$TEMP_OUT_DIR"

    echo "✅ [3/3] 提取完成！"
    echo "================================================================="
    echo "🤖 请将以下指令复制给 AI Assistant (CatPaw):"
    echo "-----------------------------------------------------------------"
    echo "我已经执行了提取。材料存放在 $TEMP_OUT_DIR 。"
    echo "请读取该目录下的 chapter_text_layout.txt (辅助参考)，"
    echo "并根据里面的内容和你的内置知识库，严格按照 SKILL.md 生成"
    echo "《$KEYWORD》的双版本讲义，保存为："
    echo "  1. $TEMP_OUT_DIR/${KEYWORD}_教师版.md"
    echo "  2. $TEMP_OUT_DIR/${KEYWORD}_学生版.md"
    echo "================================================================="

elif [ "$COMMAND" = "publish" ]; then
    MD_FILE=$2

    if [ -z "$MD_FILE" ] || [ ! -f "$MD_FILE" ]; then
        echo "❌ 用法: $0 publish <生成的Markdown文件路径>"
        exit 1
    fi

    echo "🎨 [1/3] 正在渲染 HTML..."
    python3 "$RENDER_SCRIPT" render-html "$MD_FILE"
    HTML_FILE="${MD_FILE%.md}.html"

    echo "🔄 [2/3] 同步并拷贝文件到 math 仓库..."
    if [ ! -d "$MATH_REPO" ]; then
        cd "$BASE_DIR"
        git clone https://github.com/yygyxk/math.git
    else
        cd "$MATH_REPO"
        git pull origin main
    fi

    mkdir -p "$MATH_REPO/handouts"
    cp "$MD_FILE" "$MATH_REPO/handouts/"
    cp "$HTML_FILE" "$MATH_REPO/handouts/"

    echo "🚀 [3/3] 提交并推送到 GitHub..."
    cd "$MATH_REPO"
    git add .
    BASENAME=$(basename "$MD_FILE")
    git commit -m "feat: auto-publish ${BASENAME%.md} handout"
    git push origin main

    echo "🎉 发布成功！讲义已上线到 GitHub: https://github.com/yygyxk/math"

else
    echo "用法:"
    echo "  $0 extract <PDF文件名> \"<章节关键词>\""
    echo "  $0 publish <Markdown文件路径>"
    exit 1
fi

