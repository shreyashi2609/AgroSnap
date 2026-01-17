# AgroSnap - AI-Powered Smart Farming Assistant 🌱

AgroSnap is an innovative, AI-driven agricultural assistant designed to empower farmers with advanced technology. By leveraging the power of **Google's Gemini Vision API** and **real-time government data**, AgroSnap provides instant crop analysis, disease detection, personalized treatment recommendations, and live market prices—all in the farmer's local language.

Our mission is to bridge the gap between technology and agriculture, helping farmers increase yield, reduce crop loss, and maximize profits.

---

## 🚀 Key Features

*   **🤖 AI Crop Analysis:** Upload photos of crops to detect diseases, pests, and nutrient deficiencies with high accuracy using Google Gemini Vision AI.
*   **💊 Smart Recommendations:** Get actionable advice on treatment, prevention, and optimal growing conditions.
*   **💰 Real-Time Market Prices:** Access live mandi prices (APMC) for various crops across different states and districts via Government of India APIs.
*   **🗣️ Multilingual Support:** Full support for **English, Hindi, Marathi, Telugu, and Tamil**, making it accessible to a diverse farming community.
*   **📄 PDF Reports:** Generate and download detailed analysis reports for offline reference.
*   **📊 Price Trends:** Visualize market trends with interactive charts and historical price comparisons.

---

## 🛠️ Tech Stack

*   **Frontend & Application Logic:** [Streamlit](https://streamlit.io/) (Python)
*   **AI Engine:** [Google Gemini Pro Vision](https://deepmind.google/technologies/gemini/)
*   **Backend API (Alternative):** [FastAPI](https://fastapi.tiangolo.com/) (Python) & [Express.js](https://expressjs.com/) (Node.js)
*   **Data Source:** [Data.gov.in](https://data.gov.in/) (Agmarknet API)
*   **Visualization:** Plotly
*   **Image Processing:** Pillow (PIL)

---

## 📂 Project Structure

```
AgroSnap/
├── backend/
│   ├── app.py           # Main Streamlit Application
│   ├── main.py          # FastAPI Backend Implementation
│   ├── server.js        # Node.js/Express Backend Implementation
│   ├── style.css        # Custom Styling
│   └── requirements.txt # Python Dependencies
├── .streamlit/          # Streamlit Configuration
├── package.json         # Node.js Dependencies
└── README.md            # Project Documentation
```

---

## ⚡ Getting Started

You can run AgroSnap using the **Streamlit** interface (recommended for the full experience) or deploy the backend APIs separately.

### Prerequisites

*   **Python 3.8+**
*   **Node.js** (optional, for the Express server)
*   **API Keys:**
    *   **Google Gemini API Key:** [Get it here](https://makersuite.google.com/app/apikey)
    *   **Data.gov.in API Key:** [Get it here](https://data.gov.in/)

### 1️⃣ Installation (Python/Streamlit)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/agrosnap.git
    cd agrosnap
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory (or inside `backend/`) and add your keys:
    ```env
    GOOGLE_API_KEY="your_google_api_key_here"
    DATA_GOV_IN_API_KEY="your_data_gov_api_key_here"
    ```

### 2️⃣ Running the Application

#### Option A: Streamlit App (Frontend + Backend)
This runs the full interactive dashboard.

```bash
streamlit run backend/app.py
```
The app will open in your browser at `http://localhost:8501`.

#### Option B: FastAPI Backend
If you want to use the Python backend API separately:

```bash
cd backend
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. Documentation at `/docs`.

#### Option C: Node.js Backend
If you prefer the Node.js implementation:

1.  Install dependencies:
    ```bash
    npm install
    ```
2.  Run the server:
    ```bash
    node backend/server.js
    ```
The server will run on port `3000`.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements, please feel free to:

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

<div align="center">
    <p>Made with ❤️</p>
</div>
