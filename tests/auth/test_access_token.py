from datetime import datetime, timedelta, UTC
from unittest.mock import patch

import jwt
import pytest

from recommendation_engine.app.auth.access_token import HashLibPasswordHasher, JWTAccessTokenAuth
from recommendation_engine.app.auth.exceptions import AuthAccessTokenExpired, AuthAccessTokenInvalid
from recommendation_engine.app.auth.models import AccessToken


@pytest.mark.unit
class TestHashLibPasswordHasher:

    def test_hash_password_generates_consistent_hash(self):
        password = "test_password"
        hashed_password1 = HashLibPasswordHasher.hash_password(password)
        hashed_password2 = HashLibPasswordHasher.hash_password(password)
        assert (
                hashed_password1 == hashed_password2
        ), "Hashing the same password should produce consistent results"

    def test_hash_password_generates_different_hashes_for_different_inputs(self):
        password1 = "password_one"
        password2 = "password_two"
        hashed_password1 = HashLibPasswordHasher.hash_password(password1)
        hashed_password2 = HashLibPasswordHasher.hash_password(password2)
        assert (
                hashed_password1 != hashed_password2
        ), "Hashing different passwords should produce different results"

    def test_verify_password_with_matching_password(self):
        password = "secure_password"
        hashed_password = HashLibPasswordHasher.hash_password(password)
        result = HashLibPasswordHasher.verify_password(password, hashed_password)
        assert (
                result is True
        ), "verify_password should return True for matching password and hash"

    def test_verify_password_with_non_matching_password(self):
        password = "secure_password"
        hashed_password = HashLibPasswordHasher.hash_password(password)
        fake_password = "fake_password"
        result = HashLibPasswordHasher.verify_password(fake_password, hashed_password)
        assert (
                result is False
        ), "verify_password should return False for non-matching password and hash"


@pytest.mark.unit
class TestJWTAccessTokenGenerator:

    def test_generate_access_token_creates_valid_token(self):
        generator = JWTAccessTokenAuth()

        token = generator.generate_access_token(user_id=1, username="user")
        assert isinstance(
            token, AccessToken,
        ), "Generated token must be of type AccessToken"

        assert "user" == token.username, "Generated token must have the correct values"

    def test_generated_token_has_valid_expiration(self):
        generator = JWTAccessTokenAuth()
        token = generator.generate_access_token(user_id=1, username="user")
        now = datetime.now(UTC)
        expiration_time = datetime.fromtimestamp(token.expires, tz=UTC)
        assert (
                expiration_time > now
        ), "Generated token must have a future expiration time"
        assert expiration_time <= now + timedelta(
            hours=1,
        ), "Generated token must expire within the correct time frame"

    @patch("jwt.decode")
    def test_parse_access_token_raises_expired_error(self, mock_decode):
        generator = JWTAccessTokenAuth()
        mock_decode.side_effect = jwt.ExpiredSignatureError
        with pytest.raises(AuthAccessTokenExpired):
            generator.parse_access_token("expired_token")

    @patch("jwt.decode")
    def test_parse_access_token_raises_invalid_error(self, mock_decode):
        generator = JWTAccessTokenAuth()
        mock_decode.side_effect = jwt.InvalidTokenError
        with pytest.raises(AuthAccessTokenInvalid):
            generator.parse_access_token("invalid_token")
