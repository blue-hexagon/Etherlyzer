import datetime
from pathlib import Path

from etherlyzer.util.dirs import DEFAULT_CACHE_DIR
from etherlyzer.util.knobs import etherlyzer_knobs


class RegistryCache:
    def __init__(self, name: str, cache_dir: Path | None = None):
        self.name = name
        self.cache_dir = cache_dir if cache_dir is not None else DEFAULT_CACHE_DIR
        # Check that filepath exists
        # Get file mod ts if, else set to 0.0 (epoch zero)
        # Modify stateful variable that is used later to ensure a (recent) copy exists.
        f_mod_ts = self.filepath.stat().st_mtime if self.filepath.exists() else 0.0
        self.last_retrieved = datetime.datetime.fromtimestamp(
            f_mod_ts,
            tz=datetime.UTC,
        )
        self.update_interval: datetime.timedelta = datetime.timedelta(
            hours=etherlyzer_knobs.db_update_interval_hours
        )

    @property
    def filepath(self) -> Path:
        return self.cache_dir / Path("".join([self.name, ".csv"]))

    def need_updates(self, inform_if_synced_about_expiration: bool = False) -> bool:
        expires = self.last_retrieved + self.update_interval
        expires_humanized = expires.replace(microsecond=0)
        now = datetime.datetime.now(datetime.UTC)
        f_not_exists = not self.filepath.exists()

        if f_not_exists and etherlyzer_knobs.show_sync_messages:
            print(f"Cache for {self.name} not found.")
        elif expires <= now and etherlyzer_knobs.show_sync_messages:
            print(f"Cache for {self.name} has expired.")
        elif etherlyzer_knobs.show_sync_messages and inform_if_synced_about_expiration:
            namelen = len("EtherType") - len(self.name)
            print(f"Cache for {self.name} expires at: {' ' * namelen} {expires_humanized} UTC")

        return f_not_exists or expires <= now
