import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data(ttl=600)
def load_data():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/17ncvKhRIvn6z8vcAjHC0ZZjdbHRmCliG/export?format=csv"
    return pd.read_csv(SHEET_URL)

def main():
    st.title("Steps Dashboard 🏃‍♂️")
  
    df_activity = load_data()  # Call the function to get the cached DataFrame


    # Convert necessary columns
    numeric_cols = ["Steps", "DistanceInMeters", "Calories", "VigorousIntensityDurationInSeconds",
                    "ModerateIntensityDurationInSeconds", "SedentaryDurationInSeconds"]
    df_activity[numeric_cols] = df_activity[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df_activity["RecordDate"] = pd.to_datetime(df_activity["RecordDate"], errors="coerce")
    df_activity["StartTimeFormatted"] = pd.to_datetime(df_activity["StartTimeOffsetFormatted"], errors="coerce")
    # Create Participant Name
    df_activity["ParticipantName"] = df_activity["LastName"] + " " + df_activity["FirstName"]

    # Streamlit App Layout
    #st.title("Activity Tracking Dashboard 🏃‍♂️")
    st.sidebar.header("Filter Data")

#import streamlit as st

    # Select Organization
    selected_org = st.sidebar.selectbox("Select Organization", ["All"] + sorted(df_activity["OrganizationName"].dropna().unique().tolist()))

    # Filter Data Based on Organization
    filtered_df = df_activity.copy()
    if selected_org != "All":
        filtered_df = filtered_df[filtered_df["OrganizationName"] == selected_org]

    # Select Cohort (Filtered Based on Organization)
    selected_cohort = st.sidebar.selectbox("Select Cohort", ["All"] + sorted(filtered_df["CohortName"].dropna().unique().tolist()))
    if selected_cohort != "All":
        filtered_df = filtered_df[filtered_df["CohortName"] == selected_cohort]

    # Select Program (Filtered Based on Cohort)
    selected_program = st.sidebar.selectbox("Select Program", ["All"] + sorted(filtered_df["ProgramName"].dropna().unique().tolist()))
    if selected_program != "All":
        filtered_df = filtered_df[filtered_df["ProgramName"] == selected_program]

    # Select Physician (Filtered Based on Program)
    selected_physician = st.sidebar.selectbox("Select Physician", ["All"] + sorted(filtered_df["PhysicianName"].dropna().unique().tolist()))
    if selected_physician != "All":
        filtered_df = filtered_df[filtered_df["PhysicianName"] == selected_physician]

    # Select Gender BEFORE Participant (To prevent conflicts)
    selected_gender = st.sidebar.selectbox("Select Gender", ["All"] + sorted(filtered_df["ParticipantGender"].dropna().unique().tolist()))
    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df["ParticipantGender"] == selected_gender]

    # Select Age Group (Filtered Based on Gender)
    selected_age_group = st.sidebar.selectbox("Select Age Group", ["All"] + sorted(filtered_df["AgeGroup"].dropna().unique().tolist()))
    if selected_age_group != "All":
        filtered_df = filtered_df[filtered_df["AgeGroup"] == selected_age_group]

    # Select Ethnicity (Filtered Based on Gender & Age Group)
    selected_ethnicity = st.sidebar.selectbox("Select Ethnicity", ["All"] + sorted(filtered_df["Ethnicity"].dropna().unique().tolist()))
    if selected_ethnicity != "All":
        filtered_df = filtered_df[filtered_df["Ethnicity"] == selected_ethnicity]

    # Select City (Filtered Based on Ethnicity)
    selected_city = st.sidebar.selectbox("Select City", ["All"] + sorted(filtered_df["City"].dropna().unique().tolist()))
    if selected_city != "All":
        filtered_df = filtered_df[filtered_df["City"] == selected_city]

    # Select Participant (Filtered Based on Previous Selections)
    valid_participants = sorted(filtered_df["ParticipantName"].dropna().unique().tolist())
    selected_participant = st.sidebar.selectbox("Select Participant", ["All"] + valid_participants)
    if selected_participant != "All":
        filtered_df = filtered_df[filtered_df["ParticipantName"] == selected_participant]

    # Final Filtered Data
    df_filtered = filtered_df.copy()



    # Dependent Filters
    # selected_org = st.sidebar.selectbox("Select Organization", ["All"] + sorted(df_activity["OrganizationName"].dropna().unique().tolist()))
    # filtered_cohorts = df_activity[df_activity["OrganizationName"] == selected_org] if selected_org != "All" else df_activity
    # selected_cohort = st.sidebar.selectbox("Select Cohort", ["All"] + sorted(filtered_cohorts["CohortName"].dropna().unique().tolist()))
    # filtered_programs = filtered_cohorts[filtered_cohorts["CohortName"] == selected_cohort] if selected_cohort != "All" else filtered_cohorts
    # selected_program = st.sidebar.selectbox("Select Program", ["All"] + sorted(filtered_programs["ProgramName"].dropna().unique().tolist()))
    # filtered_physicians = filtered_programs[filtered_programs["ProgramName"] == selected_program] if selected_program != "All" else filtered_programs
    # selected_physician = st.sidebar.selectbox("Select Physician", ["All"] + sorted(filtered_physicians["PhysicianName"].dropna().unique().tolist()))
    # filtered_participants = filtered_physicians[filtered_physicians["PhysicianName"] == selected_physician] if selected_physician != "All" else filtered_physicians
    # selected_participant = st.sidebar.selectbox("Select Participant", ["All"] + sorted(filtered_participants["ParticipantName"].dropna().unique().tolist()))
    # selected_age_group = st.sidebar.selectbox("Select Age Group", ["All"] + sorted(filtered_participants["AgeGroup"].dropna().unique().tolist()))
    # selected_gender = st.sidebar.selectbox("Select Gender", ["All"] + sorted(filtered_participants["ParticipantGender"].dropna().unique().tolist()))
    # selected_ethnicity = st.sidebar.selectbox("Select Ethnicity", ["All"] + sorted(filtered_participants["Ethnicity"].dropna().unique().tolist()))
    # # selected_race = st.sidebar.selectbox("Select Race", ["All"] + sorted(filtered_participants["Race"].dropna().unique().tolist()))
    # selected_city = st.sidebar.selectbox("Select City", ["All"] + sorted(filtered_participants["City"].dropna().unique().tolist()))
   # # selected_country = st.sidebar.selectbox("Select Country", ["All"] + sorted(filtered_participants["Country"].dropna().unique().tolist()))

    # # Apply Filters
    # df_filtered = filtered_participants.copy()
    # if selected_gender != "All":
        # df_filtered = df_filtered[df_filtered["ParticipantGender"] == selected_gender]
    # if selected_age_group != "All":
        # df_filtered = df_filtered[df_filtered["AgeGroup"] == selected_age_group]
    # if selected_ethnicity != "All":
        # df_filtered = df_filtered[df_filtered["Ethnicity"] == selected_ethnicity]
    
    # valid_participants = df_filtered["ParticipantName"].dropna().unique().tolist()
    # selected_participant = st.sidebar.selectbox("Select Participant", ["All"] + sorted(valid_participants))

    # if selected_participant != "All":
        # df_filtered = df_filtered[df_filtered["ParticipantName"] == selected_participant]
    # #if selected_age_group != "All":
    # #    df_filtered = df_filtered[df_filtered["AgeGroup"] == selected_age_group]
    # #if selected_gender != "All":
     # #   df_filtered = df_filtered[df_filtered["ParticipantGender"] == selected_gender]
    # #if selected_ethnicity != "All":
      # #  df_filtered = df_filtered[df_filtered["Ethnicity"] == selected_ethnicity]
    # # if selected_race != "All":
        # # df_filtered = df_filtered[df_filtered["Race"] == selected_race]
    # if selected_city != "All":
        # df_filtered = df_filtered[df_filtered["City"] == selected_city]
    #if selected_country != "All":
     #   df_filtered = df_filtered[df_filtered["Country"] == selected_country]

    # Display Participant and Physician Photos in Main Dashboard
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

    # 1️⃣ Steps Trend Over Time
    if not df_filtered.empty:
        st.subheader("Steps Trend Over Time")
        steps_trend = df_filtered.groupby("RecordDate")["Steps"].sum().reset_index()
        fig1 = px.line(steps_trend, x="RecordDate", y="Steps", markers=True,
                       title="Steps Trend Over Time",
                       labels={"Steps": "Total Steps", "RecordDate": "Date"},
                       line_shape='linear', render_mode='svg')
        st.plotly_chart(fig1)
    else:
        st.warning("No data available for Steps Trend.")

    # 2️⃣ Distance Covered Trend
    if not df_filtered.empty:
        st.subheader("Distance Covered Trend")
        distance_trend = df_filtered.groupby("RecordDate")["DistanceInMeters"].sum().reset_index()
        fig2 = px.line(distance_trend, x="RecordDate", y="DistanceInMeters", markers=True,
                       title="Distance Covered Trend Over Time",
                       labels={"DistanceInMeters": "Total Distance (Meters)", "RecordDate": "Date"},
                       line_shape='linear', render_mode='svg')
        st.plotly_chart(fig2)
    else:
        st.warning("No data available for Distance Covered Trend.")

    # 3️⃣ Calories Burned Trend
    if not df_filtered.empty:
        st.subheader("Calories Burned Trend")
        calories_trend = df_filtered.groupby("RecordDate")["Calories"].sum().reset_index()
        fig3 = px.line(calories_trend, x="RecordDate", y="Calories", markers=True,
                       title="Calories Burned Trend Over Time",
                       labels={"Calories": "Total Calories Burned", "RecordDate": "Date"},
                       line_shape='linear', render_mode='svg')
        st.plotly_chart(fig3)
    else:
        st.warning("No data available for Calories Burned Trend.")

    # 4️⃣ Activity Intensity Breakdown (Stacked Bar)
    if not df_filtered.empty:
        st.subheader("Activity Intensity Breakdown")
        activity_intensity = df_filtered.groupby("OrganizationName")[["VigorousIntensityDurationInSeconds",
                                                                      "ModerateIntensityDurationInSeconds",
                                                                      "SedentaryDurationInSeconds"]].sum().reset_index()
        fig4 = px.bar(activity_intensity, x="OrganizationName", y=["VigorousIntensityDurationInSeconds",
                                                                    "ModerateIntensityDurationInSeconds",
                                                                    "SedentaryDurationInSeconds"],
                      title="Activity Intensity Breakdown",
                      labels={"value": "Total Duration (Seconds)", "variable": "Activity Intensity"},
                      barmode="stack")
        st.plotly_chart(fig4)
    else:
        st.warning("No data available for Activity Intensity Breakdown.")

    # 1️⃣ Activity Patterns by Time of Day (Heatmap)
    if not df_filtered.empty:
        st.subheader("Activity Patterns by Time of Day (Heatmap)")
        
        # Extract Time of Day in 2-hour slots
        df_filtered["Hour"] = df_filtered["StartTimeFormatted"].dt.hour
        df_filtered["TimeSlot"] = pd.cut(df_filtered["Hour"], bins=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
                                         labels=["00-02", "02-04", "04-06", "06-08", "08-10", "10-12", 
                                                 "12-14", "14-16", "16-18", "18-20", "20-22", "22-00"])

        # Apply Hierarchical Filters
        heatmap_data = df_filtered.groupby(["TimeSlot", "OrganizationName"])["Steps"].sum().unstack()

        if not heatmap_data.empty:
            # Plot Heatmap
            plt.figure(figsize=(10, 6))
            sns.heatmap(heatmap_data, cmap="Blues", linewidths=0.5, annot=True, fmt=".0f")
            plt.xlabel("Organization")
            plt.ylabel("Time Slot")
            plt.title("Activity Patterns by Time of Day")
            st.pyplot(plt)
        else:
            st.warning("No data available after applying filters.")
    else:
        st.warning("No data available for Activity Patterns Heatmap.")

    # 2️⃣ Weekly Trends in Steps, Distance & Calories
    if not df_filtered.empty:
        st.subheader("Weekly Trends in Steps, Distance & Calories")
        
        # Extract Day of the Week
        df_filtered["DayOfWeek"] = df_filtered["RecordDate"].dt.day_name()

        # Apply Hierarchical Filters
        weekly_trends = df_filtered.groupby("DayOfWeek")[["Steps", "DistanceInMeters", "Calories"]].sum().reset_index()

        if not weekly_trends.empty:
            # Create Line Chart
            fig_weekly = px.line(weekly_trends, x="DayOfWeek", y=["Steps", "DistanceInMeters", "Calories"], 
                                 title="Weekly Trends in Activity",
                                 labels={"value": "Total Activity", "variable": "Metric"},
                                 markers=True)
            st.plotly_chart(fig_weekly)
        else:
            st.warning("No data available after applying filters.")
    else:
        st.warning("No data available for Weekly Trends.")

    # 3️⃣ Anomalies in Activity Data (Box Plot)
    
    
    # Count anomalies by type
    anomaly_counts = df_filtered["AnomalyType"].value_counts()
    
    if not df_filtered.empty:
        st.subheader("Anomaly Type Breakdown")
        
        # Apply Hierarchical Filters
        if "OrganizationName" in df_filtered.columns and not df_filtered.empty:
           # Plot anomaly type distribution
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=anomaly_counts.index, y=anomaly_counts.values, ax=ax, palette="coolwarm")
            ax.set_title("Anomaly Type Distribution")
            ax.set_xlabel("Anomaly Type")
            ax.set_ylabel("Count")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
            st.pyplot(fig)
        else:
            st.warning("No data available after applying filters.")
    else:
        st.warning("No data available for Activity Anomalies.")

    # Convert Date column to datetime
    df_filtered["RecordDate"] = pd.to_datetime(df_filtered["RecordDate"])
    st.subheader("Anomalies Over Time")
    # Count anomalies per day
    anomaly_trend = df_filtered.groupby("RecordDate")["AnomalyType"].count()

    # Plot anomaly trend over time
    fig, ax = plt.subplots(figsize=(10, 5))
    anomaly_trend.plot(ax=ax, color="red", marker="o", linestyle="-")
    ax.set_title("Anomalies Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Anomalies")

    st.pyplot(fig)


    # Count anomalies per participant
    top_anomalies = df_filtered["ParticipantName"].value_counts().head(10)
    st.subheader("Top 10 Participants with  Most Anomalies") 
    # Plot bar chart
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_anomalies.values, y=top_anomalies.index, ax=ax, palette="magma")
    ax.set_title("Top 10 Participants with Most Anomalies")
    ax.set_xlabel("Number of Anomalies")
    ax.set_ylabel("Participant Name")

    st.pyplot(fig)



# Ensure this function is accessible from app.py
if __name__ == "__main__":
    main()
