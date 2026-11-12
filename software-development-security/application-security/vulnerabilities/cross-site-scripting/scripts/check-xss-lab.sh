#!/usr/bin/env bash
# Drive the XSS lab with headless Chrome and report whether each payload executed.
# Bash 5, Google Chrome 155 (headless), curl. Start run-xss-lab.py first.
# The payload only sets a data attribute on <body>; nothing leaves the machine.
set -euo pipefail
BASE=${BASE:-http://127.0.0.1:8088}
PAYLOAD='<img src=x onerror="document.body.dataset.xss=1">'
ENC=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$PAYLOAD")

fired() {   # $1 = URL; prints EXECUTED or blocked
  if google-chrome --headless=new --disable-gpu --no-first-run --virtual-time-budget=3000 \
       --dump-dom "$1" 2>/dev/null | grep -q 'data-xss="1"'; then
    echo EXECUTED
  else
    echo blocked
  fi
}

curl -s -o /dev/null --data-urlencode "body=$PAYLOAD" "$BASE/comment"
printf '%-34s %s\n' "reflected  /search"        "$(fired "$BASE/search?q=$ENC")"
printf '%-34s %s\n' "reflected  /search-safe"   "$(fired "$BASE/search-safe?q=$ENC")"
printf '%-34s %s\n' "reflected  /search-csp"    "$(fired "$BASE/search-csp?q=$ENC")"
printf '%-34s %s\n' "stored     /comments"      "$(fired "$BASE/comments")"
printf '%-34s %s\n' "stored     /comments-safe" "$(fired "$BASE/comments-safe")"
printf '%-34s %s\n' "DOM-based  /dom#payload"   "$(fired "$BASE/dom#$ENC")"
printf '%-34s %s\n' "DOM-based  /dom-safe#payload" "$(fired "$BASE/dom-safe#$ENC")"
printf '%-34s %s\n' "DOM-based  /dom-tt#payload"   "$(fired "$BASE/dom-tt#$ENC")"
