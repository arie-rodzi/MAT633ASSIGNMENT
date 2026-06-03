import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import re

# =====================================================
# MAT633 FUZZY SET THEORY PROJECT REGISTRATION SYSTEM
# Prepared for: Dr Zahari Bin Md Rodzi
# Semester: March -- September 2026
# =====================================================

st.set_page_config(
    page_title="MAT633 Project Registration",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "mat633_project_submissions.csv"
ADMIN_PASSWORD = "mat633admin"  # Change this password before real deployment

COLUMNS = [
    "timestamp", "class_group", "project_title", "abstract",
    "leader_name", "leader_matrix",
    "member2_name", "member2_matrix",
    "member3_name", "member3_matrix",
    "member4_name", "member4_matrix",
    "contact_email", "contact_phone", "declaration"
]

if not DATA_FILE.exists():
    pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)

# =====================================================
# PREMIUM CSS DESIGN
# =====================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f4f8ff 0%, #ffffff 45%, #fff7df 100%);
    }
    .main-title {
        background: linear-gradient(90deg, #001845, #003f88);
        padding: 28px 34px;
        border-radius: 22px;
        color: white;
        box-shadow: 0 12px 30px rgba(0,0,0,0.16);
        border-bottom: 6px solid #C5A017;
        margin-bottom: 25px;
    }
    .main-title h1 {
        margin: 0;
        font-size: 38px;
        letter-spacing: 0.5px;
    }
    .main-title p {
        margin-top: 8px;
        font-size: 17px;
        opacity: 0.95;
    }
    .gold-card {
        background: #fff8dd;
        padding: 18px 22px;
        border-radius: 18px;
        border-left: 7px solid #C5A017;
        box-shadow: 0 8px 20px rgba(0,0,0,0.07);
        margin-bottom: 18px;
    }
    .blue-card {
        background: #eaf2ff;
        padding: 18px 22px;
        border-radius: 18px;
        border-left: 7px solid #001845;
        box-shadow: 0 8px 20px rgba(0,0,0,0.07);
        margin-bottom: 18px;
    }
    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #e6eaf2;
        box-shadow: 0 8px 22px rgba(0,0,0,0.08);
        text-align: center;
    }
    .small-muted {
        color: #5b6575;
        font-size: 14px;
    }
    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.88);
        border: 1px solid #e6eaf2;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.08);
    }
    .stButton>button {
        background: linear-gradient(90deg, #001845, #003f88);
        color: white;
        border-radius: 12px;
        border: 0px;
        padding: 0.7rem 1.2rem;
        font-weight: 700;
    }
    .stDownloadButton>button {
        border-radius: 12px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# HELPER FUNCTIONS
# =====================================================
def clean_text(text: str) -> str:
    if text is None:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def load_data() -> pd.DataFrame:
    try:
        return pd.read_csv(DATA_FILE)
    except Exception:
        return pd.DataFrame(columns=COLUMNS)


def save_submission(row: dict):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


def duplicate_check(class_group, title, leader_matrix):
    df = load_data()
    if df.empty:
        return False, ""
    title_norm = clean_text(title).lower()
    leader_norm = clean_text(leader_matrix).lower()
    same_title = df["project_title"].fillna("").str.strip().str.lower().eq(title_norm)
    same_leader = df["leader_matrix"].fillna("").str.strip().str.lower().eq(leader_norm)
    if same_leader.any():
        return True, "This group leader matrix number has already submitted a registration."
    if same_title.any():
        return True, "This project title already exists. Please check with the lecturer if this is intentional."
    return False, ""


def validate_submission(data):
    errors = []
    required_fields = {
        "Class": data["class_group"],
        "Project Title": data["project_title"],
        "Abstract": data["abstract"],
        "Group Leader Name": data["leader_name"],
        "Group Leader Matrix No.": data["leader_matrix"],
        "Member 2 Name": data["member2_name"],
        "Member 2 Matrix No.": data["member2_matrix"],
        "Member 3 Name": data["member3_name"],
        "Member 3 Matrix No.": data["member3_matrix"],
    }
    for label, value in required_fields.items():
        if not clean_text(value):
            errors.append(f"{label} is required.")

    abstract_words = len(clean_text(data["abstract"]).split())
    if abstract_words < 80:
        errors.append("Abstract is too short. Please write at least 80 words.")
    if abstract_words > 250:
        errors.append("Abstract is too long. Please keep it within 250 words.")

    matrix_values = [
        data["leader_matrix"], data["member2_matrix"], data["member3_matrix"],
        data["member4_matrix"]
    ]
    matrix_values = [clean_text(x).upper() for x in matrix_values if clean_text(x)]
    if len(matrix_values) != len(set(matrix_values)):
        errors.append("Duplicate matrix numbers detected within the same group.")

    if not data["declaration"]:
        errors.append("Please tick the declaration before submitting.")

    return errors

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.markdown("### 📘 MAT633 System")
page = st.sidebar.radio("Select Page", ["Student Registration", "Admin Dashboard", "Submission Guide"])
st.sidebar.markdown("---")
st.sidebar.info("Prepared for MAT633 Fuzzy Set Theory\n\nDr Zahari Bin Md Rodzi\n\nSemester March -- September 2026")

# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="main-title">
    <h1>MAT633 Fuzzy Set Theory</h1>
    <p>Online Group Project Registration System | Semester March -- September 2026</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# STUDENT REGISTRATION PAGE
# =====================================================
if page == "Student Registration":
    st.markdown("""
    <div class="gold-card">
        <h3>📌 Student Instruction</h3>
        <p>Please complete this form once only for each group. The group leader should submit the project title, group member details, class, and abstract. The abstract should be written in English between 80 and 250 words.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("registration_form", clear_on_submit=False):
        st.subheader("A. Class and Project Information")
        col1, col2 = st.columns([1, 2])
        with col1:
            class_group = st.selectbox(
                "Class",
                ["", "CS248", "CS290", "Other"],
                help="Choose your programme/class."
            )
            if class_group == "Other":
                class_group = st.text_input("Please specify class")
        with col2:
            project_title = st.text_input(
                "Project Title",
                placeholder="Example: Traffic Congestion Assessment using Fuzzy Inference System"
            )

        abstract = st.text_area(
            "Project Abstract",
            height=180,
            placeholder="Write 80 to 250 words about the selected problem, input variables, output variable, and how FIS will be used."
        )
        word_count = len(clean_text(abstract).split())
        st.caption(f"Current abstract word count: {word_count} words")

        st.subheader("B. Group Members")
        st.markdown("The group should normally consist of 3 to 4 students.")

        c1, c2 = st.columns(2)
        with c1:
            leader_name = st.text_input("Group Leader Name")
        with c2:
            leader_matrix = st.text_input("Group Leader Matrix No.")

        c3, c4 = st.columns(2)
        with c3:
            member2_name = st.text_input("Member 2 Name")
        with c4:
            member2_matrix = st.text_input("Member 2 Matrix No.")

        c5, c6 = st.columns(2)
        with c5:
            member3_name = st.text_input("Member 3 Name")
        with c6:
            member3_matrix = st.text_input("Member 3 Matrix No.")

        c7, c8 = st.columns(2)
        with c7:
            member4_name = st.text_input("Member 4 Name (optional)")
        with c8:
            member4_matrix = st.text_input("Member 4 Matrix No. (optional)")

        st.subheader("C. Contact Information")
        c9, c10 = st.columns(2)
        with c9:
            contact_email = st.text_input("Group Leader Email (optional)")
        with c10:
            contact_phone = st.text_input("Group Leader Phone No. (optional)")

        declaration = st.checkbox("I confirm that the information submitted is correct and this form is submitted once only for my group.")

        submitted = st.form_submit_button("Submit Project Registration")

        if submitted:
            row = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "class_group": clean_text(class_group),
                "project_title": clean_text(project_title),
                "abstract": clean_text(abstract),
                "leader_name": clean_text(leader_name),
                "leader_matrix": clean_text(leader_matrix).upper(),
                "member2_name": clean_text(member2_name),
                "member2_matrix": clean_text(member2_matrix).upper(),
                "member3_name": clean_text(member3_name),
                "member3_matrix": clean_text(member3_matrix).upper(),
                "member4_name": clean_text(member4_name),
                "member4_matrix": clean_text(member4_matrix).upper(),
                "contact_email": clean_text(contact_email),
                "contact_phone": clean_text(contact_phone),
                "declaration": bool(declaration)
            }
            errors = validate_submission(row)
            is_dup, dup_msg = duplicate_check(row["class_group"], row["project_title"], row["leader_matrix"])
            if is_dup:
                errors.append(dup_msg)

            if errors:
                st.error("Please correct the following issue(s):")
                for e in errors:
                    st.write(f"- {e}")
            else:
                save_submission(row)
                st.success("Your group project registration has been submitted successfully.")
                st.balloons()

# =====================================================
# ADMIN DASHBOARD
# =====================================================
elif page == "Admin Dashboard":
    st.markdown("""
    <div class="blue-card">
        <h3>🔐 Admin Dashboard</h3>
        <p>This page is for the lecturer/admin to monitor submitted groups, project titles, abstracts, and class distribution.</p>
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input("Admin Password", type="password")
    if password != ADMIN_PASSWORD:
        st.warning("Enter the admin password to view submissions.")
    else:
        df = load_data()
        if df.empty:
            st.info("No submissions yet.")
        else:
            total = len(df)
            class_count = df["class_group"].nunique()
            latest = df["timestamp"].max()

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Groups", total)
            with m2:
                st.metric("Number of Classes", class_count)
            with m3:
                st.metric("Latest Submission", latest)

            st.markdown("### Filter Submissions")
            classes = ["All"] + sorted(df["class_group"].dropna().unique().tolist())
            selected_class = st.selectbox("Filter by Class", classes)
            search = st.text_input("Search by title, name, matrix number, or abstract")

            filtered = df.copy()
            if selected_class != "All":
                filtered = filtered[filtered["class_group"] == selected_class]
            if search:
                s = search.lower().strip()
                filtered = filtered[filtered.apply(lambda r: s in " ".join(map(str, r.values)).lower(), axis=1)]

            st.markdown("### Submission List")
            st.dataframe(filtered, use_container_width=True, hide_index=True)

            st.markdown("### Class Summary")
            summary = df.groupby("class_group", dropna=False).size().reset_index(name="number_of_groups")
            st.dataframe(summary, use_container_width=True, hide_index=True)

            csv = filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Filtered CSV",
                data=csv,
                file_name="mat633_project_submissions_filtered.csv",
                mime="text/csv"
            )

            full_csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Full CSV",
                data=full_csv,
                file_name="mat633_project_submissions_full.csv",
                mime="text/csv"
            )

# =====================================================
# SUBMISSION GUIDE PAGE
# =====================================================
elif page == "Submission Guide":
    st.markdown("""
    <div class="gold-card">
        <h3>📖 Guide for Students</h3>
        <p>Please prepare your project title and abstract before filling in the form.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("What to Write in the Abstract?")
    st.write("Your abstract should briefly explain:")
    st.markdown("""
    - The real-life problem selected by your group.
    - Why the problem involves uncertainty or vague decision-making.
    - The input variables and output variable proposed for the FIS model.
    - How MATLAB Fuzzy Logic Toolbox will be used.
    - The expected benefit of the fuzzy system.
    """)

    st.subheader("Example Abstract")
    st.info(
        "This project develops a Fuzzy Inference System for evaluating traffic congestion level based on vehicle density, average speed, and weather condition. The problem is selected because traffic condition is often uncertain and cannot be classified using fixed boundaries only. The proposed system uses linguistic variables such as low, medium, and high to represent the input and output conditions. Membership functions and fuzzy rules will be constructed using MATLAB Fuzzy Logic Toolbox. The expected output is a congestion level that can support better traffic monitoring and decision-making."
    )

    st.subheader("Before Submitting")
    st.checkbox("My group has 3 or 4 members.")
    st.checkbox("The project title is clear and related to Fuzzy Inference System.")
    st.checkbox("The abstract is between 80 and 250 words.")
    st.checkbox("All matrix numbers are correct.")
    st.checkbox("Only one submission will be made by the group leader.")
