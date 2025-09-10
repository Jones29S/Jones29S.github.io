app.pyfrom flask import Flask, render_template, request, redirect
import pandas as pd
from datetime import datetime

app = Flask(__name__)

CSV_FILE = "roi_track_sm.csv"

@app.route("/")
def home():
    return render_template("tracker.html")

@app.route("/submit", methods=["POST"])
def submit():
    platform = request.form["platform"]
    revenue = float(request.form["revenue"])
    followers = int(request.form["followers"])
    engagement = float(request.form["engagement"])
    date = datetime.now().strftime("%Y-%m-%d")

    new_entry = pd.DataFrame([{
        "Date": date,
        "Platform": platform,
        "Revenue": revenue,
        "Followers": followers,
        "Engagement": engagement
    }])

    try:
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, new_entry], ignore_index=True)
    except FileNotFoundError:
        df = new_entry

    df.to_csv(CSV_FILE, index=False)
    return redirect("/analytics")

@app.route("/analytics")
def analytics():
    df = pd.read_csv(CSV_FILE)
    total_revenue = df["Revenue"].sum()
    top_platform = df.groupby("Platform")["Revenue"].sum().idxmax()
    avg_engagement = df["Engagement"].mean()

    return render_template("analytics.html",
                           total_revenue=total_revenue,
                           top_platform=top_platform,
                           avg_engagement=round(avg_engagement, 2),
                           data=df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
