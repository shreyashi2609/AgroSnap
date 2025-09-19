"""A Streamlit app for extracting Image information using latest gemini-vision-pro API """
# Load the libraries

# from dotenv import load_dotenv
# load_dotenv()


import time
import streamlit as st
#import os
from PIL import Image
import google.generativeai as genai
import requests
import json


# Configure the Google API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Additional info on the input to generate_content method.

#     ### Input type flexibility

#     While the underlying API strictly expects a `list[glm.Content]` objects, this method
#     will convert the user input into the correct type. The hierarchy of types that can be
#     converted is below. Any of these objects can be passed as an equivalent `dict`.

#     * `Iterable[glm.Content]`
#     * `glm.Content`
#     * `Iterable[glm.Part]`
#     * `glm.Part`
#     * `str`, `Image`, or `glm.Blob`

#     In an `Iterable[glm.Content]` each `content` is a separate message.
#     But note that an `Iterable[glm.Part]` is taken as the parts of a single message.

# GEMINI's RESPONSE IS AMAZING
# Interpretation:
# This code snippet is likely passing three separate pieces of information to the generate_content method of the Gemini model:
# input_: This could be any valid input type accepted by glm.Content, such as a string, an image, or another glm.Content object.
# img[0]: This seems to be accessing the first element of a list or array named img. It's likely an image or some representation of visual data.
# prompt_input: This is likely a string containing a prompt or instruction for the model.
# By enclosing these elements in a list, you are essentially creating an Iterable[glm.Content] object, where each element in the list represents a separate piece of content for the model to process.
# Therefore, the model might be interpreting this input as:
# First message: input_ (content type depends on the actual data)
# Second message: img (likely an image)
# Third message: prompt_input (a text prompt)
# The model would then generate content based on this sequence of messages. The exact nature of the generated content would depend on the specific model and the provided inputs.
# Note: This is just one possible interpretation based on the limited information provided. The actual meaning and behavior might vary depending on the specific context and implementation of the model.
# If you can provide more details about the model and the types of the input variables, I can give you a more precise explanation.







# Function for generating the response
def get_gemini_content( prompt_input, img):
    # Instantiate Gemini model
    ## CHANGE model name : July 12 2024 : 
    #To avoid interruptions, we encourage switching to Gemini 1.5 Flash, our next-generation model that is faster and more cost-efficient with advanced vision understanding. Update your code to call 1.5 Flash:
    # Old
    # model = genai.GenerativeModel(name='gemini-pro-vision')
    # New
    # model = genai.GenerativeModel(name='gemini-1.5-flash’)
    # Please note this change does not affect the Gemini 1.0 Pro NLP model.

    model = genai.GenerativeModel('gemini-1.5-flash') # or gemini-pro
    response = model.generate_content([img, prompt_input])
    print("Print Generated content,",response)               
    print("Print candidates",response._result)
    return response.text

# Image function for getting data in bytes : Required by Gemini models
def input_img_bytes(uploaded_file):
    if uploaded_file is not None:
        image_data = {
        'mime_type': uploaded_file.type,
        'data': uploaded_file.getvalue()}
        return image_data
    else:
        raise FileNotFoundError("File is not Uploaded...")
    
    
 # For streaming data with streamlit : Words generate word by word
def stream_data_(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)

# Streamlit Page Configuration
st.set_page_config(page_title="AgroSnap", layout="wide")
st.title("AgroSnap 🤖")
st.text("Your AI-powered farming assistant")



uploaded_file = st.file_uploader("Choose a file to upload...", type = ['jpg','jpeg','png'])
st.markdown("**Note:** Do not upload confidential files.")
image = ""

if uploaded_file is not None:
    image =  Image.open(uploaded_file)


submit = st.button("Generate")

# The input task to perform
system_instruction = """
You are an expert in agriculture. Your task is to analyze an image of a crop and provide the following information in a JSON format:
- "crop_name": The name of the crop.
- "disease_pest": The name of the disease or pest affecting the crop.
- "treatment": A detailed treatment plan, including both organic and chemical solutions.

Your response must be a valid JSON object, with no extra text before or after the JSON.
"""


