import streamlit as st
from datetime import datetime
import pandas as pd

# Streamlit Configuration
st.set_page_config(page_title="Marathon Tracker", layout="wide")

# State Initialization
if "events" not in st.session_state:
    st.session_state["events"] = []

if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

# Theme Toggle
def toggle_theme():
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

# Event Form Submission
def add_event(event_date, event_name, event_type, event_location, target_time, event_notes):
    event = {
        "Date": event_date,
        "Name": event_name,
        "Type": event_type,
        "Location": event_location,
        "Target Time": target_time,
        "Notes": event_notes
    }
    st.session_state["events"].append(event)

# App Title and Theme Button
st.title("마라톤 일정 관리 앱")
st.button("🌓 테마 전환", on_click=toggle_theme)

# Event Form
st.header("새 마라톤 일정 추가")
with st.form("event_form"):
    event_date = st.date_input("날짜", value=datetime.now())
    event_name = st.text_input("마라톤 이름")
    event_type = st.selectbox("마라톤 종류", ["풀코스 (42.195km)", "하프 (21.0975km)", "10K", "5K"])
    event_location = st.text_input("장소")
    target_time = st.time_input("목표 기록", value=datetime.strptime("01:00:00", "%H:%M:%S").time())
    event_notes = st.text_area("메모")
    submit = st.form_submit_button("일정 추가")

    if submit:
        add_event(event_date, event_name, event_type, event_location, target_time, event_notes)
        st.success("새로운 마라톤 일정이 추가되었습니다!")

# Display Upcoming Marathon
st.header("다음 마라톤")
if st.session_state["events"]:
    upcoming_events = sorted(st.session_state["events"], key=lambda x: x["Date"])
    next_event = upcoming_events[0]
    st.subheader(f"{next_event['Name']} ({next_event['Type']})")
    st.write(f"날짜: {next_event['Date']}")
    st.write(f"장소: {next_event['Location']}")
    st.write(f"목표 기록: {next_event['Target Time']}")
    st.write(f"메모: {next_event['Notes']}")
else:
    st.write("예정된 마라톤이 없습니다.")

# Checklist
st.header("준비물 체크리스트")
checklist_items = ["러닝화", "운동복", "물통", "에너지젤", "배번"]
checklist = {}
for item in checklist_items:
    checklist[item] = st.checkbox(item)

# Event Table
st.header("등록된 마라톤 일정")
if st.session_state["events"]:
    events_df = pd.DataFrame(st.session_state["events"])
    st.dataframe(events_df)
else:
    st.write("아직 등록된 마라톤 일정이 없습니다.")
