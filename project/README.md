# Quantum News Agent

An AI-powered quantum computing news aggregator that automatically fetches, processes, and summarizes the latest quantum computing articles from MIT News.

## Features

- **RSS Feed Parsing**: Automatically fetches the latest quantum computing articles from MIT News RSS feed
- **Duplicate Prevention**: Smart deduplication ensures articles are not processed multiple times
- **AI Summarization**: Uses Google's Gemini AI to generate engaging 250-word summaries in plain English
- **Modern Web Interface**: Beautiful, responsive web UI to browse articles and summaries
- **Daily Automation**: Scheduled daily processing of new articles
- **Content Extraction**: Full article content extraction for comprehensive AI analysis

## System Components

### 1. Enhanced RSS Parser (`enhanced_rss_parser.py`)
- Fetches latest articles from MIT Quantum Computing RSS feed
- Extracts full article content using newspaper3k
- Stores articles with deduplication in SQLite database
- Schema includes: title, author, publish_date, article_link, content, ai_summary

### 2. Enhanced AI Agent (`enhanced_agent.py`)
- Integrates with Google Gemini 2.0 Flash model
- Generates 250-word summaries in accessible language
- Processes both new articles and backlog articles
- Handles content length limitations and error recovery

### 3. Enhanced Web Application (`enhanced_app.py`)
- Flask-based REST API
- Serves article data with statistics
- Modern responsive web interface
- Real-time article updates

### 4. Daily Processing System
- **`daily_runner.py`**: Main orchestrator for daily workflow
- **`scheduler.py`**: Scheduling system for automated execution
- Comprehensive logging and error handling

## Installation

1. **Clone and setup virtual environment**:
```bash
cd /home/liuyiwen/AI/AI\ Agent/quantum_news_agent
source .venv/bin/activate
```

2. **Install dependencies**:
```bash
pip install -r project/requirements.txt
```

3. **Set up Google AI API key**:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

## Usage

### Manual Testing

1. **Test RSS parsing and AI summarization**:
```bash
cd project/news_agent
python daily_runner.py
```

2. **Start the web application**:
```bash
python enhanced_app.py
```

3. **Access the web interface**:
Open `http://localhost:5000` in your browser

### Automated Daily Processing

1. **Start the scheduler**:
```bash
python scheduler.py
```

This will run daily processing at 8:00 AM every day.

### API Endpoints

- `GET /` - Main web interface
- `GET /api/articles` - Get all articles with summaries (JSON)
- `GET /api/stats` - Get article statistics (JSON)
- `GET /api/health` - Health check endpoint
- `GET /get_news` - Legacy endpoint for backward compatibility

## Database Schema

The system uses SQLite with the following schema:

```sql
CREATE TABLE quantum_news_rss (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    publish_date TEXT,
    article_link TEXT UNIQUE NOT NULL,
    content TEXT,
    ai_summary TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## Workflow

1. **Daily RSS Check**: System fetches the latest article from MIT's quantum computing RSS feed
2. **Deduplication**: Checks if the article already exists in the database
3. **Content Extraction**: If new, extracts full article content using newspaper3k
4. **AI Summarization**: Generates a 250-word engaging summary using Gemini AI
5. **Database Storage**: Saves article with metadata and AI summary
6. **Web Display**: Updated articles appear in the web interface immediately

## Configuration

### RSS Feed URL
Currently configured for MIT Quantum Computing News:
```
https://news.mit.edu/topic/mitquantum-computing-rss.xml
```

### AI Model Configuration
- Model: `gemini-2.0-flash`
- Summary length: 250 words
- Focus: Plain English, engaging content for general audiences

### Scheduling
- Default: Daily at 8:00 AM
- Configurable in `scheduler.py`

## Logging

The system maintains comprehensive logs:
- `quantum_news_daily.log` - Daily processing logs
- `quantum_news_scheduler.log` - Scheduler operation logs
- Console output for real-time monitoring

## File Structure

```
project/
├── news_agent/
│   ├── enhanced_rss_parser.py    # RSS feed processing
│   ├── enhanced_agent.py         # AI summarization
│   ├── enhanced_app.py           # Web application
│   ├── daily_runner.py           # Daily orchestrator
│   ├── scheduler.py              # Automated scheduling
│   └── templates/
│       └── enhanced_index.html   # Modern web interface
├── requirements.txt              # Dependencies
├── README.md                     # This file
└── quantum_news_rss.db          # SQLite database
```

## Error Handling

The system includes comprehensive error handling:
- Network failures during RSS fetching
- AI API rate limits and timeouts
- Database connection issues
- Content extraction failures
- Graceful degradation for partial failures

## Security Considerations

- API keys are stored in environment variables
- SQL injection prevention through parameterized queries
- XSS prevention in web interface
- Content sanitization for displayed text

## Contributing

1. Follow the existing code structure and patterns
2. Add comprehensive logging for new features
3. Update tests for any new functionality
4. Maintain backward compatibility with existing API endpoints

## License

This project is for educational and research purposes.