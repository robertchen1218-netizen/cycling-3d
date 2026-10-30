# GPX 3D 坡度地形

把 GPX 騎乘紀錄放在真實地形（AWS Terrain Tiles 高程 + 衛星影像）上，用 3D 回放，路線依坡度著色。單一 `index.html`（Three.js r128），放在 GitHub Pages 就能用。

網站：<https://robertchen1218-netizen.github.io/cycling-3d/>

## 功能

- **歷史路線**：`rides/` 裡的 GPX，依日期新到舊排序，預設開最新一筆；也可以上傳或拖放自己的 GPX。
- **騎乘統計**：總距離、爬升／下降、最大坡度、最高點；有時間資料時另外顯示日期、總時間、移動時間（不算停車休息）、平均速度、最高速度。
- **爬坡路段**：自動找出明顯的爬坡，選一段就跳過去。
- **回放**：播放／暫停、時間軸、播放速度（60×～2400×）、自由／追蹤車後／俯視視角、鏡頭跟隨；點或拖曳下方海拔、速度圖表也能跳到該位置。
- **圖資**：Esri 衛星影像或內政部國土測繪中心正射影像；圖磚下載失敗會自動重試，仍失敗時改用估算地形。
- **藍牙訓練台**（Chrome／Edge，電腦或 Android）：FTMS 訓練台依坡度調整阻力、心率帶、模擬模式，騎完可下載 CSV。
- **手機**：選單可收合、時間軸全寬、按鈕加大，觸控拖曳旋轉、雙指縮放。

## 網址深連結

- `?ride=20261018.gpx`：直接開某條路線（也可以用 `index.json` 裡的名稱）。
- `?ride=20261018.gpx&t=3600`：開在出發後第 3600 秒的位置。暫停或拖動時網址會自動更新，直接複製網址就能分享目前的位置。

## 鍵盤快捷鍵

| 按鍵 | 動作 |
| --- | --- |
| 空白鍵／K | 播放／暫停 |
| ← → | 前後跳 1%（按住 Shift 跳 10%） |
| Home／End | 回到起點／跳到終點 |

焦點在選單、按鈕或滑桿上時，按鍵照原本的方式運作。

## 新增路線

1. （選用）縮小檔案：移除用不到的 extensions、去掉多餘點，約可縮小 90%，網頁載入更快：
   `python3 scripts/simplify_gpx.py rides/武嶺.gpx`
2. 把 GPX 放進 `rides/`，執行 `python3 scripts/make_index.py` 更新 `rides/index.json`（依日期新到舊；已有的名稱會保留，可以手動改成好讀的名稱）。
3. commit 並 push 到 `main`，GitHub Pages 約一分鐘後更新。

`scripts/trim_gpx.py 原檔.gpx 輸出.gpx 公尺` 可以裁掉頭尾一段距離（例如不想公開住家位置時使用），不是必要步驟。

## 部署

Settings → Pages，Source 選 `main` / root。不需要建置步驟。

## 資料來源

- 高程：[AWS Terrain Tiles](https://registry.opendata.aws/terrain-tiles/)（Terrarium 格式）
- 影像：Esri World Imagery、內政部國土測繪中心 NLSC WMTS
- 3D：[Three.js](https://threejs.org/) r128（jsDelivr CDN）
