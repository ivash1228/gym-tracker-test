from dataclasses import dataclass, field


@dataclass
class Field:
    name: str
    type: str
    required: bool = False
    format: str | None = None
    pattern: str | None = None
    enum: list[str] | None = None


@dataclass
class PathParam:
    name: str
    type: str
    format: str | None = None
    required: bool = True


@dataclass
class Endpoint:
    path: str
    method: str
    operation_id: str
    tag: str
    auth_required: bool = True
    path_params: list[PathParam] = field(default_factory=list)
    body_fields: list[Field] = field(default_factory=list)
    success_status: int = 200
    response_type: str | None = None
