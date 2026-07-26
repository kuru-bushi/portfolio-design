#!/usr/bin/env python3
"""現役候補ページから本番 index.html を生成する。

公開サイト（GitHub Pages）は push 時に GitHub Actions がこのスクリプトを実行して
デプロイするため、index.html を直接編集せず、SRC の候補ページを編集して push する。
採用候補を切り替えるときは SRC を書き換える。
"""
import re
from pathlib import Path

SRC = Path("drafts/mock-p2d2-oilmoon.html")  # 現役候補（採用アイコン: D2 3D 油絵の月）
DST = Path("index.html")
TITLE = "IKEDA.K — Portfolio"

html = SRC.read_text(encoding="utf-8")

# 草案用タイトルを本番タイトルへ
html = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", html, count=1)

# 草案用の「パターン一覧へ」フローティングリンク（.pback）の CSS とマークアップを除去
html = re.sub(r"  \.pback \{[^}]*\}\n  \.pback:hover[^\n]*\n\n", "", html, count=1)
html = re.sub(r"\n    \.pback[^\n]*", "", html, count=1)
html = re.sub(r'<a class="pback[^\n]*\n', "", html, count=1)

if ".pback" in html or "p2-index" in html:
    raise SystemExit("エラー: 草案用要素（.pback / p2-index）を除去しきれていません")

DST.write_text(html, encoding="utf-8")
print(f"generated {DST} from {SRC}")
