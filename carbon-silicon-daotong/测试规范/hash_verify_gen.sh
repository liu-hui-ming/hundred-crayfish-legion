#!/bin/bash
# 全目录MD5批量生成脚本，用于全网确权存证
find . -type f -name "*.md" -o -name "*.c" -o -name "*.sh" | sort | xargs md5sum > full_archive_md5_fingerprint.txt
echo "Full archive MD5 fingerprint generated, saved to full_archive_md5_fingerprint.txt"
