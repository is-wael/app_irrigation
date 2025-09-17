<div align="center">

💧 Système d'Irrigation Intelligent avec IA
Un simulateur web interactif pour l'optimisation de l'irrigation agricole piloté par l'intelligence artificielle.

</div>

Ce projet propose une solution complète pour la gestion intelligente de l'irrigation, depuis la modélisation d'un "jumeau numérique" jusqu'à une application web de simulation interactive. En s'appuyant sur des données météorologiques en temps réel et un modèle d'intelligence artificielle, l'application permet de tester et de visualiser des stratégies d'arrosage pour optimiser la consommation d'eau.

<br>

<p align="center">
<img src="placeholder_demo.gif" alt="Démo de l'application" width="80%">
<em>(Remplacez ce placeholder par un GIF ou une capture d'écran de votre application)</em>
</p>

🎯 Problématique et Objectifs
Face aux défis croissants liés à la gestion des ressources en eau, l'agriculture de précision est devenue essentielle. Ce projet s'attaque à l'inefficacité des méthodes d'irrigation traditionnelles en proposant un système qui décide de manière autonome quand et combien irriguer.

Les principaux objectifs sont :

Simuler un écosystème sol-plante-météo de manière réaliste.

Développer un cerveau IA capable de prendre des décisions d'irrigation nuancées.

Créer une interface web interactive pour le contrôle et l'analyse.

Valider la méthodologie "Virtual First" pour le développement de systèmes IoT.

✨ Fonctionnalités Principales
🧠 Cerveau Intelligent : Les décisions sont prises par un modèle de Machine Learning (RandomForestRegressor) entraîné sur des milliers de scénarios simulés.

🌦️ Données en Temps Réel : Connexion directe à l'API OpenWeatherMap pour des conditions météorologiques à jour.

🌍 Modélisation de Sol Avancée : Simule différents types de sol (sableux, normal, argileux) avec des propriétés d'absorption et d'évaporation distinctes.

🖥️ Tableau de Bord Interactif : Une interface web construite avec Streamlit permet de configurer chaque paramètre de la simulation et de visualiser les résultats en temps réel.

📊 Analyse Visuelle Détaillée : Des graphiques interactifs (Plotly) et des moniteurs de statut clairs pour une analyse approfondie des résultats.

🔐 Gestion Sécurisée des Clés : Utilise le système de secrets de Streamlit pour protéger les clés API.

🛠️ Stack Technique
Domaine

Technologie

Rôle

Langage

Python

Langage principal du projet.

Application Web

Streamlit

Framework pour la création de l'interface utilisateur interactive.

Analyse de Données

Pandas

Manipulation et stockage de l'historique de simulation.

Machine Learning

Scikit-learn

Entraînement et exécution du modèle d'IA.

Visualisation

Plotly

Création des graphiques interactifs.

Requêtes API

Requests

Communication avec l'API OpenWeatherMap.

Sauvegarde Modèle

Joblib

Sérialisation et chargement du modèle d'IA.

🚀 Lancer le Projet en Local
Suivez ces instructions pour exécuter l'application sur votre machine.

Prérequis
Python 3.9+

Un gestionnaire de paquets (pip)

1. Configuration Initiale
Clonez ce dépôt sur votre machine locale :

git clone [https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_REPO.git](https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_REPO.git)
cd VOTRE_REPO

2. Création de l'Environnement Virtuel
Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.

# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Sur Windows :
venv\Scripts\activate
# Sur macOS/Linux :
source venv/bin/activate

3. Installation des Dépendances
Le fichier requirements.txt contient toutes les bibliothèques nécessaires.

pip install -r requirements.txt

4. Configuration de la Clé API
Pour que l'application puisse communiquer avec OpenWeatherMap, vous devez fournir votre clé API. Créez un dossier .streamlit et, à l'intérieur, un fichier secrets.toml.

# Contenu du fichier : .streamlit/secrets.toml

OPENWEATHER_API_KEY = "VOTRE_CLE_API_PERSONNELLE_ICI"

(Remplacez VOTRE_CLE_API_PERSONNELLE_ICI par votre clé réelle.)

5. Lancement de l'Application
Une fois la configuration terminée, lancez l'application avec la commande suivante :

streamlit run app.py

Votre navigateur devrait s'ouvrir automatiquement à l'adresse http://localhost:8501.

📁 Structure du Dépôt
.
├── .gitignore               # Fichiers et dossiers ignorés par Git.
├── app.py                   # Script principal de l'application Streamlit.
├── irrigation_model.joblib  # Modèle d'IA pré-entraîné.
├── README.md                # Ce fichier.
├── requirements.txt         # Dépendances Python du projet.
└── .streamlit/
    └── secrets.toml         # Fichier (local) pour stocker la clé API.
