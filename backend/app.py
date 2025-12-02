from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

CSV_PATH = r"C:\Users\deeks\OneDrive\Desktop\bda project\clinical_trial_data.csv"

# Load dataset
df = pd.read_csv(CSV_PATH)

# Clean up whitespace
df["Disease"] = df["Disease"].str.strip()
df["Treatment"] = df["Treatment"].str.strip()

# Convert date columns to datetime
df["StartDate"] = pd.to_datetime(df["StartDate"], errors='coerce')
df["EndDate"] = pd.to_datetime(df["EndDate"], errors='coerce')


@app.route('/')
def index():
    """Dashboard Home Page"""
    diseases = sorted(df["Disease"].unique())
    treatments = sorted(df["Treatment"].unique())

    # Summary stats
    total_patients = len(df)
    patients_per_disease = df["Disease"].value_counts().to_dict()
    patients_per_treatment = df["Treatment"].value_counts().to_dict()

    return render_template(
        "index.html",
        diseases=diseases,
        treatments=treatments,
        total_patients=total_patients,
        patients_per_disease=patients_per_disease,
        patients_per_treatment=patients_per_treatment
    )


@app.route('/graph', methods=['POST'])
def graph():
    """Graph Page"""

    disease = request.form.get("disease")
    treatment = request.form.get("treatment")

    filtered = df.copy()

    if disease != "All":
        filtered = filtered[filtered["Disease"] == disease]

    if treatment != "All":
        filtered = filtered[filtered["Treatment"] == treatment]

    # Graph 1: Patients per Treatment
    fig1 = px.bar(
        filtered,
        x="Treatment",
        color="Disease",
        title="Treatment Distribution",
        barmode="group"
    )

    # Graph 2: Patients per Disease (Pie)
    fig2 = px.pie(
        filtered,
        names="Disease",
        title="Patient Distribution by Disease"
    )

    # Graph 3: Patients per Treatment & Disease (Stacked Bar)
    counts = filtered.groupby(["Disease", "Treatment"]).size().reset_index(name="Count")
    fig3 = px.bar(
        counts,
        x="Treatment",
        y="Count",
        color="Disease",
        title="Patients per Treatment and Disease",
        barmode="stack"
    )

    # Graph 4: Timeline of patients per Treatment
    timeline_df = filtered.dropna(subset=["StartDate", "EndDate"])
    if not timeline_df.empty:
        fig4 = px.timeline(
            timeline_df,
            x_start="StartDate",
            x_end="EndDate",
            y="Treatment",
            color="Disease",
            title="Patient Timeline per Treatment",
            hover_data=["PatientID"]
        )
        fig4.update_yaxes(autorange="reversed")
        graph4_html = fig4.to_html(full_html=False)
    else:
        graph4_html = "<p>No date information available for timeline chart.</p>"

    graph1_html = fig1.to_html(full_html=False)
    graph2_html = fig2.to_html(full_html=False)
    graph3_html = fig3.to_html(full_html=False)

    return render_template(
        "graph.html",
        graph1_html=graph1_html,
        graph2_html=graph2_html,
        graph3_html=graph3_html,
        graph4_html=graph4_html
    )


if __name__ == '__main__':
    app.run(debug=True)
