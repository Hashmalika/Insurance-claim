#!/bin/bash

FILE_ID="1_kMX0MRZtXpnAl1Jlr2N8YxPhNCNo3o4"
FILE_NAME="phi-3-mini-4k-instruct-q4.gguf"
TARGET_DIR="phi3"

# Only download if the file doesn't exist
if [ -f "${TARGET_DIR}/${FILE_NAME}" ]; then
  echo "✅ ${FILE_NAME} already exists. Skipping download."
  exit 0
fi

mkdir -p ${TARGET_DIR}
echo "📥 Downloading $FILE_NAME to ${TARGET_DIR}/ from Google Drive..."

CONFIRM=$(wget --quiet --save-cookies cookies.txt --keep-session-cookies --no-check-certificate \
"https://docs.google.com/uc?export=download&id=${FILE_ID}" -O- | \
sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1/p')

wget --load-cookies cookies.txt \
"https://docs.google.com/uc?export=download&confirm=${CONFIRM}&id=${FILE_ID}" \
-O "${TARGET_DIR}/${FILE_NAME}"

rm -f cookies.txt

echo "✅ Download complete: ${TARGET_DIR}/${FILE_NAME}"
