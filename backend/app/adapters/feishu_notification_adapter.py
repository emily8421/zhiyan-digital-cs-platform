import base64
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


_VALID_NOTIFY_MODES = {"mock", "sandbox", "disabled"}


@dataclass(frozen=True)
class FeishuNotificationResult:
    send_status: str
    payload: dict[str, object]
    mock: bool


class FeishuNotificationConfigError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason


class FeishuNotificationSendError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason


def deliver_feishu_notification(
    event_type: str,
    related_id: str,
    target_type: str,
    payload: dict[str, object],
) -> FeishuNotificationResult:
    if target_type != "feishu":
        return _mock_result(payload, "non_feishu_target")

    try:
        mode = get_feishu_notify_mode()
    except FeishuNotificationConfigError as error:
        return _mock_result(payload, error.reason)

    if mode in {"mock", "disabled"}:
        return _mock_result(payload, f"mode_{mode}")

    try:
        config = get_feishu_sandbox_config()
    except FeishuNotificationConfigError as error:
        return _mock_result(payload, error.reason)

    message = build_feishu_text_message(event_type, related_id, payload)
    request_body = build_signed_feishu_request_body(message, config["secret"])
    try:
        _post_json(config["webhook_url"], request_body, config["timeout_seconds"])
    except FeishuNotificationSendError as error:
        failed_payload = _base_delivery_payload(payload)
        failed_payload.update(
            {
                "notify_mode": "sandbox",
                "send_status": "failed",
                "fallback_reason": error.reason,
            }
        )
        return FeishuNotificationResult(
            send_status="failed",
            payload=failed_payload,
            mock=True,
        )

    sent_payload = _base_delivery_payload(payload)
    sent_payload.update(
        {
            "notify_mode": "sandbox",
            "send_status": "sent",
            "feishu_msg_type": "text",
            "mock": False,
        }
    )
    return FeishuNotificationResult(send_status="sent", payload=sent_payload, mock=False)


def get_feishu_notify_mode() -> str:
    value = os.getenv("ZYCS_FEISHU_NOTIFY_MODE", "mock").strip().lower()
    if value == "":
        return "mock"
    if value not in _VALID_NOTIFY_MODES:
        raise FeishuNotificationConfigError(
            "ZYCS_FEISHU_NOTIFY_MODE must be unset, 'mock', 'sandbox', or 'disabled'"
        )
    return value


def get_feishu_sandbox_config() -> dict[str, Any]:
    webhook_url = os.getenv("ZYCS_FEISHU_WEBHOOK_URL", "").strip()
    secret = os.getenv("ZYCS_FEISHU_WEBHOOK_SECRET", "").strip()
    timeout_seconds = _get_timeout_seconds()
    if not webhook_url or not secret:
        raise FeishuNotificationConfigError(
            "ZYCS_FEISHU_WEBHOOK_URL and ZYCS_FEISHU_WEBHOOK_SECRET are required when ZYCS_FEISHU_NOTIFY_MODE=sandbox"
        )
    return {
        "webhook_url": webhook_url,
        "secret": secret,
        "timeout_seconds": timeout_seconds,
    }


def build_feishu_text_message(
    event_type: str,
    related_id: str,
    payload: dict[str, object],
) -> dict[str, object]:
    title = "知衍数字客服 Demo 通知"
    lines = [
        title,
        f"类型：{event_type}",
        f"关联 ID：{related_id}",
        "环境：sandbox",
        "说明：仅沙箱验证，不包含真实客户隐私或生产数据。",
    ]
    if event_type == "handoff":
        _append_if_present(lines, "风险等级", payload.get("risk_level"))
        _append_if_present(lines, "转人工原因", payload.get("reason"))
        _append_if_present(lines, "建议负责人", payload.get("suggested_owner"))
    if event_type == "knowledge_gap":
        _append_if_present(lines, "缺口问题", payload.get("question"))
        tags = payload.get("tags")
        if isinstance(tags, list) and tags:
            lines.append(f"建议标签：{', '.join(str(tag) for tag in tags)}")
    return {"msg_type": "text", "content": {"text": "\n".join(lines)}}


def build_signed_feishu_request_body(
    message: dict[str, object],
    secret: str,
    timestamp: int | None = None,
) -> dict[str, object]:
    resolved_timestamp = int(time.time()) if timestamp is None else timestamp
    body = dict(message)
    body["timestamp"] = str(resolved_timestamp)
    body["sign"] = create_feishu_signature(str(resolved_timestamp), secret)
    return body


def create_feishu_signature(timestamp: str, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(string_to_sign, digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def _post_json(
    webhook_url: str,
    body: dict[str, object],
    timeout_seconds: float,
) -> dict[str, object]:
    request = urllib.request.Request(
        webhook_url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise FeishuNotificationSendError("feishu_request_failed") from exc
    if not response_body:
        return {}
    try:
        parsed = json.loads(response_body)
    except json.JSONDecodeError as exc:
        raise FeishuNotificationSendError("feishu_response_not_json") from exc
    if isinstance(parsed, dict):
        code = parsed.get("code")
        status_code = parsed.get("StatusCode")
        if code not in {None, 0} or status_code not in {None, 0}:
            raise FeishuNotificationSendError("feishu_response_not_ok")
        return parsed
    raise FeishuNotificationSendError("feishu_response_not_object")


def _mock_result(payload: dict[str, object], reason: str) -> FeishuNotificationResult:
    mock_payload = _base_delivery_payload(payload)
    mock_payload.update(
        {
            "notify_mode": "mock",
            "send_status": "mocked",
            "fallback_reason": reason,
            "mock": True,
        }
    )
    return FeishuNotificationResult(send_status="mocked", payload=mock_payload, mock=True)


def _base_delivery_payload(payload: dict[str, object]) -> dict[str, object]:
    safe_payload = dict(payload)
    safe_payload.pop("webhook_url", None)
    safe_payload.pop("secret", None)
    return safe_payload


def _append_if_present(lines: list[str], label: str, value: object) -> None:
    if value is None:
        return
    text = str(value).strip()
    if text:
        lines.append(f"{label}：{text}")


def _get_timeout_seconds() -> float:
    raw_value = os.getenv("ZYCS_FEISHU_REQUEST_TIMEOUT_SECONDS", "5").strip()
    try:
        timeout_seconds = float(raw_value)
    except ValueError as exc:
        raise FeishuNotificationConfigError(
            "ZYCS_FEISHU_REQUEST_TIMEOUT_SECONDS must be a positive number"
        ) from exc
    if timeout_seconds <= 0:
        raise FeishuNotificationConfigError(
            "ZYCS_FEISHU_REQUEST_TIMEOUT_SECONDS must be a positive number"
        )
    return timeout_seconds
