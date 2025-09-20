const express = require('express');
const cors = require('cors');
const axios = require('axios');
const multer = require('multer');
const FormData = require('form-data');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.static('public')); // Serve your HTML file from public folder

// Google Gemini API integration
app.post('/api/analyze', async (req, res) => {
  try {
    const { image, language } = req.body;
    
    // Call Google Gemini API with your GOOGLE_API_KEY
    const response = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${process.env.GOOGLE_API_KEY}`,
      {
        contents: [{
          parts: [{
            text: `Analyze this crop image and provide detailed information about the crop type, health, diseases, and recommendations. Use ${language} for the response.`
          }, {
            inline_data: {
              mime_type: "image/jpeg",
              data: image
            }
          }]
        }]
      }
    );

    // Process the response and extract relevant information
    const analysisResult = processGeminiResponse(response.data);
    res.json(analysisResult);
  } catch (error) {
    console.error('Error calling Gemini API:', error);
    res.status(500).json({ error: 'Failed to analyze image' });
  }
});

// Data.gov.in API integration
app.get('/api/market-prices', async (req, res) => {
  try {
    const { crop } = req.query;
    
    // Call Data.gov.in API with your DATA_GOV_IN_API_KEY
    const response = await axios.get(
      `https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070`,
      {
        params: {
          'api-key': process.env.DATA_GOV_IN_API_KEY,
          'format': 'json',
          'filters[commodity]': crop,
          'limit': 10
        }
      }
    );

    res.json(response.data);
  } catch (error) {
    console.error('Error calling Data.gov.in API:', error);
    res.status(500).json({ error: 'Failed to fetch market data' });
  }
});

function processGeminiResponse(geminiData) {
  // Process the Gemini API response into your application's format
  // This will depend on the actual structure of Gemini's response
  return {
    crop: "Identified Crop",
    variety: "Crop Variety",
    health: "Good",
    issues: [],
    recommendations: [],
    growingConditions: {},
    harvestInfo: {}
  };
}

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});