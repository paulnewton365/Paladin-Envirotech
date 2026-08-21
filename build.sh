#!/bin/bash
# build.sh VERSION "notes"
#
# Regenerates the sitemap from the pages on disk, stamps the build version
# across every page, and packages the site. Run this instead of the individual
# scripts so /sitemap can never drift from the actual page set.
set -e

VERSION="$1"
NOTES="$2"
if [ -z "$VERSION" ]; then
  echo "usage: ./build.sh X.Y.Z \"notes\""
  exit 1
fi

cd "$(dirname "$0")"

echo "==> stamping version"
python3 stamp-version.py "$VERSION" "$NOTES"

echo "==> regenerating /sitemap"
python3 generate-sitemap.py

echo "==> stamping the generated sitemap"
python3 stamp-version.py "$VERSION" "$NOTES" >/dev/null

echo "==> packaging"
rm -rf /mnt/user-data/outputs/paladin-site /mnt/user-data/outputs/paladin-site.zip 2>/dev/null || true
cp -r paladin-site /mnt/user-data/outputs/
cp stamp-version.py generate-sitemap.py build.sh /mnt/user-data/outputs/paladin-site/
cd /mnt/user-data/outputs
zip -qr paladin-site.zip paladin-site -x "*.DS_Store"
echo "==> done: $(find paladin-site -type f | wc -l) files"
