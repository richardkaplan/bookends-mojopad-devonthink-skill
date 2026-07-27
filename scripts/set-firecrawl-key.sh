#!/usr/bin/env bash
# set-firecrawl-key.sh — one low-friction place to stash your Firecrawl API key.
#
# The Bookends Research Skill finds candidate papers through the Firecrawl MCP
# server, which reads the key from the FIRECRAWL_API_KEY environment variable.
# (It is NOT read by Bookends' MCP or by this skill's Python scripts.) This helper
# saves the key to a standard local file and then prints the exact snippet to add
# to your Firecrawl MCP config so the server actually picks it up — in Claude Code,
# Cowork, or Dispatch.
#
# Usage:
#   bash scripts/set-firecrawl-key.sh                 # prompts (input hidden)
#   bash scripts/set-firecrawl-key.sh fc-xxxxxxxx     # key as an argument
#   FIRECRAWL_API_KEY=fc-xxxx bash scripts/set-firecrawl-key.sh   # from env
#
# It NEVER prints your full key and NEVER commits it. The stored file is chmod 600.

set -euo pipefail

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/bookends-research"
CONFIG_FILE="$CONFIG_DIR/firecrawl.env"

# 1) Obtain the key: argument > env var > interactive prompt.
KEY="${1:-${FIRECRAWL_API_KEY:-}}"
if [ -z "$KEY" ]; then
  printf 'Enter your Firecrawl API key (input hidden): ' >&2
  read -r -s KEY || true
  printf '\n' >&2
fi

if [ -z "$KEY" ]; then
  echo "No key provided. Get one at https://firecrawl.dev, then re-run." >&2
  exit 1
fi

# 2) Store it privately.
mkdir -p "$CONFIG_DIR"
umask 177
printf 'FIRECRAWL_API_KEY=%s\n' "$KEY" > "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE"

# Masked echo so the terminal/scrollback never shows the whole key.
mask() { local k="$1"; local n=${#k}; if [ "$n" -le 8 ]; then printf '****'; else printf '%s…%s' "${k:0:4}" "${k: -4}"; fi; }

cat >&2 <<EOF

Saved FIRECRAWL_API_KEY ($(mask "$KEY")) to:
  $CONFIG_FILE   (permissions 600)

Now make your Firecrawl MCP server read it. Pick the line that matches your setup:

CLAUDE CODE (CLI) — register/replace the Firecrawl server with the key in its env:
  claude mcp add firecrawl --env FIRECRAWL_API_KEY=$KEY -- npx -y firecrawl-mcp
  # (or add  "env": { "FIRECRAWL_API_KEY": "$KEY" }  to the firecrawl entry in your .mcp.json)

COWORK / CLAUDE DESKTOP — open the Firecrawl connector's settings and paste the key
into its API key / FIRECRAWL_API_KEY field, then reconnect. (Cowork and Dispatch read
the connector config, not this file or your shell.)

SHELL-LAUNCHED MCP — if you start the MCP from a terminal, have the server inherit it:
  echo 'set -a; . "$CONFIG_FILE"; set +a' >> ~/.zprofile   # or ~/.bash_profile
  # then open a new terminal before launching Claude.

Nothing here is committed to git, and your key was not printed in full.
EOF
