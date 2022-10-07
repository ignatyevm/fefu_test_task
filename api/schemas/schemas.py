from typing import Literal, Optional, List

from pydantic import BaseModel, HttpUrl, Field, validator


class ErrorResponse(BaseModel):
    type: str
    message: str


class ValidationErrorResponse(ErrorResponse):
    field: str
    loc: str


class CreateProfileRequest(BaseModel):
    guid: str = Field()
    full_name: str = Field()
    scientometric_db: Literal["scopus", "wos", "risc"] = Field()
    document_count: int = Field(ge=0)
    citation_count: int = Field(ge=0)
    h_index: int = Field(ge=0)
    url: HttpUrl = Field()

    @validator('full_name')
    def full_name_validator(cls, value):
        if len(value.split(' ')) != 3 or not value.replace(' ', '').isalpha():
            raise ValueError('full_name is incorrect')
        return value


class CreateProfileResponse(BaseModel):
    profile_id: int


class ProfileResponse(BaseModel):
    full_name: str
    h_index: int
    url: str
    document_count: Optional[int]
    citation_count: Optional[int]


class ProfilesResponse(BaseModel):
    profiles: List[ProfileResponse]


class StatisticsResponse(BaseModel):
    scientometric_db: str
    total_document_count: int
    total_citation_count: int
    average_h_index: float
