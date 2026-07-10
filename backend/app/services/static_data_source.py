import os


class StaticDataSourceConfigError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason


def get_static_data_source() -> str:
    value = os.getenv("ZYCS_STATIC_DATA_SOURCE", "json").strip().lower()
    if value in {"", "json", "postgres"}:
        return value or "json"
    raise StaticDataSourceConfigError(
        "ZYCS_STATIC_DATA_SOURCE must be unset, 'json', or 'postgres'"
    )


def get_database_url() -> str:
    database_url = os.getenv("ZYCS_DATABASE_URL", "").strip()
    if not database_url:
        raise StaticDataSourceConfigError(
            "ZYCS_DATABASE_URL is required when ZYCS_STATIC_DATA_SOURCE=postgres"
        )
    return database_url


def should_use_postgres_static_data() -> bool:
    return get_static_data_source() == "postgres"

