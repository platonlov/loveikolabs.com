#!/bin/sh
# Build and deploy loveikolabs.com to Cloudflare (Workers + Static Assets; worker/index.js adds the www redirect and headers).
# Uses a dedicated wrangler profile (~/.config/loveiko-cf) so other Cloudflare logins on this Mac are untouched.
# First run: XDG_CONFIG_HOME=~/.config/loveiko-cf npx wrangler login
set -e
export XDG_CONFIG_HOME="$HOME/.config/loveiko-cf"
WRANGLER="${WRANGLER:-npx --yes wrangler@4}"
cd "$(dirname "$0")/.."
python3 tools/build.py
rm -rf .dist && mkdir .dist
rsync -a --exclude .git --exclude .github --exclude .claude --exclude .dist --exclude tools --exclude 'GEO PACKS' \
  --exclude '*.md' --exclude .DS_Store --exclude CNAME --exclude wrangler.jsonc --exclude worker --exclude .gitignore ./ .dist/
$WRANGLER deploy
