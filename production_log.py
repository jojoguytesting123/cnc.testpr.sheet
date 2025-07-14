import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="PCI Production Logger", page_icon="🏭", layout="wide")
st.title("🏭 PCI Multi-Department Production Logger")

# Department mapping
departments = {
    "CNC 🛠️": ("cnc", "cnc_log.csv"),
    "Lids 🧢": ("lids", "lids_log.csv"),
    "Water Test 💧": ("water", "water_test_log.csv")
}

# Admin login sidebar
admin_mode = st.sidebar.checkbox("🔐 Admin Mode")
if admin_mode:
    password = st.sidebar.text_input("Enter Admin Password", type="password")
    if password != "pci123":
        st.sidebar.warning("Incorrect password")
        st.stop()
    st.sidebar.success("Access granted")
    st.header("🔎 Admin Dashboard")
    admin_choice = st.selectbox("Select Department to View", list(departments.keys()))
    _, admin_file = departments[admin_choice]
    if os.path.exists(admin_file):
        df = pd.read_csv(admin_file)
        st.subheader(f"📈 {admin_choice} Production Data")
        st.dataframe(df)
        st.download_button(f"📥 Download {admin_choice} Data", df.to_csv(index=False), admin_file, "text/csv")
        st.markdown("---")
        st.subheader("📊 Summary Stats")
        st.write(df.describe(include="all"))
    else:
        st.warning("No data available for this department yet.")
    st.stop()

# User side — department selection
choice = st.radio("Select Your Department", list(departments.keys()))
selected_key, file_path = departments[choice]

# Save to CSV
def save_entry(entry, path):
    df = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(path, index=False)

# CNC Department
if selected_key == "cnc":
    st.header("🛠️ CNC Production Form")
    with st.form("cnc_form"):
        operator = st.text_input("Operator Name", "")
        date = st.date_input("Date", datetime.today())
        male = st.number_input("Male Cuts", 0, 1000, 0)
        female = st.number_input("Female Cuts", 0, 1000, 0)
        rsc = st.number_input("RSC Cuts", 0, 1000, 0)
        issues = st.text_area("Problems / Slowdowns (optional)", "")
        submit = st.form_submit_button("Submit")

    if submit:
        entry = {
            "Date": date.strftime("%Y-%m-%d"),
            "Operator": operator,
            "Male Cuts": male,
            "Female Cuts": female,
            "RSC Cuts": rsc,
            "Issues": issues.strip()
        }
        save_entry(entry, file_path)
        st.success("✅ CNC entry saved!")

# Lids Department
elif selected_key == "lids":
    st.header("🧢 Lids Production Form")
    with st.form("lids_form"):
        worker = st.text_input("Worker Name", "")
        date = st.date_input("Date", datetime.today())
        lids_done = st.number_input("Completed Lids", 0, 1000, 0)
        submit = st.form_submit_button("Submit")

    if submit:
        entry = {
            "Date": date.strftime("%Y-%m-%d"),
            "Worker": worker,
            "Completed Lids": lids_done
        }
        save_entry(entry, file_path)
        st.success("✅ Lids entry saved!")

# Water Test Department
elif selected_key == "water":
    st.header("💧 Water Test Production Form")
    with st.form("water_form"):
        tester = st.text_input("Tester Name", "")
        date = st.date_input("Date", datetime.today())
        good_lids = st.number_input("Good Lids", 0, 1000, 0)
        bad_lids = st.number_input("Bad Lids", 0, 1000, 0)
        good_threads = st.number_input("Good Threads", 0, 1000, 0)
        bad_threads = st.number_input("Bad Threads", 0, 1000, 0)
        complete_tests = st.number_input("Complete Tests", 0, 1000, 0)
        submit = st.form_submit_button("Submit")

    if submit:
        entry = {
            "Date": date.strftime("%Y-%m-%d"),
            "Tester": tester,
            "Good Lids": good_lids,
            "Bad Lids": bad_lids,
            "Good Threads": good_threads,
            "Bad Threads": bad_threads,
            "Complete Tests": complete_tests
        }
        save_entry(entry, file_path)
        st.success("✅ Water Test entry saved!")

# Show department log
st.markdown("---")
st.subheader("📊 Department History Viewer")

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.write("### Showing entries for:", choice)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv, file_name=file_path, mime="text/csv")
else:
    st.info("No data found for this department yet.")

st.markdown("---")
st.caption("Made for PCI · Multi-Department Logger")
