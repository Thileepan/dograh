"""Model and language options for the Soniox real-time STT provider."""

SONIOX_STT_MODELS = ["stt-rt-v5"]

# Curated subset of Soniox's 60+ supported languages (ISO 639-1). The UI allows
# custom input, so any other supported code can be typed in directly.
SONIOX_STT_LANGUAGES = [
    "en",
    "ta",
    "hi",
    "te",
    "kn",
    "ml",
    "mr",
    "bn",
    "gu",
    "pa",
    "ur",
    "es",
    "fr",
    "de",
    "pt",
    "ar",
    "zh",
    "ja",
]
