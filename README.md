# AI Study Assistant
It is an AI tool that allows you to upload PDFs via the user interface without making any code changes and ask questions based on them, as well as ask additional questions beyond the content of the PDFs.

## 🛠️ A platform where users:
* upload notes or PDFs
* ask questions
* get answers grounded in their own material

## How to use it:
Before using this, you need to paste your Gemini API key into the `.env` file; then, you can run the project on your system by executing `app.py` with the help of `streamlit run app.py` command.

## 📂 Project Structure
```text
├── Assest/           # Useful asset files and images
├── UI/               # Dashboard UI components and frontend files
├── app.py            # Main application entry point
├── ai_agent.py       # Core RAG system and AI agent implementation
└── requirements.txt  # Project dependencies