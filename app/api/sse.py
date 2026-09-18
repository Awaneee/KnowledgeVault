"""Server-Sent Events framing for the streaming ask endpoint."""

import json
import logging

from app.services.ask_service import StreamCitations


logger = logging.getLogger(__name__)


def sse_frame(payload: str, event: str | None = None) -> str:
    """
    Build a single SSE frame.

    The payload is JSON-encoded so that a token's own newlines and leading
    spaces survive the transport - SSE is a line-oriented protocol, so a raw
    token containing "\n" would otherwise be split across frames (or silently
    reassembled without its whitespace by the client).
    """
    prefix = f"event: {event}\n" if event else ""
    return f"{prefix}data: {payload}\n\n"


def sse_stream(items):
    """
    Wrap the ask_stream generator in SSE frames, always ending with [DONE].

    Frame types:
      data: "<token>"                      - one JSON-encoded answer token
      event: citations / data: [ ... ]     - citation objects, sent once after
                                             the last token when the answer
                                             cited any sources
      event: error / data: "<message>"     - the stream broke mid-generation
      data: [DONE]                         - end of stream
    """
    try:
        for item in items:
            if isinstance(item, StreamCitations):
                yield sse_frame(
                    json.dumps(
                        [c.model_dump() for c in item.citations],
                        ensure_ascii=False,
                    ),
                    event="citations",
                )
            elif item:
                yield sse_frame(json.dumps(item, ensure_ascii=False))
    except Exception as exc:
        logger.exception("STREAM failed mid-generation: %s", exc)
        yield sse_frame(
            json.dumps("The answer stream was interrupted. Please try again."),
            event="error",
        )
    finally:
        yield sse_frame("[DONE]")
