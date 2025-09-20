# POWER\_OF\_PLAYWRIGHT 🚀

A collection of **web scraping projects powered by [Playwright](https://playwright.dev/)**.
This repository demonstrates modern, asynchronous scraping techniques with robust error handling, concurrency, and structured data output.

The goal: **showcase scraping skills with Playwright across different websites**.

---

## 📂 Project Structure

```
POWER_OF_PLAYWRIGHT/
│
├── OpenLibrary_SCRAPER/
│   ├── ol_category_scraper.py
│   ├── ol_subject_scraper.py
│   └── DATA/
│       ├── data_files/   # CSVs or other structured scraped data
│       └── data_viz/     # Charts, plots, and other visualizations
│
└── (More scrapers coming soon...)
```

---

## 🔎 Current Implementation: OpenLibrary

Website: [Open Library](https://openlibrary.org/)

Two scrapers are included:

* **Category Scraper (`ol_category_scraper.py`)**
  Scrapes data from any subject URL, with flexible page limits capable of handling large volumes, saving details such as:
  
  * Title
  * Author(s)
  * Rating
  * “Want to Read” count

* **Subject Scraper (`ol_subject_scraper.py`)**
  Scrapes books for **any subject** by adjusting the query in the script (`self.query`).
  Saves results in `<SUBJECT>.csv` (e.g., `Chemistry.csv`).

Both scripts:
✅ Run asynchronously with Playwright
✅ Scrape multiple pages in parallel
✅ Handle errors with retries and exponential backoff
✅ Save clean structured data to CSV

---

## ⚙️ Installation

1. **Clone the repository**:

```bash
git clone https://github.com/<your-username>/POWER_OF_PLAYWRIGHT.git
cd POWER_OF_PLAYWRIGHT/OpenLibrary_SCRAPER
```

2. **Create and activate a virtual environment**:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install playwright pandas plotly wordcloud statsmodels
playwright install
```

---

## ▶️ Usage

1. **Activate your virtual environment** (created during installation):

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. **Navigate to the scraper folder**:

```bash
cd OpenLibrary_SCRAPER
```

3. **Run a scraper**:

* **Category Scraper (e.g. any subject url)**:

```bash
python ol_category_scraper.py
```

* **Subject Scraper (e.g., Chemistry)**:

```bash
python ol_subject_scraper.py
```

4. **Check the output**:

* CSV files will be automatically saved inside the `OpenLibrary_SCRAPER/DATA` folder.
* Visualizations can be saved or generated in the `OpenLibrary_SCRAPER/DATA` folder.

---

## 📊 Data Visualizations

Visual insights generated from the scraped OpenLibrary data.

1. **Bar Chart** – Shows the top 10 most wanted books per subject, comparing demand across Chemistry, Physics, and Computer Science.
   ![Bar Chart](https://github.com/SHAIMOOM251283/POWER_OF_PLAYWRIGHT/blob/main/OpenLibrary_SCRAPER/DATA/data_viz/bar_chart.png)
   
2. **Treemap** – A hierarchical map of Subject → Author → Book, sized by demand and colored by rating.
   ![Treemap](https://github.com/SHAIMOOM251283/POWER_OF_PLAYWRIGHT/blob/main/OpenLibrary_SCRAPER/DATA/data_viz/treemap.png)

3. **Bubble Chart** – Plots ratings vs. demand, where bubble size represents demand and colors distinguish subjects.
   ![Bubble Chart](https://github.com/SHAIMOOM251283/POWER_OF_PLAYWRIGHT/blob/main/OpenLibrary_SCRAPER/DATA/data_viz/bubble_chart.png)

4. **Scatter Plot (with Trendline)** – Displays demand vs. rating for all books, with a regression trendline to show correlation.
   ![Scatter Plot](https://github.com/SHAIMOOM251283/POWER_OF_PLAYWRIGHT/blob/main/OpenLibrary_SCRAPER/DATA/data_viz/scatter_plot.png)

5. **Word Cloud** – Highlights the most common words in book titles, with larger words appearing more frequently.
   ![Word Cloud](https://github.com/SHAIMOOM251283/POWER_OF_PLAYWRIGHT/blob/main/OpenLibrary_SCRAPER/DATA/data_viz/wordcloud.png)

6. **Heatmap** – Compares the average rating and demand per subject side by side.
   ![Heatmap](https://github.com/SHAIMOOM251283/POWER_OF_PLAYWRIGHT/blob/main/OpenLibrary_SCRAPER/DATA/data_viz/heatmap.png)

7. **Sunburst Chart** – A hierarchical breakdown of Subject → Author → Book, with slice size for demand and color for rating.
   ![Sunburst Chart](https://github.com/SHAIMOOM251283/POWER_OF_PLAYWRIGHT/blob/main/OpenLibrary_SCRAPER/DATA/data_viz/sunburst_chart.png)

---

## 🔮 Future Plans

* Extend to other websites beyond Open Library
* Showcase login-protected scraping
* Handle JavaScript-heavy pages
* Demonstrate scraping + data visualization

---

## 📜 License

MIT License 

---