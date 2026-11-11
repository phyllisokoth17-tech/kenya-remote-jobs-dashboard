import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(
    page_title="Kenya Remote Jobs Analytics",
    page_icon="💻",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #1E293B;
    color: white;
}

h1 {
    color: #38BDF8;
}

div[data-testid="stMetric"] {
    background-color: #334155;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🇰🇪 Kenya Remote Jobs Analytics Dashboard")

job_category = st.selectbox(
    "Select Job Category",
    ["All", "Data Analyst", "Data Scientist", "Python Developer"]
)

st.write(
    "Explore remote job opportunities, salary estimates, "
    "and skills in demand."
)

# Sample job data
data = {
    "Job Title": [
        "Data Analyst",
        "Python Developer",
        "Data Scientist",
        "Data Annotator",
        "Business Analyst",
        "Machine Learning Engineer",
        "SQL Deeveloper",
        "AI Trainer",
        "Research Analyst",
        "Data Emtry Specialist",
        "BI Analyst",
        "Software Engineer",
        "Statistician",
        "Transcriptionist",
        "Virtual Assistant",
        "Cloud Engineer",
        "Database Administrator",
        "Data Engineer",
        "Cybersecurity Analyst",
        "Web Developer",
        "UX Designer",
        "Product Manager",
        "IT Support Specialist",
        "QA Tester",
        "Devops Engineer",
        "AI Research Assistant",
        "Data Quality Analyst",
        "Market Research Assistant",
        "Financial Analyst",
        "Project coordinator",
        "Content Writer",
        "Custormer Support Agent",
        "SEO Specialist",
        "BI Developer",
        "Operations Analyst"
    
    ],
    "Category": [
        "Data Analytics",
        "Programming",
        "Data Science",
        "Data Annotation",
        "Data Analytics",
        "Data Science",
        "Programming",
        "Data Annotation",
        "Data Annalytics",
        "Data Entry",
        "Data Analytics",
        "Programming",
        "Data Science",
        "Transcription",
        "Virtual Assistant",
        "Programming",
        "Data Management",
        "Data Engineering",
        "Cybersecurity",
        "Programming",
        "Design",
        "Management",
        "IT Support",
        "Software Testing",
        "Programming",
        "Data Science",
        "Data Analytics",
        "Research",
        "Finance",
        "Administration",
        "Writing",
        "Customer Service",
        "Marketing",
        "Data Analytics",
        "Operations"
    ],
    "Salary (USD)": [
        800, 1200, 1500, 500, 1000,
        2000, 1100, 700, 900, 400,
        1300, 1800, 1400, 600, 750,
        2200,
        1600,
        1900,
        1800,
        1400,
        1300,
        2500,
        900,
        1200,
        2100,
        1700,
        1100,
        1000,
        1800,
        950,
        800,
        700,
        1200,
        1600,
        1300
    ],   
    "Location": [
        "Remote - Kenya",
        "Remote - Africa",
        "Remote - Worldwide",
        "Remote - Kenya",
        "Remote - Africa",
        "Remote - Worldwide",
        "Remote - Africa",
        "Remote - Kenya",
        "Remote - Worldwide",
        "Remote - Kenya",
        "Remote - Africa",
        "Remote - worldwide",
        "Remote - Kenya",
        "Remote - Worldwide",
        "Remote - Africa",
        "Remote - Worldwide",
        "Remote - Africa",
        "Remote - Kenya",
        "Remote - Worldwide",
        "Remote - Africa",
        "Remote - Worldwide",
        "Remote - Africa",
        "Remote - Kenya",
        "Remote - Worldwide",
        "Remote - Africa",
        "Remote - Worldwide",
        "Remote - Kenya",
        "Remote - Africa",
        "Remote - Worldwide",
        "Remote - Kenya",
        "Remote - Worldwide",
        "Remote - Africa",
        "Remote - Worldwide",
        "Remote - Africa",
        "Remote - Kenya"
    ]
}

df = pd.DataFrame(data)

# Sidebar filter
st.sidebar.header("Filter Jobs")

# Reset Filters button
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state["category_filter"] = "All Categories"
    st.session_state["salary_range"] = (0, 2000)
    st.session_state["job_title_search"] = ""
    st.rerun()

# Job Category Filter
category = st.sidebar.selectbox(
    "Select Job Category",
    ["All Categories"] + list(df["Category"].unique()),
    key="category_filter"
)

if category != "All Categories":
    filtered_df = df[df["Category"] == category]
else:
    filtered_df = df.copy()

# Salary Range Filter
st.sidebar.header("Salary Filter")

salary_range = st.sidebar.slider(
    "Select Salary Range (USD)",
    min_value=0,
    max_value=2000,
    value=(0, 2000),
    key="salary_range"
)

filtered_df = filtered_df[
    (filtered_df["Salary (USD)"] >= salary_range[0]) &
    (filtered_df["Salary (USD)"] <= salary_range[1])
]

# Search Jobs by Title
st.subheader("🔎 Search Jobs by Title")

search = st.text_input(
    "Enter a job title",
    key="job_title_search"
)

if search:
    filtered_df = filtered_df[
        filtered_df["Job Title"].str.contains(
            search, case=False, na=False
        )
    ]

    #Salary Range Filter
    st.sidebar .header(" Salary Filter")

    min_salary = 0
    max_salary = 2000

    salary_range = st.sidebar .slider(
        "select Salary Range (USD)",
        min_value=min_salary,
        max_value=max_salary,
        value=(min_salary, max_salary)
    )

    filtered_df = filtered_df[
        (filtered_df["Salary (USD)"] >= salary_range[0])&
        (filtered_df["Salary (USD)"] <= salary_range[1])
    ]

# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Jobs", len(filtered_df))

col2.metric(
    "Average Salary",
    f"${filtered_df['Salary (USD)'].mean():,.0f}"
)

col3.metric(
    "Highest Salary",
    f"${filtered_df['Salary (USD)'].max():,.0f}"
)

col4.metric(
    "Most Popular Category",
    filtered_df["Category"].mode()[0] if not filtered_df.empty else "N/A"
)

# Salary chart
st.subheader("💰 Salary by Job Title")

st.bar_chart(
    filtered_df.set_index("Job Title")["Salary (USD)"]
)

# Job category distribution
st.subheader("📊 Job Category Distribution")

category_counts = filtered_df["Category"].value_counts()

st.bar_chart(category_counts)

# Average Salary by Category
st.subheader("💵 Average Salary by Job Category")

salary_by_category = filtered_df.groupby("Category")["Salary (USD)"].mean()

st.bar_chart(salary_by_category)

# Jobs by Location
st.subheader("🌍 Remote Jobs by Location")

location_counts = filtered_df["Location"].value_counts()

st.bar_chart(location_counts)

# Job Count by Location
st.subheader("📍 Job Count by Location")

location_summary = filtered_df.groupby("Location").size().reset_index(name="Number of Jobs")

st.dataframe(
    location_summary,
    use_container_width=True
)

 # Sort Jobs by Salary
st.subheader("📈 Sort Jobs by Salary")

sort_order = st.selectbox(
    "Choose salary order",
    ["Highest to Lowest", "Lowest to Highest"]
)

if sort_order == "Highest to Lowest":
    sorted_df = filtered_df.sort_values(
        by="Salary (USD)",
        ascending=False
    )
else:
    sorted_df = filtered_df.sort_values(
        by="Salary (USD)",
        ascending=True
    )

# Job listings
st.subheader("💼 Remote Job Listings")

jobs_per_page = 5

total_pages = max(1, (len(filtered_df) - 1) // jobs_per_page + 1)

if "page" not in st.session_state:
    st.session_state.page = 1

start_index = (st.session_state.page - 1) * jobs_per_page
end_index = start_index + jobs_per_page

page_df = sorted_df.iloc[start_index:end_index]

st.dataframe(
    page_df.style.highlight_max(
        subset=["Salary (USD)"],
        color="lightgreen"
    ),
    use_container_width=True
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Previous"):
        if st.session_state.page > 1:
            st.session_state.page -= 1
            st.rerun()

with col2:
    st.write(f"Page {st.session_state.page} of {total_pages}")

with col3:
    if st.button("Next ➡️"):
        if st.session_state.page < total_pages:
            st.session_state.page += 1
            st.rerun()

def generate_applications_pdf(dataframe):
        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(
            Paragraph("My Job Application Report", styles["Title"])
        )

        elements.append(Spacer(1, 15))

        elements.append(
            Paragraph(
                f"Total Applications: {len(dataframe)}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 15))

        table_data = [
            ["Job Title", "Company", "Status", "Date Applied", "Days Waiting"]
        ]

        for _, row in dataframe.iterrows():
            table_data.append([
                str(row["Job Title"]),
                str(row["Company"]),
                str(row["Status"]),
                str(row["Date Applied"]),
                str(row["Days Since Application"])
            ])

        table = Table(table_data, repeatRows=1)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))

        elements.append(table)

        doc.build(elements)
        buffer.seek(0)

        return buffer.getvalue()

st.download_button(
    label="📥 Download Jobs",
    data=filtered_df.to_csv(index=False),
    file_name="Kenya_Remote_Jobs.csv",
    mime="text/csv"
)

# Generate PDF Report
def generate_pdf(dataframe):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )

    elements = []
    total_jobs = len(dataframe)
    styles = getSampleStyleSheet()

    # Report title
    elements.append(
        Paragraph(
            "Kenya Remote Jobs Analytics Report",
            styles["Title"]
        )
    )

    if total_jobs > 0:
     highest_job = dataframe.loc[
        dataframe["Salary (USD)"].idxmax()
    ]

    lowest_job = dataframe.loc[
        dataframe["Salary (USD)"].idxmin()
    ]

    elements.append(
        Paragraph(
            f"Highest Paying Job: {highest_job['Job Title']} "
            f"(${highest_job['Salary (USD)']:,})",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Lowest Paying Job: {lowest_job['Job Title']} "
            f"(${lowest_job['Salary (USD)']:,})",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 10))

    # Report date
    report_date = datetime.now().strftime("%d %B %Y, %I:%M %p")

    elements.append(
        Paragraph(
            f"Report Date: {report_date}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 15))

    # Report statistics
    total_jobs = len(dataframe)

    if total_jobs > 0:
        average_salary = dataframe["Salary (USD)"].mean()
    else:
        average_salary = 0

    elements.append(
        Paragraph(
            f"Total Jobs: {total_jobs}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Average Salary: ${average_salary:,.2f}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
    Paragraph(
        f"Executive Summary: This report contains {total_jobs} "
        f"remote job opportunities, with an average salary of "
        f"${average_salary:,.2f}. Salaries range from "
        f"${dataframe['Salary (USD)'].min():,.0f} to "
        f"${dataframe['Salary (USD)'].max():,.0f}.",
        styles["Normal"]
    )
    )

    if not dataframe.empty:
        popular_category = dataframe["Category"].mode()[0]

    elements.append(
        Paragraph(
            f"Most Popular Job Category: {popular_category}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 15))
    elements.append(Spacer(1, 15)) 

    # Job table
    table_data = [
        ["Job Title", "Category", "Salary (USD)", "Location"]
    ]

    for _, row in dataframe.iterrows():
        table_data.append([
            row["Job Title"],
            row["Category"],
            f"${row['Salary (USD)']:,}",
            row["Location"]
        ])

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)

    # Page numbers
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)

        canvas.drawString(
            40, 20,
            "Kenya Remote Jobs Analytics | Generated automatically"
        )

        canvas.drawRightString(
            550, 20,
            f"Page {doc.page}"
        )
        canvas.restoreState()

    doc.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    buffer.seek(0)

    return buffer.getvalue()


# PDF Download Button
st.download_button(
    label="📄 Download Jobs as PDF",
    data=generate_pdf(filtered_df),
    file_name="Kenya_Remote_Jobs_Report.pdf",
    mime="application/pdf"
)

st.success("Dashboard is running successfully!")

# Skills Demand Chart
st.subheader("🧠 Skills in Demand")

skills_data = {
    "Skill": ["Python", "SQL", "Excel", "Power BI", "Machine Learning"],
    "Number of Jobs": [45, 38, 30, 25, 20]
}

skills_df = pd.DataFrame(skills_data)

st.bar_chart(
    skills_df.set_index("Skill")["Number of Jobs"]
)

# Job Category Pie Chart
st.subheader("🥧 Job Categories Breakdown")

import matplotlib.pyplot as plt                                                                                                                                                                                                                                                                                                                                

fig, ax = plt.subplots()

ax.pie(
    category_counts,
    labels=category_counts.index,
    autopct="%1.1f%%"
)

ax.set_title("Job Categories")

st.pyplot(fig)

st.subheader("💰 Salary Comparison by Job")

salary_chart = df.groupby("Job Title")["Salary (USD)"].mean()

st.bar_chart(salary_chart)

    # Job Details Section
st.subheader("📋 Job Details")

selected_job = st.selectbox(
    "Choose a job to view its details",
    df["Job Title"].unique()
)

job_details = df[df["Job Title"] == selected_job].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Estimated Salary",
    f"${job_details['Salary (USD)']:,}"
)

col2.metric(
    "🌍 Location",
    job_details["Location"]
)

col3.metric(
    "💼 Job Category",
    job_details["Category"]
)

# Skills required for each job
job_skills = {
    "Data Analyst": ["Python", "SQL", "Excel", "Power BI"],
    "Python Developer": ["Python", "Git", "APIs", "Problem Solving"],
    "Data Scientist": ["Python", "Statistics", "Machine Learning", "SQL"],
    "Data Annotator": ["Attention to Detail", "Labeling", "English"],
    "Business Analyst": ["Excel", "SQL", "Communication", "Data Analysis"],
    "Machine Learning Engineer": ["Python", "Machine Learning", "TensorFlow"],
    "SQL Deeveloper": ["SQL", "Database Management", "Python"],
    "AI Trainer": ["English", "Critical Thinking", "AI Evaluation"],
    "Research Analyst": ["Statistics", "Excel", "Research", "Python"],
    "Data Emtry Specialist": ["Typing", "Excel", "Accuracy"],
    "BI Analyst": ["Power BI", "SQL", "Excel", "Data Visualization"],
    "Software Engineer": ["Python", "Programming", "Git", "Problem Solving"],
    "Statistician": ["Statistics", "R", "Python", "Mathematics"],
    "Transcriptionist": ["Typing", "Listening", "English", "Grammar"],
    "Virtual Assistant": ["Communication", "Organization", "Excel", "Time Management"]
}

st.write("### 🧠 Skills Required")

for skill in job_skills[selected_job]:
    st.write(f"✅ {skill}")

    # Real Job Search Platforms
st.subheader("🌐 Find Real Remote Jobs")

st.write(
    "Our dashboard uses sample job data. "
    "Visit these platforms to search for actual job opportunities."
)

st.markdown(
    "[🔎 Search Jobs on BrighterMonday Kenya](https://www.brightermonday.co.ke/)"
)

st.markdown(
    "[🔎 Search Jobs on LinkedIn](https://www.linkedin.com/jobs/)"
)

st.markdown(
    "[🔎 Search Jobs on Indeed](https://www.indeed.com/)"
)

st.markdown(
    "[🔎 Search Remote Jobs on Remote OK](https://remoteok.com/)"
)

st.subheader("📩 Apply for This Job")

st.write("Click below to find remote job opportunities.")

st.link_button(
    "Search for Remote Jobs",
    "https://www.linkedin.com/jobs/search/?keywords=remote%20jobs"
)

st.subheader("🌟 Recommended Jobs")

if not filtered_df.empty:
    recommended_jobs = filtered_df.sort_values(
        by="Salary (USD)",
        ascending=False
    ).head(3)

    st.write("Here are the top 3 jobs based on salary:")

    st.dataframe(
        recommended_jobs,
        use_container_width=True
    )
else:
    st.write("No jobs available for recommendation.")

    st.subheader("📊 Salary Distribution")

st.write("See how salaries are distributed across remote jobs.")

if not filtered_df.empty:
    fig, ax = plt.subplots()

    ax.hist(filtered_df["Salary (USD)"], bins=5)

    ax.set_xlabel("Salary (USD)")
    ax.set_ylabel("Number of Jobs")
    ax.set_title("Distribution of Remote Job Salaries")

    st.pyplot(fig)

    plt.close(fig)

    st.subheader("🏆 Top 5 Highest-Paying Jobs")

top_jobs = filtered_df.nlargest(5, "Salary (USD)")

st.bar_chart(
    top_jobs.set_index("Job Title")["Salary (USD)"]
)

exchange_rate = st.sidebar.number_input(
    "USD to KES Exchange Rate",
    min_value=1.0,
    value=130.0,
    step=1.0
)

st.subheader("🇰🇪 Salaries in Kenyan Shillings")

filtered_df["Salary (KES)"] = (
    filtered_df["Salary (USD)"] * exchange_rate
)

st.dataframe(
    filtered_df[["Job Title", "Salary (USD)", "Salary (KES)"]],
    use_container_width=True
)

st.subheader("📊 Job Salary Comparison in KES")

kes_salary_chart = filtered_df.nlargest(
    5, "Salary (KES)"
)

st.bar_chart(
    kes_salary_chart.set_index("Job Title")["Salary (KES)"]
)

st.subheader("💰 Salary Statistics in KES")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Salary",
        f"KSh {filtered_df['Salary (KES)'].mean():,.0f}"
    )

with col2:
    st.metric(
        "Highest Salary",
        f"KSh {filtered_df['Salary (KES)'].max():,.0f}"
    )

with col3:
    st.metric(
        "Lowest Salary",
        f"KSh {filtered_df['Salary (KES)'].min():,.0f}"
    )

# Permanent Application Storage

def load_applications():
    try:
        with open("applications.json", "r") as file:
            applications = json.load(file)

        for application in applications:
            if isinstance(application.get("Date Applied"), str):
                application["Date Applied"] = datetime.strptime(
                    application["Date Applied"], "%Y-%m-%d"
                ).date()

        return applications
    
    except FileNotFoundError:
        return[]
    

def save_applications(applications):
    with open("applications.json", "w") as file:
        json.dump(applications, file, default=str, indent=4)

# Job Application Tracker
st.subheader("📨 Job Application Tracker")

st.write("Track the jobs you have applied for.")

if "applications" not in st.session_state:
    st.session_state.applications = load_applications()

for application in st.session_state.applications:
    application.setdefault("Date Applied", datetime.now().date())

with st.form("application_form"):
    job_applied = st.text_input("Job Title")
    application_date = st.date_input("Date Applied")
    company = st.text_input("Company Name")
    application_source = st.selectbox(
        "Where did you find this job?",
        ["LinkedIn", "BrighterMonday", "Indeed", "Remote OK", "Company Website", "Other"]
    )
    application_notes = st.text_area("Application Notes")

    application_status = st.selectbox(
        "Application Status",
        ["Applied", "Interviewing", "Rejected", "Accepted"]
    )

    submit_application = st.form_submit_button("Add Application")

    if submit_application:
        if job_applied and company:
            st.session_state.applications.append({
                "Job Title": job_applied,
                "Company": company,
                "Source": application_source,
                "Status": application_status,
                "Date Applied": application_date,
                "Notes": application_notes
            })

            save_applications(st.session_state.applications)
            st.success("Application added successfully!")
        else:
            st.warning("Please enter both job title and company name.")

if st.session_state.applications:
    applications_df = pd.DataFrame(st.session_state.applications)
    applications_df["Days Since Application"] = (
        pd.Timestamp.today().normalize() -
        pd.to_datetime(applications_df["Date Applied"])
    ).dt.days
    applications_df["Follow-up Reminder"] = applications_df.apply(
        lambda row: "Follow Up" if row["Days Since Application"] >=7
        and row["Status"] not in ["Accepted", "Rejected"]
        else "No Reminder",
        axis=1
    )

    total_applications = len(applications_df)

    follow_ups_due = len(
        applications_df[applications_df["Follow-up Reminder"] == "Follow Up"]
    )

    interviewing = len(
        applications_df[applications_df["Status"] == "Interviewing"]
    )

    accepted = len(
        applications_df[applications_df["Status"] == "Accepted"]
    )

    success_rate = (
        (accepted / total_applications) * 100
        if total_applications > 0
        else 0
    )

    col1, col2, col3, col4, col5  = st.columns(5)

    col1.metric("📨 Total Applications", total_applications)
    col2.metric("🎤 Interviews", interviewing)
    col3.metric("🏆 Accepted", accepted)
    col4.metric("⏰ Follow-Ups Due", follow_ups_due)
    col5.metric("📈 Success Rate", f"{success_rate:.1f}%")

    application_options = [
        f"{i}: {app['Job Title']} at {app['Company']} ({app['Status']})"
        for i, app in enumerate(st.session_state.applications)
    ]

    selected_application = st.selectbox(
        "Choose an application to delete",
        application_options
    )

    new_status = st.selectbox(
        "Update Application Status",
        ["Applied", "Interviewing", "Rejected", "Accepted"]
    )

    selected_index = int(selected_application.split(":")[0])

    edited_job_title = st.text_input(
        "Edit Job Title",
        value=st.session_state.applications[selected_index]["Job Title"]
    )

    edited_company = st.text_input(
        "Edit Company Name",
        value=st.session_state.applications[selected_index]["Company"]
    )

    edited_date = st.date_input(
        "Edit Application Date",
        value=st.session_state.applications[selected_index]["Date Applied"]
    )

    if st.button("💾 Save Job Details"):
        if edited_job_title and edited_company:
            st.session_state.applications[selected_index]["Job Title"] = edited_job_title
            st.session_state.applications[selected_index]["Company"] = edited_company
            st.session_state.applications[selected_index]["Date Applied"] = edited_date
            st.success("Job details updated!")
            st.rerun()
        else:
            st.warning("Please enter both job title and company name.")

    edited_notes = st.text_area(
        "Edit Application Notes",
        value=st.session_state.applications[
            int(selected_application.split(":")[0])
        ].get("Notes", "")
    )

    if st.button("💾 Save Edited Notes"):
        selected_index = int(selected_application.split(":")[0])
        st.session_state.applications[selected_index]["Notes"] = edited_notes
        save_applications(st.session_state.applications)
        st.success("Application notes updated!")
        st.rerun()

    if st.button("✏️ Update Application Status"):
        selected_index = int(selected_application.split(":")[0])

        st.session_state.applications[selected_index]["Status"] = new_status
        save_applications(st.session_state.applications)

        st.success("Application status updated!")
        st.rerun()

    if st.button("🗑️ Delete Selected Application"):
        selected_index = int(selected_application.split(":")[0])
        st.session_state.applications.pop(selected_index)
        save_applications(st.session_state.applications)
        st.success("Application deleted successfully!")
        st.rerun()

    application_search = st.text_input(
        " Search Applicationa",
        placeholder="Enter a Job title or company name..."
    )

    date_filter = st.selectbox(
        "Filter Application by Date",
        ["All Time", "Last 7 Days", "Last 30 Days", "Last 90 Days"]
    )
    status_filter = st.selectbox(
        "Filter Applications by Status",
        ["All", "Applied", "Interviewing", "Rejected", "Accepted"]
    )  

    source_filter = st.selectbox(
        "Filter Application by Source", 
        ["All Sources"] + 
        sorted(applications_df["Source"].dropna().unique().tolist())
    )

    if status_filter == "All":
     display_applications = applications_df.copy()
    else:
     display_applications = applications_df[
        applications_df["Status"] == status_filter
    ].copy()

    if source_filter != "All Sources":
        display_applications = display_applications[
            display_applications["Source"] == source_filter
        ].copy() 

    if application_search:
        display_applications = display_applications[display_applications["Job Title"].str.contains(
            application_search, case=False, na=False
        )
        |
display_applications["Company"].str.contains(
           application_search, case=False, na=False
        )
    ].copy()

    if date_filter == "Last 7 Days":
        display_applications = display_applications[
            pd.to_datetime(display_applications["Date Applied"]) >=
            pd.Timestamp.today().normalize() - pd.Timedelta(days=7)
        ].copy()

    elif date_filter == "Last 30 Days":
        display_applications = display_applications[
            pd.to_datetime(display_applications["Date Applied"]) >=
            pd.Timestamp.today().normalize() - pd.Timedelta(days=30)
        ].copy()

    elif date_filter == "Last 90 Days":
        display_applications = display_applications[
            pd.to_datetime(display_applications["Date Applied"]) >=
            pd.Timestamp.today().normalize() - pd.Timedelta(days=90)
        ].copy()

    sort_option = st.selectbox(
        "Sort Applications By",
        ["Newest First", "Oldest First", "Longest Waiting"]
    )

    if sort_option == "Newest First":
        display_applications = display_applications.sort_values(
            "Date Applied", ascending=False
        )
    elif sort_option == "Oldest First":
        display_applications = display_applications.sort_values(
            "Date Applied", ascending=True
        )
    else:
        display_applications = display_applications.sort_values(
            "Days Since Application", ascending=False
        )
    
    st.download_button(
        label="📄 Download Applications as PDF",
        data=generate_applications_pdf(display_applications),
        file_name="My_Job_Applications.pdf",
        mime="application/pdf"
    )

    st.dataframe(
    display_applications,
    use_container_width=True
)

    if date_filter == "Last 7 Days":
        display_applications = display_applications[
            pd.to_datetime(display_applications["Date Applied"]) >=
            pd.Timestamp.today().normalize() - pd.Timedelta(days=7)
        ].copy()

    elif date_filter == "Last 30 Days":
        display_applications = display_applications[
            pd.to_datetime(display_applications["Date Applied"]) >=
            pd.Timestamp.today().normalize() - pd.Timedelta(days=30)
        ].copy()

    elif date_filter == "Last 90 Days":
        display_applications = display_applications[
            pd.to_datetime(display_applications["Date Applied"]) >=
            pd.Timestamp.today().normalize() - pd.Timedelta(days=90)
        ].copy()

    st.download_button(
        label="Download Application Records",
        data=display_applications.to_csv(index=False),
        file_name="My_Job_Applications.csv",
        mime="text/csv"
    )
    
    st.subheader("📅 Application Activity Timeline")

    timeline_data = applications_df.groupby(
        "Date Applied"
    ).size().reset_index(name="Applications")

    timeline_data = timeline_data.sort_values("Date Applied")

    st.line_chart(
        timeline_data.set_index("Date Applied")["Applications"]
    )

    st.subheader("🏆 Success Rate by Company")

    company_success = applications_df.groupby("Company").agg(
        Total=("Status", "count"),
        Accepted=("Status", lambda x: (x == "Accepted").sum())
    )

    company_success["Success Rate (%)"] = (
        company_success["Accepted"] / company_success["Total"] * 100
    )

    st.dataframe(company_success, use_container_width=True)

    st.subheader("🏢 Applications by Company")

    company_counts = applications_df["Company"].value_counts()

    st.bar_chart(company_counts)

    st.subheader("📊 Applications by Source")

    source_counts = applications_df.get(
    "Source",
    pd.Series("Not specified", index=applications_df.index)
).fillna("Not specified").value_counts()

    st.bar_chart(source_counts)
    st.subheader("⏰ Applications Needing Follow-Up")

    follow_up_list = applications_df[
        applications_df["Follow-up Reminder"] == "Follow Up"
    ]

    if not follow_up_list.empty:
        st.dataframe(
            follow_up_list[
                ["Job Title", "Company", "Status", "Days Since Application"]
            ],
            use_container_width=True
        )
    else:
        st.success("No applications currently need follow-up!")

    st.subheader(" Application Status Breakdown")

    status_counts = applications_df["Status"].value_counts()

    st.write("### 📋 Application Progress Summary")

    for status in ["Applied", "Interviewing", "Rejected", "Accepted"]:
        count = status_counts.get(status, 0)
        st.write(f"**{status}:** {count} applications")

    st.bar_chart(status_counts)

else:
    st.info("No job applications recorded yet.")