# pulm-rehab

**pulm-rehab** es un conjunto de funciones serverless desplegadas en Google Cloud Functions, diseñadas para procesar, transformar y cargar datos clínicos relacionados con programas de rehabilitación pulmonar.

## 🧱 Estructura del proyecto

```
pulm-rehab/
├── common/             # Módulos reutilizables (Excel, Sheets, BigQuery, configuración)
├── config/             # Configuración global (YAML)
├── secrets/            # Credenciales sensibles (no compartidas en control de versiones)
├── functions/          # Funciones Cloud independientes
│   ├── asma_extract/
│   │   ├── main.py
│   │   ├── config_asma_extract.yaml
│   │   └── common/ → symlink a ../../common/
│   ├── asma_load/
│   ├── psg_extract/
│   └── psg_load/
├── .env                # Variables de entorno locales
├── requirements.txt    # Dependencias comunes
├── deploy.sh           # Script para desplegar todas las funciones
└── README.md
```

## ⚙️ Funciones incluidas

| Función        | Descripción |
|----------------|-------------|
| `asma_extract` | Extrae datos de asma desde archivos de entrada (OneDrive) y los copia en Google Sheets |
| `asma_load`    | Carga datos procesados de asma en BigQuery |

## 🔗 Symlinks y código compartido

Este proyecto utiliza symlinks para compartir una única carpeta `common/` entre todas las funciones. Cada función incluye un enlace simbólico que apunta al código común, lo que evita duplicación y asegura consistencia. Google Cloud Functions sigue estos symlinks durante el despliegue sin problemas.

## 🧬 Estructura interna de cada función

Cada función contiene:

```
functions/<nombre_funcion>/
├── main.py                    # Punto de entrada
├── config_<nombre>.yaml       # Configuración específica
└── common/ → symlink          # Acceso al código compartido
```

Este diseño garantiza que cada función sea modular y configurable de forma independiente, al tiempo que conserva acceso eficiente a componentes reutilizables mediante una arquitectura centralizada y sin redundancias.

## 🚀 Despliegue

Requiere tener instalado `gcloud` y autenticado en el proyecto.

```bash
./deploy.sh
```

Esto desplegará todas las funciones en la región especificada en `.env`.

## 🧪 Ejecución local (debug)

Instala dependencias y ejecuta una función con `functions-framework`:

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar desde carpeta de función
cd functions/asma_extract
functions-framework --target=asma_extract
```

## 🔐 Credenciales

El archivo `.env` debe incluir la ruta al archivo de credenciales de GCP. Este archivo no debe subirse a repositorios:

```
GOOGLE_APPLICATION_CREDENTIALS=secrets/observatorio-ino-1-xxx.json
```

## 📚 Requisitos

- Python 3.10
- Google Cloud CLI (`gcloud`)
- Acceso habilitado a APIs de BigQuery, Cloud Functions y Sheets

## 📄 Licencia

Proyecto interno para aprendizaje y prototipado. No redistribuir sin autorización.

