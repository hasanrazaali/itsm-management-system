---
title: ITSM Database
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# ITSM Analytics System

An AI-powered IT Service Management (ITSM) Analytics Platform built using:

- MySQL
- Python
- Streamlit
- Plotly
- Hugging Face Spaces

This project provides analytics and dashboarding capabilities for:

- Incident Management
- Problem Management
- Change Management
- SLA Monitoring
- IT Operations Analytics

# Features
Incident Management
Incident Logging
Priority Tracking
SLA Monitoring
Status Tracking
Incident Analytics
MTTR Analysis
Problem Management
Root Cause Tracking
Problem Trends
Workaround Management
Change Management
Change Scheduling
Risk Tracking
Rollback Planning
Change Success Analysis
Dashboard Analytics
KPI Dashboard
Priority Analysis
Monthly Trends
Open vs Closed Incidents
SLA Breach Tracking
Assignment Group Analytics

# Technologies Used
Technology	Purpose
MySQL	Database
Python	Backend
SQLAlchemy	Database Connectivity
Pandas	Data Analysis
Gradio	Dashboard UI
Plotly	Interactive Charts
Hugging Face	Cloud Deployment
Project Structure

# Project Architecture

```text
MySQL Database
       ↓
Python + SQLAlchemy
       ↓
Pandas Data Processing
       ↓
Gradio Dashboard
       ↓
Hugging Face Deployment

itsm_project/
│
├── app.py
├── db_connection.py
├── analytics.py
├── requirements.txt
├── README.md
│
├── sql/
│   ├── schema.sql
│   ├── inserts.sql
│
├── modules/
│   ├── incidents.py
│   ├── problems.py
│   ├── changes.py
│
├── assets/
│
└── notebooks/

# Database Tables
Master Tables
departments
users
category
priority
status
assignment_group

Transaction Tables
incident
problem
change
Mapping Tables
incident_problem_map
change_ci_map

Future AI Enhancements
AI Ticket Classification
Sentiment Analysis
Root Cause Prediction
Auto Assignment
GenAI ITSM Assistant
Change Risk Prediction
Predictive SLA Breach Alerts
Learning Objectives

This project demonstrates:

Relational Database Design
ITSM Data Modeling
SQL Querying
Python Integration
Dashboard Development
Cloud Deployment
AI Integration
Author

Hasan Raza Ali

Senior Lead Data Science | AI & Analytics

License

This project is for educational and research purposes.