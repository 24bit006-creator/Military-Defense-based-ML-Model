# Multimodal Tactical Reconnaissance & Threat Verification System

An advanced, software-only defence decision support system combining:
1. **Visual Reconnaissance Classifier**: MobileNetV2 pre-trained deep learning feature extractor detecting military assets (tanks, fighter jets, transport vehicles).
2. **Tactical Dispatch Classifier**: TF-IDF + Logistic Regression NLP model categorizing dispatches into routine vs hostile.
3. **Cross-Verification Decision Engine**: Detects deception (e.g. enemy combat armor disguised with a false routine clearance message).
4. **Interactive Tactical UI**: Streamlit dashboard with incident evaluation and a tactical query assistant.

## Quickstart

1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

2. Train the text dispatch model:
   ```bash
   python train_text_model.py
   ```

3. Launch the Tactical Dashboard:
   ```bash
   python -m streamlit run app.py
   ```
