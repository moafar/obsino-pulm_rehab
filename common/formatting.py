from datetime import datetime
from flask import jsonify

def normalizar_campos_datetime(data, campos_datetime):
    """
    Convierte los valores de campos tipo DATETIME al formato ISO compatible con BigQuery.
    Acepta formatos como 'dd/mm/yyyy' o ISO (yyyy-mm-dd HH:MM:SS).

    Parameters:
        data (list[dict]): Lista de registros a procesar.
        campos_datetime (list[str]): Lista de nombres de campos tipo DATETIME.

    Returns:
        (list[dict], tuple): Registros transformados o una tupla con mensaje de error (dict, status_code).
    """
    for i, item in enumerate(data):
        for campo in campos_datetime:
            valor = item.get(campo)
            if valor:
                try:
                    if isinstance(valor, str):
                        if '/' in valor:
                            # dd/mm/yyyy -> yyyy-mm-dd HH:MM:SS
                            valor = datetime.strptime(valor.strip(), '%d/%m/%Y').strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            valor = datetime.fromisoformat(valor.strip()).strftime('%Y-%m-%d %H:%M:%S')
                    item[campo] = valor
                except Exception:
                    return None, (jsonify({
                        "status": "error",
                        "message": f"Valor inválido para '{campo}' en fila {i}: '{item[campo]}'"
                    }), 400)
    return data, None

def preparar_datos_para_bq(data, timestamp):
    """
    Limpia los campos vacíos ("") convirtiéndolos a None, y agrega el campo 'migrado' con timestamp.

    Parameters:
        data (list[dict]): Registros a preparar
        timestamp (str): Marca de tiempo en formato ISO (usualmente datetime.now(timezone.utc).isoformat())

    Returns:
        list[dict]: Registros transformados listos para insertar en BigQuery
    """
    for item in data:
        for k, v in item.items():
            if v == "":
                item[k] = None
        item['migrado'] = timestamp
    return data
