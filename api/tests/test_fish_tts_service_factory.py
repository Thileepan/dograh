from types import SimpleNamespace
from unittest.mock import patch

from api.services.configuration.options import (
    FISH_TTS_DEFAULT_VOICE,
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
    assert config.latency == "balanced"
    assert config.speed == 1.0
    assert config.volume == 0
    # Only these four are valid values for Fish's `model` header.
    assert FISH_TTS_MODELS == ("s2-pro", "s2.1-pro", "s2.1-pro-free", "s1")
    assert schema["title"] == "Fish Audio"
    assert schema["properties"]["voice"]["allow_custom_input"] is True
    # Fish's TTS API has no language parameter — the model detects the language
    # from the text, so exposing the knob would be a lie.
    assert "language" not in schema["properties"]


def test_fish_factory_builds_service_with_settings():
    user_config = _fish_config(voice="abc123", speed=1.2, volume=-3)

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
    assert settings.latency == "balanced"
    assert settings.prosody_speed == 1.2
    assert settings.prosody_volume == -3


def test_fish_registered_in_tts_registry():
    from api.services.configuration.registry import REGISTRY, ServiceType

    assert (
        REGISTRY[ServiceType.TTS][ServiceProviders.FISH.value]
        is FishAudioTTSConfiguration
    )
