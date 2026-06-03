```python
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
    "timestamp",
    "group_name",
    "project_title",
    "abstract",

    "leader_name",
    "leader_matrix",
    "leader_class",

    "member2_name",
    "member2_matrix",
    "member2_class",

    "member3_name",
    "member3_matrix",
    "member3_class",

    "member4_name",
    "member4_matrix",
    "member4_class",

    "contact_email",
    "contact_phone",
    "declaration"
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
        padding: 30px 35px;
        border-radius: 22px;
        color: white;
        box-shadow: 0 12px 30px rgba(0,0,0,0.16);
        border-bottom: 7px solid #C5A017;
        margin-bottom: 25px;
    }

    .main-title h1 {
        margin: 0;
        font-size: 40px;
        letter-spacing: 0.5px;
    }

    .main-title p {
        margin-top: 10px;
        font-size: 17px;
        opacity: 0.95;
    }

    .gold-card {
        background: #fff8dd;
        padding: 20px 24px;
        border-radius: 18px;
        border-left: 8px solid #C5A017;
        box-shadow: 0 8px 20px rgba(0,0,0,0.07);
        margin-bottom: 20px;
    }

    .blue-card {
        background: #eaf2ff;
        padding: 20px 24px;
        border-radius: 18px;
        border-left: 8px solid #001845;
        box-shadow: 0 8px 20px rgba(0,0,0,0.07);
        margin-bottom: 20px;
    }

    .white-card {
        background: white;
        padding: 20px 24px;
        border-radius: 18px;
        border: 1px solid #e6eaf2;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        margin-bottom: 18px;
    }

    .small-muted {
        color: #5b6575;
        font-size: 14px;
    }

    div[data-testid="stForm"] {
        background: rgba(255,255,255,0.90);
        border: 1px solid #e6eaf2;
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.08);
    }

    .stButton>button {
        background: linear-gradient(90deg, #001845, #003f88);
        color: white;
        border-radius: 12px;
        border: 0px;
        padding: 0.75rem 1.3rem;
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


def duplicate_check(project_title, leader_matrix):
    df = load_data()

    if df.empty:
        return False, ""

    title_norm = clean_text(project_title).lower()
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
        "Group Name": data["group_name"],
        "Project Title": data["project_title"],
        "Abstract": data["abstract"],

        "Group Leader Name": data["leader_name"],
        "Group Leader Matrix No.": data["leader_matrix"],
        "Group Leader Class": data["leader_class"],

        "Member 2 Name": data["member2_name"],
        "Member 2 Matrix No.": data["member2_matrix"],
        "Member 2 Class": data["member2_class"],

        "Member 3 Name": data["member3_name"],
        "Member 3 Matrix No.": data["member3_matrix"],
        "Member 3 Class": data["member3_class"],
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
        data["leader_matrix"],
        data["member2_matrix"],
        data["member3_matrix"],
        data["member4_matrix"]
    ]

    matrix_values = [clean_text(x).upper() for x in matrix_values if clean_text(x)]

    if len(matrix_values) != len(set(matrix_values)):
        errors.append("Duplicate matrix numbers detected within the same group.")

    if clean_text(data["member4_name"]) or clean_text(data["member4_matrix"]) or clean_text(data["member4_class"]):
        if not clean_text(data["member4_name"]):
            errors.append("Member 4 name is required if Member 4 information is provided.")
        if not clean_text(data["member4_matrix"]):
            errors.append("Member 4 matrix number is required if Member 4 information is provided.")
        if not clean_text(data["member4_class"]):
            errors.append("Member 4 class is required if Member 4 information is provided.")

    if not data["declaration"]:
        errors.append("Please tick the declaration before submitting.")

    return errors


def prepare_member_list(df):
    member_rows = []

    for _, row in df.iterrows():
        group_name = row.get("group_name", "")
        project_title = row.get("project_title", "")

        members = [
            ("Leader", row.get("leader_name", ""), row.get("leader_matrix", ""), row.get("leader_class", "")),
            ("Member 2", row.get("member2_name", ""), row.get("member2_matrix", ""), row.get("member2_class", "")),
            ("Member 3", row.get("member3_name", ""), row.get("member3_matrix", ""), row.get("member3_class", "")),
            ("Member 4", row.get("member4_name", ""), row.get("member4_matrix", ""), row.get("member4_class", "")),
        ]

        for role, name, matrix, student_class in members:
            if clean_text(name):
                member_rows.append({
                    "group_name": group_name,
                    "project_title": project_title,
                    "role": role,
                    "student_name": name,
                    "matrix_number": matrix,
                    "student_class": student_class
                })

    return pd.DataFrame(member_rows)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("### 📘 MAT633 System")

page = st.sidebar.radio(
    "Select Page",
    [
        "Student Registration",
        "Admin Dashboard",
        "Submission Guide"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Prepared for MAT633 Fuzzy Set Theory\n\n"
    "Dr Zahari Bin Md Rodzi\n\n"
    "Semester March -- September 2026"
)

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
        <p>
        Please complete this form once only for each group.
        Students from different classes may join the same group.
        Therefore, each member must enter their own class individually.
        The abstract must be written in English between 80 and 250 words.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("registration_form", clear_on_submit=False):

        st.subheader("A. Group and Project Information")

        group_name = st.text_input(
            "Group Name",
            placeholder="Example: Group 1 / Fuzzy Innovators / Alpha Team"
        )

        project_title = st.text_input(
            "Project Title",
            placeholder="Example: Traffic Congestion Assessment using Fuzzy Inference System"
        )

        abstract = st.text_area(
            "Project Abstract",
            height=190,
            placeholder=(
                "Write 80 to 250 words about the selected problem, "
                "input variables, output variable, and how FIS will be used."
            )
        )

        word_count = len(clean_text(abstract).split())
        st.caption(f"Current abstract word count: {word_count} words")

        st.divider()

        st.subheader("B. Group Members Information")
        st.markdown(
            "Each student must enter their own **name**, **matrix number**, and **class**. "
            "This is important because students from different classes may be in the same group."
        )

        st.markdown("#### Group Leader")

        c1, c2, c3 = st.columns(3)
        with c1:
            leader_name = st.text_input("Group Leader Name")
        with c2:
            leader_matrix = st.text_input("Group Leader Matrix No.")
        with c3:
            leader_class = st.text_input("Group Leader Class", placeholder="Example: CS2484A / CS2905B")

        st.markdown("#### Member 2")

        c4, c5, c6 = st.columns(3)
        with c4:
            member2_name = st.text_input("Member 2 Name")
        with c5:
            member2_matrix = st.text_input("Member 2 Matrix No.")
        with c6:
            member2_class = st.text_input("Member 2 Class", placeholder="Example: CS2484A / CS2905B")

        st.markdown("#### Member 3")

        c7, c8, c9 = st.columns(3)
        with c7:
            member3_name = st.text_input("Member 3 Name")
        with c8:
            member3_matrix = st.text_input("Member 3 Matrix No.")
        with c9:
            member3_class = st.text_input("Member 3 Class", placeholder="Example: CS2484A / CS2905B")

        st.markdown("#### Member 4 Optional")

        c10, c11, c12 = st.columns(3)
        with c10:
            member4_name = st.text_input("Member 4 Name Optional")
        with c11:
            member4_matrix = st.text_input("Member 4 Matrix No. Optional")
        with c12:
            member4_class = st.text_input("Member 4 Class Optional", placeholder="Example: CS2484A / CS2905B")

        st.divider()

        st.subheader("C. Contact Information")

        c13, c14 = st.columns(2)
        with c13:
            contact_email = st.text_input("Group Leader Email Optional")
        with c14:
            contact_phone = st.text_input("Group Leader Phone No. Optional")

        declaration = st.checkbox(
            "I confirm that the information submitted is correct and this form is submitted once only for my group."
        )

        submitted = st.form_submit_button("Submit Project Registration")

        if submitted:

            row = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "group_name": clean_text(group_name),
                "project_title": clean_text(project_title),
                "abstract": clean_text(abstract),

                "leader_name": clean_text(leader_name),
                "leader_matrix": clean_text(leader_matrix).upper(),
                "leader_class": clean_text(leader_class).upper(),

                "member2_name": clean_text(member2_name),
                "member2_matrix": clean_text(member2_matrix).upper(),
                "member2_class": clean_text(member2_class).upper(),

                "member3_name": clean_text(member3_name),
                "member3_matrix": clean_text(member3_matrix).upper(),
                "member3_class": clean_text(member3_class).upper(),

                "member4_name": clean_text(member4_name),
                "member4_matrix": clean_text(member4_matrix).upper(),
                "member4_class": clean_text(member4_class).upper(),

                "contact_email": clean_text(contact_email),
                "contact_phone": clean_text(contact_phone),
                "declaration": bool(declaration)
            }

            errors = validate_submission(row)

            is_dup, dup_msg = duplicate_check(
                row["project_title"],
                row["leader_matrix"]
            )

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
        <p>
        This page is for the lecturer/admin to monitor submitted groups,
        project titles, abstracts, students, matrix numbers, and individual student classes.
        </p>
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
            member_df = prepare_member_list(df)

            total_groups = len(df)
            total_students = len(member_df)
            total_titles = df["project_title"].nunique()
            total_classes = member_df["student_class"].replace("", pd.NA).dropna().nunique()
            latest = df["timestamp"].max()

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Total Groups", total_groups)
            with m2:
                st.metric("Total Students", total_students)
            with m3:
                st.metric("Project Titles", total_titles)
            with m4:
                st.metric("Student Classes", total_classes)

            st.caption(f"Latest submission: {latest}")

            st.divider()

            st.markdown("### Filter Submissions")

            class_options = ["All"] + sorted(
                member_df["student_class"]
                .replace("", pd.NA)
                .dropna()
                .unique()
                .tolist()
            )

            selected_class = st.selectbox("Filter by Student Class", class_options)

            search = st.text_input(
                "Search by group, title, name, matrix number, class, or abstract"
            )

            filtered = df.copy()

            if selected_class != "All":
                matched_groups = member_df[
                    member_df["student_class"] == selected_class
                ]["group_name"].unique()

                filtered = filtered[filtered["group_name"].isin(matched_groups)]

            if search:
                s = search.lower().strip()
                filtered = filtered[
                    filtered.apply(
                        lambda r: s in " ".join(map(str, r.values)).lower(),
                        axis=1
                    )
                ]

            st.markdown("### Group Submission List")
            st.dataframe(filtered, use_container_width=True, hide_index=True)

            st.markdown("### Student-Level List")
            filtered_member_df = prepare_member_list(filtered)

            if selected_class != "All":
                filtered_member_df = filtered_member_df[
                    filtered_member_df["student_class"] == selected_class
                ]

            if search:
                s = search.lower().strip()
                filtered_member_df = filtered_member_df[
                    filtered_member_df.apply(
                        lambda r: s in " ".join(map(str, r.values)).lower(),
                        axis=1
                    )
                ]

            st.dataframe(filtered_member_df, use_container_width=True, hide_index=True)

            st.markdown("### Summary by Student Class")

            class_summary = (
                member_df
                .replace("", pd.NA)
                .dropna(subset=["student_class"])
                .groupby("student_class")
                .size()
                .reset_index(name="number_of_students")
                .sort_values("student_class")
            )

            st.dataframe(class_summary, use_container_width=True, hide_index=True)

            st.divider()

            csv_group = filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Group-Level CSV",
                data=csv_group,
                file_name="mat633_group_project_submissions.csv",
                mime="text/csv"
            )

            csv_student = filtered_member_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Student-Level CSV",
                data=csv_student,
                file_name="mat633_student_level_list.csv",
                mime="text/csv"
            )

# =====================================================
# SUBMISSION GUIDE PAGE
# =====================================================

elif page == "Submission Guide":

    st.markdown("""
    <div class="gold-card">
        <h3>📖 Guide for Students</h3>
        <p>
        Please prepare your group name, project title, member details,
        individual class information, and abstract before filling in the form.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("What Students Need to Submit")

    st.markdown("""
    Each group must submit:

    - Group name
    - Project title
    - Abstract
    - Group leader name, matrix number, and class
    - Member 2 name, matrix number, and class
    - Member 3 name, matrix number, and class
    - Member 4 name, matrix number, and class, if applicable
    - Group leader contact information, optional
    """)

    st.subheader("Important Note About Class")

    st.info(
        "Students from different classes may join the same group. "
        "Therefore, class information must be entered individually for each student."
    )

    st.subheader("What to Write in the Abstract")

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
        "This project develops a Fuzzy Inference System for evaluating traffic "
        "congestion level based on vehicle density, average speed, and weather "
        "condition. The problem is selected because traffic condition is often "
        "uncertain and cannot be classified using fixed boundaries only. The "
        "proposed system uses linguistic variables such as low, medium, and high "
        "to represent the input and output conditions. Membership functions and "
        "fuzzy rules will be constructed using MATLAB Fuzzy Logic Toolbox. The "
        "expected output is a congestion level that can support better traffic "
        "monitoring and decision-making."
    )

    st.subheader("Before Submitting")

    st.checkbox("My group has 3 or 4 members.")
    st.checkbox("Every member has entered their own class.")
    st.checkbox("The project title is clear and related to Fuzzy Inference System.")
    st.checkbox("The abstract is between 80 and 250 words.")
    st.checkbox("All matrix numbers are correct.")
    st.checkbox("Only one submission will be made by the group leader.")
