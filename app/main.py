import asyncio

from fastapi import APIRouter, FastAPI

from app.config import Settings
from app.endpoints import router
from app.managers import db_app
from app.models import Base


class FastApiManager:
    def __init__(
        self,
        settings: Settings = Settings(),
        title: str = "Api",
        openapi_url: str = "/api/openapi.json",
        version: str = "0.1.0",
    ) -> None:
        """
        Initializes a new instance of the FastApiManager class.

        Args:
            settings (Settings, optional): The settings to use for the application. Defaults to Settings().
            title (str, optional): The title of the application. Defaults to "api".
            openapi_url (str, optional): The URL for the OpenAPI specification. Defaults to "/api/openapi.json".
            version (str, optional): The version of the application. Defaults to "0.1.0".
        """
        self._settings = settings

        self._app = FastAPI(
            title=title, openapi_url=openapi_url, version=version
        )

    @property
    def app(self) -> FastAPI:
        """
        The FastAPI application.
        """
        return self._app

    @property
    def settings(self) -> Settings:
        """
        The application settings object.
        """
        return self._settings

    async def init_app(self) -> None:
        """
        Initializes the application.
        """
        await self._setup_apps()
        await self._setup_blueprint()

    async def _setup_blueprint(self) -> None:
        """
        Sets up the API blueprint with the necessary routers.
        """
        root_router = APIRouter(prefix="/api/v1")
        root_router.include_router(router)

        self.app.include_router(root_router)

    async def _setup_apps(self) -> None:
        """
        Set up the applications.
        """
        await self._setup_db()

    async def _setup_db(self) -> None:
        """
        Sets up the database connection and initializes the database schema.
        """
        db_app.init_app(self._settings)
        assert db_app.engine

        async with db_app.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


def create_app() -> FastAPI:
    """
    Creates a new instance of the FastAPI application.

    Note:
        We use uvicorn's event loop otherwise we might encounter some errors
        because we might be trying to access another event loop.

    Returns:
        FastAPI: The FastAPI application.
    """
    app_manager = FastApiManager()
    loop = asyncio.get_event_loop()
    loop.create_task(app_manager.init_app())
    return app_manager.app
