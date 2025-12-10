# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import numpy as np
import tflite_runtime.interpreter as tflite
import paho.mqtt.client as mqtt
import json
from scipy.signal import find_peaks

# ----- CONSTANTES -----
ECG_PIN = 18
SAMPLES = 187
CLASS_NAMES = ["Normal", "SVEB", "VEB", "Fusion", "Unknown"]  # <-- corrigé selon ton modèle
SAMPLING_RATE = 250  # Hz

# ----- GPIO CONFIG -----
GPIO.setmode(GPIO.BCM)
GPIO.setup(ECG_PIN, GPIO.IN)

# ----- THINGSBOARD -----
THINGBOARD_HOST = "mqtt.eu.thingsboard.cloud"
ACCESS_TOKEN = "NA8k7b8mZzH74oMcPbTb"

client = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)
client.username_pw_set(ACCESS_TOKEN)
client.tls_set()  # pour MQTT sécurisé
client.connect(THINGBOARD_HOST, 8883, 60)
client.loop_start()

# ----- LOAD TFLITE MODEL -----
interpreter = tflite.Interpreter(model_path="/home/pi/ecg/ecg_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# ----- READ ECG SIGNAL -----
def read_ecg_signal(samples=SAMPLES):
    signal = []
    while len(signal) < samples:
        val = GPIO.input(ECG_PIN)
        signal.append(val)
        time.sleep(1/SAMPLING_RATE)
    
    signal = np.array(signal, dtype=np.float32).reshape(1, -1, 1)
    if signal.dtype != input_details[0]["dtype"]:
        signal = signal.astype(input_details[0]["dtype"])
    return signal

# ----- ESTIMATE HEART RATE -----
def estimate_hr(signal_1d):
    # Détecte les pics R
    peaks, _ = find_peaks(signal_1d, height=0.5, distance=SAMPLING_RATE*0.3)
    if len(peaks) < 2:
        return 0
    rr_intervals = np.diff(peaks) / SAMPLING_RATE
    hr = 60 / np.mean(rr_intervals)
    return int(hr)

# ----- PREDICTION -----
def predict_ecg(signal):
    interpreter.set_tensor(input_details[0]["index"], signal)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])[0]
    output_data = output_data[:len(CLASS_NAMES)]
    predicted_class_index = np.argmax(output_data)
    predicted_class_name = CLASS_NAMES[predicted_class_index]
    return predicted_class_name, output_data

# ----- MAIN LOOP -----
if __name__ == "__main__":
    try:
        while True:
            ecg_signal = read_ecg_signal()
            pred_class, probs = predict_ecg(ecg_signal)
            
            signal_flat = ecg_signal.flatten()
            hr = estimate_hr(signal_flat)
            
            print(f"Classe: {pred_class} | Probabilités: {probs} | HR: {hr} bpm")
            
            telemetry = {
                "classe": pred_class,
                "HR_bpm": hr,
                "prob_Normal": float(probs[0]),
                "prob_SVEB": float(probs[1]),
                "prob_VEB": float(probs[2]),
                "prob_Fusion": float(probs[3]),
                "prob_Unknown": float(probs[4])
            }
            client.publish('v1/devices/me/telemetry', json.dumps(telemetry))
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        GPIO.cleanup()
        print("Programme arrêté.")


