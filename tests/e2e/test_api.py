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

    def test_create_ticket(self):
        """POST /tickets/ doit créer un ticket."""
        response = client.post(
            "/tickets/",
            json={
                "title": "Bug urgent",
                "description": "L'appli plante",
                "creator_id": "user-001",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Bug urgent"
        assert data["status"] == "open"
        assert "id" in data

    def test_list_tickets(self):
        """GET /tickets/ doit retourner la liste des tickets."""
        response = client.get("/tickets/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    # def test_get_ticket_by_id(self):
    #     """GET /tickets/{id} doit retourner un ticket spécifique."""
    #     # D'abord créer un ticket
    #     create_response = client.post(
    #         "/tickets/",
    #         json={"title": "Test", "description": "Desc"},
    #     )
    #     ticket_id = create_response.json()["id"]

    #     # Puis le récupérer
    #     response = client.get(f"/tickets/{ticket_id}")
    #     assert response.status_code == 200
    #     assert response.json()["id"] == ticket_id

    def test_get_nonexistent_ticket_returns_404(self):
        """GET /tickets/{id} avec un ID inexistant doit retourner 404."""
        response = client.get("/tickets/nonexistent-id")
        assert response.status_code == 404


class TestUserAPI:
    """Tests pour les routes /users."""

    def test_create_user(self):
        """POST /users/ doit créer un utilisateur."""
        import uuid

        unique_username = f"alice-{uuid.uuid4().hex[:6]}"
        response = client.post(
            "/users/",
            json={"username": unique_username, "is_agent": False, "is_admin": False},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == unique_username
        assert data["is_agent"] is False
        assert data["is_admin"] is False
        assert "id" in data

    def test_create_agent(self):
        """POST /users/ doit pouvoir créer un agent."""
        import uuid

        unique_username = f"agent-bob-{uuid.uuid4().hex[:6]}"
        response = client.post(
            "/users/",
            json={"username": unique_username, "is_agent": True, "is_admin": False},
        )
        assert response.status_code == 201
        assert response.json()["is_agent"] is True

    def test_create_duplicate_user_returns_400(self):
        """POST /users/ avec un username existant doit retourner 400."""
        import uuid

        unique_username = f"dupuser-{uuid.uuid4().hex[:6]}"
        client.post("/users/", json={"username": unique_username})
        response = client.post("/users/", json={"username": unique_username})
        assert response.status_code == 400

    def test_list_users(self):
        """GET /users/ doit retourner la liste des utilisateurs."""
        response = client.get("/users/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestStartTicketAPI:
    """Tests de la route PATCH /tickets/{id}/start"""

    def test_start_ticket_success(self):
        """Démarrer un ticket assigné doit retourner 200."""
        # ARRANGE : Créer un ticket
        ticket_data = {
            "title": "Bug critique",
            "description": "Le serveur crash",
            "creator_id": "user-123",
        }
        create_response = client.post("/tickets/", json=ticket_data)
        assert create_response.status_code == 201
        ticket_id = create_response.json()["id"]

        # Assigner le ticket via PATCH /assign
        client.patch(f"/tickets/{ticket_id}/assign", json={"agent_id": "agent-456"})

        # ACT : Démarrer le ticket
        response = client.patch(
            f"/tickets/{ticket_id}/start", 
            json={"agent_id": "agent-456"}
        )

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ticket_id
        assert data["status"] == "in_progress"  # Valeur de Status.IN_PROGRESS.value

    def test_start_nonexistent_ticket_returns_404(self):
        """Démarrer un ticket inexistant doit retourner 404."""
        # ACT
        response = client.patch(
            "/tickets/ticket-inexistant/start", 
            json={"agent_id": "agent-456"}
        )

        # ASSERT
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_start_unassigned_ticket_returns_400(self):
        """Démarrer un ticket non assigné doit retourner 400."""
        # ARRANGE : Créer un ticket NON assigné
        ticket_data = {
            "title": "Bug critique",
            "description": "Le serveur crash",
            "creator_id": "user-123",
        }
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]

        # ACT : Essayer de démarrer sans assignation préalable
        response = client.patch(
            f"/tickets/{ticket_id}/start",
            json={"agent_id": "agent-456"}
        )

        # ASSERT
        assert response.status_code == 400
        assert "assigned" in response.json()["detail"].lower()  # TicketNotAssignedError

    def test_start_with_wrong_agent_returns_400(self):
        """Démarrer avec un agent différent de celui assigné doit retourner 400."""
        # ARRANGE : Créer un ticket et l'assigner à agent-456
        ticket_data = {
            "title": "Bug critique",
            "description": "Le serveur crash",
            "creator_id": "user-123",
        }
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]

        client.patch(f"/tickets/{ticket_id}/assign", json={"agent_id": "agent-456"})

        # ACT : Démarrer avec un autre agent
        response = client.patch(
            f"/tickets/{ticket_id}/start",
            json={"agent_id": "agent-789"}
        )

        # ASSERT
        assert response.status_code == 400
        assert "agent" in response.json()["detail"].lower()  # WrongAgentError

    def test_start_with_invalid_data_returns_422(self):
        """Envoyer des données invalides doit retourner 422."""
        # ARRANGE : Créer et assigner un ticket
        ticket_data = {
            "title": "Bug critique",
            "description": "Le serveur crash",
            "creator_id": "user-123",
        }
        create_response = client.post("/tickets/", json=ticket_data)
        ticket_id = create_response.json()["id"]

        client.patch(f"/tickets/{ticket_id}/assign", json={"agent_id": "agent-456"})

        # ACT : Envoyer un agent_id de type invalide
        response = client.patch(
            f"/tickets/{ticket_id}/start",
            json={"agent_id": 123}  # int au lieu de string
        )

        # ASSERT
        assert response.status_code == 422