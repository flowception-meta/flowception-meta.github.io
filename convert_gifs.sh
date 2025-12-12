#!/bin/bash

# GIF to MP4/WebM Conversion Script
# This script converts all GIFs to optimized MP4 and WebM formats

echo "Starting GIF conversion..."
echo "================================"

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed"
    echo "Install with: brew install ffmpeg"
    exit 1
fi

# Function to convert a single GIF
convert_gif() {
    local input_file="$1"
    local output_base="${input_file%.gif}"
    
    echo ""
    echo "Converting: $input_file"
    echo "--------------------------------"
    
    # Convert to MP4 (H.264) - best compatibility
    echo "  Creating MP4..."
    ffmpeg -i "$input_file" \
        -movflags faststart \
        -pix_fmt yuv420p \
        -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
        -c:v libx264 \
        -crf 23 \
        -preset medium \
        -an \
        "${output_base}.mp4" \
        -y -loglevel error
    
    # Convert to WebM (VP9) - better compression
    echo "  Creating WebM..."
    ffmpeg -i "$input_file" \
        -c:v libvpx-vp9 \
        -b:v 0 \
        -crf 35 \
        -an \
        "${output_base}.webm" \
        -y -loglevel error
    
    # Show file sizes
    if [ -f "${output_base}.mp4" ] && [ -f "${output_base}.webm" ]; then
        original_size=$(du -h "$input_file" | cut -f1)
        mp4_size=$(du -h "${output_base}.mp4" | cut -f1)
        webm_size=$(du -h "${output_base}.webm" | cut -f1)
        
        echo "  Original GIF: $original_size"
        echo "  MP4:          $mp4_size"
        echo "  WebM:         $webm_size"
        echo "  ✓ Done"
    else
        echo "  ✗ Error during conversion"
    fi
}

# Convert all GIFs in static/videos/
echo ""
echo "Converting videos..."
for gif in static/videos/*.gif; do
    if [ -f "$gif" ]; then
        convert_gif "$gif"
    fi
done

# Convert all GIFs in static/animations/
echo ""
echo "Converting animations..."
for gif in static/animations/*.gif; do
    if [ -f "$gif" ]; then
        convert_gif "$gif"
    fi
done

echo ""
echo "================================"
echo "Conversion complete!"
echo ""
echo "Next steps:"
echo "1. Update your HTML to use <video> tags instead of <img> tags"
echo "2. Keep the original GIFs as fallback (or delete them to save space)"
echo ""

