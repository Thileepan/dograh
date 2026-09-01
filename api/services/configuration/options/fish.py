"""Model, voice, and language options for the Fish Audio TTS and STT providers."""

# Chosen per request via the `model` header. s1 covers 13 languages; s2-pro
# covers 80+ and s2.1-pro 83, both detecting the language from the text itself.
# s2.1-pro-free is s2.1-pro at no cost, without its latency or availability
# guarantees.
FISH_TTS_MODELS = ("s2-pro", "s2.1-pro", "s2.1-pro-free", "s1")

# Fish Audio voices are ``reference_id`` model IDs from fish.audio — either a
# public voice from their library or one cloned in the account that owns the
# API key — so the UI accepts free-form input. This default is the public voice
# used by pipecat's Fish examples; replace it with an owned voice ID.
FISH_TTS_DEFAULT_VOICE = "4ce7e917cedd4bc2bb2e6ff3a46acaa1"

FISH_TTS_LATENCY_MODES = ("balanced", "normal")


# Fish Audio's ASR endpoint exposes no model selection — this single value keeps
# the STT configuration shape consistent with the other providers.
FISH_STT_MODELS = ("asr",)

# The ASR endpoint detects the spoken language itself and a hint is optional, so
# "auto" (send no hint) is the default. Fish does not publish which languages
# the recognizer covers, so these are common codes to pick from rather than a
# guarantee — the UI allows custom input for anything missing.
FISH_STT_LANGUAGES = [
    "auto",
    "en",
    "zh",
    "ja",
    "ko",
    "de",
    "fr",
    "es",
    "pt",
    "it",
    "nl",
    "pl",
    "ru",
    "ar",
    "hi",
    "ta",
    "th",
    "vi",
    "id",
    "tr",
]
