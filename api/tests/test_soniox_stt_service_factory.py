from types import SimpleNamespace
from unittest.mock import patch

from pipecat.transcriptions.language import Language

from api.services.configuration.options import (
    SONIOX_STT_LANGUAGES,
    SONIOX_STT_MODELS,
)
from api.services.configuration.registry import (
    ServiceProviders,
    SonioxSTTConfiguration,
)
from api.services.pipecat.audio_config import AudioConfig
from api.services.pipecat.service_factory import (
    create_stt_service,
    stt_uses_external_turns,
)


def _audio_config() -> AudioConfig:
    return AudioConfig(
        transport_in_sample_rate=16000,
        transport_out_sample_rate=16000,
    )


def _soniox_config(model: str = "stt-rt-v5", language: str = "en") -> SimpleNamespace:
    return SimpleNamespace(
        stt=SimpleNamespace(
            provider=ServiceProviders.SONIOX.value,
            api_key="test-key",
            model=model,
            language=language,
        )
    )


def test_soniox_stt_configuration_defaults_and_schema():
    config = SonioxSTTConfiguration(api_key="test-key")
    schema = SonioxSTTConfiguration.model_json_schema()

    assert config.provider == ServiceProviders.SONIOX
    assert config.model == "stt-rt-v5"
    assert config.language == "en"
    assert SONIOX_STT_MODELS == ["stt-rt-v5"]
    assert "ta" in SONIOX_STT_LANGUAGES
    assert schema["title"] == "Soniox"
    language_schema = schema["properties"]["language"]
    assert "ta" in language_schema["examples"]
    assert language_schema["allow_custom_input"] is True


def test_soniox_does_not_use_external_turns():
    assert not stt_uses_external_turns(_soniox_config())


def test_soniox_factory_builds_service_with_language_hint():
    user_config = _soniox_config(language="ta")

    with patch("api.services.pipecat.service_factory.SonioxSTTService") as stt_service:
        create_stt_service(user_config, _audio_config())

    stt_service.assert_called_once()
    kwargs = stt_service.call_args.kwargs
    assert kwargs["api_key"] == "test-key"
    assert kwargs["sample_rate"] == 16000
    assert kwargs["settings"].model == "stt-rt-v5"
    assert kwargs["settings"].language_hints == [Language.TA]


def test_soniox_factory_omits_hint_for_unknown_language():
    user_config = _soniox_config(language="not-a-language")

    with patch("api.services.pipecat.service_factory.SonioxSTTService") as stt_service:
        create_stt_service(user_config, _audio_config())

    stt_service.assert_called_once()
    settings = stt_service.call_args.kwargs["settings"]
    assert settings.model == "stt-rt-v5"
