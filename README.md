# SICK SLS Editor (Web)

Flask + Plotly を用いたブラウザ向け SICK SLS エディタの試作版です。Plotly グラフをローカル UI から作成・保存・読込でき、`Export_ScanPlanes` / `Export_FieldsetsAndFields` / TriOrb 独自メニューを編集した上で `.sgexml` を再生成できます。

## セットアップ
1. Python 3.10 以降をインストール
2. 仮想環境を作成・有効化
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. 依存パッケージをインストール
   ```powershell
   pip install -r requirements.txt
   ```

## 実行方法
```powershell
python main.py          # または  flask --app main run
```
ブラウザで http://127.0.0.1:5000/ を開きます。

## 現在の機能
- Plotly グラフの表示・保存・読込（Trace/Polygon/Circle/Rectangle 等を自動生成）
- FileInfo / Export_ScanPlanes / Export_FieldsetsAndFields 編集 UI（ScanPlane, Device, Fieldset, Field, TriOrb メニュー）
- TriOrb メニューによる MultipleSampling のグローバル制御と Fieldset Device の Typekey 選択
- XML 出力時に `SdImportExport` へ現在 Timestamp と xmlns 属性を付与し、サンプル XML に倣った属性順序でシリアライズ

## 注意
- `sample/20251111-105839_ScannerDTM-Export.sgexml` の構造を元に UI を構成しています。追加の XML スキーマを扱う場合は `main.py` / `templates/index.html` のロジックを拡張してください。