def get_mandi_prices(crop_name):
    """
    Fetches mandi prices using Government of India's Agmarknet API
    """
    # Get API key from data.gov.in
    api_key = st.secrets.get("DATA_GOV_IN_API_KEY")
    
    url = "https://www.data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi#api"
    
    params = {
        "api-key": api_key,
        "format": "json",
        "filters[commodity]": crop_name,
        "limit": 10,
        "offset": 0
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("records"):
            return data
        else:
            st.warning(f"No mandi price data found for {crop_name}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching mandi prices: {e}")
        return None
        
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error fetching mandi prices: {e}")
        st.error(f"Response content: {response.text if 'response' in locals() else 'No response'}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching mandi prices: {e}")
        return None


def translate_text(text, target_language):
    """
    Translates text to the target language using the Gemini API.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Translate the following text to {target_language}:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

TRANSLATIONS = {
    "Hindi": {
        "Gemini Response": "जेमिनी प्रतिक्रिया",
        "Mandi Prices": "मंडी की कीमतें",
        "Crop Analysis": "फसल विश्लेषण",
        "Select Language:": "भाषा चुनें:",
        "Disease/Pest:": "रोग/कीट:",
        "Treatment:": "उपचार:",
    },
    "Marathi": {
        "Gemini Response": "जेमिनी प्रतिसाद",
        "Mandi Prices": "मंडीच्या किमती",
        "Crop Analysis": "पीक विश्लेषण",
        "Select Language:": "भाषा निवडा:",
        "Disease/Pest:": "रोग/कीड:",
        "Treatment:": "उपचार:",
    }
}

# Initialize session state
# Initialize session state
if 'gemini_response_json' not in st.session_state:
    st.session_state.gemini_response_json = None
if 'translations' not in st.session_state:
    st.session_state.translations = {}

if submit:
    if uploaded_file is not None:
        image_data = input_img_bytes(uploaded_file)
        gemini_response = get_gemini_content(system_instruction, image_data)
        try:
            # Clean the response to remove markdown and parse JSON
            cleaned_response = gemini_response.replace("```json", "").replace("```", "").strip()
            st.session_state.gemini_response_json = json.loads(cleaned_response)
        except json.JSONDecodeError:
            st.error("Failed to parse the response from Gemini. The response was not valid JSON.")
            st.session_state.gemini_response_json = None
        st.session_state.translations = {}  # Clear old translations

if st.session_state.gemini_response_json:
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)
        language = st.radio(
            "Select Language:",
            ('English', 'Hindi', 'Marathi')
        )

    with col2:
        response_data = st.session_state.gemini_response_json
        if language == 'English':
            display_data = response_data
            gemini_header = "Gemini Response"
            mandi_header = "Mandi Prices"
            analysis_tab_title = "Crop Analysis"
            mandi_tab_title = "Mandi Prices"
            disease_pest_header = "Disease/Pest:"
            treatment_header = "Treatment:"
        else:
            if language not in st.session_state.translations:
                st.session_state.translations[language] = {
                    'disease_pest': translate_text(response_data.get('disease_pest', ''), language),
                    'treatment': translate_text(response_data.get('treatment', ''), language),
                }
            
            translated_data = st.session_state.translations[language]
            display_data = {
                "crop_name": response_data.get('crop_name'), # Crop name should not be translated
                "disease_pest": translated_data['disease_pest'],
                "treatment": translated_data['treatment']
            }
            gemini_header = TRANSLATIONS[language]["Gemini Response"]
            mandi_header = TRANSLATIONS[language]["Mandi Prices"]
            analysis_tab_title = TRANSLATIONS[language]["Crop Analysis"]
            mandi_tab_title = TRANSLATIONS[language]["Mandi Prices"]
            disease_pest_header = TRANSLATIONS[language]["Disease/Pest:"]
            treatment_header = TRANSLATIONS[language]["Treatment:"]

        tab1, tab2 = st.tabs([analysis_tab_title, mandi_tab_title])

        with tab1:
            st.subheader(gemini_header)
            st.markdown(f"**{disease_pest_header}** {display_data.get('disease_pest', 'N/A')}")
            st.markdown(f"**{treatment_header}**")
            st.write(display_data.get('treatment', 'N/A'))


        with tab2:
            st.subheader(mandi_header)
            crop_name = response_data.get('crop_name')
            if crop_name:
                mandi_prices = get_mandi_prices(crop_name)
                if mandi_prices:
                    st.write(mandi_prices)
            else:
                st.warning("Could not extract crop name from the response.")

elif submit:
    st.write("Please upload a file to start")
