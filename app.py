# Fichier : app.py (Version 5.1 - Humidité de Départ Automatique)

import streamlit as st
import pandas as pd
import requests
import datetime
import random
import plotly.graph_objects as go
import joblib
import os

# ==============================================================================
# PARTIE 1 : LOGIQUE DE SIMULATION (INCHANGÉE)
# ==============================================================================
class SolVirtuel_v2:
    def __init__(self, humidite_initiale=60.0, temperature_initiale=18.0, type_sol='normal'):
        self.humidite_sol = float(humidite_initiale)
        self.temperature_sol = float(temperature_initiale)
        self.type_sol = type_sol
        self.proprietes_sol = {'normal': {'facteur_evaporation': 1.0, 'facteur_absorption': 1.0},'sandy':  {'facteur_evaporation': 1.5, 'facteur_absorption': 0.8},'clay':   {'facteur_evaporation': 0.7, 'facteur_absorption': 1.2}}
        self.params = self.proprietes_sol.get(self.type_sol, self.proprietes_sol['normal'])
    def _calculer_evapotranspiration(self, temp_air, hum_air):
        K_EVAP = 0.2
        perte = K_EVAP * (temp_air / (hum_air + 1)) * (self.humidite_sol / 100.0)
        return perte * self.params['facteur_evaporation']
    def mettre_a_jour(self, donnees_meteo):
        perte_et = self._calculer_evapotranspiration(donnees_meteo['temperature'], donnees_meteo['humidity'])
        self.humidite_sol -= perte_et
        gain_pluie = donnees_meteo['precipitation_1h'] * self.params['facteur_absorption']
        self.humidite_sol += gain_pluie
        self.temperature_sol = (self.temperature_sol * 0.95) + (donnees_meteo['temperature'] * 0.05)
        self.humidite_sol = max(0.0, min(100.0, self.humidite_sol))
    def irriguer(self, quantite_mm):
        gain_irrigation = quantite_mm * self.params['facteur_absorption']
        self.humidite_sol += gain_irrigation
        self.humidite_sol = min(100.0, self.humidite_sol)

@st.cache_data(ttl=600)
def get_weather_data(api_key, city_name):
    if not api_key or not city_name:
        return None
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    url = f"{base_url}?q={city_name}&appid={api_key}&units=metric&lang=fr"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"temperature": data["main"]["temp"], "humidity": data["main"]["humidity"], "precipitation_1h": data.get('rain', {}).get('1h', 0)}
    except: return None

@st.cache_resource
def load_model(path):
    if not os.path.exists(path):
        return None
    return joblib.load(path)

def decider_irrigation_ia(model, sol, meteo):
    if model is None: return 0, 0
    input_data = {
        'humidite_sol': sol.humidite_sol, 'temperature_air': meteo['temperature'], 'humidite_air': meteo['humidity'],
        'type_sol_normal': 1 if sol.type_sol == 'normal' else 0, 'type_sol_sandy': 1 if sol.type_sol == 'sandy' else 0,
    }
    df_input = pd.DataFrame([input_data])
    prediction_brute = model.predict(df_input)[0]
    decision_finale = prediction_brute
    if meteo['precipitation_1h'] > 0 or prediction_brute < 0.2:
        decision_finale = 0.0
    return decision_finale, prediction_brute

# ==============================================================================
# PARTIE 2 : INTERFACE UTILISATEUR
# ==============================================================================

st.set_page_config(page_title="Simulateur d'Irrigation IA", layout="wide", initial_sidebar_state="expanded")
st.title("💧 Simulateur d'Irrigation Intelligente")

# --- SIDEBAR ---
st.sidebar.title("Paramètres")
model_ia = load_model('irrigation_model.joblib')
if model_ia is None: st.sidebar.error("Modèle IA non trouvé.")
else: st.sidebar.success("Modèle IA chargé.")
    
api_key = st.sidebar.text_input("Clé API OpenWeatherMap", type="password")
city_name = st.sidebar.text_input("Nom de la ville", "Kenitra")
duree_sim = st.sidebar.slider("Durée de simulation (heures)", 24, 168, 72)
type_sol = st.sidebar.selectbox("Type de sol", ('normal', 'sandy', 'clay'))

