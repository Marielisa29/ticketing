"""
Utilitaires helper pour SQLite.

Ce module fournit des fonctions pour gérer les connexions SQLite,
l'initialisation de la base de données et la création du schéma.
"""

import sqlite3
from pathlib import Path
from typing import Optional


def get_connection(db_path: str = "ticketing.db") -> sqlite3.Connection:
    """
    Obtient une connexion à la base de données SQLite.

    Args:
        db_path: Chemin vers le fichier de base de données

    Returns:
        Connexion SQLite avec Row factory activé
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Active l'accès type dictionnaire aux lignes
    return conn


def init_database(db_path: str = "ticketing.db", schema_path: Optional[str] = None):
    """
    Initialise la base de données en créant les tables depuis schema.sql.

    Args:
        db_path: Chemin vers le fichier de base de données
        schema_path: Chemin vers le fichier schema.sql
        (optionnel, auto-détecté si non fourni)
    """
    if schema_path is None:
        # Auto-détection de schema.sql dans le même répertoire
        schema_path = Path(__file__).parent / "schema.sql"

    if not Path(schema_path).exists():
        raise FileNotFoundError(f"Fichier schema non trouvé : {schema_path}")

    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Lecture et exécution du schéma
    with open(schema_path, encoding="utf-8") as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)

    conn.commit()
    conn.close()


def close_connection(conn: sqlite3.Connection):
    """
    Ferme une connexion à la base de données.

    Args:
        conn: La connexion à fermer
    """
    if conn:
        conn.close()
