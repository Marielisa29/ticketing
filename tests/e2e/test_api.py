"""
Tests end-to-end pour l'API REST (TD03+).

Ces tests vérifient le comportement de l'API via des requêtes HTTP.
Ils testent l'intégration complète : API -> Use Cases -> Repository.

Instructions :
1. Terminez d'abord TD01 et TD02
2. Les tests de la route racine fonctionnent déjà
3. Complétez les routes dans ticket_router.py
4. Décommentez les tests au fur et à mesure
5. Lancez : pytest tests/e2e/
"""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


class TestHealthCheck:
    """Tests de base pour vérifier que l'API fonctionne."""

    def test_root_returns_ok(self):
        """La route racine doit retourner status: ok."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json().get("status") == "ok"


class TestTicketAPI:
    """Tests pour les routes /tickets."""

    # TODO (TD03): Décommenter et implémenter les routes correspondantes

    # def test_create_ticket(self):
    #     """POST /tickets/ doit créer un ticket."""
    #     response = client.post(
    #         "/tickets/",
    #         json={"title": "Bug urgent", "description": "L'appli plante"},
    #     )
    #     assert response.status_code == 201
    #     data = response.json()
    #     assert data["title"] == "Bug urgent"
    #     assert data["status"] == "open"
    #     assert "id" in data

    # def test_list_tickets(self):
    #     """GET /tickets/ doit retourner la liste des tickets."""
    #     response = client.get("/tickets/")
    #     assert response.status_code == 200
    #     assert isinstance(response.json(), list)

    # def test_get_ticket_by_id(self):
    #     """GET /tickets/{id} doit retourner un ticket spécifique."""
    #     # D'abord créer un ticket
    #     create_response = client.post(
    #         "/tickets/",
    #         json={"title": "Test", "description": "Desc"},
    #     )
    #     ticket_id = create_response.json()["id"]
    #
    #     # Puis le récupérer
    #     response = client.get(f"/tickets/{ticket_id}")
    #     assert response.status_code == 200
    #     assert response.json()["id"] == ticket_id

    # def test_get_nonexistent_ticket_returns_404(self):
    #     """GET /tickets/{id} avec un ID inexistant doit retourner 404."""
    #     response = client.get("/tickets/nonexistent-id")
    #     assert response.status_code == 404
