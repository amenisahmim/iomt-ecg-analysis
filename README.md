# 🫀 Système de surveillance ECG IoMT
**Raspberry Pi et capteur AD8232**

---

## 📌 Introduction
Ce projet présente une solution IoMT (Internet of Medical Things) dédiée à la surveillance cardiaque en temps réel.

Le système permet :
- l'acquisition du signal ECG via le capteur AD8232
- le traitement local sur Raspberry Pi
- la détection automatique des anomalies cardiaques à l'aide d'un modèle d'intelligence artificielle embarquée (TensorFlow Lite)

Les données analysées sont transmises de manière sécurisée vers le cloud pour une visualisation en temps réel via ThingsBoard.

---

## 🎯 Objectifs
- Surveillance continue de l'activité cardiaque
- Détection automatique des anomalies ECG
- Classification des battements cardiaques en 5 classes
- Estimation de la fréquence cardiaque (HR)
- Supervision cloud sécurisée en temps réel

---

## ⚙️ Technologies utilisées
- Raspberry Pi
- Capteur ECG AD8232
- Python
- TensorFlow / TensorFlow Lite
- MQTT sécurisé (TLS)
- ThingsBoard Cloud
- Edge Computing

---

## 🧱 Architecture du système
Le système repose sur une architecture IoT en couches :

**Couche Physique**
- Capteur ECG AD8232
- Électrodes médicales

**Couche Réseau**
- Communication MQTT sur TLS
- Connexion Wi-Fi

**Couche Application**
- IA embarquée (TensorFlow Lite)
- Tableau de bord ThingsBoard

👉 Le traitement est effectué localement sur le Raspberry Pi afin de réduire la latence et la consommation réseau.

---

## 🔌 Câblage matériel
**AD8232 ↔ Raspberry Pi**

| AD8232 | Raspberry Pi |
|--------|-------------|
| VCC    | 3,3 V       |
| GND    | GND         |
| SORTIE | GPIO / ADC  |
| LO+    | GPIO        |
| LO-    | GPIO        |

Le capteur AD8232 permet une acquisition ECG précise avec une faible consommation d'énergie, adaptée aux applications médicales IoT.

![Câblage AD8232 avec Raspberry Pi](docs/Capture d’écran 2025-12-26 230244.png)

---

## 🤖 Modèle d'Intelligence Artificielle
Le cœur du système repose sur un CNN 1D (Convolutional Neural Network), particulièrement adapté à l'analyse des signaux temporels ECG.

### 🩺 Classes ECG détectées
- Normale
- SVEB – Extrasystole supraventriculaire
- VEB – Extrasystole ventriculaire
- Fusion Beat
- Inconnu

Le modèle est entraîné hors ligne puis converti au format TensorFlow Lite pour une exécution rapide et efficace sur Raspberry Pi.

**📈 Précision du modèle : ~98 %**

---

## ☁️ Supervision Cloud avec ThingsBoard
**Données affichées :**
- Signal ECG en temps réel
- Classe prédite du battement cardiaque
- Probabilités associées
- Fréquence cardiaque (FC)
- Historique des données

La communication est assurée via MQTT sécurisé (TLS) avec authentification par Access Token.

![Tableau de bord ThingsBoard](docs/Capture d'écran 2025-12-13 1957128888.png)

---

## 📁 Structure du projet  
.
├── README.md

├── requirements.txt

├── ecg.py

├── ecg.ipynb

├── ecg_model.tflite

└── docs/
    ├── cablage_ad8232_raspberry.png
    
    └── dashboard_thingsboard.png
    

---


## 🚀 Exécution du projet  

### 1️⃣ Installation des dépendance

pip install -r requirements.txt

### 2️⃣  Lancer le système

python ecg.py

---
## 🔄 Fonctionnalités du script 

-Lecture des données ECG à partir du capteur AD8232

-Prétraitement du signal (normalisation, segmentation)

-Exécution du modèle TensorFlow Lite pour la classification

-Publication sécurisée des résultats vers ThingsBoard via MQTT

 ---
 ## 🔐  Sécurité 


-Communication MQTT chiffrée (TLS)

-Authentification par Access Token

-Traitement local des données sensibles (Edge Computing)


 ---
 



