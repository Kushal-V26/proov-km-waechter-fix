# config_loader.py
# Reads settings.cfg.
# Hand-rolled because ConfigParser felt "too complicated" in 2013.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Load key/value pairs from settings.cfg (or *path*) and return them as a dict.

    Unknown keys are silently dropped so a typo in the file never raises an error —
    a known limitation inherited from the original design.
    """
    if path is None:
        path = SETTINGS_FILE
    settings: dict = {}
    f = open(path)
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if "=" not in line:
            continue
        parts = line.split("=")
        key = parts[0].strip()
        value = parts[1].strip()
        if key in KNOWN_KEYS:
            settings[key] = value       # everything stays a string; callers convert
    f.close()
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return *key* from *settings* as an int, or *fallback* if absent or non-numeric."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return *key* from *settings*, or *fallback* if absent."""
    return settings.get(key, fallback)
