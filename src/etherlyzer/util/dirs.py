from pathlib import Path

from platformdirs import user_cache_dir

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PLATFORM_DIR = Path(user_cache_dir(appname="etherlyzer", appauthor="Manjana", version="1.0", ensure_exists=True))
