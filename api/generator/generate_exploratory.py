"""
LLM-generated exploratory tests for POST /clients.

Usage:
    python -m api.generator.generate_exploratory
"""

import ast
import re
from pathlib import Path

from anthropic import Anthropic

from api.generator.parse_spec import parse_spec
from config import ANTHROPIC_API_KEY


def _find_create_client(endpoints):
    for ep in endpoints:
        if ep.method == "POST" and ep.path == "/clients":
            return ep
    return None


def _build_prompt(ep) -> str:
    fields = ", ".join(
        f"{f.name}({f.type}{', required' if f.required else ''}{f', pattern={f.pattern}' if f.pattern else ''})"
        for f in ep.body_fields
    )
    return f"""Generate 3-5 pytest tests for POST {ep.path}. Exploratory edge cases only.

Endpoint: POST {ep.path}
Auth: Bearer token (fixture: auth_headers)
Body fields: {fields}

Fixtures available: api_url, auth_headers (use these, no setup).

Use fake.email() for all email fields and fake.numerify("+1-###-###-####") for valid phone to avoid duplicate-email 409.

Generate tests for: type mismatch (e.g. number instead of string), null for required field, empty string, extra unknown field.
Use requests.post(url, headers=auth_headers, json=body). Assert resp.status_code == 400 for validation errors (exact, not a list).
For extra unknown field only: assert resp.status_code in (200, 201, 400, 422) since API may accept or reject.

Output ONLY valid Python. No markdown, no explanation. Start with def test_."""


def _extract_code(text: str) -> str:
    match = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def generate(spec_path: str = "api/spec/openapi.json", output_dir: str = "api/tests") -> str:
    if not ANTHROPIC_API_KEY:
        raise ValueError("Set ANTHROPIC_API_KEY in .env")

    endpoints = parse_spec(spec_path)
    ep = _find_create_client(endpoints)
    if not ep:
        raise ValueError("POST /clients not found in spec")

    client = Anthropic()
    prompt = _build_prompt(ep)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text
    code = _extract_code(raw)

    header = '''"""Exploratory tests for POST /clients. LLM-generated."""

import requests
from faker import Faker

fake = Faker()
'''

    full = header + code
    ast.parse(full)

    out = Path(output_dir) / "test_client_controller_exploratory.py"
    out.write_text(full, encoding="utf-8")
    print(f"Wrote {out}")
    return str(out)


if __name__ == "__main__":
    generate()
