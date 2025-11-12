
from flask_frozen import Freezer
from main import app

# Flask アプリを静的 HTML に書き出す設定。
# GitHub Pages へ公開するときに `docs/` 配下へ出力する想定。
app.config['FREEZER_DESTINATION'] = 'docs'
freezer = Freezer(app)

if __name__ == '__main__':
    # `python freeze.py` で静的サイトを生成する。
    freezer.freeze()
