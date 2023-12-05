import streamlit as st
from datetime import timedelta

def business_days_difference(start_date, end_date):
    current_date = start_date
    business_days = 0

    while current_date <= end_date:
        # Exclude Saturdays (5) and Sundays (6)
        if current_date.weekday() < 5:
            business_days += 1

        # Move to the next day
        current_date += timedelta(days=1)
    return business_days


def notice_check(duration, notice_time):
    if duration > 5 and notice_time < timedelta(days=15):
        st.warning(
            "Les congés supérieur à 5 jours se posent minimum 15 jours en avance",
            icon="⚠️",
        )
        st.session_state.warning = True
    else:
        st.session_state.warning = False