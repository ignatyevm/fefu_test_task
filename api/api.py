from pathlib import Path
from typing import List, Literal, Optional

from fastapi import FastAPI, Depends, APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi_utils.cbv import cbv
from starlette import status
from starlette.responses import JSONResponse

from api.config import get_database_url
from api.db.database import Database
from api.exceptions.exceptions import ProfileAlreadyExists, ProfileNotFound
from api.schemas.schemas import ProfilesResponse, ProfileResponse, CreateProfileResponse, \
    CreateProfileRequest, StatisticsResponse, ErrorResponse, ValidationErrorResponse
from api.services.profile_service import ProfileService
from api.utils import db_filler, dataset

api = FastAPI(dependencies=[Depends(get_database_url)])
api_router = APIRouter()


@cbv(api_router)
class API:
    __profile_service: ProfileService = Depends()

    @api_router.get("/profiles", response_model=ProfilesResponse, response_model_exclude_none=True)
    async def get_profiles(self, scientometric_database: Literal["scopus", "wos", "risc"] = Query(),
                           limit: Optional[int] = Query(ge=0, default=10),
                           offset: Optional[int] = Query(ge=0, default=0),
                           order_by: Literal["date", "h_index"] = Query(default="date"),
                           order_dir: Literal["asc", "desc"] = Query(default="asc")) -> ProfilesResponse:
        return self.__profile_service.get_profiles(scientometric_database, limit, offset,
                                                   order_by, order_dir)

    @api_router.get("/profiles/{guid}", response_model=ProfileResponse, response_model_exclude_none=True)
    async def get_profile(self, guid: str = Path(), scientometric_database: Literal["scopus", "wos", "risc"] = Query(),
                          fields: Optional[List[str]] = Query(default=[])) -> ProfileResponse:
        return self.__profile_service.get_profile(guid, scientometric_database, fields)

    @api_router.post("/profiles", response_model=CreateProfileResponse, status_code=status.HTTP_201_CREATED)
    async def create_profile(self, dto: CreateProfileRequest) -> CreateProfileResponse:
        return self.__profile_service.create_profile(dto)

    @api_router.get("/publication_activity_statistics", response_model=List[StatisticsResponse])
    async def get_statistics(self) -> List[StatisticsResponse]:
        return self.__profile_service.get_statistics()


api.include_router(api_router)


@api.on_event("startup")
async def startup_event():
    db: Database = Database(get_database_url())
    session = db.get_session()
    db_initialized = session.execute("SELECT EXISTS (SELECT FROM information_schema.tables "
                                     "WHERE table_name = 'scientometric_db')").first()[0]
    if not db_initialized:
        authors, scientometric_databases, profiles = dataset.parse()
        db_filler.fill(db, authors, scientometric_databases, profiles)


@api.exception_handler(ProfileAlreadyExists)
async def profile_already_exists_handler(request, exception: ProfileAlreadyExists):
    return JSONResponse(jsonable_encoder(ErrorResponse(type=exception.get_type(), message=exception.message)),
                        status_code=status.HTTP_409_CONFLICT)


@api.exception_handler(ProfileNotFound)
async def profile_not_found_handler(request, exception: ProfileAlreadyExists):
    return JSONResponse(jsonable_encoder(ErrorResponse(type=exception.get_type(), message=exception.message)),
                        status_code=status.HTTP_404_NOT_FOUND)


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exception):
    response: List[ErrorResponse] = []
    for error in exception.errors():
        response.append(ValidationErrorResponse(type=error['type'], message=error['msg'],
                                                loc=error['loc'][0], field=error['loc'][1]))
    return JSONResponse(jsonable_encoder(response), status_code=status.HTTP_400_BAD_REQUEST)
