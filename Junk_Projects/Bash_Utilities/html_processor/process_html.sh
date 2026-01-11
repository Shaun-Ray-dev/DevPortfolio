INPUT_DIR="./test_html"

OUTPUT_DIR="./output_files"
mkdir -p "$OUTPUT_DIR"

for htmlfile in "$INPUT_DIR"/*.html; do
    [ -e "$htmlfile" ] || continue

    base=$(basename "$htmlfile" .html)

    txtfile="$OUTPUT_DIR/${base}.txt"
    lynx -dump "$htmlfile" > "$txtfile" 2>/dev/null

    content=$(lynx -dump "$htmlfile" 2>/dev/null | sed 's/"/\\"/g' | tr -d '\r')
    jsonfile="$OUTPUT_DIR/${base}.json"
    echo "{\"content\":\"$content\"}" > "$jsonfile"

    echo "Processed $htmlfile -> $txtfile and $jsonfile"
done

echo "All HTML files processed. Output saved in $OUTPUT_DIR"
