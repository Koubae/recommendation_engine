from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from recommendation_engine.app.api.controllers.auth import LoginResponse, LoginRequest, AuthController
from recommendation_engine.app.auth.exceptions import AuthUsernameInvalid, AuthPasswordInvalid


@pytest.mark.unit
class TestUnitAuthController:
    @pytest.mark.asyncio
    @patch(
        "recommendation_engine.app.providers.auth_service",
        new_callable=AsyncMock,
    )
    async def test_login_success(self, mock_auth_service):
        mock_request = LoginRequest(username="admin", password="admin")
        mock_response = LoginResponse(access_token="token123", expires=1234567890.0)

        mock_service = AsyncMock()
        mock_service.login.return_value = mock_response
        mock_auth_service.return_value = mock_service

        result = await AuthController.login(request=mock_request, auth_service=mock_service)
        assert result == mock_response

    @pytest.mark.asyncio
    @patch(
        "recommendation_engine.app.providers.auth_service",
        new_callable=AsyncMock,
    )
    async def test_login_account_does_not_exist(self, mock_auth_service):
        mock_request = LoginRequest(username="nonexistentuser", password="admin")

        mock_service = AsyncMock()
        mock_service.login.side_effect = AuthUsernameInvalid()
        mock_auth_service.return_value = mock_service

        with pytest.raises(HTTPException) as exc:
            await AuthController.login(request=mock_request, auth_service=mock_service)

        assert exc.value.status_code == 401

    @pytest.mark.asyncio
    @patch(
        "recommendation_engine.app.providers.auth_service",
        new_callable=AsyncMock,
    )
    async def test_login_invalid_credentials(self, mock_auth_service):
        mock_request = LoginRequest(username="admin", password="wrongpassword")

        mock_service = AsyncMock()
        mock_service.login.side_effect = AuthPasswordInvalid()
        mock_auth_service.return_value = mock_service

        with pytest.raises(HTTPException) as exc:
            await AuthController.login(request=mock_request, auth_service=mock_service)

        assert exc.value.status_code == 401
