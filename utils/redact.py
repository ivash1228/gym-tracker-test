"""Redact common secret patterns from strings (logs, CI artifacts, issue bodies)."""

from __future__ import annotations

import re


def redact_sensitive(text: str) -> str:
    s = str(text)
    s = re.sub(
        r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+",
        "***REDACTED_JWT***",
        s,
    )
    s = re.sub(r"(Bearer\s+)[^\s'\"]+", r"\1***REDACTED***", s, flags=re.IGNORECASE)
    s = re.sub(
        r'(["\']?Authorization["\']?\s*[:=]\s*["\'])[^"\']+(["\'])',
        r"\1***REDACTED***\2",
        s,
        flags=re.IGNORECASE,
    )
    s = re.sub(
        r'(["\']?id_token["\']?\s*[:=]\s*["\'])[^"\']+(["\'])',
        r"\1***REDACTED***\2",
        s,
        flags=re.IGNORECASE,
    )
    s = re.sub(
        r'(["\']?refresh_token["\']?\s*[:=]\s*["\'])[^"\']+(["\'])',
        r"\1***REDACTED***\2",
        s,
        flags=re.IGNORECASE,
    )
    s = re.sub(
        r'(["\']?client_secret["\']?\s*[:=]\s*["\'])[^"\']+(["\'])',
        r"\1***REDACTED***\2",
        s,
        flags=re.IGNORECASE,
    )
    return s
