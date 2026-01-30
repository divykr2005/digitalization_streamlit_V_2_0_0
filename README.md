# Bank Digitization Score Calculator

A Streamlit web application that analyzes bank annual reports (PDFs) and calculates digitization scores based on keyword analysis across multiple technology categories.

## Features

- 📄 PDF text extraction and analysis
- 🔢 Customizable scoring system with category weights
- 📊 Word count normalization toggle
- 📈 Interactive visualizations
- 💾 CSV export functionality
- ⚙️ Configurable normalization factors

## Technology Categories

The app analyzes the following categories:
1. Artificial Intelligence (AI) & Machine Learning (ML)
2. Blockchain Technology
3. Cloud Computing & Infrastructure
4. Big Data & Analytics
5. Digital Technology Applications
6. Cybersecurity & Compliance
7. Digital Banking & Transformation

## Deployment Instructions

### Step 1: Prepare Your GitHub Repository

1. Create a new repository on GitHub
2. Upload these files:
   - `digitization_score_calculator.py` (main app file)
   - `requirements.txt` (dependencies)
   - `README.md` (this file)

### Step 2: Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch, and main file
5. Click "Deploy"

## Local Development

To run locally:

```bash
pip install -r requirements.txt
streamlit run digitization_score_calculator.py
```

## Usage

1. Configure settings in the sidebar (optional)
2. Upload one or more PDF annual reports
3. Review the calculated digitization scores
4. Download results as CSV

## File Naming Convention

For best results, name your PDF files as: `BankName_FYXXXX.pdf`

Example: `HDFC_FY2023.pdf`

## License

MIT License
