# GPX 3D 坡度地形

1. 把整個資料夾內容推到 GitHub 儲存庫，Settings → Pages，Source 選 main / root。
2. 公開前先裁頭尾：`python3 scripts/trim_gpx.py 原檔.gpx rides/武嶺.gpx 300`
3. 把 GPX 放進 `rides/` 並 push，Actions 會自動更新 `rides/index.json`。
4. 開啟 `https://帳號.github.io/儲存庫/`，或用 `?ride=武嶺.gpx` 直接指定路線。
