#!/usr/bin/env bash
# Turn lecture PDFs into page images an AI can read one by one.
#   bash tools/pdf_to_images.sh my/slides/固收讲义.pdf my/pages/fi
# Needs poppler: macOS `brew install poppler`, Ubuntu `sudo apt install poppler-utils`.
set -euo pipefail
pdf="$1"; out="$2"
mkdir -p "$out"
pdftoppm -r 100 -png "$pdf" "$out/p"
ls "$out" | wc -l | xargs echo "pages written to $out:"
