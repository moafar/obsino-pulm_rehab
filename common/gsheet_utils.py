import os
import gspread
import pandas as pd
from google.auth import default
from common.logger import get_logger

logger = get_logger("asma_extract")

def escribir_dataframe_a_hoja(spreadsheet_id: str, sheet_name: str, df):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds, _ = default()
    client = gspread.authorize(creds)

    logger.info(f"Usando spreadsheet_id: {spreadsheet_id} y sheet_name: {sheet_name}")
    hoja = client.open_by_key(spreadsheet_id).worksheet(sheet_name)

    # Convertir tipos no compatibles antes de enviar
    df = df.copy()

    # 1. Convertir datetime a string
    datetime_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns
    for col in datetime_cols:
        df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 2. Reemplazar NaN por None
    df = df.astype(object).where(pd.notnull(df), None)

    # Actualizar contenido
    hoja.clear()
    hoja.update([df.columns.tolist()] + df.values.tolist())
