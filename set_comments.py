# -*- coding: utf-8 -*-
from pathlib import Path
path=Path('templates/index.html')
lines=path.read_text(encoding='utf-8').splitlines()
lines[917]='    <!-- アプリ全体のヘッダー領域 -->'
lines[921]='    <!-- メインレイアウト：左に Plotly 表示、右に設定メニュー -->'
lines[924]='        <!-- 図形の追加・保存などのツール系 UI -->'
path.write_text('\\n'.join(lines)+'\\n',encoding='utf-8')
