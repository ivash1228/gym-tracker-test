"""
Parses an OpenAPI 3.x spec into a list of Endpoint dataclasses.

Usage:
    from api.generator.parse_spec import parse_spec
    endpoints = parse_spec("api/spec/openapi.json")
"""

import json
from pathlib import Path
from api.generator.models import Endpoint, Field, PathParam


def parse_spec(spec_path: str) -> list[Endpoint]:
    raw = json.loads(Path(spec_path).read_text())
    schemas = raw.get("components", {}).get("schemas", {})
    global_security = raw.get("security", [])

    endpoints = []
    for path, methods in raw["paths"].items():
        for method, details in methods.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue

            path_params = _parse_path_params(details.get("parameters", []))
            body_fields = _parse_request_body(details.get("requestBody"), schemas)
            response_type = _parse_response_type(details.get("responses", {}), schemas)
            security = details.get("security", global_security)

            endpoints.append(Endpoint(
                path=path,
                method=method.upper(),
                operation_id=details.get("operationId", ""),
                tag=details.get("tags", ["unknown"])[0],
                auth_required=len(security) > 0,
                path_params=path_params,
                body_fields=body_fields,
                success_status=_get_success_status(details.get("responses", {})),
                response_type=response_type,
            ))

    return endpoints


def _parse_path_params(parameters: list) -> list[PathParam]:
    params = []
    for p in parameters:
        if p.get("in") == "path":
            schema = p.get("schema", {})
            params.append(PathParam(
                name=p["name"],
                type=schema.get("type", "string"),
                format=schema.get("format"),
                required=p.get("required", True),
            ))
    return params


def _parse_request_body(request_body: dict | None, schemas: dict) -> list[Field]:
    if not request_body:
        return []

    content = request_body.get("content", {})
    json_schema = content.get("application/json", {}).get("schema", {})

    if "$ref" in json_schema:
        schema_name = json_schema["$ref"].split("/")[-1]
        json_schema = schemas.get(schema_name, {})

    required_fields = set(json_schema.get("required", []))
    properties = json_schema.get("properties", {})

    fields = []
    for name, prop in properties.items():
        fields.append(Field(
            name=name,
            type=prop.get("type", "string"),
            required=name in required_fields,
            format=prop.get("format"),
            pattern=prop.get("pattern"),
            enum=prop.get("enum"),
        ))
    return fields


def _parse_response_type(responses: dict, schemas: dict) -> str | None:
    for status in ("200", "201"):
        resp = responses.get(status, {})
        content = resp.get("content", {})
        for media_type, media in content.items():
            schema = media.get("schema", {})
            if "$ref" in schema:
                return schema["$ref"].split("/")[-1]
            if schema.get("type") == "array":
                items = schema.get("items", {})
                if "$ref" in items:
                    return f"array[{items['$ref'].split('/')[-1]}]"
                return f"array[{items.get('type', 'unknown')}]"
            return schema.get("type") or schema.get("format")
    return None


def _get_success_status(responses: dict) -> int:
    for status in ("200", "201", "204"):
        if status in responses:
            return int(status)
    return 200


if __name__ == "__main__":
    endpoints = parse_spec("api/spec/openapi.json")
    for ep in endpoints:
        print(f"\n{ep.method} {ep.path} ({ep.operation_id})")
        print(f"  Tag: {ep.tag} | Auth: {ep.auth_required}")
        if ep.path_params:
            print(f"  Path params: {[p.name for p in ep.path_params]}")
        if ep.body_fields:
            print(f"  Body fields:")
            for f in ep.body_fields:
                constraints = []
                if f.required:
                    constraints.append("required")
                if f.pattern:
                    constraints.append(f"pattern: {f.pattern}")
                if f.enum:
                    constraints.append(f"enum: {f.enum}")
                if f.format:
                    constraints.append(f"format: {f.format}")
                print(f"    - {f.name}: {f.type} ({', '.join(constraints) or 'optional'})")
        print(f"  Response: {ep.success_status} → {ep.response_type}")
