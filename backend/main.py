from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import requests
import json
import os
from dotenv import load_dotenv

app = FastAPI(title="AgroSnap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], # Add your React app's origin here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables from .env file
load_dotenv()

# Configure the Google API key
# It's better to get it from environment variables for a backend service
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    # In a real app, you might have a fallback or a more robust configuration system
    print("Warning: GOOGLE_API_KEY environment variable not set.")
    # For now, I'll let it proceed, but genai.configure will likely fail if the key is truly needed immediately.
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize FastAPI app
app = FastAPI(title="AgroSnap API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity, can be restricted in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# System instruction for Gemini
system_instruction = """
You are an expert in agriculture. Your task is to analyze an image of a crop and provide the following information in a JSON format:
- "crop_name": The name of the crop.
- "disease_pest": The name of the disease or pest affecting the crop.
- "treatment": A detailed treatment plan, including both organic and chemical solutions.

Your response must be a valid JSON object, with no extra text before or after the JSON.
"""

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyzes an uploaded crop image.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Read image data
    image_data = {
        'mime_type': file.content_type,
        'data': await file.read()
    }

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([image_data, system_instruction])
        
        # Clean the response to remove markdown and parse JSON
        cleaned_response = response.text.replace("```json", "").replace("```", "").strip()
        response_json = json.loads(cleaned_response)
        return response_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during Gemini API call: {e}")


@app.post("/translate")
async def translate_text_endpoint(text: str = Form(...), target_language: str = Form(...)):
    """
    Translates text to the target language.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Translate the following text to {target_language}:\n\n{text}"
        response = model.generate_content(prompt)
        return {"translation": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during translation: {e}")

@app.get("/mandi-prices/{crop_name}")
async def get_mandi_prices(crop_name: str):
    """
    Fetches mandi prices for a given crop.
    """
    api_key = os.getenv("DATA_GOV_IN_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="DATA_GOV_IN_API_KEY not configured")

    # This is a more direct API endpoint for the data
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    params = {
        "api-key": api_key,
        "format": "json",
        "filters[commodity]": crop_name,
        "limit": 10,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("records"):
            return data
        else:
            return {"message": f"No mandi price data found for {crop_name}"}
            
    except requests.exceptions.HTTPError as e:
        # It's helpful to return the actual error from the external API if possible
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Error fetching mandi prices: {e.response.text}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Service Unavailable: Error fetching mandi prices: {e}")

# To run this app:
# 1. Create a .env file in the backend directory with your API keys:
#    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
#    DATA_GOV_IN_API_KEY="YOUR_DATA_GOV_IN_API_KEY"
# 2. Install dependencies: pip install -r requirements.txt
# 3. Run the server: uvicorn main:app --reload
