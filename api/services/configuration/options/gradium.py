"""Model, voice, and language options for the Gradium AI TTS and STT providers."""

# Gradium runs a single model in each direction and its APIs take no model
# selection, so this value exists only to keep the configuration shape
# consistent with the other providers.
GRADIUM_MODELS = ("default",)

# Gradium's model covers exactly these five languages, all at the same latency.
# Anything else is unsupported — it degrades to the base language code and is
# unlikely to transcribe usefully.
GRADIUM_LANGUAGES = ["en", "fr", "de", "es", "pt"]

# Gradium voices are opaque IDs from your Gradium account, including the
# ten-second clones, so the UI accepts free-form input. This default is the
# voice used by pipecat's Gradium service; replace it with an owned voice ID.
GRADIUM_TTS_DEFAULT_VOICE = "_6Aslh2DxfmnRLmP"

# How much audio the recognizer buffers before emitting text, in 80ms frames.
# Lower reacts faster, higher gives the model more context. 12 frames = 960ms.
GRADIUM_STT_DELAY_FRAMES = (7, 8, 10, 12, 14, 16, 20, 24, 36, 48)
