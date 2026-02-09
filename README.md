---
title: Cocoa Intel AI
emoji: 🍫
colorFrom: yellow
colorTo: gray
sdk: streamlit
sdk_version: 1.31.0
app_file: app.py
pinned: false
---

# 🍫 Cocoa Strategic Intelligence
**Advanced Market Monitoring & AI Arbitrage Analysis Platform**

> 🚀 **Live Demo:** [Access Cocoa Intel AI](https://huggingface.co/spaces/vpozza/Cocoa-Intel-AI)

A professional-grade market intelligence platform developed for strategic analysis within the cocoa sector. The system integrates real-time data from the New York Stock Exchange (ICE) and the Brazilian physical market, leveraging Generative AI to provide deep insights into arbitrage, price parities, and global trends.

## 🚀 Key Features
- **Real-Time Monitoring:** Direct integration with NY Cocoa Futures (USD/t).
- **Physical Market Intelligence:** Automated data scraping for Bahia physical prices (R$/@).
- **Parity Intelligence:** Automated conversion based on live exchange rates (USD/BRL).
- **Historical Performance:** Interactive 36-month charts with peak (max) and bottom (min) indicators.
- **AI Strategic Analyst:** Specialized Commodity AI engine for market forecasts.

## 🛠️ Tech Stack
- **Python** | **Streamlit** | **Google Gemini API** | **Yahoo Finance** | **BeautifulSoup4**

## ⚙️ Local Installation & Setup
Follow these steps to run the platform on your local machine:

### 1. Clone the repository
```bash
git clone [https://github.com/vitorpozza/Cocoa-Intel-AI.git](https://github.com/vitorpozza/Cocoa-Intel-AI.git)
cd cocoa-intel-ai
```
### 2. Install dependencies
Make sure you have Python installed, then run:
```Bash
pip install -r requirements.txt
```
### 3. Configure Gemini API Key
To use the AI Analyst, you need a Google AI API Key.

   -*Get your key at: Google AI Studio

   -*For Local Run: Create a .env file or set an environment variable:
```Bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your_key_here"
```
```Bash
# Ubuntu Linux
export GEMINI_API_KEY="your_key_here"
```
### 4. Run the App
```Bash
streamlit run app.py
```
## 📊 Project Structure
   app.py: Main application logic.

   requirements.txt: List of required libraries.

   README.md: Documentation and Space metadata.

*Developed by Vitor Pozza Market Intelligence Lead