"""Model, voice, and language options for the Fish Audio TTS provider."""

FISH_TTS_MODELS = ("s2-pro", "s1", "s1-mini")

# Fish Audio voices are ``reference_id`` model IDs from fish.audio — either a
# public voice from their library or one cloned in the account that owns the
# API key — so the UI accepts free-form input. This default is the public voice
# used by pipecat's own Fish examples; replace it with an owned voice ID.
FISH_TTS_DEFAULT_VOICE = "4ce7e917cedd4bc2bb2e6ff3a46acaa1"

# Fish Audio's s1/s2 models cover these languages. Tamil is NOT among them —
# use Sarvam for Tamil synthesis. The UI allows custom input, so any language
# Fish adds later can be typed in directly.
FISH_TTS_LANGUAGES = [
    "en",
    "zh",
    "ja",
    "de",
    "fr",
    "es",
    "ko",
    "ar",
    "ru",
    "nl",
    "it",
    "pl",
    "pt",
]

FISH_TTS_LATENCY_MODES = ("balanced", "normal")


# Fish Audio's ASR endpoint exposes no model selection — this single value keeps
# the STT configuration shape consistent with the other providers.
FISH_STT_MODELS = ("asr",)

# The ASR endpoint auto-detects the spoken language; a hint is optional, so
# "auto" (send no hint) is the default. The rest mirrors Fish's synthesis
# coverage, and the UI allows custom input for anything not listed.
FISH_STT_LANGUAGES = ["auto", *FISH_TTS_LANGUAGES]
