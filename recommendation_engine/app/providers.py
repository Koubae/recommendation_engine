from functools import cache
from typing import Annotated

from fastapi import Depends

from recommendation_engine.app.auth.access_token import HashLibPasswordHasher, JWTAccessTokenAuth
from recommendation_engine.app.auth.service import AuthService
from recommendation_engine.app.core.database.mongo_database import MongoDatabase
from recommendation_engine.app.recommendation.repository import RecommendationRepository


def provide_access_token_auth() -> JWTAccessTokenAuth:
    auth = JWTAccessTokenAuth()
    return auth


@cache
def auth_service(jwt_auth: JWTAccessTokenAuth = Depends(provide_access_token_auth)) -> AuthService:
    service = AuthService(
        password_hasher=HashLibPasswordHasher(),
        auth=jwt_auth,
    )
    return service


AuthServiceSingleton = Annotated[AuthService, Depends(auth_service)]


@cache
def get_database() -> MongoDatabase:
    _database = MongoDatabase()
    return _database


@cache
def recommendation_repository(database_client: MongoDatabase = Depends(get_database)) -> RecommendationRepository:
    _repository = RecommendationRepository(
        database_client=database_client,
    )
    return _repository


RecommendationRepositorySingleton = Annotated[RecommendationRepository, Depends(recommendation_repository)]
