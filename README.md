# 📊 Survey Comment Analyzer

An interactive web application for analyzing survey comments, extracting themes, and generating cluster summaries automatically.

## ✨ Features

- **📁 File Upload**: Support for CSV and XLSX files
- **🔍 Text Processing**: Advanced text cleaning and stopword removal
- **📊 Clustering Analysis**: Elbow method and silhouette analysis for optimal cluster selection
- **🎯 Theme Extraction**: Automatic identification of prevalent themes in comment clusters
- **📝 Smart Summarization**: Generate descriptive summaries and headlines for each cluster
- **📥 Export Results**: Download analysis results as CSV files
- **🎨 Interactive UI**: Step-by-step guided workflow with progress tracking

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## 📋 How to Use

### Step 1: Upload Your Data
- Upload a CSV or XLSX file containing survey responses
- The app will automatically detect and display your data

### Step 2: Select Text Column
- Choose the column containing the comments/text you want to analyze
- Preview sample comments to ensure correct selection

### Step 3: Process Text Data
- Configure text processing options:
  - Add custom stopwords for your domain
  - Set minimum comment length filter
- The app will clean, process, and vectorize your text data

### Step 4: Analyze Clusters
- View interactive elbow and silhouette analysis plots
- Get automatic recommendations for optimal number of clusters

### Step 5: Select Clusters
- Use the slider to choose your preferred number of clusters
- Apply clustering to group similar comments

### Step 6: Generate Summaries
- Automatically generate:
  - Descriptive headlines for each cluster
  - Paragraph summaries of comment themes
  - Key themes and patterns
  - Sample comments for each cluster
- Download results as CSV for further analysis

## 🎯 Use Cases

- **Customer Feedback Analysis**: Understand common themes in customer reviews
- **Employee Survey Analysis**: Identify key concerns and suggestions from staff
- **Market Research**: Analyze open-ended survey responses
- **Academic Research**: Process qualitative data from questionnaires
- **Social Media Analysis**: Cluster and analyze user comments and feedback

## 📊 Data Format

Your input file should contain:
- **CSV or XLSX format**
- **At least one text column** with comments/responses
- **Minimum 10-20 comments** for meaningful analysis
- **UTF-8 encoding** for proper text processing

Example data structure:
```csv
ID,Question,Response,Rating
1,What did you like most?,"Great customer service and fast delivery",5
2,What did you like most?,"Easy to use website and good prices",4
3,What could be improved?,"Shipping took too long, packaging was poor",2
```

## 🔧 Technical Details

### Text Processing
- Automatic text cleaning and normalization
- Stopword removal with customizable word lists
- TF-IDF vectorization for numerical representation

### Clustering
- K-means clustering algorithm
- Elbow method for optimal cluster selection
- Silhouette analysis for cluster validation

### Theme Extraction
- TF-IDF based theme identification
- N-gram analysis for multi-word themes
- Frequency-based keyword extraction

## 🎨 Customization

The app includes several customization options:

- **Custom Stopwords**: Add domain-specific words to remove
- **Minimum Length**: Filter out very short comments
- **Cluster Range**: Automatic optimization of cluster numbers
- **Theme Count**: Adjustable number of themes per cluster

## 📈 Output

The app generates comprehensive results including:

- **Cluster Headlines**: Descriptive titles for each group
- **Summaries**: Paragraph descriptions of cluster contents
- **Themes**: Key topics and patterns identified
- **Sample Comments**: Representative examples from each cluster
- **Statistics**: Comment counts and distribution

## 🔍 Troubleshooting

**Common Issues:**

1. **"No text columns found"**: Ensure your file has text/string columns
2. **"Not enough data"**: You need at least 10-20 comments for analysis
3. **"Processing failed"**: Check for special characters or encoding issues
4. **"Clustering error"**: Try adjusting minimum comment length or stopwords

**Performance Tips:**

- For large datasets (>10,000 comments), consider sampling
- Use custom stopwords to improve theme quality
- Experiment with different cluster numbers for best results

## 📚 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning algorithms
- **nltk**: Natural language processing
- **plotly**: Interactive visualizations
- **numpy**: Numerical computing
- **matplotlib**: Additional plotting capabilities

## 🤝 Contributing

This is a background agent project, but suggestions for improvements are welcome:

- Enhanced summarization algorithms
- Additional visualization options
- Support for more file formats
- Advanced theme extraction methods
- Multi-language support

## 📄 License

This project is provided as-is for educational and research purposes.

## 🎉 Getting Started

Ready to analyze your survey comments? Simply run:

```bash
streamlit run app.py
```

And start discovering insights from your data! 🚀