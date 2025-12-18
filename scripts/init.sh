#!/bin/bash
# Script d'initialisation de l'environnement de travail
# ⚠️ À exécuter avec : source scripts/init.sh

set -e  # Arrêter en cas d'erreur

# Vérifier que le script est sourcé, pas exécuté
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "❌ Erreur : Ce script doit être exécuté avec 'source'"
    echo ""
    echo "   Utilisez : source scripts/init.sh"
    echo "   Et non   : ./scripts/init.sh"
    echo ""
    exit 1
fi

echo "🚀 Initialisation de l'environnement de travail..."
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Vérifier qu'on est dans le bon dossier
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erreur : Ce script doit être exécuté à la racine du projet (où se trouve requirements.txt)"
    return 1
fi

# 2. Récupérer les dernières modifications
echo "📥 Récupération des dernières modifications..."
git pull origin main 2>/dev/null || git pull 2>/dev/null || echo -e "${YELLOW}⚠️  Impossible de pull (pas de remote configuré ou pas de connexion)${NC}"
echo ""

# 3. Créer l'environnement virtuel si nécessaire
if [ ! -d ".venv" ]; then
    echo "🐍 Création de l'environnement virtuel..."
    python3 -m venv .venv
    echo -e "${GREEN}✅ Environnement virtuel créé${NC}"
else
    echo -e "${GREEN}✅ Environnement virtuel existant${NC}"
fi
echo ""

# 4. Activer l'environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
source .venv/bin/activate
echo -e "${GREEN}✅ Environnement activé${NC}"
echo ""

# 5. Installer/mettre à jour les dépendances
echo "📦 Installation des dépendances..."
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Dépendances installées${NC}"
echo ""

# 6. Configurer pre-commit si nécessaire
if [ ! -f ".git/hooks/pre-commit" ]; then
    echo "🔧 Configuration de pre-commit..."
    pre-commit install
    echo -e "${GREEN}✅ Pre-commit configuré${NC}"
else
    echo -e "${GREEN}✅ Pre-commit déjà configuré${NC}"
fi
echo ""

# 7. Lancer les tests pour vérifier
echo "🧪 Vérification avec les tests..."
if pytest -q; then
    echo ""
    echo -e "${GREEN}✅ Tous les tests passent !${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Certains tests échouent. Vérifiez votre code.${NC}"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}🎉 Environnement prêt !${NC}"
echo ""
echo "Commandes utiles :"
echo "  pytest                         → Lancer les tests"
echo "  uvicorn src.main:app --reload  → Démarrer le serveur"
echo "=========================================="
