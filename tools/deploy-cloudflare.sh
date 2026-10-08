#!/bin/sh
# Build and upload the site to Cloudflare Pages (project "loveikolabs").
# First run: `npx wrangler login` with the Cloudflare account that should own the site.
set -e
cd "$(dirname "$0")/.."
python3 tools/build.py
DIST=$(mktemp -d)
rsync -a --exclude .git --exclude .github --exclude .claude --exclude tools --exclude 'GEO PACKS' \
  --exclude '*.md' --exclude .DS_Store --exclude CNAME ./ "$DIST/"
npx wrangler pages deploy "$DIST" --project-name loveikolabs --branch main
rm -rf "$DIST"
