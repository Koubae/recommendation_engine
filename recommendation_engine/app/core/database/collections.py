import typing as t

from pydantic import BeforeValidator

PyObjectId = t.Annotated[str, BeforeValidator(str)]
