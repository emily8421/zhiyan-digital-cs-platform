from app.schemas.mock_business import MockBusinessRecordResponse
from app.schemas.scenario_packs import MockBusinessRecord
from app.services.scenario_pack_service import load_scenario_packs


class MockRecordNotFoundError(Exception):
    def __init__(self, record_type: str, external_ref: str) -> None:
        self.record_type = record_type
        self.external_ref = external_ref


def get_mock_business_record(record_type: str, external_ref: str) -> MockBusinessRecordResponse:
    normalized_type = record_type.lower()
    normalized_ref = external_ref.upper()

    for pack in load_scenario_packs().values():
        for record in pack.mock_business_records:
            if record.record_type == normalized_type and record.external_ref.upper() == normalized_ref:
                return MockBusinessRecordResponse(**_to_response_fields(record, pack.code))

    raise MockRecordNotFoundError(normalized_type, normalized_ref)


def list_mock_business_records(
    record_type: str | None = None,
    scenario_pack_code: str | None = None,
) -> list[MockBusinessRecordResponse]:
    records: list[MockBusinessRecordResponse] = []
    for pack in load_scenario_packs().values():
        if scenario_pack_code is not None and pack.code != scenario_pack_code:
            continue
        for record in pack.mock_business_records:
            if record_type is not None and record.record_type != record_type.lower():
                continue
            records.append(MockBusinessRecordResponse(**_to_response_fields(record, pack.code)))
    return records


def _to_response_fields(record: MockBusinessRecord, scenario_pack_code: str) -> dict[str, object]:
    source_ref = record.source_ref or f"demo_sandbox:{record.record_type}:{record.external_ref}"
    payload = dict(record.payload)
    payload.setdefault("source_ref", source_ref)
    payload.setdefault("environment", record.environment)
    payload.setdefault("mock", record.is_mock)
    return {
        "record_type": record.record_type,
        "external_ref": record.external_ref,
        "scenario_pack_code": scenario_pack_code,
        "status": record.status,
        "summary": record.summary,
        "next_step": record.next_step,
        "eta": record.eta,
        "source_ref": source_ref,
        "source_system": record.source_system,
        "environment": record.environment,
        "stage": record.stage,
        "payload": payload,
        "mock": record.is_mock,
    }
