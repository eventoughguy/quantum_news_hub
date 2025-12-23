# Quantum News Hub

An AI-powered web application that aggregates and summarizes quantum computing news with an interactive supply chain ontology visualization.

## Features

- **RSS News Aggregation**: Automatically fetches quantum computing news from RSS feeds
- **AI-Powered Summaries**: Uses Google's Gemini AI to generate 250-word summaries
- **Interactive Ontology Visualization**: D3.js-powered network graph of quantum supply chain
- **Real-time Updates**: Displays the latest quantum computing articles with summaries
- **Clean Web Interface**: Modern, responsive design for easy reading

## Deployment

### Environment Variables

Set the following environment variable in your deployment platform:

- `GOOGLE_API_KEY`: Your Google API key for Gemini AI access

### Deploy to Render

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service from your forked repository
4. Set the environment variable `GOOGLE_API_KEY` in the Render dashboard
5. Deploy!

### Deploy to Railway

1. Fork this repository
2. Connect your GitHub account to Railway
3. Create a new project from your forked repository
4. Set the environment variable `GOOGLE_API_KEY` in Railway
5. Deploy!

### Deploy to Heroku

1. Fork this repository
2. Create a new Heroku app
3. Connect to your forked GitHub repository
4. Set the environment variable `GOOGLE_API_KEY` in Heroku settings
5. Deploy!

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r project/requirements.txt`
5. Set your Google API key in `.env` file
6. Run: `cd project/news_agent && python enhanced_app.py`

## Architecture

- **Backend**: Flask web framework
- **Database**: SQLite for article storage
- **AI Integration**: Google Gemini API for content summarization
- **Ontology**: RDF/OWL with RDFLib for supply chain modeling
- **Frontend**: HTML/CSS/JavaScript with D3.js for visualizations

## API Endpoints

- `GET /api/articles` - Get all articles with summaries
- `GET /api/stats` - Get article statistics
- `GET /api/health` - Health check
- `GET /api/ontology/graph` - Get ontology visualization data
- `GET /api/ontology/node/<id>` - Get detailed node information