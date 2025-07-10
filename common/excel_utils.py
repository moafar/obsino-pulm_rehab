# Funciones para trabajar con archivos Excel

import requests
import pandas as pd
from io import BytesIO

def leer_excel_desde_url(
    url: str,
    sheet_name: str,
    names=None,
    skiprows: int = 0,
    col_final: str = "IZ"
) -> pd.DataFrame:
    usecols = f"A:{col_final}"
    
    response = requests.get(url)
    response.raise_for_status()
    with BytesIO(response.content) as buffer:
        return pd.read_excel(
            buffer,
            sheet_name=sheet_name,
            engine="openpyxl",
            dtype=str,
            skiprows=skiprows,
            names=names,
            usecols=usecols
        )
