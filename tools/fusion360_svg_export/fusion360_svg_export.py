"""
Fusion 360 向けの簡易 SVG エクスポート アドイン（Python 版）。
- Sketch を選択して SVG として書き出す最小構成。
- Scripts/Add-Ins 配下にフォルダーごと配置し、Fusion 360 の Add-Ins から実行する。

SICK SLS Editor の SVG インポート ワークフロー向けに、Fusion 側で
スケッチを SVG 化する用途を想定しています。
"""

import adsk.core
import adsk.fusion
import traceback
import re

COMMAND_ID = "SlsEditor_SvgExport"
COMMAND_NAME = "Export Sketch to SVG (SICK SLS)"
COMMAND_DESCRIPTION = "選択した Sketch を SVG 形式で保存します"

_handlers = []


def _app_and_ui():
    app = adsk.core.Application.get()
    if not app:
        return None, None
    return app, app.userInterface


def _show_error(ui: adsk.core.UserInterface | None, message: str):
    if ui:
        ui.messageBox(message, "SVG Export")


class _CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args: adsk.core.CommandEventArgs):
        app, ui = _app_and_ui()
        design = adsk.fusion.Design.cast(app.activeProduct) if app else None
        if not design:
            _show_error(ui, "Design ワークスペースで実行してください。")
            return

        inputs = args.command.commandInputs
        selection_input = inputs.itemById("sls-sketch")
        file_name_input = inputs.itemById("sls-filename")
        single_layer_input = inputs.itemById("sls-single-layer")
        fit_to_page_input = inputs.itemById("sls-fit")

        if not selection_input or selection_input.selectionCount < 1:
            _show_error(ui, "Sketch を 1 件選択してください。")
            return

        selection = selection_input.selection(0)
        sketch = selection.entity

        folder_dialog = ui.createFolderDialog()
        folder_dialog.title = "SVG の出力先フォルダーを選択"
        if folder_dialog.showDialog() != adsk.core.DialogResults.DialogOK:
            return

        base_name = str(file_name_input.value or f"{sketch.name or 'sketch'}.svg")
        base_name = re.sub(r"\.svg$", "", base_name, flags=re.IGNORECASE)
        file_path = f"{folder_dialog.folder}/{base_name}.svg"

        export_manager = design.exportManager
        options = export_manager.createSVGExportOptions(sketch, file_path)
        options.isSingleLayer = bool(single_layer_input.value)
        options.isFitToPage = bool(fit_to_page_input.value)
        options.isViewScaled = True
        # Polygon の切れ目（パス分割）はスケッチ内のクローズドプロファイルごとに
        # Fusion 標準の SVG Export が自動で区切る。個別の頂点を分割する処理は
        # 行っていないため、エッジを明示的に分けたい場合はスケッチ側で輪郭を
        # それぞれ独立したプロファイルとして作図する。

        succeeded = export_manager.execute(options)
        if succeeded:
            ui.messageBox(f"SVG を保存しました:\n{file_path}", "SVG Export")
        else:
            _show_error(ui, "SVG の保存に失敗しました。")


class _CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args: adsk.core.CommandCreatedEventArgs):
        command = args.command
        inputs = command.commandInputs

        selection_input = inputs.addSelectionInput(
            "sls-sketch", "Sketch", "SVG 化するスケッチを選択"
        )
        selection_input.addSelectionFilter("Sketches")
        selection_input.setSelectionLimits(1, 1)

        inputs.addStringValueInput("sls-filename", "ファイル名", "sls-sketch.svg")
        inputs.addBoolValueInput("sls-single-layer", "単一レイヤーで出力", True, "", True)
        inputs.addBoolValueInput("sls-fit", "用紙に合わせる", True, "", True)

        on_execute = _CommandExecuteHandler()
        command.execute.add(on_execute)
        _handlers.append(on_execute)


def run(_context):
    try:
        app, ui = _app_and_ui()
        if not ui:
            return

        command_definitions = ui.commandDefinitions
        command_definition = command_definitions.itemById(COMMAND_ID)
        if not command_definition:
            command_definition = command_definitions.addButtonDefinition(
                COMMAND_ID, COMMAND_NAME, COMMAND_DESCRIPTION
            )

        on_created = _CommandCreatedHandler()
        command_definition.commandCreated.add(on_created)
        _handlers.append(on_created)

        command_definition.execute()
        adsk.autoTerminate(False)
    except Exception:
        _, ui = _app_and_ui()
        _show_error(ui, traceback.format_exc())


def stop(_context):
    app, ui = _app_and_ui()
    if not ui:
        return

    command_definition = ui.commandDefinitions.itemById(COMMAND_ID)
    if command_definition:
        command_definition.deleteMe()

    _handlers.clear()
