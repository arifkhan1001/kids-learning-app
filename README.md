# 🌟 Kids Learning Hub

A super fun, interactive AI-powered learning app designed specifically for kids (ages 5-8)! Built with Python, Streamlit, and the Google Gemini API.

## 🎮 Features

The fun never stops with these built-in learning adventures:

1. **📖 Vocabulary Builder:** Kids can type in any word they hear or see, and the AI will act like an encouraging teacher. It provides a simple definition, two synonyms, a fun example sentence, and a mini-challenge — all wrapped in emojis!
2. **🧩 Synonym Quiz:** A full 10-question multiple choice game where kids pick words that mean the same thing. 
   - **3 Difficulty Levels:** Easy 🐱, Medium 🦅, and Hard 🐯
   - **Personalised Feedback:** The app asks for the child's name and cheers them on when they win.
   - **🎉 Fun Celebrations:** Every correct answer triggers a rewarding full-screen animation (Balloons, Rockets, Snow bursts, Butterflies, and Raining Flowers!).
   - **Smart Memory:** The AI remembers which words were recently asked so it doesn't repeat the same words across quizzes!

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.9+ installed on your computer.
- A Google Gemini API Key (get one for free at [Google AI Studio](https://aistudio.google.com/)). 
  - *Note: You may need to set up a billing account in Google Cloud depending on your region to unlock the API quotas, but usage is generally covered by the massive free tier!*

### 2. Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/arifkhan1001/kids-learning-app.git
   cd kids-learning-app
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API Key:**
   Create a file named `.env` in the main folder and add your key:
   ```env
   GEMINI_API_KEY="your-api-key-here"
   ```

### 3. Start the App

Run the following command from the main directory:
```bash
streamlit run Home.py
```
Your browser will automatically open to `http://localhost:8501`.

## ☁️ How to Deploy Online (For Free)

You can share this app with family and friends for free using **Streamlit Community Cloud**!

1. Push your code to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **"New App"**.
4. Select your repository, and set the **Main file path** to `Home.py`.
5. Click **"Advanced Settings"** and paste your API key in the Secrets box:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
6. Click **Deploy!**

## 🛠️ Technology Stack
- **Frontend/Backend:** [Streamlit](https://streamlit.io/) (Python)
- **AI Engine:** Google Gemini (`gemini-2.5-flash`) via `langchain-google-genai`
- **Animations:** Custom HTML/JS injected via Streamlit Components

---
*Made with ❤️ for kids who love to learn!*
