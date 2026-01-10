#!/usr/bin/env bash

BASE_DIR="$(pwd)"
INPUT_DIR="$BASE_DIR/scraped_files"
OUTPUT_DIR="$BASE_DIR/proc_html"

mkdir -p "$OUTPUT_DIR"

for htmlfile in "$INPUT_DIR"/*.html; do
    [ -e "$htmlfile" ] || continue
    base=$(basename "$htmlfile" .html)
    txtfile="$OUTPUT_DIR/${base}.txt"
    sed 's/<[^>]*>//g' "$htmlfile" | tr -s '\n' > "$txtfile"
    echo "Processed $base"
done

echo "HTML processing complete."