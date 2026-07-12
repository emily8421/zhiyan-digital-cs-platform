import pytest

from app.adapters.llm_adapter import (
    LlmConfigError,
    generate_llm_answer,
    get_llm_mode,
    get_llm_sandbox_config,
)


def test_default_llm_mode_is_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ZYCS_LLM_MODE", raising=False)

    assert get_llm_mode() == "disabled"


def test_invalid_llm_mode_raises_config_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZYCS_LLM_MODE", "production")

    with pytest.raises(LlmConfigError):
        get_llm_mode()


def test_generate_llm_answer_disabled_returns_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZYCS_LLM_MODE", "disabled")

    assert generate_llm_answer(
        question="灯带有什么规格？",
        base_answer_type="knowledge",
        base_answer="灯带规格说明",
        source_ref="SRC-SP-PRODUCT-001",
    ) is None


def test_generate_llm_answer_invalid_mode_is_safe_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZYCS_LLM_MODE", "production")

    assert generate_llm_answer(
        question="灯带有什么规格？",
        base_answer_type="knowledge",
        base_answer="灯带规格说明",
        source_ref="SRC-SP-PRODUCT-001",
    ) is None


def test_generate_llm_answer_mock_rewrites_with_source_ref(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ZYCS_LLM_MODE", "mock")

    result = generate_llm_answer(
        question="灯带有什么规格？",
        base_answer_type="knowledge",
        base_answer="灯带规格说明",
        source_ref="SRC-SP-PRODUCT-001",
    )

    assert result is not None
    assert result.mock is True
    assert result.mode_used == "mock"
    assert result.base_answer_type == "knowledge"
    assert result.source_ref == "SRC-SP-PRODUCT-001"
    assert result.evidence == ["SRC-SP-PRODUCT-001"]
    assert result.fallback_reason is None
    assert "SRC-SP-PRODUCT-001" in result.answer
    assert "灯带规格说明" in result.answer


def test_generate_llm_answer_sandbox_without_key_degrades_to_mock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ZYCS_LLM_MODE", "sandbox")
    monkeypatch.delenv("ZYCS_LLM_API_KEY", raising=False)
    monkeypatch.delenv("ZYCS_LLM_BASE_URL", raising=False)

    result = generate_llm_answer(
        question="查订单进度",
        base_answer_type="mock_business",
        base_answer="Mock 进度：生产中",
        source_ref="demo_erp:order:DEMO-ORDER-202607-001",
    )

    assert result is not None
    assert result.mock is True
    assert result.mode_used == "mock"
    assert result.fallback_reason is not None
    assert result.fallback_reason.startswith("ZYCS_LLM_API_KEY")


def test_generate_llm_answer_sandbox_with_key_still_mock_not_implemented(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ZYCS_LLM_MODE", "sandbox")
    monkeypatch.setenv("ZYCS_LLM_API_KEY", "demo-key-not-real")
    monkeypatch.setenv("ZYCS_LLM_BASE_URL", "https://example.invalid/llm")

    result = generate_llm_answer(
        question="查订单进度",
        base_answer_type="mock_business",
        base_answer="Mock 进度：生产中",
        source_ref="demo_erp:order:DEMO-ORDER-202607-001",
    )

    assert result is not None
    assert result.mock is True
    assert result.fallback_reason == "sandbox_real_call_not_implemented"


def test_sandbox_config_does_not_expose_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ZYCS_LLM_API_KEY", "super-secret-key")
    monkeypatch.setenv("ZYCS_LLM_BASE_URL", "https://example.invalid/llm")

    config = get_llm_sandbox_config()

    assert config["base_url"] == "https://example.invalid/llm"
    assert "api_key" not in config
    assert "super-secret-key" not in str(config)
