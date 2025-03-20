# WebDataLooter

A powerful web scraping and content analysis tool that combines Selenium, BeautifulSoup, and Ollama AI to extract and analyze web content intelligently.

## 🌟 Features

- **Smart Web Scraping**: Uses Selenium with anti-detection measures
- **Content Extraction**: Clean and structured extraction of web content
- **AI-Powered Analysis**: Leverages Ollama's LLM for intelligent content parsing
- **User-Friendly Interface**: Built with Streamlit for easy interaction
- **Data Export**: Export results in CSV format
- **Robust Error Handling**: Built-in retry mechanisms and error recovery

## 🛠️ Technologies Used

- Python 3.x
- Selenium WebDriver
- BeautifulSoup4
- Ollama (LLM)
- Streamlit
- LangChain
- Pandas

## 🚀 Getting Started

### Prerequisites

- Python 3.x installed
- Chrome browser installed
- ChromeDriver matching your Chrome version
- Ollama installed and running locally

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Web-Scraper.git
cd AI-Web-Scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `sample.env` to `.env`
   - Configure your environment variables

### Usage

1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Open your browser and navigate to the provided local URL (typically http://localhost:8501)

3. Enter a website URL and click "Scrape Website"

4. Once scraping is complete, you can:
   - View the scraped content
   - Ask questions about the content
   - Export results as CSV

## 🔧 Configuration

The scraper includes several configurable options:
- User agent rotation
- Retry mechanisms
- Content chunking size
- AI model selection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## ⚠️ Disclaimer

Please ensure you have permission to scrape websites and comply with their terms of service and robots.txt files.
