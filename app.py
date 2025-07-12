import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from collections import Counter
import io
import base64

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    with st.spinner("Downloading required language data..."):
        nltk.download('punkt')
        nltk.download('punkt_tab')
        nltk.download('stopwords')

# Set page config
st.set_page_config(
    page_title="Survey Comment Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .step-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def clean_text(text):
    """Clean and preprocess text data"""
    if pd.isna(text):
        return ""
    
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def remove_stopwords(text, custom_stopwords=None):
    """Remove stopwords from text"""
    if not text:
        return ""
    
    stop_words = set(stopwords.words('english'))
    if custom_stopwords:
        stop_words.update(custom_stopwords)
    
    # Tokenize and remove stopwords
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words and len(word) > 2]
    
    return ' '.join(filtered_text)

def calculate_clustering_metrics(X, max_clusters=10):
    """Calculate elbow and silhouette scores for different numbers of clusters"""
    if len(X) < 2:
        return [], []
    
    max_clusters = min(max_clusters, len(X) - 1)
    K_range = range(2, max_clusters + 1)
    
    distortions = []
    silhouette_scores = []
    
    for k in K_range:
        try:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            distortions.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X, kmeans.labels_))
        except Exception as e:
            st.error(f"Error calculating metrics for k={k}: {str(e)}")
            break
    
    return K_range[:len(distortions)], distortions, silhouette_scores

