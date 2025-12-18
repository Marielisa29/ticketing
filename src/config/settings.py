"""
Configuration de l'application.

Ce module centralise les paramètres de configuration.
Les valeurs peuvent être surchargées via des variables d'environnement.
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Paramètres de configuration de l'application.

    Attributes:
        APP_NAME: Nom de l'application
        DEBUG: Mode débogage activé ou non
    """

    APP_NAME: str = "Ticketing Starter"
    DEBUG: bool = True


settings = Settings()
