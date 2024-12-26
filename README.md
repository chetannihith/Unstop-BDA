```markdown
# Big Data Analytics on Unstop Data

This repository contains the code and resources for a comprehensive project on **Big Data Analytics**. The project involves data scraping, preprocessing, creating visualizations, and applying analytics techniques to analyze hackathons, internships, and job datasets scraped from the Unstop platform.

## 🚀 Project Features
- **Data Preprocessing**: Cleaned and prepared datasets for analysis.
- **Visualizations**: Created critical visualizations to derive insights.
- **Analytics Applications**: Applied various analytics techniques to uncover hidden patterns.
- **Cross-Dataset Insights**: Combined datasets to generate deeper insights.

---

## 📂 Repository Structure

```plaintext
Unstop-BDA
│
├── Preprocessed_files
│   ├── cleaned_hackathons.csv
│   ├── cleaned_internship.csv
│   ├── cleaned_jobs.csv
│   ├── hackathon_clean.ipynb
│   ├── internship_clean.ipynb
│   └── jobs_clean.ipynb
│
├── Project_files
│   ├── app.py
│   ├── main.ipynb
│   └── requirements.txt
│
├── Scraping_files
│   ├── scrape_unstop_hackathon.py
│   ├── scrape_unstop_internship.py
│   └── scrape_unstop_job.py
│   ├── scraped_hackathons.csv
│   ├── scraped_internships.csv
│   └── scraped_jobs.csv
│
└── README.md
```

---

## 📊 Datasets

### Hackathons
- **Columns**: Category, Eligibility, Applied, Impressions, Deadline, etc.
- **Insights**: Trends in categories, application patterns, and deadlines.

### Internships
- **Columns**: Position, Company, Eligibility, Impressions, Applied, etc.
- **Insights**: Popular internship domains, top companies, and application trends.

### Jobs
- **Columns**: Position, Eligibility, Impressions, Applied, etc.
- **Insights**: Popular job roles, application vs. impressions patterns.

---

## 🛠️ Steps to Run

### 1. Clone the Repository
```bash
git clone https://github.com/chetannihith/Unstop-BDA.git
```

### 2. Install Dependencies
Navigate to the repository folder and install the required Python libraries using:
```bash
pip install -r requirements.txt
```

### 3. Run Notebooks or Scripts
Use Jupyter notebooks or directly execute Python scripts:
- **Preprocessing**: `Preprocessed_files/hackathon_clean.ipynb`, `Preprocessed_files/internship_clean.ipynb`, or `Preprocessed_files/jobs_clean.ipynb`
- **Scraping**: `Scraping_files/scrape_unstop_hackathon.py`, `Scraping_files/scrape_unstop_internship.py`, or `Scraping_files/scrape_unstop_job.py`
- **Visualization**: `Project_files/main.ipynb`
- **Streamlit App**: Create a Streamlit website using `app.py`
  ```bash
  streamlit run Project_files/app.py
  ```

---

## 📈 Key Visualizations
1. **Hackathon Trends**: Most popular categories and deadlines.
2. **Internship Patterns**: Application trends and top companies.
3. **Job Insights**: Role popularity and impression patterns.
4. **Cross-Dataset Analysis**: Application correlations across datasets.

---

## 📜 Requirements
- Python 3.8 or higher
- Libraries:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `scikit-learn`
  - `streamlit`
  - `plotly`
  - `wordcloud`
  - `jupyter`

Install using:
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork this repository and submit a pull request with your changes.

---

## `requirements.txt`

```plaintext
streamlit==1.22.0
pandas==1.5.3
numpy==1.23.5
matplotlib==3.6.2
seaborn==0.12.1
plotly==5.11.0
wordcloud==1.8.2.2
```

---

## `.gitignore`

```plaintext
*.csv
*.ipynb_checkpoints
__pycache__/
```
```
