from typing import List

from fastapi import Depends

from api.exceptions.exceptions import ProfileAlreadyExists, ProfileNotFound
from api.models.models import Author, AuthorProfile
from api.repositories.profile_repository import ProfileRepository
from api.schemas.schemas import ProfilesResponse, ProfileResponse, CreateProfileResponse, \
    CreateProfileRequest, StatisticsResponse


class ProfileService:
    def __init__(self, profile_repo: ProfileRepository = Depends()):
        self.__profile_repo = profile_repo

    def get_profiles(self, scientometric_database: str, limit: int, offset: int,
                     order_by: str, order_dir: str) -> ProfilesResponse:
        profiles = self.__profile_repo.find_profiles(scientometric_database, limit, offset,
                                                     order_by, order_dir)
        return ProfilesResponse(profiles=profiles)

    def get_profile(self, guid: str, scientometric_database: str, fields: List[str]) -> ProfileResponse:
        profile = self.__profile_repo.find_profile(guid, scientometric_database, fields)
        if profile is None:
            raise ProfileNotFound(guid, scientometric_database)
        return profile

    def create_profile(self, dto: CreateProfileRequest) -> CreateProfileResponse:
        self.__profile_repo.begin_transaction()
        scientometric_db = self.__profile_repo.find_scientometric_db_by_name(dto.scientometric_db)

        profile = self.__profile_repo.find_profile(dto.guid, dto.scientometric_db)
        if profile is not None:
            raise ProfileAlreadyExists(dto.guid, dto.full_name, dto.scientometric_db)

        author = self.__profile_repo.find_author_by_guid(dto.guid)
        if author is None:
            author = self.__profile_repo.create_author(Author(guid=dto.guid, full_name=dto.full_name))
        self.__profile_repo.commit_transaction()

        self.__profile_repo.begin_transaction()
        profile = AuthorProfile(author=author, scientometric_db=scientometric_db, document_count=dto.document_count,
                                citation_count=dto.citation_count, h_index=dto.h_index, url=dto.url)
        profile = self.__profile_repo.create_profile(profile)
        self.__profile_repo.commit_transaction()

        return CreateProfileResponse(profile_id=profile.id)

    def get_statistics(self) -> List[StatisticsResponse]:
        self.__profile_repo.begin_transaction()
        statistics = self.__profile_repo.get_statistics()
        self.__profile_repo.commit_transaction()
        return statistics
