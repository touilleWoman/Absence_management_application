from datetime import datetime, timedelta, date
import streamlit as st



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




st.header("Bienvenue à la crèche :blue[Grand Bateaux] :boat:", divider="rainbow")
st.subheader("Pose les congés de votre enfant")

today = datetime.now()
next_year = today.year + 1
minimum_start_day = date.today() + timedelta(days=2)
max_day = date(next_year, 9, 1)
input = st.date_input(
    "Sélectionner une journée ou une période",
    (minimum_start_day, minimum_start_day),
    minimum_start_day,
    max_day,
    format="YYYY.MM.DD",
)

if len(input) == 2:
    notice_time = input[0] - date.today()
    duration = business_days_difference(input[0], input[1])

    st.write(
        "Vous allez poser",
        duration,
        "jours de congé, avec",
        notice_time.days,
        "jours en avance",
    )
    if duration > 5 and notice_time < timedelta(days=15):
        st.warning(
            "Les congés supérieur à 5 jours se posent minimum 15 jours en avance", icon="⚠️"
        )


st.divider()
st.subheader("Délai de prévenance")
st.text("Congé inférieur à une semaine: prévenir 2 jours avant")
st.text("Congé supérieur à une semaine: prévenir 15 jours avant")
