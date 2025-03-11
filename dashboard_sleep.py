import streamlit as st
import pandas as pd
# import plotly as px
import plotly.express as px
import numpy as np
import seaborn

@st.cache_data(ttl=600)
def load_data():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/14BGFfbaTbEaLLA0clc38D80G3u2h3_I9/export?format=csv"
    return pd.read_csv(SHEET_URL)



def main():
    st.title("Sleep Dashboard")
   # st.write("This is the second dashboard.")

    df = load_data()  # Call the function to get the cached DataFrame

    # Convert necessary columns
    numeric_cols = ["DurationInSeconds", "DeepSleep", "LightSleep", "RemSleep", "AwakeTime", "TimeSpent", "DurationAsleep"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["RecordDate"] = pd.to_datetime(df["RecordDate"], errors="coerce")
    df["BirthDate"] = pd.to_datetime(df["BirthDate"], errors="coerce")

    # Calculate Age from BirthDate
    df["Age"] = (pd.Timestamp.today() - df["BirthDate"]).dt.days // 365

    df["DurationAsleep"] = df["DeepSleep"] + df["LightSleep"] + df["RemSleep"]

    df["SleepEfficiency"] = (df["DurationAsleep"] / df["TimeSpent"]) * 100
    df["SleepEfficiency"] = df["SleepEfficiency"].fillna(0).round(2)


    #Streamlit App Layout
    st.title("Sleep Activity Dashboard 💤")
    st.sidebar.header("Filter Data")

    #Dependent Filters
    selected_org = st.sidebar.selectbox("Select Organization", ["All"] + sorted(df["OrganizationName"].dropna().unique().tolist()))
    filtered_cohorts = df[df["OrganizationName"] == selected_org] if selected_org != "All" else df
    selected_cohort = st.sidebar.selectbox("Select Cohort", ["All"] + sorted(filtered_cohorts["CohortName"].dropna().unique().tolist()))
    filtered_programs = filtered_cohorts[filtered_cohorts["CohortName"] == selected_cohort] if selected_cohort != "All" else filtered_cohorts
    selected_program = st.sidebar.selectbox("Select Program", ["All"] + sorted(filtered_programs["ProgramName"].dropna().unique().tolist()))
    filtered_physicians = filtered_programs[filtered_programs["ProgramName"] == selected_program] if selected_program != "All" else filtered_programs
    selected_physician = st.sidebar.selectbox("Select Physician", ["All"] + sorted(filtered_physicians["PhysicianName"].dropna().unique().tolist()))
    filtered_participants = filtered_physicians[filtered_physicians["PhysicianName"] == selected_physician] if selected_physician != "All" else filtered_physicians
    selected_participant = st.sidebar.selectbox("Select Participant", ["All"] + sorted((filtered_participants["FirstName"] + " " + filtered_participants["LastName"]).dropna().unique().tolist()))
    selected_gender = st.sidebar.selectbox("Select Gender", ["All"] + sorted(filtered_participants["ParticipantGender"].dropna().unique().tolist()))
    selected_ethnicity = st.sidebar.selectbox("Select Ethnicity", ["All"] + sorted(filtered_participants["Ethnicity"].dropna().unique().tolist()))
    selected_race = st.sidebar.selectbox("Select Race", ["All"] + sorted(filtered_participants["Race"].dropna().unique().tolist()))
    selected_city = st.sidebar.selectbox("Select City", ["All"] + sorted(filtered_participants["City"].dropna().unique().tolist()))
    selected_country = st.sidebar.selectbox("Select Country", ["All"] + sorted(filtered_participants["Country"].dropna().unique().tolist()))

    # filter_cols = st.columns(6)  # Adjust the number of columns as needed

    # with filter_cols[0]:
        # selected_org = st.selectbox("Select Organization", ["All"] + sorted(df["OrganizationName"].dropna().unique().tolist()))
    # with filter_cols[1]:
        # selected_cohort = st.selectbox("Select Cohort", ["All"] + sorted(df["CohortName"].dropna().unique().tolist()))
    # with filter_cols[2]:
        # selected_program = st.selectbox("Select Program", ["All"] + sorted(df["ProgramName"].dropna().unique().tolist()))
    # with filter_cols[3]:
        # selected_physician = st.selectbox("Select Physician", ["All"] + sorted(df["PhysicianName"].dropna().unique().tolist()))
    # with filter_cols[4]:
        # selected_participant = st.selectbox("Select Participant", ["All"] + sorted((df["FirstName"] + " " + df["LastName"]).dropna().unique().tolist()))

    # # Additional filters in another row
    # filter_cols2 = st.columns(5)

    # with filter_cols2[0]:
        # selected_gender = st.selectbox("Select Gender", ["All"] + sorted(df["ParticipantGender"].dropna().unique().tolist()))
    # with filter_cols2[1]:
        # selected_ethnicity = st.selectbox("Select Ethnicity", ["All"] + sorted(df["Ethnicity"].dropna().unique().tolist()))
    # with filter_cols2[2]:
        # selected_race = st.selectbox("Select Race", ["All"] + sorted(df["Race"].dropna().unique().tolist()))
    # with filter_cols2[3]:
        # selected_city = st.selectbox("Select City", ["All"] + sorted(df["City"].dropna().unique().tolist()))
    # with filter_cols2[4]:
        # selected_country = st.selectbox("Select Country", ["All"] + sorted(df["Country"].dropna().unique().tolist()))





    # Apply Filters
    df_filtered = filtered_participants.copy()
    df_filtered["ParticipantName"] = df_filtered["FirstName"] + " " + df_filtered["LastName"]
    if selected_participant != "All":
        df_filtered = df_filtered[df_filtered["ParticipantName"] == selected_participant]
    if selected_gender != "All":
        df_filtered = df_filtered[df_filtered["ParticipantGender"] == selected_gender]
    if selected_ethnicity != "All":
        df_filtered = df_filtered[df_filtered["Ethnicity"] == selected_ethnicity]
    if selected_race != "All":
        df_filtered = df_filtered[df_filtered["Race"] == selected_race]
    if selected_city != "All":
        df_filtered = df_filtered[df_filtered["City"] == selected_city]
    if selected_country != "All":
        df_filtered = df_filtered[df_filtered["Country"] == selected_country]

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

    # 1️⃣ Average Sleep Duration per Organization
    st.subheader("Average Sleep Duration per Organization")
    avg_sleep_by_org = df_filtered.groupby("OrganizationName")["DurationInSeconds"].mean().reset_index()
    fig1 = px.bar(avg_sleep_by_org, x="OrganizationName", y="DurationInSeconds", color="OrganizationName",
                  title="Average Sleep Duration per Organization", labels={"DurationInSeconds": "Avg Sleep (Seconds)"}, barmode='group')
    st.plotly_chart(fig1)

    # 2️⃣ Sleep Duration Trend Over Time
    if not df_filtered.empty:
        st.subheader("Sleep Duration Trend Over Time")
        avg_sleep_trend = df_filtered.groupby("RecordDate")["DurationInSeconds"].mean().reset_index()
        fig2 = px.line(avg_sleep_trend, x="RecordDate", y="DurationInSeconds", markers=True,
                       title="Sleep Duration Trend Over Time",
                       labels={"DurationInSeconds": "Avg Sleep (Seconds)", "RecordDate": "Date"},
                       line_shape='linear', render_mode='svg')
        st.plotly_chart(fig2)
    else:
        st.warning("No data available for the selected filters.")

    # 3️⃣ Sleep Stages Breakdown (Stacked Bar Chart)
    if not df_filtered.empty:
        st.subheader("Sleep Stages Breakdown")
        
        # Summing up sleep stages
        sleep_stages = df_filtered.groupby("OrganizationName")[["DeepSleep", "LightSleep", "RemSleep", "AwakeTime"]].mean().reset_index()

        # Create stacked bar chart
        fig3 = px.bar(sleep_stages, x="OrganizationName", y=["DeepSleep", "LightSleep", "RemSleep", "AwakeTime"],
                      title="Average Sleep Stages per Organization",
                      labels={"value": "Avg Duration (Seconds)", "variable": "Sleep Stage"},
                      barmode="stack")

        st.plotly_chart(fig3)
    else:
        st.warning("No data available for Sleep Stages Breakdown.")

    # 4️⃣ Total Time in Bed vs. Actual Sleep (Scatter Plot)
    if not df_filtered.empty:
        st.subheader("Total Time in Bed vs. Actual Sleep")
        
        fig4 = px.scatter(df_filtered, x="TimeSpent", y="DurationAsleep",
                          title="Total Time in Bed vs. Actual Sleep",
                          labels={"TimeSpent": "Total Time in Bed (Seconds)", "DurationAsleep": "Actual Sleep Duration (Seconds)"},
                          opacity=0.7, color="OrganizationName")

        st.plotly_chart(fig4)
    else:
        st.warning("No data available for Time in Bed vs. Actual Sleep.")

    # 5️⃣ Sleep Start Time Distribution (Histogram)
    if not df_filtered.empty:
        st.subheader("Sleep Start Time Distribution")
        
        df_filtered["Sleep Start Hour"] = df_filtered["Start"].dt.hour

        fig5 = px.histogram(df_filtered, x="Sleep Start Hour", nbins=24, color="OrganizationName",
                            title="Sleep Start Time Distribution",
                            labels={"Sleep Start Hour": "Hour of the Day", "count": "Number of Participants"},
                            opacity=0.75)

        st.plotly_chart(fig5)
    else:
        st.warning("No data available for Sleep Start Time Distribution.")

    # Display Participants with Lowest Sleep Efficiency
    st.subheader("Participants with Lowest Sleep Efficiency")
    if not df_filtered.empty:
        lowest_efficiency_df = df_filtered.nsmallest(10, "SleepEfficiency")[["FirstName", "LastName", "OrganizationName", "SleepEfficiency"]]
        lowest_efficiency_df["ParticipantName"] = lowest_efficiency_df["FirstName"] + " " + lowest_efficiency_df["LastName"]
        lowest_efficiency_df = lowest_efficiency_df[["ParticipantName", "OrganizationName", "SleepEfficiency"]]
        st.dataframe(lowest_efficiency_df)
    else:
        st.warning("No data available for lowest sleep efficiency.")

    # Sleep Duration vs Age Group Visualization
    st.subheader("Sleep Duration vs Age Group")
    if not df_filtered.empty:
        fig_age = px.box(df_filtered, x="AgeGroup", y="DurationInSeconds", color="AgeGroup",
                          title="Sleep Duration Across Age Groups",
                          labels={"DurationInSeconds": "Sleep Duration (Seconds)", "AgeGroup": "Age Group"})
        st.plotly_chart(fig_age)
    else:
        st.warning("No data available for Sleep Duration vs Age Group.")

    # Sleep Duration vs Age Visualization
    st.subheader("Sleep Duration vs Age")
    if not df_filtered.empty:
        fig_age_scatter = px.scatter(df_filtered, x="Age", y="DurationInSeconds", color="Age",
                          title="Sleep Duration vs Age",
                          labels={"DurationInSeconds": "Sleep Duration (Seconds)", "Age": "Age"},
                          opacity=0.7)
        st.plotly_chart(fig_age_scatter)
    else:
        st.warning("No data available for Sleep Duration vs Age.")


# Ensure this function is accessible from app.py
if __name__ == "__main__":
    main()