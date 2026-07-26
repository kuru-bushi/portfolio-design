# Codex システムレビュー: スクロール時の表示アクション（2026-07-26）

- レビュアー: Codex CLI (gpt-5.5, --sandbox read-only)
- 対象: drafts/mock-p2e2-impasto.html（mock-p2d2-oilmoon.html はアイコン違いの同一実装）
- 観点: スクロール表示アクションの見やすさ・動きの一貫性・実装の穴（PC=ホバー主役 / スマホ=下スクロール通過グロー の仕様分離後）
- 対応方針: **中程度 1〜3 を修正**（次コミット）。軽微 1〜3 は未対応（影響が小さいため見送り）

---

**重大**

なし。仕様から外れて即座に UX を壊すレベルの問題は見当たりません。

**中程度**

1. **内容**: `prefers-reduced-motion` 時もスクロール系アニメーションが残ります。  
   **該当箇所**: [mock-p2e2-impasto.html](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:55), [604](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:604), [871](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:871), [904](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:904)  
   **理由**: JS では背景ループのみ停止していますが、`.reveal` の移動フェード、`section.focus` の下線伸長、`.mfocus` の通過グロー、`scroll-behavior: smooth`、CSS keyframes は残ります。動きに敏感なユーザーにはまだ負荷があります。  
   **修正案**: `@media (prefers-reduced-motion: reduce)` で `animation: none; transition: none; scroll-behavior: auto;` を適用し、JS 側も `if (!reduced && matchMedia('(hover: none)').matches)` のように `.mfocus` を止めるのが安全です。

2. **内容**: スマホで `:hover` スタイルが残るため、通過グローとタップ後 hover が混ざる可能性があります。  
   **該当箇所**: [187](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:187), [221](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:221), [235](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:235), [280](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:280), [344](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:344)  
   **理由**: 一部のタッチ環境では `:hover` がタップ後に残り、スマホ仕様の「約 1.1 秒で消える通過グロー」と違う持続ハイライトになります。特に `.article:hover` は padding 変化もあり、見た目の一貫性が崩れます。  
   **修正案**: hover 系 CSS を `@media (hover: hover) and (pointer: fine)` に閉じ込め、スマホは `.mfocus` だけで状態表現する構成に寄せるのがよいです。

3. **内容**: 初期表示・アンカー遷移・表示切替で、下スクロールしていないのに `.mfocus` が発火し得ます。  
   **該当箇所**: [905](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:905), [911](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:911), [957](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:957)  
   **理由**: `goingDown` の初期値が `true` なので、IntersectionObserver の初回 callback や `.more` の `display:block` 化で「入ってきた」と判定されると、実スクロールなしでも光る可能性があります。  
   **修正案**: `hasScrolledDown` を別に持ち、実際に `scrollY > lastScrollY` になった後だけ発火させる。展開直後の `.more` は必要なら `mio.observe` の対象から外す、または一度 `requestAnimationFrame` 後に方向判定をリセットするとよいです。

**軽微**

1. **内容**: `.mfocus` の強さが要素間でやや不均一です。  
   **該当箇所**: [345](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:345), [352](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:352), [354](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:354), [355](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:355)  
   **理由**: `.work` は枠・星・背景・見出しが変わって明確ですが、`.article` は青い背景と白文字、`.tl-item` は点だけ、`.contact-box` は枠色だけです。「金色の通過グロー」として認識できる強度に差があります。  
   **修正案**: 各対象に共通の淡い金色 `box-shadow` または `outline-color` を 1 要素 1 箇所だけ足し、強さは `rgba(255, 215, 106, 0.25〜0.45)` 程度に抑えると読みやすさを保てます。

2. **内容**: `.reveal` の IntersectionObserver が発火後も監視を続けます。  
   **該当箇所**: [876](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:876)  
   **理由**: 表示後は `.in` が外れないため、以後の callback は不要です。体感差は小さいですが、スクロール時処理を少し減らせます。  
   **修正案**: `if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }` にする。

3. **内容**: スクロールスパイはヒーロー表示中も `WORKS` が focus / active になります。  
   **該当箇所**: [391](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:391), [938](/mnt/c/Users/USER/Documents/DevClaude/portfolio-desgin/drafts/mock-p2e2-impasto.html:938)  
   **理由**: `cur = secs[0]` 初期化なので、最初の section が中央線を越える前から Works 扱いです。「常に 1 つ focus」という仕様には合いますが、現在地表示としては少し先取りに見えます。  
   **修正案**: 仕様優先なら現状維持で可。違和感を減らすなら、ヒーロー中は nav active だけ非表示にし、section focus は Works のままにするなど表示差をつける案があります。
