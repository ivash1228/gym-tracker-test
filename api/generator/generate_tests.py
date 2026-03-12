"""
Generates pytest API test files from parsed OpenAPI endpoints.

Usage:
    python -m api.generator.generate_tests
"""

import uuid
from pathlib import Path

from api.generator.parse_spec import parse_spec
from api.generator.models import Endpoint, Field


PARAM_TO_FIXTURE = {
    "clientId": "client_id",
    "workoutId": "workout_id",
    "exerciseId": "exercise_id",
    "workoutExerciseId": "workout_exercise_id",
}


def _valid_value(field: Field, fixture_map: dict[str, str]) -> str:
    if field.enum:
        return repr(field.enum[0])
    if field.pattern and "phone" in field.name.lower():
        return 'fake.numerify("+1-###-###-####")'
    if field.format == "uuid":
        fixture = PARAM_TO_FIXTURE.get(field.name)
        if fixture:
            return fixture
        return "str(uuid.uuid4())"
    if field.format == "date":
        return "fake.date_this_year().isoformat()"
    if field.type == "integer":
        return "10" if "weight" in field.name.lower() else "5"
    if field.name in ("firstName", "first_name"):
        return "fake.first_name()"
    if field.name in ("lastName", "last_name"):
        return "fake.last_name()"
    if "email" in field.name.lower():
        return "fake.email()"
    if "name" in field.name.lower() and "workout" in field.name.lower():
        return "fake.catch_phrase()"
    if field.name == "name":
        return "fake.word()"
    if field.name == "type" and field.enum:
        return repr(field.enum[0])
    return "fake.word()"


def _invalid_value(field: Field) -> tuple[str, str]:
    if field.enum:
        return "INVALID_ENUM", repr("INVALID_ENUM")
    if field.pattern:
        return "invalid_format", repr("invalid")
    if field.format == "uuid":
        return "not_a_uuid", repr("not-a-uuid")
    if field.format == "date":
        return "invalid_date", repr("2025-13-99")
    if field.type == "integer":
        return "invalid_int", '"not-a-number"'
    if "email" in field.name.lower():
        return "invalid_email", repr("not-an-email")
    return "invalid", repr("")


def _fixture_deps(ep: Endpoint) -> list[str]:
    deps = []
    for p in ep.path_params:
        fixture = PARAM_TO_FIXTURE.get(p.name)
        if fixture and fixture not in deps:
            deps.append(fixture)
    for f in ep.body_fields:
        fixture = PARAM_TO_FIXTURE.get(f.name)
        if fixture and fixture not in deps:
            deps.append(fixture)
    return deps


def _build_path(path: str, path_params: list, fixture_map: dict[str, str]) -> str:
    result = path
    for p in path_params:
        fixture = PARAM_TO_FIXTURE.get(p.name)
        placeholder = "{" + p.name + "}"
        if fixture:
            result = result.replace(placeholder, f'{{{fixture}}}')
        else:
            result = result.replace(placeholder, "str(uuid.uuid4())")
    return result


def _body_dict(fields: list[Field], fixture_map: dict[str, str], exclude: str | None = None, invalid_field: str | None = None) -> str:
    lines = []
    for f in fields:
        if exclude and f.name == exclude:
            continue
        if invalid_field and f.name == invalid_field:
            _, val = _invalid_value(f)
            lines.append(f'        "{f.name}": {val},')
        else:
            val = _valid_value(f, fixture_map)
            lines.append(f'        "{f.name}": {val},')
    return "\n".join(lines) if lines else ""


def _generate_test_success(ep: Endpoint, fixture_deps: list[str]) -> str:
    path = _build_path(ep.path, ep.path_params, {})
    params = ", ".join(["api_url", "auth_headers"] + fixture_deps)
    body = ""
    if ep.body_fields:
        body = f'\n    body = {{\n{_body_dict(ep.body_fields, {})}\n    }}\n    '
    method_lower = ep.method.lower()
    req = f'requests.{method_lower}(url, headers=auth_headers, json=body)' if ep.body_fields else f'requests.{method_lower}(url, headers=auth_headers)'
    return f'''
def test_{ep.operation_id}_success({params}):
    """Happy path: {ep.method} {ep.path} returns {ep.success_status}."""
    url = f"{{api_url}}{path}"{body}
    resp = {req}
    assert resp.status_code == {ep.success_status}
'''


