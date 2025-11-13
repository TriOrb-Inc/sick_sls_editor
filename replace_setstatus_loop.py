from pathlib import Path
path=Path('templates/index.html')
text=path.read_text(encoding='utf-8')
for target,new_text in [
    ('', 'setStatus(\n                ${updatedShape.name} を更新しました。（ フィールドに紐付け）。,\n                \"ok\"\n              );'),
    ('', 'setStatus(\n                ${draft.name} を追加しました。（ フィールドに紐付け）。,\n                \"ok\"\n              );'),
]:
    while True:
        idx=text.find(target)
        if idx==-1:
            break
        start=text.rfind('setStatus(', 0, idx)
        end=text.find(');', idx)+2
        text=text[:start]+new_text+text[end:]
path.write_text(text,encoding='utf-8')
