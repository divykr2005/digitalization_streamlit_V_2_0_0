import os
import pandas as pd
from pypdf import PdfReader
import re
import streamlit as st

# -------------------- KEYWORDS & WEIGHTS --------------------
keywords = {
    "Artificial Intelligence (AI) & Machine Learning (ML)": [
        "Artificial Intelligence", "Business Intelligence", "Image Understanding", "Investment Decision Aid System",
        "Intelligent Data Analysis", "Intelligent Robotics", "Machine Learning", "Deep Learning", "Semantic Search",
        "Biometrics", "Face Recognition", "Voice Recognition", "Identity Verification", "Autonomous Driving",
        "Natural Language Processing", "AI/ML", "Chatbots", "Credit Risk Assessment Models", "Robo-advisor", "Generative AI"
    ],
    "Blockchain Technology": [
        "Blockchain", "Digital Currency", "Cryptocurrency", "Crypto", "Distributed Computing",
        "Differential Privacy Technology", "Smart Financial Contracts", "NFT", "Web 3.0"
    ],
    "Cloud Computing & Infrastructure": [
        "Cloud Computing", "Cloud", "Cloud Technologies", "Streaming Computing", "Graph Computing",
        "In-Memory Computing", "Multi-party Secure Computing", "Brain-like Computing", "Green Computing",
        "Cognitive Computing", "Converged Architecture", "Billion-level Concurrency", "EB-level Storage",
        "APIs", "Digital Infrastructure"
    ],
    "Big Data & Analytics": [
        "Big Data", "Data Mining", "Text Mining", "Data Visualization", "Heterogeneous Data",
        "Credit Analytics", "Augmented Reality", "Mixed Reality", "Virtual Reality", "Transaction Monitoring"
    ],
    "Digital Technology Applications": [
        "Mobile Internet", "Industrial Internet", "Internet Healthcare", "E-commerce", "Mobile Payment",
        "Third-party Payment", "NFC Payment", "Smart Energy", "B2B", "B2C", "C2B", "C2C", "O2O", "Netlink",
        "Smart Wear", "Smart Agriculture", "Smart Transportation", "Smart Healthcare", "Smart Customer Service",
        "Smart Home", "Smart Investment", "Smart Cultural Tourism", "Smart Environmental Protection", "Smart Grid",
        "Smart Marketing", "Digital Marketing", "Unmanned Retail", "Internet Finance", "Digital Finance",
        "Fintech", "Quantitative Finance", "Open Banking", "Embedded Finance", "Peer-to-Peer", "Buy Now Pay Later",
        "Contactless Payments", "Request to Pay", "Payment Service Directive", "Neobank", "Mobile-first Banking",
        "Banking-as-a-Service", "Metaverse"
    ],
    "Cybersecurity & Compliance": [
        "Cyber Security", "Anti-Money Laundering", "Fraud Detection"
    ],
    "Digital Banking & Transformation": [
        "Digitization", "Digital Transformation", "Net Banking", "Internet Banking", "New-to-Digital Customers",
        "E-money", "Robotic Process Automation", "Internet of Things", "Digital Adoption", "Branch on the Move",
        "DBT", "Innovation", "Banking Technology"
    ]
}

default_weights = {
    "Artificial Intelligence (AI) & Machine Learning (ML)": 1,
    "Blockchain Technology": 1,
    "Cloud Computing & Infrastructure": 1,
    "Big Data & Analytics": 1,
    "Digital Technology Applications": 1,
    "Cybersecurity & Compliance": 1,
    "Digital Banking & Transformation": 1
}

# -------------------- FUNCTIONS --------------------
def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.lower()
    except Exception as e:
        return ""

def compute_digitization_score(text, keywords, weights, normalize=True, normalization_factor=1000):
    total_words = len(re.findall(r'\w+', text))
    category_details = {}
    total_score = 0

    for category, keyword_list in keywords.items():
        category_score = 0
        for keyword in keyword_list:
            count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text))
            category_score += count
        
        weighted_score = category_score * weights[category]
        
        if normalize and total_words > 0:
            normalized_score = (weighted_score / total_words) * normalization_factor
        else:
            normalized_score = weighted_score
            
        category_details[category] = {
            "raw_count": category_score,
            "weighted_score": weighted_score,
            "normalized_score": round(normalized_score, 2)
        }
        total_score += normalized_score

    return round(total_score, 2), category_details, total_words

# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="Digitization Score Calculator", layout="wide")
st.title("🏦 Bank Digitization Score Calculator")

# -------------------- SIDEBAR CONFIGURATION --------------------
st.sidebar.header("⚙️ Configuration")

# Normalization Toggle
st.sidebar.subheader("📊 Normalization Settings")
use_normalization = st.sidebar.checkbox("Enable Word Count Normalization", value=True, 
                                        help="When enabled, scores are normalized by total word count")

normalization_factor = 1000
if use_normalization:
    normalization_factor = st.sidebar.number_input(
        "Normalization Factor", 
        min_value=1, 
        max_value=10000, 
        value=1000,
        step=100,
        help="Multiplier for normalized scores (default: 1000)"
    )

# Custom Weights Section
st.sidebar.subheader("⚖️ Category Weights")
use_custom_weights = st.sidebar.checkbox("Use Custom Weights", value=False,
                                         help="Enable to set custom weights for each category")

