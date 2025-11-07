from typing import Literal

from pydantic import BaseModel


class ProgressResponse(BaseModel):
    state: Literal["PROGRESS", "FINISHED"]
    progress: float
    result: None | str
