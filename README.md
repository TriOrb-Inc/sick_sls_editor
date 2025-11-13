# SICK SLS Editor (Web)

Flask と Plotly で構築された SICK SLS Editor の Web 版です。`.sgexml` (SdImportExport) をロードし、Structure メニューや TriOrb メニューから編集内容をブラウザ上で確認できます。

## 特徴まとめ
- **Structure メニュー**: FileInfo / Export_ScanPlanes / Export_FieldsetsAndFields など XML の主要セクションを編集。GlobalGeometry や Devices は必要時に展開して利用します。
- **TriOrb メニュー**: Field セクションの MultipleSampling / Resolution / Tolerance± を一括調整し、Fieldset 側へ同期します。`?debug` を付けると Fieldset の対応入力も表示されます。
- **図形編集**: Polygon / Circle / Rectangle を Plotly 上で表示し、共有図形 (TriOrb Shapes) と連動します。
- **Plotly 表示**: Fieldset 図形と TriOrb の FieldOfView 扇を重ねて表示し、レスポンシブなレイアウトで編集体験を最適化しています。

ローカル端末でのセットアップ例です。

python main.py  # または flask --app main run
ブラウザで http://127.0.0.1:5000/ を開き、UI を確認します。

### GitHub Codespaces を利用する場合
1. GitHub 上で本リポジトリを開き、`Code` ボタンから `Create codespace on main` を選択します。
2. Codespaces が起動したら VS Code のターミナルで次を実行します。
   ```bash
   pip install -r requirements.txt
   flask --app main run --host 0.0.0.0 --port 5000
   ```
3. `Ports` タブに表示される 5000 番ポートを `Open in Browser` してアプリを確認します。
4. Playwright を使用する場合は追加で `playwright install` を実行します。

- `SdImportExport` ルートには `xmlns:xsd` / `xmlns:xsi` と現在の Timestamp を含めます。
- Export_FieldsetsAndFields の Polygon / Circle / Rectangle は UI と XML で必ず同期させます。
- TriOrb の設定値は `TriOrb_SICK_SLS_Editor` 配下で管理し、FileInfo など他セクションへ重複させません。
### 単体テスト
- Flask レイヤーの基本的な動作確認には `pytest` を使用します。
  ```bash
  pytest
  ```

### Playwright による E2E テスト
1. 依存パッケージをインストールします。
   ```bash
   pip install playwright
   playwright install
2. 別ターミナルで Flask サーバーを起動します。
3. `python tests/playwright/test_shapes.py` を実行すると、TriOrb グローバル値が Fieldset に同期することを検証できます。
4. PowerShell では `run_playwright.ps1` でサーバー起動からテスト実行までを一括で行えます。
## 静的サイトの生成とデプロイ
### Frozen-Flask による静的化
python freeze.py
`docs/` ディレクトリに静的ファイルが生成されます。ローカル確認は `python -m http.server` などで行えます。
### mkdocs + mike での GitHub Pages デプロイ
1. 初回は `mike deploy --push --branch gh-pages latest --update-aliases` を実行します。
2. `mike set-default latest --push --branch gh-pages` で `latest` を既定バージョンに設定します。
3. GitHub Pages の設定で `gh-pages` ブランチを公開対象にします。
## 自動化ワークフロー
- `.github/workflows/test.yml` で push / pull request 時に `pytest` を実行します。
- `.github/workflows/deploy.yml` は `main` へ push されたときに `mike deploy` を実行し、`gh-pages` ブランチへ自動公開します。既定では `latest` バージョンを更新します。
## 既知の手動確認項目
- Plotly 図面に表示される Fieldset / TriOrb Shapes の表示切り替えボタン。
- Save / Load による `.sgexml` ファイルの入出力挙動。
- Device の Typekey 選択時に Version 情報が反映されること。
詳細な手動テスト項目は `TestMatrix.md` を参照してください。
- 銉愩兗銈搞儳銉冲垏銈婃浛銇堛儭銉嬨儱銉笺倰琛ㄧず銇椼仧銇勫牬鍚堛伅銆乣mkdocs-material`銉嗐兗銉炪倰鍒╃敤锛�
	```yaml
	theme:
		name: material
	extra:
		favicon: favicon.ico
		version:
			provider: mike
	```
	銇濄伄寰� `pip install mkdocs-material` 銈掑疅琛屻��
- mike銇�2銇や互涓娿伄銉愩兗銈搞儳銉炽倰銉囥儣銉偆銇椼�乣mike set-default <銉愩兗銈搞儳銉冲悕>`銇с儑銉曘偐銉儓銈掕ō瀹氥仚銈嬨仺銆併儛銉笺偢銉с兂鍒囥倞鏇裤亪銉°儖銉ャ兗銇岃嚜鍕曘仹琛ㄧず銇曘倢銇俱仚銆�
	渚嬶細
	```bash
	mike deploy v1.0
	mike deploy v2.0
	mike set-default v2.0
	```- **Plotly 僼傿儖僞**丗Plotly 僌儔僼壓偺 Fieldset/TriOrb Shapes 偺壜帇愗懼偼僩僌儖僺儖 UI丅All check/All uncheck 儃僞儞偼 UI 傪嵞昤夋偟偰偐傜忬懺傪崌傢偣傞丅
- **Save**丗\Save (TriOrb)\ 偼 TriOrb XML丄\Save (SICK)\ 偼廬棃峔憿傪 Device 扨埵 {DeviceName}_timestamp.sgexml 偱曐懚丅Load 帪偼 TriOrb 敾掕僼儔僌偱帺摦敾暿丅
