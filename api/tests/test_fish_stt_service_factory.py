from types import SimpleNamespace
from unittest.mock import patch

from pipecat.transcriptions.language import Language

from api.services.configuration.options import (
    FISH_STT_LANGUAGES,
    FISH_STT_MODELS,
)
from api.services.configuration.registry import (
    FishAudioSTTConfiguration,
    ServiceProviders,
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


def _fish_config(model: str = "asr", language: str = "auto") -> SimpleNamespace:
    return SimpleNamespace(
        stt=SimpleNamespace(
            provider=ServiceProviders.FISH.value,
            api_key="test-key",
            model=model,
            language=language,
        )
    )


def test_fish_stt_configuration_defaults_and_schema():
    config = FishAudioSTTConfiguration(api_key="test-key")
    schema = FishAudioSTTConfiguration.model_json_schema()

    assert config.provider == ServiceProviders.FISH
    assert config.model == "asr"
    assert config.language == "auto"
    assert FISH_STT_MODELS == ("asr",)
    assert FISH_STT_LANGUAGES[0] == "auto"
    assert schema["title"] == "Fish Audio"
    language_schema = schema["properties"]["language"]
    assert "auto" in language_schema["examples"]
    assert language_schema["allow_custom_input"] is True


def test_fish_stt_does_not_use_external_turns():
    # Fish Audio transcribes VAD-delimited segments, so turn boundaries stay
    # with the pipeline's own VAD rather than the provider.
    assert not stt_uses_external_turns(_fish_config())


def test_fish_stt_factory_passes_language_hint():
    user_config = _fish_config(language="ja")

    with patch(
        "api.services.pipecat.service_factory.FishAudioSTTService"
    ) as stt_service:
        create_stt_service(user_config, _audio_config())

    stt_service.assert_called_once()
    kwargs = stt_service.call_args.kwargs
    assert kwargs["api_key"] == "test-key"
    assert kwargs["sample_rate"] == 16000
    assert kwargs["settings"].language == Language.JA


def test_fish_stt_factory_omits_hint_for_auto():
    user_config = _fish_config(language="auto")

    with patch(
        "api.services.pipecat.service_factory.FishAudioSTTService"
    ) as stt_service:
        create_stt_service(user_config, _audio_config())

    assert stt_service.call_args.kwargs["settings"].language is None


def test_fish_stt_factory_omits_hint_for_unknown_language():
    user_config = _fish_config(language="not-a-language")

    with patch(
        "api.services.pipecat.service_factory.FishAudioSTTService"
    ) as stt_service:
        create_stt_service(user_config, _audio_config())

    assert stt_service.call_args.kwargs["settings"].language is None


def test_fish_registered_in_stt_registry():
    from api.services.configuration.registry import REGISTRY, ServiceType

    assert (
        REGISTRY[ServiceType.STT][ServiceProviders.FISH.value]
        is FishAudioSTTConfiguration
    )
