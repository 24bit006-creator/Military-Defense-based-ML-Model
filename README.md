<div align="center">

#    VigilanteE-X
### Autonomous Multimodal Tactical Reconnaissance & Threat Verification Engine

[![Python Version](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Deep Learning](https://img.shields.io/badge/Vision-MobileNetV2%20(PyTorch)-EE4C2C.svg)](https://pytorch.org/)
[![NLP](https://img.shields.io/badge/NLP-TF--IDF%20%2B%20Logistic%20Regression-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<p align="center">
  <b>A software-only defence decision-support system cross-referencing visual sensor telemetry with intercepted field dispatches to identify hostile assets, prevent spoofing attacks, and automate tactical response protocols.</b>
</p>

</div>

---

##  Executive Summary

Modern perimeter defense networks and forward outposts are increasingly targeted by **asymmetric warfare tactics** and **communication spoofing**—where hostile combat assets mask their approach by broadcasting routine civilian or logistics clearance dispatches.

**Vigilante-X** is an edge-ready, multimodal intelligence verification engine designed to address this challenge. By coupling a pre-trained **MobileNetV2** Convolutional Neural Network with a **TF-IDF & Logistic Regression** NLP pipeline, the system verifies whether incoming optical imagery matches accompanying textual dispatches, flagging tactical deception in real time.

---

##  System Architecture

```
                      ┌──────────────────────────────────────────────┐
                      │          INCIDENT TELEMETRY INGEST           │
                      │  [ Optical Photo ]  +  [ Radio Dispatch ]    │
                      └──────────────┬──────────────────┬────────────┘
                                     │                  │
                    ┌────────────────▼───┐          ┌───▼────────────────┐
                    │   VISION MODULE    │          │    TEXT MODULE     │
                    │  (MobileNetV2 CNN) │          │ (TF-IDF + LogReg)  │
                    └────────────────┬───┘          └───┬────────────────┘
                                     │                  │
                                     ▼                  ▼
                              Detected Class      Intent Class
                           (Combat Tank / Jet)  (Hostile / Routine)
                                     │                  │
                                     └─────────┬────────┘
                                               │
                                               ▼
                         ┌─────────────────────────────────────────────┐
                         │          CROSS-VERIFICATION ENGINE          │
                         │  - Cross-checks visual class vs dispatch    │
                         │  - Detects deception / spoofing             │
                         │  - Computes composite threat index (0-100)  │
                         └─────────────────────┬───────────────────────┘
                                               │
                                               ▼
                         ┌─────────────────────────────────────────────┐
                         │      STREAMLIT TACTICAL OPERATOR HUD        │
                         │  - Dual-theme (Tactical Slate / Sky Blue)   │
                         │  - Composite risk gauge & visual metrics    │
                         │  - Automated Standard Operating Procedures  │
                         └─────────────────────────────────────────────┘
```

---

##  Core Technical Modules

### 1. Visual Reconnaissance Module (`vision_classifier.py`)
* **Architecture:** MobileNetV2 with pre-trained ImageNet feature extraction weights.
* **Pre-processing:** Bilinear resize ($256 \times 256$), center crop ($224 \times 224$), and tensor normalization ($\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$).
* **Tactical Mapping:** Softmax probabilities are mapped across defense categories:
  * `Combat Tank / Heavy Armor` (Hostile)
  * `Tactical Fighter Jet` (Hostile)
  * `Airborne Threat / Recon UAV` (Hostile)
  * `Civilian / Supply Transport` (Routine)

### 2. Tactical Intent NLP Module (`train_text_model.py`)
* **Architecture:** TF-IDF (Term Frequency-Inverse Document Frequency) Vectorizer + Logistic Regression Classifier.
* **Feature Extraction:** Sub-linear TF scaling with unigram and bigram ranges (`ngram_range=(1, 2)`) to capture tactical phrases (e.g., *"heavy armor"*, *"routine supply"*).
* **Optimization:** Class-balanced weighting with maximum iterations set to 1000 for convergence on sparse military vocabularies.

### 3. Decision Cross-Verification Engine (`decision_engine.py`)
* Compares classification labels and confidence values across both modalities.
* **Deception Rule:** If $\text{Visual}_{\text{hostile}} = \text{True}$ and $\text{Text}_{\text{hostile}} = \text{False}$, the system triggers an immediate **Tactical Deception / Spoofing Alert**.
* Generates a calibrated **Composite Threat Index** ($0 - 100$) and recommends specific operational protocols (e.g., QRF dispatch, checkpoint lockdowns).

---

##  Repository Structure

```text
Vigilante-X/
├── dataset/
│   └── dispatches.csv         # Labeled tactical radio communications dataset
├── sample_inputs/
│   └── sample_tank.png        # Sample synthetic reconnaissance asset
├── models/
│   └── text_threat_pipeline.pkl  # Trained NLP vectorizer & classifier artifact
├── app.py                     # Streamlit tactical command dashboard
├── decision_engine.py         # Multimodal correlation & deception logic
├── vision_classifier.py       # MobileNetV2 image inference pipeline
├── train_text_model.py        # Model training & evaluation script
├── requirements.txt           # Project dependencies
├── .gitignore                 # Version control exclusions
└── README.md                  # System documentation
```

---

##  Quickstart Guide

### Prerequisites
* Python 3.9, 3.10, or 3.11 installed.
* Standard terminal / command prompt.

### 1. Clone the Repository
```bash
git clone https://github.com/24bit006-creator/Vigilante-X.git
cd Vigilante-X
```

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Train the Text Intent Pipeline
```bash
python train_text_model.py
```
*Outputs evaluation metrics (Precision, Recall, F1-Score) and exports `models/text_threat_pipeline.pkl`.*

### 4. Launch the Tactical Operator Interface
```bash
python -m streamlit run app.py
```
The interface will automatically launch in your browser at `http://localhost:8501`.

---

##  Demonstration & Test Scenarios

| Scenario | Input Image | Sample Radio Dispatch | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **1. Confirmed Combat Advance** | Combat Tank / Fighter Jet | `"Unmarked heavy armored tank moving aggressively toward outpost bravo"` | **CRITICAL THREAT** (Score $\ge 75$)<br>Standard protocol: Scramble QRF and initiate perimeter lockdown. |
| **2. Tactical Deception / Spoofing** | Combat Tank | `"Routine supply convoy approaching main base gate for scheduled cargo drop"` | **SPOOFING WARNING**<br>Deception detected: Visual confirms combat asset while dispatch deceptively claims routine supplies. |
| **3. Verified Logistics Transit** | Supply Truck / Van | `"Authorized civil transport requesting entry for scheduled medical rations"` | **ROUTINE / ALL CLEAR** (Score $< 30$)<br>Standard protocol: Grant standard sector clearance and log entry. |

---

##  Tech Stack

* **Language:** Python
* **Computer Vision:** PyTorch, Torchvision, Pillow
* **Natural Language Processing:** Scikit-Learn (TF-IDF, Logistic Regression)
* **Data Processing:** Pandas, NumPy, Joblib
* **User Interface:** Streamlit (Custom CSS, Theme Formal and Simple)

