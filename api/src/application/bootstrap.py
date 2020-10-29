from config import get_configuration
from src.application.postgresql_artists_repository import PostgreSQLArtistsRepository


config = get_configuration()

postgresql_artists_repository = PostgreSQLArtistsRepository(config.POSTGRESQL_SETTINGS)
