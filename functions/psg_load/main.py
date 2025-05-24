from common.config import load_config
import os

def psg_load(request):
    cfg = load_config("psg_load")
    env = os.getenv("ENV")
    return {
        "funcion": "psg_load",
        "spreadsheet_id": cfg.get("gspreadsheet_id"),
        "hoja": cfg.get("gspreadsheet_sheet_name"),
        "env": env
    }, 200
