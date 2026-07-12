"""LLM Sandbox 适配器（mock-LLM-first）。

定位（见 docs/research/2026-07-11-demo-sandbox-readiness-evaluation.md §5）：
LLM 只作为「证据改写器 / 话术生成器」，不是事实来源。输入只来自已找到证据的回答
（mock_business / knowledge / rule），输出强制透传 source_ref 与 evidence；高风险与
无依据缺口不进入本适配器（由 message_policy_service 在调用前短路）。

本增量只实现 mock 模式（确定性模板改写，零依赖、不联网、不引模型文件）。sandbox 模式
留接口但本增量安全降级到 mock：缺 provider / key 时降级，key 齐备时也降级
（real_call_not_implemented），真实 LLM 调用由后续授权任务实现（RG-003 真实启用仍阻塞）。
"""

import os
from dataclasses import dataclass


_VALID_LLM_MODES = {"disabled", "mock", "sandbox"}

_DEMO_DISCLAIMERS = {
    "knowledge": "（以上来自 Demo 演示知识库，仅供参考，非真实系统。）",
    "mock_business": "（以上进度来自 Demo 模拟业务数据，非真实系统查询。）",
    "rule": "（以上来自 Demo 场景包规则，涉及承诺 / 风险事项以人工确认为准。）",
}


@dataclass(frozen=True)
class LlmResult:
    answer: str
    source_ref: str
    evidence: list[str]
    mock: bool
    mode_used: str
    base_answer_type: str
    fallback_reason: str | None = None


class LlmConfigError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason


def generate_llm_answer(
    question: str,
    base_answer_type: str,
    base_answer: str,
    source_ref: str,
) -> LlmResult | None:
    """对已找到证据的回答做自然语言改写。

    返回 None 表示 LLM 关闭 / 跳过，调用方应保留原 decision。
    返回 LlmResult 时调用方应改写为 answer_type=llm_sandbox 并透传 source_ref / evidence。
    本函数不处理高风险与无依据场景（调用方在证据型 answer_type 上才调用）。
    """
    try:
        mode = get_llm_mode()
    except LlmConfigError:
        # 非法 mode 值按安全口径视为关闭，不改写。
        return None
    if mode == "disabled":
        return None
    if mode == "mock":
        return _mock_rewrite(base_answer_type, base_answer, source_ref, "mock", None)

    # mode == "sandbox"：本增量不实现真实调用，统一安全降级到 mock。
    try:
        get_llm_sandbox_config()
    except LlmConfigError as error:
        return _mock_rewrite(
            base_answer_type, base_answer, source_ref, "mock", error.reason
        )
    return _mock_rewrite(
        base_answer_type,
        base_answer,
        source_ref,
        "mock",
        "sandbox_real_call_not_implemented",
    )


def get_llm_mode() -> str:
    value = os.getenv("ZYCS_LLM_MODE", "disabled").strip().lower()
    if value == "":
        return "disabled"
    if value not in _VALID_LLM_MODES:
        raise LlmConfigError(
            "ZYCS_LLM_MODE must be unset, 'disabled', 'mock', or 'sandbox'"
        )
    return value


def get_llm_sandbox_config() -> dict[str, object]:
    """读取真实 LLM provider 配置（仅在 mode=sandbox 时调用）。

    真实 key / base_url 只通过环境变量注入，绝不写入结果、日志或仓库。
    本增量即使配置齐全也不发起真实调用（见 generate_llm_answer）。
    """
    api_key = os.getenv("ZYCS_LLM_API_KEY", "").strip()
    base_url = os.getenv("ZYCS_LLM_BASE_URL", "").strip()
    if not api_key or not base_url:
        raise LlmConfigError(
            "ZYCS_LLM_API_KEY and ZYCS_LLM_BASE_URL are required when "
            "ZYCS_LLM_MODE=sandbox (real provider not wired in this mock-first increment)"
        )
    return {
        "provider": os.getenv("ZYCS_LLM_PROVIDER", "").strip(),
        "base_url": base_url,
        "timeout_seconds": _get_timeout_seconds(),
        "max_input_chars": _get_max_input_chars(),
        "demo_only": _get_demo_only(),
    }


def _mock_rewrite(
    base_answer_type: str,
    base_answer: str,
    source_ref: str,
    mode_used: str,
    fallback_reason: str | None,
) -> LlmResult:
    marker = f"【LLM Sandbox 改写】依据：{source_ref}。"
    disclaimer = _DEMO_DISCLAIMERS.get(
        base_answer_type, "（以上为 Demo 演示内容，仅供参考。）"
    )
    answer = f"{marker}\n{base_answer}\n{disclaimer}"
    return LlmResult(
        answer=answer,
        source_ref=source_ref,
        evidence=[source_ref],
        mock=True,
        mode_used=mode_used,
        base_answer_type=base_answer_type,
        fallback_reason=fallback_reason,
    )


def _get_timeout_seconds() -> float:
    raw_value = os.getenv("ZYCS_LLM_TIMEOUT_SECONDS", "10").strip()
    try:
        timeout_seconds = float(raw_value)
    except ValueError as exc:
        raise LlmConfigError(
            "ZYCS_LLM_TIMEOUT_SECONDS must be a positive number"
        ) from exc
    if timeout_seconds <= 0:
        raise LlmConfigError("ZYCS_LLM_TIMEOUT_SECONDS must be a positive number")
    return timeout_seconds


def _get_max_input_chars() -> int:
    raw_value = os.getenv("ZYCS_LLM_MAX_INPUT_CHARS", "4000").strip()
    try:
        max_input_chars = int(raw_value)
    except ValueError as exc:
        raise LlmConfigError(
            "ZYCS_LLM_MAX_INPUT_CHARS must be a positive integer"
        ) from exc
    if max_input_chars <= 0:
        raise LlmConfigError("ZYCS_LLM_MAX_INPUT_CHARS must be a positive integer")
    return max_input_chars


def _get_demo_only() -> bool:
    return os.getenv("ZYCS_LLM_DEMO_ONLY", "true").strip().lower() in {"1", "true", "yes"}
