# Dograh - Project Overview

Dograh is a voice AI platform for building and deploying conversational AI agents with telephony and WebRTC support.

## Project Structure

```
dograh/
├── api/              # Backend - FastAPI application
├── ui/               # Frontend - Next.js application
├── scripts/          # Helper scripts for local development
├── docs/             # Mintlify documentation
├── pipecat/          # Pipecat framework (git submodule)
├── sdk/              # Client SDKs
├── docker-compose.yaml       # Production/OSS deployment
├── docker-compose-local.yaml # Local development services
```

Each major directory has its own `AGENTS.md` with rules specific to that subtree — read it before changing files there: `api/AGENTS.md` (route/service layering, org scoping), `ui/AGENTS.md` (generated client, auth/error conventions), `pipecat/AGENTS.md` (frame architecture, its own tooling), `docs/AGENTS.md`, `scripts/AGENTS.md`, plus deeper ones under `api/services/telephony/` and `api/services/integrations/`.

## Tech Stack

- **Backend**: Python with FastAPI
- **Frontend**: Next.js 15 with React 19, TypeScript, Tailwind CSS
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Cache/Queue**: Redis with ARQ for background tasks
- **Storage**: MinIO (S3-compatible) for audio files

## Local Development

Contributor setup and service startup are documented in `docs/contribution/setup.mdx`.

```bash
./scripts/start_services_dev.sh   # Backend + arq worker with auto-reload (waits for /api/v1/health)
cd ui && npm run dev              # Frontend on port 3000
```

## Common Commands

```bash
# Format (ruff for api/ and pipecat/, eslint --fix for ui/)
./scripts/format.sh

# Lint gate — mypy api, ruff check, ruff format --check
./scripts/lint.sh

# UI
cd ui && npm run test              # vitest
cd ui && npm run lint
cd ui && npm run generate-client   # Regenerate src/client/ from backend OpenAPI (backend must be running)

# Database migrations
./scripts/makemigrate.sh "description"
./scripts/migrate.sh

# Pipecat submodule uses its own tooling (uv, not the repo venv) — see pipecat/AGENTS.md
cd pipecat && uv run pytest tests/test_name.py
```

## Environment Configuration

- `api/.env` - Backend environment variables. Source this when running repo-owned backend scripts against the dev DB (e.g. `python -m scripts.dump_docs_openapi`).
- `api/.env.test` - Test-only environment variables. Source this when running pytest so tests hit the test DB and never the dev/prod credentials in `api/.env`.
- `ui/.env` - Frontend environment variables

Typical invocation:

```bash
# All backend tests
source venv/bin/activate && set -a && source api/.env.test && set +a && python -m pytest api/tests/

# A single test
source venv/bin/activate && set -a && source api/.env.test && set +a && python -m pytest api/tests/test_name.py::test_function -xvs

# Backend scripts
source venv/bin/activate && set -a && source api/.env && set +a && python -m scripts.dump_docs_openapi
```

## Architecture: How a Voice Call Runs

The big picture spans `api/services/configuration/`, `api/services/pipecat/`, and the `pipecat/` submodule:

1. **Configuration resolution** — AI provider config (LLM/TTS/STT, including BYOK API keys) is stored as JSON in the `organization_configurations` table under the `MODEL_CONFIGURATION_V2` key. `api/services/configuration/ai_model_configuration.py` loads it, merges workflow-level overrides (`resolve.py`, `merge.py`), and compiles an `EffectiveAIModelConfiguration` (`api/schemas/ai_model_configuration.py`). Two modes: `"byok"` (user's own provider keys) and `"dograh"` (managed keys proxied through `MPS_API_URL`). Keys are stored plaintext and masked on read (`masking.py`).
2. **Service construction** — `api/services/pipecat/run_pipeline.py` calls `create_stt_service` / `create_tts_service` / `create_llm_service` in `api/services/pipecat/service_factory.py`, which branch on the `ServiceProviders` enum and instantiate pipecat service classes with the resolved keys.
3. **Pipeline runtime** — the call itself runs as a pipecat frame pipeline (transport → STT → LLM context aggregators → LLM → TTS → transport). Frames, turn taking, VAD, and interruption logic live in the `pipecat/` submodule.

### Provider Registry (adding/altering an AI provider)

`api/services/configuration/registry.py` is the single source of truth: the `ServiceProviders` enum, per-provider Pydantic config classes registered with `@register_stt` / `@register_tts` / `@register_llm` decorators, and `STTConfig`/`TTSConfig`/`LLMConfig` discriminated unions (discriminator = `provider`). Model/language option lists live in `api/services/configuration/options/`, API-key validation in `check_validity.py`, and the factory branch in `service_factory.py`.

The frontend is schema-driven: `GET /api/v1/user/configurations/defaults` returns `model_json_schema()` for every registered provider, and `ui/src/components/ServiceConfigurationForm.tsx` renders dropdowns and fields from it. Adding a provider to the registry therefore requires no frontend edits beyond `npm run generate-client`.

### Pipecat Submodule

`pipecat/` is a git submodule with its own commit/PR flow, its own tooling (uv, ruff line-100, towncrier changelog fragments), and its own conventions — always follow `pipecat/AGENTS.md` when changing files there, and remember submodule changes need a separate commit in the submodule plus a pointer bump in this repo.
