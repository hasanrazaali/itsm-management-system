import streamlit as st
import mysql.connector
import os

st.set_page_config(page_title="HF Test")

st.title("ITSM Deployment Test")

try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT")),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        connection_timeout=10
    )

    st.success("Database Connected")

    conn.close()

except Exception as e:
    st.error(str(e))