import logging
import sys
import os

def get_logger(name: str = "default") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:  # Para no duplicar logs si ya fue configurado
        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Nivel configurable por entorno
        env = os.getenv("ENV", "production")
        level = logging.DEBUG if env == "development" else logging.INFO
        logger.setLevel(level)

    return logger
