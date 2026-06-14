
# =========================================================
# EXECUTIVE DASHBOARD
# =========================================================

# =========================================================
# AUTO INCIDENT / PROBLEM / CHANGE NUMBERING
# REMOVE THESE INPUTS FROM FORMS:
#
# incident_number
# problem_number
# change_number
#
# They will now auto-generate from MySQL triggers:
#
# INC00001
# PRB00001
# CHG00001
# =========================================================

import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
from datetime import datetime

import streamlit as st


# =========================================================
# LOAD ENV VARIABLES
# =========================================================
load_dotenv()

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ITSM Management System",
    page_icon="🛠️",
    layout="wide"
)

st.write("🚀 App Started Successfully")

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

/* Whole application background */
.stApp {
    background-color: #0f172a !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 50%,
        #334155 100%
    ) !important;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,.25);
    border-left: 5px solid #3b82f6;
}

[data-testid="stPlotlyChart"] {
    background: white;
    padding: 12px;
    border-radius: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,.20);
}

h1 {
    color: white !important;
}

h2,h3 {
    color: #e2e8f0 !important;
}

.stButton>button,
div[data-testid="stForm"] button,
div.stForm button {
    background: linear-gradient(135deg,#2563eb,#1e40af) !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* KPI cards visible */
[data-testid="stMetric"] label,
[data-testid="stMetric"] div,
[data-testid="stMetric"] p {
    color: #111827 !important;
}



/* White text on dark background */
label, p, span {
    color: white !important;
}

.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stNumberInput label {
    color: white !important;
}

button[data-baseweb="tab"] {
    color: white !important;
}

[data-testid="stForm"] {
    color: white !important;
}


/* Data editor toolbar */
[data-testid="stDataFrame"] button,
[data-testid="stDataEditor"] button,
button[kind="secondary"]{
    background-color:#1e40af !important;
    color:white !important;
    border:none !important;
}

[data-testid="stDataFrame"] svg,
[data-testid="stDataEditor"] svg{
    fill:white !important;
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE CONFIG
# =========================================================
DB_CONFIG = {
    "host": os.getenv("MYSQLHOST"),
    "port": int(os.getenv("MYSQLPORT", "3306")),
    "user": os.getenv("MYSQLUSER"),
    "password": os.getenv("MYSQLPASSWORD"),
    "database": os.getenv("MYSQLDATABASE")
}

st.sidebar.write("App Started")

try:
    conn = mysql.connector.connect(
    **DB_CONFIG,
    connection_timeout=10
)
    conn.close()
    st.sidebar.success("✅ Railway Database Connected")

except Exception as e:
    st.sidebar.error(f"❌ DB Error: {str(e)}")

# =========================================================
# DATABASE CONNECTION
# =========================================================
def get_connection():
    return mysql.connector.connect(
        **DB_CONFIG,
        connection_timeout=10
    )

# =========================================================
# DATABASE CONNECTION TEST
# =========================================================

#try:
#    test_conn = mysql.connector.connect(**DB_CONFIG)
#    test_conn.close()
#    st.sidebar.success("✅ Railway Database Connected")

#except Exception as e:
#    st.sidebar.error(f"❌ DB Error: {e}")
# =========================================================
# GENERIC FUNCTIONS
# =========================================================
def load_data(query):

    conn = get_connection()

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def execute_query(query, values=None):

    conn = get_connection()

    cursor = conn.cursor()

    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)

    conn.commit()

    conn.close()


def get_count(table_name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")

    count = cursor.fetchone()[0]

    conn.close()

    return count


# =========================================================
# GENERIC EDITABLE TABLE
# =========================================================
def editable_table(
    query_select,
    table_name,
    primary_key,
    editable_columns
):

    df = load_data(query_select)

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    if st.button(f"💾 Save Changes - {table_name}"):

        conn = get_connection()

        cursor = conn.cursor()

        for _, row in edited_df.iterrows():

            set_clause = ", ".join(
                [f"{col}=%s" for col in editable_columns]
            )

            update_query = f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE {primary_key}=%s
            """

            values = [row[col] for col in editable_columns]

            values.append(row[primary_key])

            cursor.execute(update_query, values)

        conn.commit()

        conn.close()

        st.success(
            f"{table_name} Updated Successfully"
        )


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("🛠️ ITSM")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Dashboard",
        "Incident",
        "Problem",
        "Change",
        "Users",
        "CI Assets",
        "Assignment Groups",
        "Categories",
        "Priorities",
        "Status",
        "Incident Problem Map",
        "Change CI Map"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================
if menu == "Dashboard":

    st.title("📊 IT Service Health Dashboard")
    st.caption("Executive View of Incidents, Problems, Changes and SLA Health")

    total_incidents = get_count("incident")
    total_problems = get_count("problem")
    total_changes = get_count("`change`")
    total_users = get_count("user")
    total_ci = get_count("ci_asset")

    try:
        sla_risk = load_data("""
        SELECT COUNT(*) cnt
        FROM incident
        WHERE sla_hours <= 8
        """)
        sla_count = int(sla_risk.iloc[0]["cnt"])
    except:
        sla_count = 0

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.metric("Incidents", total_incidents)
    k2.metric("Problems", total_problems)
    k3.metric("Changes", total_changes)
    k4.metric("Users", total_users)
    k5.metric("CI Assets", total_ci)
    k6.metric("SLA Risk", sla_count)

    st.divider()

    c1,c2 = st.columns(2)

    with c1:
        df1 = load_data("""
        SELECT p.priority_name, COUNT(*) total
        FROM incident i
        JOIN priority p ON i.priority_id=p.priority_id
        GROUP BY p.priority_name
        """)
        fig = px.bar(df1,x="priority_name",y="total",color="total",
                     title="Incidents by Priority",text_auto=True)
        st.plotly_chart(fig,use_container_width=True)

    with c2:
        df2 = load_data("""
        SELECT s.status_name, COUNT(*) total
        FROM incident i
        JOIN status s ON i.status_id=s.status_id
        GROUP BY s.status_name
        """)
        fig = px.pie(df2,names="status_name",values="total",
                     hole=.55,title="Incident Status")
        st.plotly_chart(fig,use_container_width=True)

    c1,c2 = st.columns(2)

    with c1:
        df3 = load_data("""
        SELECT c.category_name, COUNT(*) total
        FROM incident i
        JOIN category c ON i.category_id=c.category_id
        GROUP BY c.category_name
        ORDER BY total DESC
        """)
        fig = px.bar(df3,x="category_name",y="total",color="total",
                     title="Top Incident Categories")
        st.plotly_chart(fig,use_container_width=True)

    with c2:
        df9 = load_data("""
        SELECT ag.group_name, COUNT(*) total
        FROM incident i
        JOIN assignment_group ag
        ON i.assignment_group_id=ag.group_id
        GROUP BY ag.group_name
        ORDER BY total DESC
        """)
        fig = px.bar(df9,x="group_name",y="total",color="total",
                     title="Assignment Group Workload")
        st.plotly_chart(fig,use_container_width=True)

    st.subheader("👥 Assignment Group Performance")

    try:
        df_perf = load_data("""
        SELECT
        ag.group_name,
        COUNT(i.incident_id) total_incidents,
        ROUND(AVG(i.sla_hours),2) avg_sla
        FROM incident i
        JOIN assignment_group ag
        ON i.assignment_group_id=ag.group_id
        GROUP BY ag.group_name
        """)

        fig_perf = px.scatter(
            df_perf,
            x="avg_sla",
            y="total_incidents",
            size="total_incidents",
            color="group_name",
            title="Workload vs SLA Performance"
        )
        st.plotly_chart(fig_perf,use_container_width=True)
    except:
        pass

    st.subheader("🔥 Priority vs Impact Analysis")

    try:
        df_heat = load_data("""
        SELECT impact, priority_id, COUNT(*) total
        FROM incident
        GROUP BY impact, priority_id
        """)

        fig_heat = px.density_heatmap(
            df_heat,
            x="priority_id",
            y="impact",
            z="total"
        )
        st.plotly_chart(fig_heat,use_container_width=True)
    except:
        pass

    st.subheader("🚨 SLA Expiring Soon")

    try:
        sla_df = load_data("""
        SELECT incident_number,
               short_description,
               sla_hours
        FROM incident
        WHERE sla_hours <= 8
        ORDER BY sla_hours
        LIMIT 20
        """)

        if len(sla_df):
            st.warning(f"{len(sla_df)} incidents approaching SLA breach")
            st.dataframe(sla_df,use_container_width=True)
        else:
            st.success("No incidents near SLA breach")
    except:
        st.info("SLA monitoring unavailable")
    st.subheader("🔗 Relationship Analytics")

    col1, col2 = st.columns(2)

    with col1:
        try:
            query_map = """
            SELECT
                p.problem_number,
                COUNT(*) total_incidents
            FROM incident_problem_map ipm
            INNER JOIN problem p
                ON p.problem_id = ipm.problem_id
            GROUP BY p.problem_number
            ORDER BY total_incidents DESC
            """
            df_map = load_data(query_map)

            if not df_map.empty:
                fig_map = px.bar(
                    df_map,
                    x="problem_number",
                    y="total_incidents",
                    color="total_incidents",
                    title="Incident → Problem Mapping"
                )
                st.plotly_chart(fig_map, use_container_width=True)
        except Exception as e:
            st.error(e)

    with col2:
        try:
            query_ci = """
            SELECT
                ci.ci_name,
                COUNT(*) total_changes
            FROM change_ci_map ccm
            INNER JOIN ci_asset ci
                ON ci.ci_id = ccm.ci_id
            GROUP BY ci.ci_name
            ORDER BY total_changes DESC
            """
            df_ci = load_data(query_ci)

            if not df_ci.empty:
                fig_ci = px.bar(
                    df_ci,
                    x="ci_name",
                    y="total_changes",
                    color="total_changes",
                    title="Change → CI Mapping"
                )
                st.plotly_chart(fig_ci, use_container_width=True)
        except Exception as e:
            st.error(e)

    st.subheader("📈 Executive Insights")
    st.info(f"""
Total Incidents : {total_incidents}

Total Problems : {total_problems}

Total Changes : {total_changes}

SLA Risk Tickets : {sla_count}
""")



# =========================================================
# INCIDENT MODULE
# =========================================================
elif menu == "Incident":

    st.title("🚨 Incident Management")

    categories_df = load_data("SELECT * FROM category")
    priorities_df = load_data("SELECT * FROM priority")
    status_df = load_data("SELECT * FROM status")
    users_df = load_data("SELECT * FROM user")
    groups_df = load_data("SELECT * FROM assignment_group")

    tab1, tab2 = st.tabs([
        "➕ Add Incident",
        "📋 Manage Incidents"
    ])

    with tab1:

        with st.form("incident_form"):

            short_description = st.text_input(
                "Short Description"
            )

            detailed_description = st.text_area(
                "Detailed Description"
            )

            category_option = st.selectbox(
                "Category",
                categories_df["category_name"]
            )

            priority_option = st.selectbox(
                "Priority",
                priorities_df["priority_name"]
            )

            status_option = st.selectbox(
                "Status",
                status_df["status_name"]
            )

            reported_option = st.selectbox(
                "Reported By",
                users_df["full_name"]
            )

            assigned_option = st.selectbox(
                "Assigned To",
                users_df["full_name"]
            )

            group_option = st.selectbox(
                "Assignment Group",
                groups_df["group_name"]
            )

            impact = st.selectbox(
                "Impact",
                ["Low", "Medium", "High"]
            )

            urgency = st.selectbox(
                "Urgency",
                ["Low", "Medium", "High"]
            )

            sla_hours = st.number_input(
                "SLA Hours",
                min_value=1
            )

            submit = st.form_submit_button(
                "Add Incident"
            )

            if submit:

                category_id = categories_df.loc[
                    categories_df["category_name"] == category_option,
                    "category_id"
                ].values[0]

                priority_id = priorities_df.loc[
                    priorities_df["priority_name"] == priority_option,
                    "priority_id"
                ].values[0]

                status_id = status_df.loc[
                    status_df["status_name"] == status_option,
                    "status_id"
                ].values[0]

                reported_by = users_df.loc[
                    users_df["full_name"] == reported_option,
                    "user_id"
                ].values[0]

                assigned_to = users_df.loc[
                    users_df["full_name"] == assigned_option,
                    "user_id"
                ].values[0]

                group_id = groups_df.loc[
                    groups_df["group_name"] == group_option,
                    "group_id"
                ].values[0]

                query = """
                INSERT INTO incident
                (
                    short_description,
                    detailed_description,
                    category_id,
                    priority_id,
                    status_id,
                    reported_by,
                    assigned_to,
                    assignment_group_id,
                    impact,
                    urgency,
                    sla_hours
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

                values = (
                    short_description,
                    detailed_description,
                    int(category_id),
                    int(priority_id),
                    int(status_id),
                    int(reported_by),
                    int(assigned_to),
                    int(group_id),
                    impact,
                    urgency,
                    sla_hours
                )

                execute_query(query, values)

                st.success("Incident Added Successfully")

    with tab2:

        query = """
        SELECT
            incident_id,
            incident_number,
            short_description,
            detailed_description,
            impact,
            urgency,
            sla_hours
        FROM incident
        """

        editable_table(
            query,
            "incident",
            "incident_id",
            [
                "short_description",
                "detailed_description",
                "impact",
                "urgency",
                "sla_hours"
            ]
        )

# =========================================================
# PROBLEM MODULE
# =========================================================
elif menu == "Problem":

    st.title("🧩 Problem Management")

    priorities_df = load_data(
        "SELECT * FROM priority"
    )

    status_df = load_data(
        "SELECT * FROM status"
    )

    tab1, tab2 = st.tabs([
        "➕ Add Problem",
        "📋 Manage Problems"
    ])

    with tab1:

        with st.form("problem_form"):

            title = st.text_input("Title")

            root_cause = st.text_area(
                "Root Cause"
            )

            workaround = st.text_area(
                "Workaround"
            )

            priority_option = st.selectbox(
                "Priority",
                priorities_df["priority_name"]
            )

            status_option = st.selectbox(
                "Status",
                status_df["status_name"]
            )

            submit = st.form_submit_button(
                "Add Problem"
            )

            if submit:

                priority_id = priorities_df.loc[
                    priorities_df["priority_name"] == priority_option,
                    "priority_id"
                ].values[0]

                status_id = status_df.loc[
                    status_df["status_name"] == status_option,
                    "status_id"
                ].values[0]

                query = """
                INSERT INTO problem
                (
                    title,
                    root_cause,
                    workaround,
                    status_id,
                    priority_id
                )
                VALUES (%s,%s,%s,%s,%s)
                """

                values = (
                    title,
                    root_cause,
                    workaround,
                    int(status_id),
                    int(priority_id)
                )

                execute_query(query, values)

                st.success("Problem Added Successfully")

    with tab2:

        query = """
        SELECT
            problem_id,
            problem_number,
            title,
            root_cause,
            workaround
        FROM problem
        """

        editable_table(
            query,
            "problem",
            "problem_id",
            [
                "title",
                "root_cause",
                "workaround"
            ]
        )

# =========================================================
# CHANGE MODULE
# =========================================================
elif menu == "Change":

    st.title("🔄 Change Management")

    status_df = load_data(
        "SELECT * FROM status"
    )

    tab1, tab2 = st.tabs([
        "➕ Add Change",
        "📋 Manage Changes"
    ])

    with tab1:

        with st.form("change_form"):

            title = st.text_input("Title")

            change_type = st.text_input(
                "Change Type"
            )

            risk_level = st.selectbox(
                "Risk Level",
                ["Low", "Medium", "High"]
            )

            implementation_plan = st.text_area(
                "Implementation Plan"
            )

            rollback_plan = st.text_area(
                "Rollback Plan"
            )

            status_option = st.selectbox(
                "Status",
                status_df["status_name"]
            )

            scheduled_start = st.datetime_input(
                "Scheduled Start"
            )

            scheduled_end = st.datetime_input(
                "Scheduled End"
            )

            submit = st.form_submit_button(
                "Add Change"
            )

            if submit:

                status_id = status_df.loc[
                    status_df["status_name"] == status_option,
                    "status_id"
                ].values[0]

                query = """
                INSERT INTO `change`
                (
                    title,
                    change_type,
                    risk_level,
                    implementation_plan,
                    rollback_plan,
                    status_id,
                    scheduled_start,
                    scheduled_end
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """

                values = (
                    title,
                    change_type,
                    risk_level,
                    implementation_plan,
                    rollback_plan,
                    int(status_id),
                    scheduled_start,
                    scheduled_end
                )

                execute_query(query, values)

                st.success("Change Added Successfully")

    with tab2:

        query = """
        SELECT
            change_id,
            change_number,
            title,
            change_type,
            risk_level,
            implementation_plan,
            rollback_plan
        FROM `change`
        """

        editable_table(
            query,
            "`change`",
            "change_id",
            [
                "title",
                "change_type",
                "risk_level",
                "implementation_plan",
                "rollback_plan"
            ]
        )

# =========================================================
# USERS MODULE
# =========================================================
elif menu == "Users":

    st.title("👥 User Management")

    tab1, tab2 = st.tabs([
        "➕ Add User",
        "📋 Manage Users"
    ])

    with tab1:

        with st.form("user_form"):

            full_name = st.text_input(
                "Full Name"
            )

            email = st.text_input(
                "Email"
            )

            role_name = st.text_input(
                "Role Name"
            )

            department_id = st.number_input(
                "Department ID",
                min_value=1
            )

            submit = st.form_submit_button(
                "Add User"
            )

            if submit:

                query = """
                INSERT INTO user
                (
                    full_name,
                    email,
                    role_name,
                    department_id
                )
                VALUES (%s,%s,%s,%s)
                """

                values = (
                    full_name,
                    email,
                    role_name,
                    department_id
                )

                execute_query(query, values)

                st.success("User Added Successfully")

    with tab2:

        query = """
        SELECT
            user_id,
            full_name,
            email,
            role_name,
            department_id
        FROM user
        """

        editable_table(
            query,
            "user",
            "user_id",
            [
                "full_name",
                "email",
                "role_name",
                "department_id"
            ]
        )

# =========================================================
# CI ASSETS
# =========================================================
elif menu == "CI Assets":

    st.title("💻 CI Asset Management")

    users_df = load_data(
        "SELECT * FROM user"
    )

    tab1, tab2 = st.tabs([
        "➕ Add Asset",
        "📋 Manage Assets"
    ])

    with tab1:

        with st.form("asset_form"):

            ci_name = st.text_input(
                "CI Name"
            )

            ci_type = st.text_input(
                "CI Type"
            )

            owner_option = st.selectbox(
                "Owner",
                users_df["full_name"]
            )

            environment_name = st.selectbox(
                "Environment",
                ["DEV", "TEST", "UAT", "PROD"]
            )

            criticality = st.selectbox(
                "Criticality",
                ["Low", "Medium", "High"]
            )

            submit = st.form_submit_button(
                "Add Asset"
            )

            if submit:

                owner_id = users_df.loc[
                    users_df["full_name"] == owner_option,
                    "user_id"
                ].values[0]

                query = """
                INSERT INTO ci_asset
                (
                    ci_name,
                    ci_type,
                    owner_id,
                    environment_name,
                    criticality
                )
                VALUES (%s,%s,%s,%s,%s)
                """

                values = (
                    ci_name,
                    ci_type,
                    int(owner_id),
                    environment_name,
                    criticality
                )

                execute_query(query, values)

                st.success("CI Asset Added Successfully")

    with tab2:

        df = load_data(
            "SELECT * FROM ci_asset"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# ASSIGNMENT GROUPS
# =========================================================
elif menu == "Assignment Groups":

    st.title("👥 Assignment Groups")

    tab1, tab2 = st.tabs([
        "➕ Add Group",
        "📋 Manage Groups"
    ])

    with tab1:

        with st.form("group_form"):

            group_name = st.text_input(
                "Group Name"
            )

            submit = st.form_submit_button(
                "Add Group"
            )

            if submit:

                query = """
                INSERT INTO assignment_group
                (
                    group_name
                )
                VALUES (%s)
                """

                execute_query(
                    query,
                    (group_name,)
                )

                st.success("Group Added Successfully")

    with tab2:

        df = load_data(
            "SELECT * FROM assignment_group"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# CATEGORIES
# =========================================================
elif menu == "Categories":

    st.title("📂 Categories")

    tab1, tab2 = st.tabs([
        "➕ Add Category",
        "📋 Manage Categories"
    ])

    with tab1:

        with st.form("category_form"):

            category_name = st.text_input(
                "Category Name"
            )

            submit = st.form_submit_button(
                "Add Category"
            )

            if submit:

                query = """
                INSERT INTO category
                (
                    category_name
                )
                VALUES (%s)
                """

                execute_query(
                    query,
                    (category_name,)
                )

                st.success("Category Added Successfully")

    with tab2:

        df = load_data(
            "SELECT * FROM category"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# PRIORITIES
# =========================================================
elif menu == "Priorities":

    st.title("⚡ Priorities")

    tab1, tab2 = st.tabs([
        "➕ Add Priority",
        "📋 Manage Priorities"
    ])

    with tab1:

        with st.form("priority_form"):

            priority_name = st.text_input(
                "Priority Name"
            )

            submit = st.form_submit_button(
                "Add Priority"
            )

            if submit:

                query = """
                INSERT INTO priority
                (
                    priority_name
                )
                VALUES (%s)
                """

                execute_query(
                    query,
                    (priority_name,)
                )

                st.success("Priority Added Successfully")

    with tab2:

        df = load_data(
            "SELECT * FROM priority"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# STATUS
# =========================================================
elif menu == "Status":

    st.title("📌 Status")

    tab1, tab2 = st.tabs([
        "➕ Add Status",
        "📋 Manage Status"
    ])

    with tab1:

        with st.form("status_form"):

            status_name = st.text_input(
                "Status Name"
            )

            submit = st.form_submit_button(
                "Add Status"
            )

            if submit:

                query = """
                INSERT INTO status
                (
                    status_name
                )
                VALUES (%s)
                """

                execute_query(
                    query,
                    (status_name,)
                )

                st.success("Status Added Successfully")

    with tab2:

        df = load_data(
            "SELECT * FROM status"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# INCIDENT PROBLEM MAP
# =========================================================
elif menu == "Incident Problem Map":

    st.title("🔗 Incident Problem Mapping")

    incidents_df = load_data("""
    SELECT
        incident_id,
        incident_number
    FROM incident
    """)

    problems_df = load_data("""
    SELECT
        problem_id,
        problem_number
    FROM problem
    """)

    tab1, tab2 = st.tabs([
        "➕ Add Mapping",
        "📋 View Mappings"
    ])

    # =====================================================
    # ADD MAPPING
    # =====================================================
    with tab1:

        with st.form("incident_problem_form"):

            incident_option = st.selectbox(
                "Incident",
                incidents_df["incident_number"]
            )

            problem_option = st.selectbox(
                "Problem",
                problems_df["problem_number"]
            )

            submit = st.form_submit_button(
                "Add Mapping"
            )

            if submit:

                incident_id = incidents_df.loc[
                    incidents_df["incident_number"] == incident_option,
                    "incident_id"
                ].values[0]

                problem_id = problems_df.loc[
                    problems_df["problem_number"] == problem_option,
                    "problem_id"
                ].values[0]

                query = """
                INSERT INTO incident_problem_map
                (
                    incident_id,
                    problem_id
                )
                VALUES (%s,%s)
                """

                values = (
                    int(incident_id),
                    int(problem_id)
                )

                execute_query(query, values)

                st.success(
                    "Incident Problem Mapping Added Successfully"
                )

    # =====================================================
    # VIEW MAPPINGS
    # =====================================================
    with tab2:

        query = """
        SELECT
            m.map_id,
            i.incident_number,
            p.problem_number
        FROM incident_problem_map m
        JOIN incident i
            ON m.incident_id = i.incident_id
        JOIN problem p
            ON m.problem_id = p.problem_id
        """

        df = load_data(query)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# CHANGE CI MAP
# =========================================================
elif menu == "Change CI Map":

    st.title("🔗 Change CI Mapping")

    changes_df = load_data("""
    SELECT
        change_id,
        change_number
    FROM `change`
    """)

    ci_df = load_data("""
    SELECT
        ci_id,
        ci_name
    FROM ci_asset
    """)

    tab1, tab2 = st.tabs([
        "➕ Add Mapping",
        "📋 View Mappings"
    ])

    # =====================================================
    # ADD MAPPING
    # =====================================================
    with tab1:

        with st.form("change_ci_form"):

            change_option = st.selectbox(
                "Change",
                changes_df["change_number"]
            )

            ci_option = st.selectbox(
                "CI Asset",
                ci_df["ci_name"]
            )

            submit = st.form_submit_button(
                "Add Mapping"
            )

            if submit:

                change_id = changes_df.loc[
                    changes_df["change_number"] == change_option,
                    "change_id"
                ].values[0]

                ci_id = ci_df.loc[
                    ci_df["ci_name"] == ci_option,
                    "ci_id"
                ].values[0]

                query = """
                INSERT INTO change_ci_map
                (
                    change_id,
                    ci_id
                )
                VALUES (%s,%s)
                """

                values = (
                    int(change_id),
                    int(ci_id)
                )

                execute_query(query, values)

                st.success(
                    "Change CI Mapping Added Successfully"
                )

    # =====================================================
    # VIEW MAPPINGS
    # =====================================================
    with tab2:

        query = """
        SELECT
            m.map_id,
            c.change_number,
            ci.ci_name
        FROM change_ci_map m
        JOIN `change` c
            ON m.change_id = c.change_id
        JOIN ci_asset ci
            ON m.ci_id = ci.ci_id
        """

        df = load_data(query)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )