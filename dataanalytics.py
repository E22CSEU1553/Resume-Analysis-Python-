import streamlit as st
import pdfplumber
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import pandas as pd
import re


st.set_page_config(page_title="📄 Resume Analyzer with ATS Score", layout="wide")

st.title("📄 Resume Analysis Dashboard with ATS Optimization")
st.write("Upload a resume in PDF format to perform ATS score analysis and get suggestions for optimization.")


job_keywords = set(["Python", "Machine Learning", "Data Analysis", "SQL", "Communication", "Teamwork", "Leadership", "Problem-Solving", "Critical Thinking", "Java", "Project Management"])


uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    if text:
        
        st.subheader("Extracted Text")
        st.write(text)

        
        st.subheader("Text Statistics")
        words = text.split()
        word_count = len(words)
        unique_words = len(set(words))
        st.write(f"**Total Words:** {word_count}")
        st.write(f"**Unique Words:** {unique_words}")

        
        st.subheader("✅ ATS Score Analysis")
        resume_words = set([word.strip('.,!?').capitalize() for word in words])
        matched_keywords = resume_words.intersection(job_keywords)
        unmatched_keywords = job_keywords - matched_keywords

        ats_score = (len(matched_keywords) / len(job_keywords)) * 100
        st.write(f"**ATS Score:** {ats_score:.2f}%")
        st.write(f"**Matched Keywords:** {', '.join(matched_keywords) if matched_keywords else 'None'}")
        st.write(f"**Missing Keywords:** {', '.join(unmatched_keywords) if unmatched_keywords else 'None'}")

        
        if unmatched_keywords:
            st.subheader("💡 Suggestions for Improvement")
            st.write("Consider including the following keywords to optimize your resume:")
            for keyword in unmatched_keywords:
                st.write(f"- {keyword}")

        
        st.subheader("🔍 Highlighted Text with Matched Keywords")
        highlighted_text = text
        for keyword in matched_keywords:
            highlighted_text = re.sub(f'(?i)\\b{keyword}\\b', f'**:green[{keyword}]**', highlighted_text)
        st.markdown(highlighted_text, unsafe_allow_html=True)

        
        st.subheader("☁️ Word Cloud")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        
        st.subheader("📊 Most Common Words")
        word_freq = Counter(words)
        common_words = word_freq.most_common(10)
        words_df = pd.DataFrame(common_words, columns=['Word', 'Frequency'])
        fig, ax = plt.subplots()
        sns.barplot(x='Frequency', y='Word', data=words_df, ax=ax)
        st.pyplot(fig)
    else:
        st.error("No text could be extracted from the uploaded PDF.")