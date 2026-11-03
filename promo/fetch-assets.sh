#!/usr/bin/env bash
# Downloads what the showreel needs but the repo doesn't keep: posters (from the website's
# list, via TMDB) and the two typefaces. Everything lands in promo/cache/.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p cache/posters cache/fonts

python3 -c "import json;print('\n'.join(json.load(open('../website/assets/posters.json'))[:36]))" | while read -r p; do
  [ -s "cache/posters${p}" ] || curl -sS -o "cache/posters${p}" "https://image.tmdb.org/t/p/w342${p}"
done
mkdir -p cache/posters780
python3 -c "import json;print('\n'.join(json.load(open('../website/assets/posters.json'))[:36]))" | while read -r p; do
  [ -s "cache/posters780${p}" ] || curl -sS -o "cache/posters780${p}" "https://image.tmdb.org/t/p/w780${p}"
done
ls cache/posters780 | python3 -c "import sys,json;print('window.P780='+json.dumps(['cache/posters780/'+l.strip() for l in sys.stdin if l.strip()])+';')" > cache/posters780.js
ls cache/posters | python3 -c "import sys,json;print('window.POSTERS='+json.dumps(['cache/posters/'+l.strip() for l in sys.stdin if l.strip()])+';')" > cache/posters.js

UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
css=$(curl -sS -A "$UA" "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400..900&display=block")
python3 - "$css" <<'EOF'
import re, subprocess, sys
for sub, block in re.findall(r'/\* (.*?) \*/\s*@font-face \{(.*?)\}', sys.argv[1], re.S):
    if sub != 'latin':
        continue
    fam = re.search(r"font-family: '(.*?)'", block).group(1).replace(' ', '')
    style = re.search(r'font-style: (\w+)', block).group(1)
    name = f"cache/fonts/{fam}-{'700' if fam == 'InterTight' else '400'}-{style}.woff2"
    subprocess.run(['curl', '-sS', '-o', name, re.search(r'url\((.*?)\)', block).group(1)], check=True)
    print('font', name)
EOF
for fam in "Archivo:wdth,wght@62..125,100..900" "JetBrains+Mono:wght@400..700" "Inter:wght@100..900"; do
  name=$(echo "$fam" | cut -d: -f1 | tr -d '+')
  url=$(curl -sS -A "$UA" "https://fonts.googleapis.com/css2?family=${fam}&display=block" | python3 -c "import sys,re;c=sys.stdin.read();print([u for s,b in re.findall(r'/\\* (.*?) \\*/\\s*@font-face \\{(.*?)\\}',c,re.S) if s=='latin' for u in re.findall(r'url\\((.*?)\\)',b)][0])")
  curl -sS -o "cache/fonts/${name}.woff2" "$url"
done
echo "assets ready"
