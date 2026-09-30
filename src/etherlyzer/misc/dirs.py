from pathlib import Path

from platformdirs import user_cache_dir

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = Path(user_cache_dir(appname="etherlyzer", appauthor="Manjana", version="1.0", ensure_exists=True))
CACHE_ROOT = PROJECT_ROOT / "cache"
USER_INPUT_ROOT = DATA_ROOT / "userinput"

for directory in (DATA_ROOT, CACHE_ROOT, USER_INPUT_ROOT):
    directory.mkdir(parents=True, exist_ok=True)
