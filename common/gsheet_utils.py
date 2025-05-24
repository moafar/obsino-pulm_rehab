import os
import gspread
from google.auth import default
from common.logger import get_logger

logger = get_logger("asma_extract")

def escribir_dataframe_a_hoja(spreadsheet_id: str, sheet_name: str, df):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds, _ = default()

    client = gspread.authorize(creds)
    logger.info(f"🧪 Usando spreadsheet_id: {spreadsheet_id} y sheet_name: {sheet_name}")
    hoja = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

    # Borrar contenido anterior
    hoja.clear()

    # Escribir encabezado + contenido
    hoja.update([df.columns.values.tolist()] + df.values.tolist())
