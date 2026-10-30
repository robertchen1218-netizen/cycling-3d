# GPX 3D 坡度地形

1. 把整個資料夾內容推到 GitHub 儲存庫，Settings → Pages，Source 選 main / root。
2. 公開前先裁頭尾：`python3 scripts/trim_gpx.py 原檔.gpx rides/武嶺.gpx 300`
3. 縮小檔案（移除用不到的 extensions、去掉多餘點，約可縮小 90%）：`python3 scripts/simplify_gpx.py rides/武嶺.gpx`
4. 把 GPX 放進 `rides/` 後執行 `python3 scripts/make_index.py` 更新 `rides/index.json`（依日期新到舊，網頁預設開最新一筆；已有的名稱會保留），再 push。
5. 開啟 `https://帳號.github.io/儲存庫/`，或用 `?ride=武嶺.gpx` 直接指定路線。
