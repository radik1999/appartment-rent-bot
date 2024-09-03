from typing import Callable, List, NamedTuple

class Variant(NamedTuple):
    view: Callable
    name: str
    method_name: str = "get"
    status_code: int = 200
    expected: dict | List[dict] | str | None = None
    body: dict | list | None = None
    query_params: dict | None = None
    url_kwargs: dict | None = None
