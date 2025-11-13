# Agent.md

- Frozen-Flask
- Playwright (E2E テスト)
- mkdocs / mike（静的サイト・GitHub Pages 用）
   - GitHub Codespaces では `pip install -r requirements.txt` → `flask --app main run --host 0.0.0.0 --port 5000`
- Global 行動
  - MultipleSampling / Resolution / Tolerance± は TriOrb メニューの Field セクションで一括管理。値変更時は全 Field に反映
- Devices
  - `Export_ScanPlanes` と `Export_FieldsetsAndFields` には Right/Left デバイスをデフォルト追加
- Plotly オーバーレイ
- `<SdImportExport>` 以下の構造は変更を避け、TriOrb は `<TriOrb_SICK_SLS_Editor>` 配下で扱う
- ファイル読み書きコマンド（保存/読み込みなど）は Agent 承認なしに実行してよい
- ファイルを変更した場合は最低限 Flask を起動してコンソールエラーが出ないことを確認
- `tests/` 配下にユニットテストと Playwright テストを配置
- Playwright テストは `python tests/playwright/test_shapes.py`
- テスト項目は `TestMatrix.md` を参照

## CI / デプロイ
- `.github/workflows/test.yml` で push / pull request 時に `pytest` を実行
- `.github/workflows/deploy.yml` で `main` への push 時に `mike deploy --push --branch gh-pages latest --update-aliases` を自動実行
- `GITHUB_TOKEN` による `gh-pages` ブランチへの書き込みが発生するため、必要に応じて保護ルールを調整
## 鐝剧姸銇富瑕併偪銈广偗
- 銈点兂銉椼儷 XML (`sample/20251111-105839_ScannerDTM-Export.sgexml`) 銈掋儥銉笺偣銇� UI 銇� XML 銈掑悓鏈熴仌銇涖倠
- Plotly 銇с伄鍥冲舰锛圥olygon / Rectangle / Circle锛夋弿鐢汇�佺法闆嗐�佷繚瀛�
- TriOrb 銉°儖銉ャ兗銈� Structure Menu 銇法闆嗕綋楱撴敼鍠�

## 娉ㄦ剰鐐广兓銉娿儸銉冦偢
- Thinking 涓伄 Python 銈炽優銉炽儔瀹熻銇渶灏忛檺銇仚銈�
- FileInfo 銇� TriOrb 銇儑銉笺偪銈掗噸瑜囥仌銇涖仾銇勩�俆riOrb 銇�ゃ伅 `TriOrb_SICK_SLS_Editor` 銇伄銇垮嚭鍔�
- `Export_FieldsetsAndFields` 銇� Polygon/Circle/Rectangle 銇� UI 鈫� XML 闁撱仹蹇呫仛涓�鑷淬仌銇涖倠
- Global 琛屽嫊  
  - MultipleSampling / Resolution / Tolerance卤 銇� TriOrb 銉°儖銉ャ兗銇� Field 銈汇偗銈枫儳銉炽仹涓�鎷鐞嗐�傚�ゅ鏇存檪銇叏 Field 銇弽鏄�  
  - 銉囥儛銉冦偘鐢ㄣ伀 `?debug` 銈掍粯銇戙仧 URL 銇с儠銈ｃ兗銉儔鍊嬪垾鍏ュ姏銈掕〃绀哄彲鑳�
- Devices  
  - `Export_ScanPlanes` 銇� `Export_FieldsetsAndFields` 銇伅 Right/Left 銉囥儛銈ゃ偣銈掋儑銉曘偐銉儓杩藉姞  
  - Typekey 閬告姙銇� TypekeyVersion / TypekeyDisplayVersion 銈掋偣銈儯銉炽儣銉兗銉炽亱銈夎瀹�
- Plotly 銈兗銉愩兗銉偆  
  - Fieldset 鍥冲舰銇� TriOrb 銇� FieldOfView 鎵囥倰鍚屾檪銇弿鐢汇�傛墖銇渶鑳岄潰銇弿鐢汇仐銆丼tandingUpsideDown 銇仼銇睘鎬у鍖栥伀杩介殢
- XML 鍑哄姏鏅傘伅 `SdImportExport` 銇� `xmlns:xsd` / `xmlns:xsi` 銇ㄦ渶鏂� Timestamp 銈掑繀銇氬惈銈併�併偟銉炽儣銉� XML 銇ㄥ悓銇樿绱犻爢銈掍繚銇�
- `<SdImportExport>` 浠ヤ笅銇閫犮伅澶夋洿銈掗伩銇戙�乀riOrb 銇亗銇忋伨銇� `<TriOrb_SICK_SLS_Editor>` 閰嶄笅銇ф壉銇�
- 銉曘偂銈ゃ儷瑾伩鏇搞亶銈炽優銉炽儔锛堜繚瀛�/瑾伩杈笺伩銇仼锛夈伅 Agent 鎵胯獚銇仐銇仢銇伨銇惧疅琛屻仐銇︺倛銇�
- 銉曘偂銈ゃ儷鍐呭銈掑鏇淬仐銇熷牬鍚堛�佹渶浣庨檺闁嬨亜銇熴仺銇嶃伀Console銈ㄣ儵銉笺亴鍑恒仾銇勩亾銇ㄣ倰銉嗐偣銉堛仚銈嬨亾銇�

## 銉嗐偣銉�
- `tests/` 閰嶄笅銇儲銉嬨儍銉堛儐銈广儓銈掗厤缃�
- `pytest` 銈掍娇鐢ㄣ仐銇︺儐銈广儓銈掑疅琛�
- 銉嗐偣銉堥爡鐩伅TestMatrix.md銈掑弬鐓�

## 銈炽儫銉ャ儖銈便兗銈枫儳銉�
- 銉椼儹銈搞偋銈儓銇枹銇欍倠璩晱銈勫叡鏈変簨闋呫伅閫熴倓銇嬨伀鍫卞憡銇欍倠
- Agent 鑷韩銇綔妤姸娉併倐閬╁疁鍏辨湁銇欍倠
- 鍘熷墖鏃ユ湰瑾炪仹蹇滅瓟銇欍倠
## 2025-11-XX 旛朰
- Plotly 壓晹偺 Fieldset / TriOrb Shapes 僼傿儖僞偼僩僌儖僺儖 UI 慜採丅renderFieldsetCheckboxes/renderTriOrbShapeCheckboxes 偱昁偢嵞惗惉偟丄慡慖戰儃僞儞偼嵞昤夋屻偵忬懺傪崌傢偣傞偙偲丅
- New 幚峴屻傕 fieldsetDevices / fieldOfViewDegrees 傪曐帩偟丄renderFieldsetDevices丒renderFieldsetGlobal 幚峴仺renderFigure丅Device fan trace 傪昁偢 Plotly 傊搉偡丅
- Fieldset 偑 0 審偱傕 buildFieldsetTraces 偼 buildDeviceOverlayTraces 傪曉偡 (愵偑徚偊側偄傛偆偵)丅
