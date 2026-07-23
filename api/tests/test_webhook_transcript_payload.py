from types import SimpleNamespace
from unittest.mock import patch

import pytest

from api.tasks.run_integrations import (
    _attach_transcript_context,
    _parse_transcript_turns,
    _render_payload_value,
    _webhook_templates_reference_transcript,
)

TRANSCRIPT_TEXT = (
    "[2026-07-22T10:00:01] user: Hello\n"
    "[2026-07-22T10:00:03] assistant: Hi there!\n"
    "How can I help?\n"
    "user: Book me for tomorrow\n"
)


def _webhook_node(payload_template: dict) -> dict:
    return {"id": "node-1", "data": {"payload_template": payload_template}}


def test_reference_detection_ignores_transcript_url():
    assert not _webhook_templates_reference_transcript(
        [_webhook_node({"transcript_url": "{{transcript_url}}"})]
    )
    assert _webhook_templates_reference_transcript(
        [_webhook_node({"transcript": "{{transcript}}"})]
    )
    assert _webhook_templates_reference_transcript(
        [_webhook_node({"turns": "{{transcript_json}}"})]
    )


def test_parse_transcript_turns_roles_timestamps_and_continuations():
    turns = _parse_transcript_turns(TRANSCRIPT_TEXT)

    assert [t["role"] for t in turns] == ["user", "assistant", "user"]
    assert turns[0] == {
        "role": "user",
        "text": "Hello",
        "timestamp": "2026-07-22T10:00:01",
    }
    # Multi-line utterance folds into the previous turn.
    assert turns[1]["text"] == "Hi there!\nHow can I help?"
    # Line without a timestamp prefix.
    assert turns[2]["timestamp"] is None
    assert turns[2]["text"] == "Book me for tomorrow"


def test_render_payload_value_injects_real_json_array():
    context = {
        "workflow_run_id": 42,
        "transcript": TRANSCRIPT_TEXT,
        "transcript_json": _parse_transcript_turns(TRANSCRIPT_TEXT),
    }
    template = {
        "call_id": "{{workflow_run_id}}",
        "transcript": "{{transcript}}",
        "turns": "{{ transcript_json }}",
        "nested": {"inner_turns": "{{transcript_json}}"},
    }

    payload = _render_payload_value(template, context)

    assert payload["call_id"] == "42"
    assert isinstance(payload["transcript"], str)
    assert "user: Hello" in payload["transcript"]
    # Exact-match values become real lists, at any nesting level.
    assert isinstance(payload["turns"], list)
    assert payload["turns"][0]["role"] == "user"
    assert isinstance(payload["nested"]["inner_turns"], list)


@pytest.mark.asyncio
async def test_attach_transcript_context_skips_fetch_when_unreferenced():
    context: dict = {}
    run = SimpleNamespace(transcript_url="transcripts/1.txt", storage_backend="s3")

    with patch("api.tasks.run_integrations._fetch_transcript_text") as fetch:
        await _attach_transcript_context(
            context, run, [_webhook_node({"transcript_url": "{{transcript_url}}"})]
        )

    fetch.assert_not_called()
    assert context["transcript"] == ""
    assert context["transcript_json"] == []


@pytest.mark.asyncio
async def test_attach_transcript_context_populates_when_referenced():
    context: dict = {}
    run = SimpleNamespace(transcript_url="transcripts/1.txt", storage_backend="s3")

    with patch(
        "api.tasks.run_integrations._fetch_transcript_text",
        return_value=TRANSCRIPT_TEXT,
    ):
        await _attach_transcript_context(
            context, run, [_webhook_node({"turns": "{{transcript_json}}"})]
        )

    assert context["transcript"] == TRANSCRIPT_TEXT
    assert len(context["transcript_json"]) == 3
