import os
from pathlib import Path
from dotenv import load_dotenv
import yaml
from typing import Optional

# Cargar .env solo si existe (entorno local)
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Resolver ruta absoluta a credenciales, si está definida y es relativa
creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Solo ajustar si está definida y es ruta relativa
if creds_path:
    creds_path_obj = Path(creds_path)
    if not creds_path_obj.is_absolute():
        full_path = (Path(__file__).resolve().parent.parent / creds_path).resolve()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(full_path)

def load_config(func_name: Optional[str] = None, global_config: bool = False):
    if global_config:
        path = Path(__file__).resolve().parent.parent / "config" / "global.yaml"
    elif func_name:
        path = Path(__file__).resolve().parent.parent / "functions" / func_name / f"config_{func_name}.yaml"
    else:
        path = Path(__file__).resolve().parent.parent / "config.yaml"

    if not path.exists():
        raise FileNotFoundError(f"❌ No se encontró el archivo de configuración: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
