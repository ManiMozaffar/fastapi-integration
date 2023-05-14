from typing import List, Optional


from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    results: List[dict] = Field(
        ...,
        description="Results OBJ of API",
        example=[{"id": 1}, {"id": 2}]
    )
    count: int = Field(
        ...,
        description="Count of results",
    )
    next_page_url: Optional[str] = Field(
        ...,
        description="Next Page URL if it exists",
    )
    previous_page_url: Optional[str] = Field(
        ...,
        description="Last Page URL if it exists",
    )

    class Config:
        orm_mode = True
