from types import SimpleNamespace
from unittest.mock import patch

from pipecat.transcriptions.language import Language

from api.services.configuration.options import (
    GRADIUM_LANGUAGES,
    GRADIUM_STT_DELAY_FRAMES,
    GRADIUM_TTS_DEFAULT_VOICE,
)
from api.services.configuration.registry import (
    GradiumSTTConfiguration,
    GradiumTTSConfiguration,
    ServiceProviders,
)
from api.services.pipecat.audio_config import AudioConfig
from api.services.pipecat.service_factory import (
    create_stt_service,
    create_tts_service,
    stt_uses_external_turns,
)


def _audio_config() -> AudioConfig:
    return AudioConfig(
        transport_in_sample_rate=16000,
        transport_out_sample_rate=24000,
    )


def _stt_config(language: str = "en", delay_in_frames: int = 12) -> SimpleNamespace:
    return SimpleNamespace(
        stt=SimpleNamespace(
            provider=ServiceProviders.GRADIUM.value,
            api_key="test-key",
            model="default",
            language=language,
            delay_in_frames=delay_in_frames,
        )
    )


def _tts_config(voice: str = GRADIUM_TTS_DEFAULT_VOICE) -> SimpleNamespace:
    return SimpleNamespace(
        tts=SimpleNamespace(
            provider=ServiceProviders.GRADIUM.value,
            api_key="test-key",
            model="default",
            voice=voice,
        )
    )


def test_gradium_configuration_defaults_and_schema():
    stt = GradiumSTTConfiguration(api_key="test-key")
    tts = GradiumTTSConfiguration(api_key="test-key")

    assert stt.provider == ServiceProviders.GRADIUM
    assert stt.model == "default"
    assert stt.language == "en"
    assert stt.delay_in_frames == 12
    assert tts.voice == GRADIUM_TTS_DEFAULT_VOICE

    stt_schema = GradiumSTTConfiguration.model_json_schema()
    assert stt_schema["title"] == "Gradium"
    # Gradium supports exactly five languages — the option list must not imply
    # broader coverage, so it stays a closed set with no custom input.
    assert stt_schema["properties"]["language"]["examples"] == GRADIUM_LANGUAGES
    assert "allow_custom_input" not in stt_schema["properties"]["language"]
    assert stt_schema["properties"]["delay_in_frames"]["examples"] == list(
        GRADIUM_STT_DELAY_FRAMES
    )
    assert GradiumTTSConfiguration.model_json_schema()["title"] == "Gradium"


def test_gradium_stt_does_not_use_external_turns():
    assert not stt_uses_external_turns(_stt_config())


def test_gradium_stt_factory_passes_language_enum_and_delay():
    with patch("api.services.pipecat.service_factory.GradiumSTTService") as stt_service:
        create_stt_service(
            _stt_config(language="fr", delay_in_frames=8), _audio_config()
        )

    stt_service.assert_called_once()
    kwargs = stt_service.call_args.kwargs
    assert kwargs["api_key"] == "test-key"
    assert kwargs["sample_rate"] == 16000
    # Gradium maps the enum itself at connect time, so it must stay an enum here.
    assert kwargs["settings"].language is Language.FR
    assert kwargs["settings"].delay_in_frames == 8


def test_gradium_stt_factory_falls_back_to_english_for_unknown_language():
    with patch("api.services.pipecat.service_factory.GradiumSTTService") as stt_service:
        create_stt_service(_stt_config(language="not-a-language"), _audio_config())

    assert stt_service.call_args.kwargs["settings"].language is Language.EN


def test_gradium_tts_factory_sends_voice_and_no_sample_rate():
    with patch("api.services.pipecat.service_factory.GradiumTTSService") as tts_service:
        create_tts_service(_tts_config(voice="_abc123"), _audio_config())

    tts_service.assert_called_once()
    kwargs = tts_service.call_args.kwargs
    assert kwargs["api_key"] == "test-key"
    assert kwargs["settings"].voice == "_abc123"
    # Gradium fixes its own 48kHz rate; passing one would collide with the
    # sample_rate the service hands to its base class.
    assert "sample_rate" not in kwargs


def test_gradium_registered_in_both_registries():
    from api.services.configuration.registry import REGISTRY, ServiceType

    assert (
        REGISTRY[ServiceType.STT][ServiceProviders.GRADIUM.value]
        is GradiumSTTConfiguration
    )
    assert (
        REGISTRY[ServiceType.TTS][ServiceProviders.GRADIUM.value]
        is GradiumTTSConfiguration
    )
