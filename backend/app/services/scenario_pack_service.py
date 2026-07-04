import json
from functools import lru_cache
from pathlib import Path

from app.schemas.scenario_packs import ScenarioPack, ScenarioPackSummary, to_summary

_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "scenario_packs"


class ScenarioPackNotFoundError(Exception):
    def __init__(self, scenario_pack_code: str) -> None:
        self.scenario_pack_code = scenario_pack_code


class InvalidScenarioPackError(Exception):
    def __init__(self, scenario_pack_code: str, reason: str) -> None:
        self.scenario_pack_code = scenario_pack_code
        self.reason = reason


@lru_cache
def load_scenario_packs() -> dict[str, ScenarioPack]:
    packs: dict[str, ScenarioPack] = {}
    for path in sorted(_DATA_DIR.glob("*.json")):
        raw_data = json.loads(path.read_text(encoding="utf-8-sig"))
        pack = ScenarioPack.model_validate(raw_data)
        _validate_scenario_pack(pack)
        packs[pack.code] = pack
    return packs


def list_scenario_pack_summaries() -> list[ScenarioPackSummary]:
    return [to_summary(pack) for pack in load_scenario_packs().values()]


def get_scenario_pack(scenario_pack_code: str) -> ScenarioPack:
    pack = load_scenario_packs().get(scenario_pack_code)
    if pack is None:
        raise ScenarioPackNotFoundError(scenario_pack_code)
    return pack


def _validate_scenario_pack(pack: ScenarioPack) -> None:
    for knowledge_item in pack.knowledge_items:
        if not knowledge_item.source_ref:
            raise InvalidScenarioPackError(pack.code, "knowledge item missing source_ref")
    for mock_record in pack.mock_business_records:
        if not mock_record.is_mock:
            raise InvalidScenarioPackError(pack.code, "mock business record must set is_mock=true")

