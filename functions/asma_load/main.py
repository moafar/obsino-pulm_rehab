from common.config import load_config
import os

def asma_load(request):
    cfg = load_config("asma_load")
    env = os.getenv("ENV")
    return {
        "funcion": "asma_load",
        "spreadsheet_id": cfg.get("gspreadsheet_id"),
        "hoja": cfg.get("gspreadsheet_sheet_name"),
        "env": env
    }, 200