def plot_clustering_analysis(K_range, distortions, silhouette_scores):
    """Create interactive plots for elbow and silhouette analysis"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Elbow Method', 'Silhouette Analysis'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Elbow plot
    fig.add_trace(
        go.Scatter(x=list(K_range), y=distortions, mode='lines+markers',
                  name='Distortion', line=dict(color='blue')),
        row=1, col=1
    )
    
    # Silhouette plot
    fig.add_trace(
        go.Scatter(x=list(K_range), y=silhouette_scores, mode='lines+markers',
                  name='Silhouette Score', line=dict(color='red')),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=True)
    fig.update_xaxes(title_text="Number of Clusters", row=1, col=1)
    fig.update_xaxes(title_text="Number of Clusters", row=1, col=2)
    fig.update_yaxes(title_text="Distortion", row=1, col=1)
    fig.update_yaxes(title_text="Silhouette Score", row=1, col=2)
    
    return fig

def extract_themes(texts, n_themes=5):
    """Extract common themes from a list of texts"""
    if not texts:
        return []
    
    # Combine all texts
    combined_text = ' '.join(texts)
    
    # Vectorize to find most common terms
    vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform([combined_text])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        # Get top themes
        top_indices = np.argsort(tfidf_scores)[-n_themes:][::-1]
        themes = [feature_names[i] for i in top_indices if tfidf_scores[i] > 0]
        
        return themes
    except Exception as e:
        st.error(f"Error extracting themes: {str(e)}")
        return []

def summarize_cluster(texts, cluster_id):
    """Create a summary of cluster texts"""
    if not texts:
        return "No comments in this cluster", [], "Empty Cluster"
    
    # Simple summarization approach
    # In a production environment, you might want to use a proper summarization model
    
    # Count most common words for summary
    all_words = []
    for text in texts:
        words = word_tokenize(text.lower())
        all_words.extend([word for word in words if len(word) > 3])
    
    if not all_words:
        return "No meaningful content found", [], f"Cluster {cluster_id + 1}"
    
    word_freq = Counter(all_words)
    top_words = [word for word, count in word_freq.most_common(10)]
    
    # Generate summary
    summary = f"This cluster contains {len(texts)} comments that frequently mention: {', '.join(top_words[:5])}. "
    
    # Extract themes
    themes = extract_themes(texts, n_themes=3)
    
    # Generate headline
    if themes:
        headline = f"Comments about {themes[0].title()}"
    else:
        headline = f"Cluster {cluster_id + 1} - {top_words[0].title()} Related"
    
    return summary, themes, headline

def main():
    st.markdown('<div class="main-header">📊 Survey Comment Analyzer</div>', unsafe_allow_html=True)
    st.markdown("**Analyze survey comments, discover themes, and summarize clusters automatically**")
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'processed_texts' not in st.session_state:
        st.session_state.processed_texts = None
    if 'tfidf_matrix' not in st.session_state:
        st.session_state.tfidf_matrix = None
    if 'clustering_results' not in st.session_state:
        st.session_state.clustering_results = None
    
    # Sidebar for progress tracking
    st.sidebar.markdown("### Progress")
    steps = [
        "1️⃣ Upload Data",
        "2️⃣ Select Column",
        "3️⃣ Process Text",
        "4️⃣ Analyze Clusters",
        "5️⃣ Select Clusters",
        "6️⃣ Generate Summary"
    ]
    
    for i, step in enumerate(steps, 1):
        if i <= st.session_state.step:
            st.sidebar.success(step)
        else:
            st.sidebar.info(step)
    
    # Step 1: File Upload
    if st.session_state.step >= 1:
        st.markdown('<div class="step-header">Step 1: Upload Your Data</div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a CSV or XLSX file",
            type=['csv', 'xlsx'],
            help="Upload a file containing survey comments or text data to analyze"
        )
        
        if uploaded_file is not None:
            try:
                # Load data
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.session_state.df = df
                st.markdown('<div class="success-box">✅ File uploaded successfully!</div>', unsafe_allow_html=True)
                
                # Show data preview
                st.subheader("Data Preview")
                st.dataframe(df.head())
                
                st.info(f"**Dataset Info:** {len(df)} rows × {len(df.columns)} columns")
                
                if st.session_state.step == 1:
                    st.session_state.step = 2
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
    
    # Step 2: Column Selection
    if st.session_state.step >= 2 and st.session_state.df is not None:
        st.markdown('<div class="step-header">Step 2: Select Text Column</div>', unsafe_allow_html=True)
        
        text_columns = st.session_state.df.select_dtypes(include=['object']).columns.tolist()
        
        if text_columns:
            selected_column = st.selectbox(
                "Select the column containing comments/text to analyze:",
                text_columns,
                help="Choose the column that contains the survey comments or text data"
            )
            
            if st.button("Confirm Column Selection"):
                st.session_state.selected_column = selected_column
                st.session_state.step = 3
                st.rerun()
        else:
            st.error("No text columns found in the dataset. Please upload a file with text data.")
    
    # Step 3: Text Processing
    if st.session_state.step >= 3 and hasattr(st.session_state, 'selected_column'):
        st.markdown('<div class="step-header">Step 3: Process Text Data</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Processing Options")
            
            # Custom stopwords
            custom_stopwords = st.text_area(
                "Additional stopwords (comma-separated):",
                help="Add domain-specific words to remove (e.g., 'survey, questionnaire, form')"
            )
            
            min_length = st.slider("Minimum comment length:", 1, 100, 10)
        
        with col2:
            st.subheader("Text Sample")
            sample_texts = st.session_state.df[st.session_state.selected_column].dropna().head(3)
            for i, text in enumerate(sample_texts):
                st.text_area(f"Sample {i+1}:", value=str(text)[:200] + "...", height=100, disabled=True)
        
        if st.button("Process Text Data"):
            with st.spinner("Processing text data..."):
                # Get text data
                df = st.session_state.df
                texts = df[st.session_state.selected_column].dropna().tolist()
                
                # Filter by minimum length
                texts = [text for text in texts if len(str(text)) >= min_length]
                
                if len(texts) < 2:
                    st.error("Not enough text data after filtering. Please adjust your minimum length or check your data.")
                    return
                
                # Process stopwords
                additional_stopwords = []
                if custom_stopwords:
                    additional_stopwords = [word.strip() for word in custom_stopwords.split(',')]
                
                # Clean and process texts
                processed_texts = []
                for text in texts:
                    cleaned = clean_text(text)
                    no_stopwords = remove_stopwords(cleaned, additional_stopwords)
                    if no_stopwords:  # Only keep non-empty texts
                        processed_texts.append(no_stopwords)
                
                if len(processed_texts) < 2:
                    st.error("Not enough processed text data. Please check your data or adjust stopword settings.")
                    return
                
                # Vectorize text
                vectorizer = TfidfVectorizer(max_features=1000, min_df=2, max_df=0.8)
                tfidf_matrix = vectorizer.fit_transform(processed_texts)
                
                # Store results
                st.session_state.processed_texts = processed_texts
                st.session_state.original_texts = texts
                st.session_state.tfidf_matrix = tfidf_matrix
                st.session_state.vectorizer = vectorizer
                
                st.success(f"✅ Processed {len(processed_texts)} comments successfully!")
                st.session_state.step = 4
                st.rerun()
    
    # Step 4: Clustering Analysis
    if st.session_state.step >= 4 and st.session_state.tfidf_matrix is not None:
        st.markdown('<div class="step-header">Step 4: Analyze Optimal Number of Clusters</div>', unsafe_allow_html=True)
        
        if st.session_state.clustering_results is None:
            with st.spinner("Calculating clustering metrics..."):
                max_clusters = min(15, len(st.session_state.processed_texts) // 2)
                K_range, distortions, silhouette_scores = calculate_clustering_metrics(
                    st.session_state.tfidf_matrix, max_clusters
                )
                
                st.session_state.clustering_results = {
                    'K_range': K_range,
                    'distortions': distortions,
                    'silhouette_scores': silhouette_scores
                }
        
        # Plot results
        if st.session_state.clustering_results['K_range']:
            fig = plot_clustering_analysis(
                st.session_state.clustering_results['K_range'],
                st.session_state.clustering_results['distortions'],
                st.session_state.clustering_results['silhouette_scores']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            silhouette_scores = st.session_state.clustering_results['silhouette_scores']
            K_range = st.session_state.clustering_results['K_range']
            
            if silhouette_scores:
                best_k = K_range[np.argmax(silhouette_scores)]
                st.info(f"**Recommendation:** Based on silhouette analysis, {best_k} clusters might work well.")
            
            st.session_state.step = 5
        else:
            st.error("Unable to calculate clustering metrics. Please check your data.")
    
    # Step 5: Select Number of Clusters
    if st.session_state.step >= 5 and st.session_state.clustering_results is not None:
        st.markdown('<div class="step-header">Step 5: Select Number of Clusters</div>', unsafe_allow_html=True)
        
        K_range = st.session_state.clustering_results['K_range']
        
        if K_range:
            n_clusters = st.slider(
                "Select number of clusters:",
                min_value=min(K_range),
                max_value=max(K_range),
                value=min(K_range) if K_range else 2,
                help="Choose the number of clusters based on the analysis above"
            )
            
            if st.button("Apply Clustering"):
                with st.spinner("Applying clustering..."):
                    # Perform clustering
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                    cluster_labels = kmeans.fit_predict(st.session_state.tfidf_matrix)
                    
                    # Store results
                    st.session_state.cluster_labels = cluster_labels
                    st.session_state.n_clusters = n_clusters
                    st.session_state.kmeans = kmeans
                    
                    st.success(f"✅ Successfully created {n_clusters} clusters!")
                    st.session_state.step = 6
                    st.rerun()
    
    # Step 6: Generate Summaries
    if st.session_state.step >= 6 and hasattr(st.session_state, 'cluster_labels'):
        st.markdown('<div class="step-header">Step 6: Cluster Summaries and Themes</div>', unsafe_allow_html=True)
        
        if st.button("Generate Cluster Summaries"):
            with st.spinner("Generating summaries and extracting themes..."):
                # Group texts by cluster
                cluster_texts = {}
                for i, label in enumerate(st.session_state.cluster_labels):
                    if label not in cluster_texts:
                        cluster_texts[label] = []
                    cluster_texts[label].append(st.session_state.original_texts[i])
                
                # Generate summaries
                summary_results = []
                for cluster_id in sorted(cluster_texts.keys()):
                    texts = cluster_texts[cluster_id]
                    summary, themes, headline = summarize_cluster(texts, cluster_id)
                    
                    summary_results.append({
                        'Cluster': f"Cluster {cluster_id + 1}",
                        'Headline': headline,
                        'Count': len(texts),
                        'Summary': summary,
                        'Themes': ', '.join(themes) if themes else 'No themes identified',
                        'Sample_Comments': ' | '.join(texts[:3])  # First 3 comments as examples
                    })
                
                st.session_state.summary_results = summary_results
        
        # Display results
        if hasattr(st.session_state, 'summary_results'):
            st.subheader("Cluster Analysis Results")
            
            # Display each cluster
            for result in st.session_state.summary_results:
                with st.expander(f"📋 {result['Headline']} ({result['Count']} comments)"):
                    st.write(f"**Summary:** {result['Summary']}")
                    st.write(f"**Key Themes:** {result['Themes']}")
                    st.write(f"**Sample Comments:** {result['Sample_Comments'][:500]}...")
            
            # Create downloadable results
            results_df = pd.DataFrame(st.session_state.summary_results)
            
            # Download button
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="survey_analysis_results.csv",
                mime="text/csv"
            )
            
            # Show results table
            st.subheader("Results Table")
            st.dataframe(results_df)
    
    # Reset button
    if st.sidebar.button("🔄 Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()