# asma_extract.main

from common.config import load_config
from common.excel_utils import leer_excel_desde_url
from common.gsheet_utils import escribir_dataframe_a_hoja
import pandas as pd
import numpy as np
import logging
from common.logger import get_logger
from flask import jsonify


logger = get_logger("asma_extract")

def asma_extract(request):
    logger.info("⚙️ Iniciando asma_extract")
    try:
        cfg = load_config("asma_extract")
        logger.info("✅ Config cargada")
        logger.debug(f"🧩 Claves en config: {list(cfg.keys())}")

        # Leer parámetros de configuración
        skiprows = cfg.get("skiprows", 0)
        cols = cfg.get("column_names", [])
        numeric_cols = cfg.get("numeric_columns", [])
        date_cols = cfg.get("date_columns", [])

        # Leer archivo Excel desde OneDrive
        df = leer_excel_desde_url(
            url=cfg["onedrive_url"],
            sheet_name=cfg["onedrive_sheet_name"],
            skiprows=skiprows,
            col_final=cfg.get("onedrive_col_final")
        )
        logger.info(f"📥 Excel leído con {df.shape[0]} filas y {df.shape[1]} columnas")

        # Recortar columnas
        df = df.iloc[:, :len(cols)]
        # Renombrar columnas
        df.columns = cols
        # Eliminar filas vacías
        df = df.dropna(how="all")
        # Eliminar filas y columnas completamente vacías
        df = df.dropna(how="all").dropna(axis=1, how="all")

        # Castear columnas numéricas
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Castear columnas de fecha
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Castear el resto a string (opcional, si lo necesitas)
        otras_col = [c for c in df.columns if c not in numeric_cols + date_cols]
        df[otras_col] = df[otras_col].astype(str)

        ##########
        spreadsheet_id = cfg.get("gspreadsheet_id")
        sheet_name = cfg.get("gspreadsheet_sheet_name")
        ##########

        if not spreadsheet_id or not sheet_name:
            raise ValueError("🛑 Faltan valores en config: gspreadsheet_id o gspreadsheet_sheet_name")
       
        # Escribir en Google Sheets
        escribir_dataframe_a_hoja(
            cfg["gspreadsheet_id"],
            cfg["gspreadsheet_sheet_name"],
            df
        )
        logger.info("📤 Datos escritos en Google Sheets")

        return jsonify({
            "status": "ok",
            "filas": int(df.shape[0])
        }), 200

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        logger.error("❌ Excepción capturada:\n" + error_msg)
        
        # ⚠️ No devuelvas el traceback completo en producción
        return jsonify({
            "status": "error",
            "mensaje": str(e)
        }), 500
