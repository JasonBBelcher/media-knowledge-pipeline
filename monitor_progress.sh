#!/bin/bash
#
# Monitor progress of media knowledge pipeline processing
#

echo "🎯 Monitoring Media Knowledge Pipeline Progress..."
echo "==============================================="
echo ""
echo "📁 Output directories:"
echo "  Main outputs: outputs/"
echo "  Markdown: outputs/markdown/"
echo ""

# Monitor file changes in outputs directory
echo "🔄 Watching for file changes (press Ctrl+C to stop)..."
echo ""

while true; do
    echo "🕒 $(date)"
    echo "📊 Current output files:"
    
    # Count and list JSON files
    json_count=$(find outputs -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$json_count" -gt 0 ]; then
        echo "  JSON files: $json_count"
        find outputs -name "*.json" -exec basename {} \;
    else
        echo "  JSON files: 0"
    fi
    
    # Count and list markdown files
    md_count=$(find outputs/markdown -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$md_count" -gt 0 ]; then
        echo "  Markdown files: $md_count"
        find outputs/markdown -name "*.md" -exec basename {} \;
    else
        echo "  Markdown files: 0"
    fi
    
    echo ""
    echo "📂 Temp files (audio processing):"
    temp_count=$(find temp -name "*" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$temp_count" -gt 0 ]; then
        echo "  Temp files: $temp_count"
        find temp -name "*" -exec ls -lh {} \; 2>/dev/null
    else
        echo "  Temp files: 0"
    fi
    
    echo ""
    echo "------------------------------"
    sleep 10
done