### NOUVELLE LOGIQUE POUR L'HUMIDITÉ DE DÉPART AUTOMATIQUE ###
humidite_depart_defaut = 60 # Valeur par défaut si l'API ne répond pas
meteo_initiale = get_weather_data(api_key, city_name)

if meteo_initiale:
    # Si on a la météo, on prend l'humidité de l'air comme valeur par défaut
    humidite_depart_defaut = int(meteo_initiale['humidity'])
    st.sidebar.info(f"L'humidité de l'air à {city_name} est de {humidite_depart_defaut}%. Elle est utilisée comme valeur de départ par défaut.")

humidite_depart = st.sidebar.slider("Humidité de départ (%)", 0, 100, humidite_depart_defaut)


start_button = st.sidebar.button("🚀 Lancer la Simulation")

# --- ZONE PRINCIPALE ---
if start_button:
    if not api_key: st.error("Veuillez entrer votre clé API pour commencer.")
    elif model_ia is None: st.error("Le modèle IA n'est pas disponible.")
    else:
        # On utilise la météo déjà récupérée si possible, sinon on la redemande
        meteo_base = meteo_initiale if meteo_initiale else get_weather_data(api_key, city_name)
        
        if not meteo_base: st.error(f"Erreur Météo pour {city_name}.")
        else:
            with st.spinner("L'IA calcule la simulation..."):
                sol = SolVirtuel_v2(humidite_initiale=humidite_depart, type_sol=type_sol)
                historique = []
                # ... (le reste de la boucle de simulation est inchangé)
                for heure in range(duree_sim):
                    meteo_heure = meteo_base.copy()
                    meteo_heure['temperature'] += random.uniform(-0.5, 0.5)
                    meteo_heure['humidity'] = max(20, min(100, meteo_base['humidity'] + random.uniform(-2, 2)))
                    meteo_heure['precipitation_1h'] = 0.0 if random.random() > 0.04 else random.uniform(0.5, 5.0)
                    quantite_irrigation, prediction_ia_brute = decider_irrigation_ia(model_ia, sol, meteo_heure)
                    if quantite_irrigation > 0: sol.irriguer(quantite_irrigation)
                    log = {"heure": heure + 1, "humidite_sol_%": sol.humidite_sol, "temperature_air": meteo_heure['temperature'], "irrigation_mm": quantite_irrigation, "prediction_IA_brute": prediction_ia_brute}
                    historique.append(log)
                    sol.mettre_a_jour(meteo_heure)
            
            st.success("Simulation IA terminée !")
            df_historique = pd.DataFrame(historique)
            
            # ... (toute la section d'affichage du dashboard est inchangée)
            st.markdown("---")
            st.header("Dashboard de Supervision")
            humidite_finale = df_historique['humidite_sol_%'].iloc[-1]
            temp_finale = df_historique['temperature_air'].iloc[-1]
            eau_totale = df_historique['irrigation_mm'].sum()
            df_irrigations = df_historique[df_historique['irrigation_mm'] > 0]
            if not df_irrigations.empty: derniere_irrigation = f"Heure {df_irrigations['heure'].iloc[-1]}"
            else: derniere_irrigation = "Aucune"
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💧 Humidité Sol", f"{humidite_finale:.1f} %")
            col2.metric("🌡️ Température Air", f"{temp_finale:.1f} °C")
            col3.metric("🚱 Eau Utilisée", f"{eau_totale:.1f} mm")
            col4.metric("🕒 Dernière Irrigation", derniere_irrigation)
            st.subheader("📈 Historique de la Simulation")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_historique['heure'], y=df_historique['humidite_sol_%'], mode='lines', name='Humidité du Sol (%)', line_color='green'))
            fig.add_trace(go.Bar(x=df_historique['heure'], y=df_historique['irrigation_mm'], name='Irrigation (mm)', marker_color='blue'))
            fig.update_layout(xaxis_title="Heures", yaxis_title="Valeur")
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("Voir les données brutes de la simulation"):
                st.dataframe(df_historique)

else:
    st.info("Configurez les paramètres et lancez la simulation pour voir le tableau de bord.")