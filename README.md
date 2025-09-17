<div align="center">

💧 Système d'Irrigation Intelligent : de la Simulation à la Réalité
Un projet complet en deux phases : un simulateur web interactif piloté par l'IA et son prototype physique fonctionnel.

</div>

Ce projet documente le cycle de vie complet d'un système d'irrigation intelligent, de sa conception et son optimisation dans un environnement virtuel à sa mise en œuvre matérielle. L'objectif est de créer une solution low-cost et open-source pour l'agriculture de précision, en utilisant une méthodologie "Virtual First" pour dé-risquer et accélérer le développement.

<br>



📂 Structure du Projet en Deux Phases
Ce dépôt est organisé en deux parties complémentaires :

Phase 1 : Le Simulateur Virtuel (Le "Cerveau") 🧠
Une application web développée avec Streamlit qui agit comme un "jumeau numérique" du système.

Modélisation Physique : Simule le comportement de l'humidité du sol en fonction de la météo (via API OpenWeatherMap) et du type de sol.

Cerveau IA : Un modèle RandomForestRegressor entraîné sur des milliers de scénarios pour prédire la quantité d'eau optimale.

Laboratoire d'Expérimentation : Permet de tester des stratégies, de calibrer des seuils et de visualiser l'impact de chaque paramètre sans aucun coût matériel.

Phase 2 : Le Prototype Physique (Le "Corps") 🦾
Un montage électronique fonctionnel qui exécute la logique d'irrigation dans le monde réel.

Microcontrôleur : Un ESP8266 (NodeMCU) sert d'unité de contrôle.

Capteur : Un capteur d'humidité du sol capacitif mesure l'état du sol en temps réel.

Actionneur : Une mini-pompe à eau est activée via un module relais pour délivrer l'eau.

Logique Embarquée : Le firmware, écrit en C++/Arduino, applique les seuils et les stratégies validés grâce au simulateur.

🛠️ Stack Technique et Matérielle
Domaine

Technologie / Composant

Rôle

Simulation Web

Streamlit, Pandas, Plotly

Interface utilisateur et analyse des données.

Intelligence Artificielle

Scikit-learn, Joblib

Entraînement et exécution du modèle prédictif.

Microcontrôleur

NodeMCU ESP8266

Unité de contrôle du prototype.

Capteur

Capteur d'humidité capacitif V1.2

Mesure de l'humidité du sol.

Actionneur

Module Relais 5V, Pompe 5V

Commande et distribution de l'eau.

🚀 Lancer le Simulateur Web (Phase 1)
1. Configuration Initiale
Clonez le dépôt et naviguez dans le dossier :

git clone [https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_REPO.git](https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_REPO.git)
cd VOTRE_REPO

2. Environnement Virtuel et Dépendances
# Créer et activer l'environnement
python -m venv venv
# Windows: venv\Scripts\activate | macOS/Linux: source venv/bin/activate

# Installer les bibliothèques
pip install -r requirements.txt

3. Configurer la Clé API
Créez le fichier .streamlit/secrets.toml et ajoutez votre clé OpenWeatherMap :

# Fichier: .streamlit/secrets.toml
OPENWEATHER_API_KEY = "VOTRE_CLE_API_ICI"

4. Lancer l'Application
streamlit run app.py

L'application sera accessible sur http://localhost:8501.

🔌 Assembler et Programmer le Prototype (Phase 2)
1. Composants Nécessaires
1x NodeMCU ESP8266

1x Capteur d'humidité du sol capacitif V1.2

1x Module Relais 1 canal 5V

1x Mini-pompe à eau submersible 5V

Des fils de connexion (Dupont)

Une source d'alimentation externe 5V pour la pompe.

2. Schéma de Câblage
(Insérez ici une image de votre schéma de câblage, par exemple schema.png)

<p align="center">
<img src="schema_placeholder.png" alt="Schéma de câblage" width="70%">
</p>

Composant

Connexion sur l'ESP8266

Capteur (VCC)

3.3V

Capteur (GND)

GND

Capteur (AOUT)

A0

Relais (VCC)

VIN (5V)

Relais (GND)

GND

Relais (IN)

D1

3. Programmation
Configurez votre Arduino IDE pour la carte NodeMCU ESP8266.

Ouvrez le fichier firmware/esp8266_firmware.ino.

Calibrez votre capteur : Modifiez les valeurs VALEUR_CAPTEUR_SEC et VALEUR_CAPTEUR_HUMIDE après avoir fait des tests (un dans l'air, un dans l'eau).

Ajustez le seuil : Modifiez la valeur SEUIL_HUMIDITE_POURCENT en vous basant sur les résultats de vos simulations.

Téléversez le code sur votre ESP8266.

📁 Structure du Dépôt
.
├── .gitignore
├── app.py                     # Script du simulateur web Streamlit
├── irrigation_model.joblib    # Modèle d'IA pré-entraîné
├── README.md                  # Ce fichier
├── requirements.txt           # Dépendances Python pour le simulateur
└── smart_irrigation.rar       # Code Arduino pour le prototype
