import base64
import hashlib
import hmac

import pytest

from app.adapters.feishu_notification_adapter import (
    build_feishu_text_message,
    build_signed_feishu_request_body,
    create_feishu_signature,
    deliver_feishu_notification,
    get_feishu_notify_mode,
)


def test_default_feishu_notify_mode_is_mock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ZYCS_FEISHU_NOTIFY_MODE", raising=False)

    assert get_feishu_notify_mode() == "mock"


def test_feishu_signature_uses_timestamp_and_secret() -> None:
    timestamp = "1720000000"
    secret = "unit-test-secret"
    expected = base64.b64encode(
        hmac.new(
            f"{timestamp}\n{secret}".encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
    ).decode("utf-8")

    assert create_feishu_signature(timestamp, secret) == expected


def test_build_signed_feishu_request_body_does_not_expose_secret() -> None:
    body = build_signed_feishu_request_body(
        {"msg_type": "text", "content": {"text": "hello"}},
        "unit-test-secret",
        timestamp=1720000000,
    )

    assert body["timestamp"] == "1720000000"
    assert body["sign"]
    assert "unit-test-secret" not in str(body)


def test_deliver_feishu_notification_defaults_to_mock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ZYCS_FEISHU_NOTIFY_MODE", raising=False)
    monkeypatch.delenv("ZYCS_FEISHU_WEBHOOK_URL", raising=False)
    monkeypatch.delenv("ZYCS_FEISHU_WEBHOOK_SECRET", raising=False)

    result = deliver_feishu_notification(
        event_type="handoff",
        related_id="handoff_001",
        target_type="feishu",
        payload={"event_type": "handoff", "related_id": "handoff_001"},
    )

    assert result.send_status == "mocked"
    assert result.mock is True
    assert result.payload["notify_mode"] == "mock"


def test_deliver_feishu_notification_sandbox_without_secret_falls_back_to_mock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ZYCS_FEISHU_NOTIFY_MODE", "sandbox")
    monkeypatch.setenv("ZYCS_FEISHU_WEBHOOK_URL", "https://example.invalid/hook")
    monkeypatch.delenv("ZYCS_FEISHU_WEBHOOK_SECRET", raising=False)

    result = deliver_feishu_notification(
        event_type="knowledge_gap",
        related_id="gap_001",
        target_type="feishu",
        payload={"event_type": "knowledge_gap", "related_id": "gap_001"},
    )

    assert result.send_status == "mocked"
    assert result.mock is True
    assert result.payload["fallback_reason"].startswith("ZYCS_FEISHU_WEBHOOK_URL")
    assert "https://example.invalid/hook" not in str(result.payload)


def test_build_feishu_text_message_uses_minimal_sandbox_payload() -> None:
    message = build_feishu_text_message(
        event_type="handoff",
        related_id="handoff_001",
        payload={
            "reason": "投诉舆情问题必须人工确认。",
            "risk_level": "high",
            "suggested_owner": "人工客服值班同事",
        },
    )

    text = message["content"]["text"]
    assert message["msg_type"] == "text"
    assert "handoff_001" in text
    assert "sandbox" in text
    assert "真实客户隐私" in text