def _generate_test_unauthorized(ep: Endpoint, fixture_deps: list[str]) -> str:
    if not ep.auth_required:
        return ""
    path = _build_path(ep.path, ep.path_params, {})
    params = ", ".join(["api_url"] + fixture_deps)
    body = ""
    if ep.body_fields:
        body = f'\n    body = {{\n{_body_dict(ep.body_fields, {})}\n    }}\n    '
    method_lower = ep.method.lower()
    req = f'requests.{method_lower}(url, json=body)' if ep.body_fields else f'requests.{method_lower}(url)'
    return f'''
def test_{ep.operation_id}_unauthorized({params}):
    """No auth header returns 401."""
    url = f"{{api_url}}{path}"{body}
    resp = {req}
    assert resp.status_code == 401
'''


def _generate_test_not_found(ep: Endpoint) -> str:
    if ep.method != "GET" or not ep.path_params:
        return ""
    path = ep.path
    for p in ep.path_params:
        path = path.replace("{" + p.name + "}", "{str(uuid.uuid4())}")
    return f'''
def test_{ep.operation_id}_not_found(api_url, auth_headers):
    """Non-existent ID returns 404."""
    url = f"{{api_url}}{path}"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 404
'''


def _generate_test_missing_required(ep: Endpoint, field: Field, fixture_deps: list[str]) -> str:
    if not field.required:
        return ""
    path = _build_path(ep.path, ep.path_params, {})
    params = ", ".join(["api_url", "auth_headers"] + fixture_deps)
    body = _body_dict(ep.body_fields, {}, exclude=field.name)
    method_lower = ep.method.lower()
    return f'''
def test_{ep.operation_id}_missing_{field.name}({params}):
    """Missing required field {field.name} returns 400."""
    url = f"{{api_url}}{path}"
    body = {{\n{body}\n    }}
    resp = requests.{method_lower}(url, headers=auth_headers, json=body)
    assert resp.status_code == 400
'''


def _generate_test_invalid_field(ep: Endpoint, field: Field, fixture_deps: list[str]) -> str:
    if not (field.pattern or field.enum or field.format):
        return ""
    path = _build_path(ep.path, ep.path_params, {})
    params = ", ".join(["api_url", "auth_headers"] + fixture_deps)
    body = _body_dict(ep.body_fields, {}, invalid_field=field.name)
    method_lower = ep.method.lower()
    return f'''
def test_{ep.operation_id}_invalid_{field.name}({params}):
    """Invalid {field.name} (pattern/enum/format) returns 400."""
    url = f"{{api_url}}{path}"
    body = {{\n{body}\n    }}
    resp = requests.{method_lower}(url, headers=auth_headers, json=body)
    assert resp.status_code == 400
'''


def _generate_file_content(tag: str, endpoints: list[Endpoint]) -> str:
    lines = [
        '"""API tests for %s. Auto-generated from OpenAPI spec."""' % tag,
        "",
        "import uuid",
        "import requests",
        "from faker import Faker",
        "",
        "fake = Faker()",
        "",
    ]
    for ep in endpoints:
        fixture_deps = _fixture_deps(ep)
        lines.append(_generate_test_success(ep, fixture_deps))
        lines.append(_generate_test_unauthorized(ep, fixture_deps))
        lines.append(_generate_test_not_found(ep))
        for f in ep.body_fields:
            lines.append(_generate_test_missing_required(ep, f, fixture_deps))
            lines.append(_generate_test_invalid_field(ep, f, fixture_deps))
    return "\n".join(lines).strip()


def generate(spec_path: str = "api/spec/openapi.json", output_dir: str = "api/tests") -> None:
    endpoints = parse_spec(spec_path)
    by_tag: dict[str, list[Endpoint]] = {}
    for ep in endpoints:
        by_tag.setdefault(ep.tag, []).append(ep)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for tag, eps in by_tag.items():
        filename = "test_" + tag.replace("-", "_") + ".py"
        content = _generate_file_content(tag, eps)
        (out / filename).write_text(content, encoding="utf-8")
        print(f"Wrote {out / filename}")


if __name__ == "__main__":
    generate()
