from app.schemas.mock_business import MockBusinessRecordResponse
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
                return MockBusinessRecordResponse(
                    record_type=record.record_type,
                    external_ref=record.external_ref,
                    scenario_pack_code=pack.code,
                    status=record.status,
                    summary=record.summary,
                    next_step=record.next_step,
                    eta=record.eta,
                    mock=record.is_mock,
                )

    raise MockRecordNotFoundError(normalized_type, normalized_ref)
