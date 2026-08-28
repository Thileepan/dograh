from types import SimpleNamespace
from unittest.mock import patch

from pipecat.transcriptions.language import Language

from api.services.configuration.options import (
    FISH_TTS_DEFAULT_VOICE,
    FISH_TTS_LANGUAGES,
    FISH_TTS_MODELS,
)
from api.services.configuration.registry import (
    FishAudioTTSConfiguration,
    ServiceProviders,
)
from api.services.pipecat.audio_config import AudioConfig
from api.services.pipecat.service_factory import create_tts_service


def _audio_config() -> AudioConfig:
    return AudioConfig(
        transport_in_sample_rate=16000,
        transport_out_sample_rate=24000,
    )


def _fish_config(
    model: str = "s2-pro",
    language: str = "en",
    voice: str = FISH_TTS_DEFAULT_VOICE,
    latency: str = "balanced",
    speed: float = 1.0,
    volume: int = 0,
) -> SimpleNamespace:
    return SimpleNamespace(
        tts=SimpleNamespace(
            provider=ServiceProviders.FISH.value,
            api_key="test-key",
            model=model,
            voice=voice,
            language=language,
            latency=latency,
            speed=speed,
            volume=volume,
        )
    )


def test_fish_tts_configuration_defaults_and_schema():
    config = FishAudioTTSConfiguration(api_key="test-key")
    schema = FishAudioTTSConfiguration.model_json_schema()

    assert config.provider == ServiceProviders.FISH
    assert config.model == "s2-pro"
    assert config.voice == FISH_TTS_DEFAULT_VOICE
    assert config.language == "en"
    assert config.latency == "balanced"
    assert config.speed == 1.0
    assert config.volume == 0
    assert "s2-pro" in FISH_TTS_MODELS
    # Fish Audio has no Tamil voice models — the option list must not imply it does.
    assert "ta" not in FISH_TTS_LANGUAGES
    assert schema["title"] == "Fish Audio"
    assert schema["properties"]["voice"]["allow_custom_input"] is True
    assert schema["properties"]["language"]["allow_custom_input"] is True


def test_fish_factory_builds_service_with_settings():
    user_config = _fish_config(language="ja", voice="abc123", speed=1.2, volume=-3)

    with patch(
        "api.services.pipecat.service_factory.FishAudioTTSService"
    ) as tts_service:
        create_tts_service(user_config, _audio_config())

    tts_service.assert_called_once()
    kwargs = tts_service.call_args.kwargs
    assert kwargs["api_key"] == "test-key"
    assert kwargs["output_format"] == "pcm"
    assert kwargs["sample_rate"] == 24000
    settings = kwargs["settings"]
    assert settings.model == "s2-pro"
    assert settings.voice == "abc123"
    assert settings.language == Language.JA
    assert settings.latency == "balanced"
    assert settings.prosody_speed == 1.2
    assert settings.prosody_volume == -3


def test_fish_factory_falls_back_to_english_for_unknown_language():
    user_config = _fish_config(language="not-a-language")

    with patch(
        "api.services.pipecat.service_factory.FishAudioTTSService"
    ) as tts_service:
        create_tts_service(user_config, _audio_config())

    settings = tts_service.call_args.kwargs["settings"]
    assert settings.language == Language.EN


def test_fish_registered_in_tts_registry():
    from api.services.configuration.registry import REGISTRY, ServiceType

    assert (
        REGISTRY[ServiceType.TTS][ServiceProviders.FISH.value]
        is FishAudioTTSConfiguration
    )
