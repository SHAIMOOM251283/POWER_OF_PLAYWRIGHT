import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import os

class DataVisualization:

    def __init__(self):
        base_path = os.path.dirname(__file__)
        csv_path = os.path.join(base_path, "..", "data_files")
        self.chem = pd.read_csv(os.path.join(csv_path, "Chemistry.csv"))
        self.phys = pd.read_csv(os.path.join(csv_path, "Physics.csv"))
        self.cs   = pd.read_csv(os.path.join(csv_path, "Computer_Science.csv"))
        self.chem["Subject"] = "Chemistry"
        self.phys["Subject"] = "Physics"
        self.cs["Subject"]   = "Computer Science"
        
    def process_data(self):
        df = pd.concat([self.chem, self.phys, self.cs], ignore_index=True)
        df["Rating"] = df["Rating"].str.extract(r'(\d+\.\d+)')
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
        df["Want to Read"] = (
            df["Want to Read"]
            .str.extract(r'(\d+)')
            .astype(float)          
            .fillna(0)              
            .astype(int)            
            )
        df["Author"] = df["Author"].fillna("Unknown Author")
        df["Title"]  = df["Title"].fillna("Unknown Title")
        df["Subject"] = df["Subject"].fillna("Unknown Subject")  
        return df
        
    def bar_chart(self):
        data_frame = self.process_data()
        top_per_subject = (
            data_frame.sort_values("Want to Read", ascending=False)
            .groupby("Subject")
            .head(10)
            )

        fig = px.bar(
            top_per_subject,
            x="Title",
            y="Want to Read",
            color="Subject",
            hover_data=["Author", "Rating"],
            title="Top 10 Most Wanted Books per Subject"
            )
        fig.show()

    def treemap(self):
        data_frame = self.process_data()
        fig = px.treemap(
            data_frame,
            path=["Subject", "Author", "Title"],
            values="Want to Read",
            color="Rating",
            color_continuous_scale="Viridis",
            title="Book Popularity by Subject and Author"
        )
        fig.show()
    
    def bubble_chart(self):
        data_frame = self.process_data()
        fig = px.scatter(
            data_frame,
            x="Rating",
            y="Want to Read",
            size="Want to Read",
            color="Subject",
            hover_data=["Title", "Author"],
            title="Ratings vs Demand (Bubble Size = Want to Read)"
            )
        fig.show()
    
    def scatter_plot(self):
        data_frame = self.process_data()
        fig = px.scatter(
            data_frame,
            x="Rating",
            y="Want to Read",
            color="Subject",
            hover_data=["Title", "Author"],
            trendline="ols",  # requires statsmodels (install via pip install statsmodels)
            title="Demand vs Rating with Trendline"
            )
        fig.show()
    
    def wordcloud(self):
        data_frame = self.process_data()
        text = " ".join(data_frame["Title"].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        fig = go.Figure()
        fig.add_trace(go.Image(z=wordcloud.to_array()))
        fig.update_layout(
            title="Most Common Words in Book Titles",
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            margin=dict(l=0, r=0, t=40, b=0)
            )
        fig.show()
    
    def heatmap(self):
        data_frame = self.process_data()
        heatmap_data = data_frame.groupby("Subject")[["Rating","Want to Read"]].mean().reset_index()
        fig = px.imshow(
            heatmap_data.set_index("Subject").T,
            text_auto=True,
            color_continuous_scale="Blues",
            title="Average Rating and Demand by Subject"
            )
        fig.show()

    def sunburst_chart(self):
        data_frame = self.process_data()
        fig = px.sunburst(
            data_frame,
            path=["Subject", "Author", "Title"],  # hierarchical levels
            values="Want to Read",                # slice size
            color="Rating",                       # color by rating
            color_continuous_scale="Viridis",
            title="Book Popularity Sunburst: Subject → Author → Book"
            )
        fig.show()
    
    def run(self):
        self.bar_chart()
        self.treemap()
        self.bubble_chart()
        self.scatter_plot()
        self.wordcloud()
        self.heatmap()
        self.sunburst_chart()
        
if __name__ == '__main__':
    DataVisualization().run()

