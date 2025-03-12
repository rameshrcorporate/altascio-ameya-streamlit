import streamlit as st
import pandas as pd
import plotly.express as px
#import boto3
#from io import BytesIO

# -------------------------------
# 🚀 AWS S3 Configuration
# -------------------------------
S3_PUBLIC_URL = "https://althealth.s3.us-east-1.amazonaws.com/Synthetic_Dataset_Sleep_V3.xlsx"

@st.cache_data(ttl=1800)
def load_s3_excel():
    return pd.read_excel(S3_PUBLIC_URL, engine="openpyxl")

def main():
    st.title("Sleep Dashboard  💤")

    # Load Data from S3
    df = load_s3_excel()
    if df is None:
        st.error("Failed to load data from S3.")
        return

    # Convert necessary columns
    numeric_cols = ["DurationInSeconds", "DeepSleep", "LightSleep", "RemSleep", "AwakeTime", "TimeSpent", "DurationAsleep"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
    df["ParticipantName"] = df["LastName"] + " " + df["FirstName"]

    # Ensure AgeGroup is treated as a string
    df["AgeGroup"] = df["AgeGroup"].astype(str)
    
    df["SleepEfficiency"] = ((df["DurationAsleep"] / df["TimeSpent"]) * 100).round(2)

    # Streamlit Sidebar Filters
    st.sidebar.header("Filter Data")

    # Organization Filter
    selected_org = st.sidebar.selectbox("Select Organization", ["All"] + sorted(df["OrganizationName"].dropna().unique().tolist()))
    df_filtered = df if selected_org == "All" else df[df["OrganizationName"] == selected_org]

    # Cohort Filter (Dependent on Organization)
    selected_cohort = st.sidebar.selectbox("Select Cohort", ["All"] + sorted(df_filtered["CohortName"].dropna().unique().tolist()))
    df_filtered = df_filtered if selected_cohort == "All" else df_filtered[df_filtered["CohortName"] == selected_cohort]

    # Program Filter (Dependent on Cohort)
    selected_program = st.sidebar.selectbox("Select Program", ["All"] + sorted(df_filtered["ProgramName"].dropna().unique().tolist()))
    df_filtered = df_filtered if selected_program == "All" else df_filtered[df_filtered["ProgramName"] == selected_program]

    # Physician Filter (Dependent on Organization)
    selected_physician = st.sidebar.selectbox("Select Physician", ["All"] + sorted(df_filtered["PhysicianName"].dropna().unique().tolist()))
    df_filtered = df_filtered if selected_physician == "All" else df_filtered[df_filtered["PhysicianName"] == selected_physician]

    # Participant Filter (Dependent on Program)
    selected_participant = st.sidebar.selectbox("Select Participant", ["All"] + sorted(df_filtered["ParticipantName"].dropna().unique().tolist()))
    df_filtered = df_filtered if selected_participant == "All" else df_filtered[df_filtered["ParticipantName"] == selected_participant]

    # Gender Filter (Independent)
    selected_gender = st.sidebar.selectbox("Select Gender", ["All"] + sorted(df_filtered["ParticipantGender"].dropna().unique().tolist()))
    df_filtered = df_filtered if selected_gender == "All" else df_filtered[df_filtered["ParticipantGender"] == selected_gender]

    # Ethnicity Filter (Independent)
    selected_ethnicity = st.sidebar.selectbox("Select Ethnicity", ["All"] + sorted(df_filtered["Ethnicity"].dropna().unique().tolist()))
    df_filtered = df_filtered if selected_ethnicity == "All" else df_filtered[df_filtered["Ethnicity"] == selected_ethnicity]

    # Age Group Filter (Using Existing Column)
    selected_age_group = st.sidebar.selectbox("Select Age Group", ["All"] + sorted(df_filtered["AgeGroup"].dropna().unique().tolist()))
    df_filtered = df_filtered if selected_age_group == "All" else df_filtered[df_filtered["AgeGroup"] == selected_age_group]

    col1, col2 = st.columns([1, 1])

    if selected_physician != "All":
        physician_photo = df_filtered["PhysicianPhoto"].iloc[0].strip("'") if not pd.isna(df_filtered["PhysicianPhoto"].iloc[0]) else None
        if physician_photo:
            with col1:
                st.image(physician_photo, caption=f"Physician: {selected_physician}", width=150)

    if selected_participant != "All":
        participant_photo = df_filtered["ParticipantPhotoURL"].iloc[0].strip("'") if not pd.isna(df_filtered["ParticipantPhotoURL"].iloc[0]) else None
        if participant_photo:
            with col2:
                st.image(participant_photo, caption=f"Participant: {selected_participant}", width=150)




    # 📊 Data Visualizations
    st.subheader("Average Sleep Duration per Organization")
    avg_sleep_by_org = df_filtered.groupby("OrganizationName")["DurationInSeconds"].mean().reset_index()
    fig1 = px.bar(avg_sleep_by_org, x="OrganizationName", y="DurationInSeconds", color="OrganizationName",
                  title="Average Sleep Duration per Organization", labels={"DurationInSeconds": "Avg Sleep (Seconds)"}, barmode='group')
    st.plotly_chart(fig1,key="avg_sleep_by_org")

    # Sleep Duration Trend Over Time
    if not df_filtered.empty:
        st.subheader("Sleep Duration Trend Over Time")
        avg_sleep_trend = df_filtered.groupby("RecordDate")["DurationInSeconds"].mean().reset_index()
        fig2 = px.line(avg_sleep_trend, x="RecordDate", y="DurationInSeconds", markers=True,
                       title="Sleep Duration Trend Over Time",
                       labels={"DurationInSeconds": "Avg Sleep (Seconds)", "RecordDate": "Date"},
                       line_shape='linear', render_mode='svg')
        st.plotly_chart(fig2,key="sleep_duratoin_trend")
    else:
        st.warning("No data available for the selected filters.")

    # Sleep Stages Breakdown
    if not df_filtered.empty:
        st.subheader("Sleep Stages Breakdown")
        sleep_stages = df_filtered.groupby("OrganizationName")[["DeepSleep", "LightSleep", "RemSleep", "AwakeTime"]].mean().reset_index()
        fig3 = px.bar(sleep_stages, x="OrganizationName", y=["DeepSleep", "LightSleep", "RemSleep", "AwakeTime"],
                      title="Average Sleep Stages per Organization",
                      labels={"value": "Avg Duration (Seconds)", "variable": "Sleep Stage"},
                      barmode="stack")
        st.plotly_chart(fig3,key="sleep_stages")
    else:
        st.warning("No data available for Sleep Stages Breakdown.")

    # Total Time in Bed vs. Actual Sleep
    if not df_filtered.empty:
        st.subheader("Total Time in Bed vs. Actual Sleep")
        fig4 = px.scatter(df_filtered, x="TimeSpent", y="DurationAsleep",
                          title="Total Time in Bed vs. Actual Sleep",
                          labels={"TimeSpent": "Total Time in Bed (Seconds)", "DurationAsleep": "Actual Sleep Duration (Seconds)"},
                          opacity=0.7, color="OrganizationName")
        st.plotly_chart(fig4,key="totaltimeinbed_vs_actualsleep")
    else:
        st.warning("No data available for Time in Bed vs. Actual Sleep.")
        
        
# Sleep Efficiency by Organization
    st.subheader("📊 Sleep Efficiency per Organization")
    sleep_efficiency_by_org = df_filtered.groupby("OrganizationName")["SleepEfficiency"].mean().reset_index()
    fig5 = px.bar(sleep_efficiency_by_org, x="OrganizationName", y="SleepEfficiency", color="OrganizationName",
                  title="Average Sleep Efficiency per Organization (%)", labels={"SleepEfficiency": "Sleep Efficiency (%)"}, barmode='group')
    st.plotly_chart(fig5,key="avg_sleep_eff_org")

   # Sleep Efficiency vs. Duration Asleep
    if not df_filtered.empty:
        st.subheader("📊 Sleep Efficiency vs. Duration Asleep")
        fig6 = px.scatter(df_filtered, x="DurationAsleep", y="SleepEfficiency", color="OrganizationName",
                      title="Relationship Between Sleep Efficiency and Sleep Duration",
                      labels={"DurationAsleep": "Duration Asleep (Seconds)", "SleepEfficiency": "Sleep Efficiency (%)"},
                      opacity=0.7)
        st.plotly_chart(fig6, key="sleep_eff_vs_durationasleep")
    else:
        st.warning("No data available for Sleep Efficiency vs. Duration Asleep.")


    # Sleep Duration by Gender
    # st.subheader("📊 Average Sleep Duration by Gender")
    # avg_sleep_by_gender = df_filtered.groupby("ParticipantGender")["DurationInSeconds"].mean().reset_index()
    # fig7 = px.bar(avg_sleep_by_gender, x="ParticipantGender", y="DurationInSeconds", color="ParticipantGender",
                  # title="Average Sleep Duration by Gender", labels={"DurationInSeconds": "Avg Sleep (Seconds)"}, barmode='group')
    # st.plotly_chart(fig7,key="avg_sleep_by_gender")

    # # Total Time in Bed vs. Actual Sleep
    # if not df_filtered.empty:
        # st.subheader("📊 Total Time in Bed vs. Actual Sleep")
        # fig5 = px.scatter(df_filtered, x="TimeSpent", y="DurationAsleep",
                          # title="Total Time in Bed vs. Actual Sleep",
                          # labels={"TimeSpent": "Total Time in Bed (Seconds)", "DurationAsleep": "Actual Sleep Duration (Seconds)"},
                          # opacity=0.7, color="OrganizationName")
        # st.plotly_chart(fig8)
    # else:
        # st.warning("No data available for Time in Bed vs. Actual Sleep.")

if __name__ == "__main__":
    main()
