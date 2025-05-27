# asma_load.main

import functions_framework
from flask import jsonify, request
from google.cloud import bigquery
from datetime import datetime, timezone, date
from common.config import load_config
from common.formatting import normalizar_campos_datetime, preparar_datos_para_bq


@functions_framework.http
def asma_load(request):
    try:
        # Cargar configuración desde archivo
        cfg = load_config("asma_load")

        campos_datetime = cfg.get("campos_datetime", [])
        project_id = cfg.get("bq_project_id")
        dataset_id = cfg.get("bq_dataset_id")
        tabla_destino = cfg.get("bq_table_id")
        campo_fecha = cfg.get("campo_fecha_particion")
        table_id = f"{project_id}.{dataset_id}.{tabla_destino}"

        print("🧾 Tabla destino configurada:", cfg.get("bq_table_id"))
        print("🧾 Dataset configurado:", cfg.get("bq_dataset_id"))
        print("🧾 Campos en config:", list(cfg.keys()))


        # Detectar si se debe truncar la tabla (solo en el primer chunk)
        is_first = request.args.get("is_first", "false").lower() == "true"

        # Leer datos del cuerpo JSON
        data = request.get_json()
        # Debug: primer elemento recibido
        if data:
            print("Primer registro recibido:", data[0])
        else:
            print("No se recibieron datos.")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        client = bigquery.Client()

        # Truncar la tabla solo si es el primer chunk
        if is_first:
            truncate_query = f"TRUNCATE TABLE `{table_id}`"
            client.query(truncate_query).result()

        # Validar y normalizar campo de fecha (partición)
        for i, item in enumerate(data):
            fecha_raw = item.get(campo_fecha)
            if not fecha_raw:
                return jsonify({"status": "error", "message": f"Falta '{campo_fecha}' en fila {i}"}), 400
            try:
                fecha = date.fromisoformat(str(fecha_raw)[:10])
                item[campo_fecha] = fecha.isoformat()
            except ValueError:
                return jsonify({"status": "error", "message": f"'{campo_fecha}' inválida en fila {i} ({fecha_raw})"}), 400

        # ✅ Normalizar campos DATETIME según configuración
        data, error = normalizar_campos_datetime(data, campos_datetime)
        if error:
            return error

        # Limpieza de campos vacíos y adición de marca de tiempo
        data = preparar_datos_para_bq(data, now)

        # Insertar en BigQuery (transaccional)
        errors = client.insert_rows_json(table_id, data) # type: ignore
        if errors:
            print("❌ Error al insertar en BigQuery. Detalles:")
            for err in errors:
                print(err)  # Muestra fila, mensaje y campo 
            return jsonify({
                "status": "error",
                "message": "Error al insertar. Ningún registro fue guardado.",
                "details": errors
            }), 400

        return jsonify({
            "status": "success",
            "rows_inserted": len(data) # type: ignore
        })

    except Exception as e:
        return jsonify({"status": "exception", "details": str(e)}), 500
