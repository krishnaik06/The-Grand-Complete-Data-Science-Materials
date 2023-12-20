from box.exceptions import BoxError as BoxError
from os import PathLike as PathLike
from typing import Any, Union, Optional, Dict

yaml_available: bool
toml_available: bool
msgpack_available: bool
BOX_PARAMETERS: Any

def _exists(filename: Union[str, PathLike], create: bool = False) -> Any: ...
def _to_json(
    obj, filename: Union[str, PathLike] = None, encoding: str = "utf-8", errors: str = "strict", **json_kwargs
) -> Any: ...
def _from_json(
    json_string: str = None,
    filename: Union[str, PathLike] = None,
    encoding: str = "utf-8",
    errors: str = "strict",
    multiline: bool = False,
    **kwargs,
) -> Any: ...
def _to_yaml(
    obj,
    filename: Union[str, PathLike] = None,
    default_flow_style: bool = False,
    encoding: str = "utf-8",
    errors: str = "strict",
    ruamel_typ: str = "rt",
    ruamel_attrs: Optional[Dict] = None,
    **yaml_kwargs,
) -> Any: ...
def _from_yaml(
    yaml_string: str = None,
    filename: Union[str, PathLike] = None,
    encoding: str = "utf-8",
    errors: str = "strict",
    ruamel_typ: str = "rt",
    ruamel_attrs: Optional[Dict] = None,
    **kwargs,
) -> Any: ...
def _to_toml(obj, filename: Union[str, PathLike] = None, encoding: str = "utf-8", errors: str = "strict") -> Any: ...
def _from_toml(
    toml_string: str = None, filename: Union[str, PathLike] = None, encoding: str = "utf-8", errors: str = "strict"
) -> Any: ...
def _to_msgpack(obj, filename: Union[str, PathLike] = None, **kwargs) -> Any: ...
def _from_msgpack(msgpack_bytes: bytes = None, filename: Union[str, PathLike] = None, **kwargs) -> Any: ...
def _to_csv(
    box_list, filename: Union[str, PathLike] = None, encoding: str = "utf-8", errors: str = "strict", **kwargs
) -> Any: ...
def _from_csv(
    csv_string: str = None,
    filename: Union[str, PathLike] = None,
    encoding: str = "utf-8",
    errors: str = "strict",
    **kwargs,
) -> Any: ...