if use_custom_weights:
    st.sidebar.info("Adjust weights for each category below:")
    custom_weights = {}
    for category in keywords.keys():
        short_name = category.split("(")[0].strip() if "(" in category else category
        custom_weights[category] = st.sidebar.number_input(
            f"{short_name}", 
            min_value=0.0, 
            max_value=10.0, 
            value=float(default_weights[category]),
            step=0.1,
            key=f"weight_{category}"
        )
    weights = custom_weights
else:
    weights = default_weights
    st.sidebar.success("Using default weights (all = 1.0)")

# Display current configuration
st.sidebar.markdown("---")
st.sidebar.subheader("📋 Current Settings")
st.sidebar.write(f"**Normalization:** {'Enabled' if use_normalization else 'Disabled'}")
if use_normalization:
    st.sidebar.write(f"**Factor:** {normalization_factor}")
st.sidebar.write(f"**Custom Weights:** {'Yes' if use_custom_weights else 'No'}")

# -------------------- FILE UPLOAD --------------------
uploaded_files = st.file_uploader("Upload PDF Reports", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    results = []
    st.info(f"Found {len(uploaded_files)} PDF file(s). Processing...")
    progress_bar = st.progress(0)
    log = st.empty()

    for i, pdf_file in enumerate(uploaded_files):
        filename = pdf_file.name
        log.markdown(f"📄 **Processing:** `{filename}`")

        text = extract_text_from_pdf(pdf_file)

        if text:
            filename_parts = os.path.splitext(filename)[0].split("_")
            bank_name = filename_parts[0]

            fy = "Unknown"
            for part in filename_parts:
                if "FY" in part or re.search(r'(20\d{2})[-_](\d{2,4})', part):
                    fy = part
                    if fy.startswith("FY"):
                        fy = fy[2:]
                    break

            total_score, category_scores, word_count = compute_digitization_score(
                text, keywords, weights, use_normalization, normalization_factor
            )
            
            # Create a result dictionary with bank name, FY, and total score
            result = {
                "FY": fy, 
                "Name of Bank": bank_name, 
                "Digitization Score": total_score,
                "Total Words": word_count
            }
            
            # Add individual category scores
            for category, details in category_scores.items():
                short_name = category.split("(")[0].strip() if "(" in category else category
                result[f"{short_name} Score"] = details["normalized_score"]
                
            results.append(result)
            st.success(f"✅ `{bank_name}` ({fy}) → Score: **{total_score}** | Words: **{word_count:,}**")
        else:
            st.error(f"❌ Failed to extract from: `{filename}`")

        progress_bar.progress((i + 1) / len(uploaded_files))

    # Show Results
    if results:
        df = pd.DataFrame(results)
        st.markdown("### 📊 Final Results")
        
        # Reorder columns to group total score and individual category scores
        cols = ["FY", "Name of Bank", "Digitization Score", "Total Words"]
        category_cols = [col for col in df.columns if col not in cols]
        df = df[cols + sorted(category_cols)]
        
        st.dataframe(df, use_container_width=True)

        # Add visualization of category scores
        st.markdown("### 📈 Category Score Breakdown")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if len(df) > 0:
                selected_bank = st.selectbox("Select a bank to view detailed scores:", df["Name of Bank"].unique())
        
        with col2:
            if len(df) > 0:
                bank_data = df[df["Name of Bank"] == selected_bank].iloc[0]
                st.metric("Total Digitization Score", f"{bank_data['Digitization Score']:.2f}")
                st.metric("Total Words", f"{bank_data['Total Words']:,}")
        
        if len(df) > 0:
            # Extract category scores for visualization
            category_scores_viz = {col.replace(" Score", ""): bank_data[col] 
                              for col in bank_data.index if " Score" in col and col != "Digitization Score"}
            
            # Create a bar chart
            chart_data = pd.DataFrame({
                "Category": list(category_scores_viz.keys()),
                "Score": list(category_scores_viz.values())
            })
            
            st.bar_chart(chart_data.set_index("Category"), use_container_width=True)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Results as CSV", 
            data=csv, 
            file_name="Digitization_Scores.csv", 
            mime="text/csv"
        )
        
        # Show applied settings in results
        st.markdown("---")
        st.markdown("### ⚙️ Settings Used for This Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Normalization:** {'Enabled' if use_normalization else 'Disabled'}")
            if use_normalization:
                st.write(f"**Normalization Factor:** {normalization_factor}")
        with col2:
            st.write(f"**Custom Weights:** {'Yes' if use_custom_weights else 'No'}")
            if use_custom_weights:
                with st.expander("View Weight Details"):
                    for cat, weight in weights.items():
                        short_name = cat.split("(")[0].strip() if "(" in cat else cat
                        st.write(f"- {short_name}: {weight}")

else:
    st.info("Please upload one or more PDF files to begin analysis.")
    
    # Show instruction guide
    with st.expander("📖 How to Use"):
        st.markdown("""
        ### Instructions:
        1. **Configure Settings** (Optional):
           - Use the sidebar to enable/disable word count normalization
           - Adjust the normalization factor if needed
           - Enable custom weights to modify category importance
        
        2. **Upload PDF Files**:
           - Click the upload button above
           - Select one or more bank annual report PDFs
           - File names should follow format: `BankName_FY20XX.pdf`
        
        3. **Review Results**:
           - View digitization scores for each bank
           - Compare category-wise scores
           - Download results as CSV
        
        ### About Normalization:
        - **Enabled**: Scores are normalized per 1000 words (accounts for document length)
        - **Disabled**: Raw weighted keyword counts are used
        
        ### About Custom Weights:
        - Default weight for all categories is 1.0
        - Increase weight to prioritize certain categories
        - Set weight to 0 to exclude a category from scoring
        """)
