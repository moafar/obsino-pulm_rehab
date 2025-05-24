# Arquitectura del Proyecto `pulm-rehab`

## Descripción General

**pulm-rehab** es una colección modular de funciones serverless desplegadas en Google Cloud Functions, orientadas al procesamiento, transformación y carga de datos clínicos para programas de rehabilitación pulmonar. El diseño enfatiza la reutilización de componentes, la separación de configuraciones y la gestión segura de credenciales.

---

## Estructura de Carpetas

```
pulm-rehab/
├── common/         # Módulos reutilizables (Excel, Sheets, BigQuery, configuración)
├── config/         # Configuración global en YAML
├── secrets/        # Credenciales sensibles (excluidas del control de versiones)
├── functions/      # Funciones Cloud independientes
│   ├── asma_extract/
│   │   ├── main.py
│   │   ├── config_asma_extract.yaml
│   │   └── common/ -> symlink a ../../common/
│   ├── asma_load/
│   ├── psg_extract/
│   └── psg_load/
├── .env            # Variables de entorno locales (no versionadas)
├── requirements.txt# Dependencias comunes
├── deploy.sh       # Script para desplegar todas las funciones
└── README.md
```

---

## Principios de Arquitectura

- **Modularidad:** Cada función es independiente, con su propia configuración y punto de entrada, facilitando el desarrollo y despliegue individual.
- **Reutilización:** El código común se mantiene en `common/` y se accede mediante symlinks desde cada función, evitando duplicidad.
- **Separación de Configuración:** Configuración global y específica por función en archivos YAML.
- **Gestión Segura de Secretos:** Las credenciales y variables sensibles se mantienen fuera de control de versiones, utilizando `.env` y la carpeta `secrets/`.
- **Despliegue Centralizado:** El script `deploy.sh` automatiza el despliegue de todas las funciones.
- **Ejecución Local:** Uso de `functions-framework` para desarrollo y pruebas locales.

---

## Flujo de Datos

1. **Extracción:** Funciones como `asma_extract` y `psg_extract` obtienen datos de fuentes externas (OneDrive, archivos clínicos, etc.) y los procesan.
2. **Transformación:** El procesamiento se realiza usando módulos de `common/` (por ejemplo, pandas, openpyxl).
3. **Carga:** Funciones como `asma_load` y `psg_load` envían los datos procesados a destinos como Google BigQuery o Google Sheets.
4. **Configuración:** Cada función utiliza su propio archivo de configuración YAML para parámetros específicos de procesamiento y credenciales.

---

## Dependencias Principales

- `functions-framework`: Para ejecución local.
- `pandas`, `openpyxl`: Procesamiento de datos.
- `gspread`, `google-auth`, `google-cloud-bigquery`: Integraciones con servicios de Google.
- `pyyaml`, `python-dotenv`: Manejo de configuración y variables de entorno.

---

## Despliegue y Entorno

1. Configura variables de entorno y credenciales en `.env` y `secrets/` (no versionados).
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Despliega funciones:
   ```bash
   ./deploy.sh
   ```
4. Para pruebas locales:
   ```bash
   cd functions/<nombre_funcion>
   functions-framework --target=<nombre_funcion>
   ```

---

## Seguridad

- Las credenciales de GCP nunca se suben al repositorio.
- `.env` y `secrets/` están en `.gitignore`.
- El acceso a APIs de Google está restringido mediante variables de entorno y configuración segura.

---

## Consideraciones de Escalabilidad

- La estructura modular permite añadir nuevas funciones fácilmente.
- La carpeta `common/` puede crecer para centralizar utilidades compartidas.
- Si alguna función requiere dependencias específicas, se puede incluir un `requirements.txt` en su carpeta.

---

## Futuras Mejoras

- Añadir tests automatizados para cada función.
- Implementar integración continua.
- Documentar cada módulo de `common/`.
- Mejorar la trazabilidad de ejecuciones y logging centralizado.

---

> _Este archivo describe la arquitectura técnica y las decisiones de diseño del proyecto. Para información operacional o instrucciones de uso, ver `README.md`._
