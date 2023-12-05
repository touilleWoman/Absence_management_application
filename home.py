import streamlit as st
from datetime import datetime, timedelta, date
from tools import notice_check, business_days_difference

st.set_page_config(
    page_title="Crèche grand bateaux", page_icon="random", initial_sidebar_state="auto"
)
st.header("Bienvenue à la crèche :blue[Grand Bateaux] :boat:", divider="rainbow")
st.subheader("Pose les congés de votre enfant")

firstname = st.text_input("Prénom")
surname = st.text_input("Nom de famille")

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

# warning will be True if user's leave is more than 5 days, but with less than 15 days notice
# confirm button will be deactivated if warning=True

if "warning" not in st.session_state:
    st.session_state.warning = False

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
    notice_check(duration, notice_time)

confirmed = st.button("Confirmer", type="primary", disabled=st.session_state.warning)
if confirmed:
    st.write(firstname, surname, "sera abente", input)


# Initialize connection.
conn = st.connection("snowflake")
session = conn.session()

if confirmed:
    formatted_start_date = input[0].strftime("%Y-%m-%d")
    formatted_end_date = input[1].strftime("%Y-%m-%d")
    child_id_df = session.sql(
        f"""SELECT id FROM DAYCARE.PUBLIC.CHILDREN WHERE firstname = '{firstname}' AND surname = '{surname}'"""
    )
    if child_id_df.to_pandas().size == 0:
        st.warning(
            "Cet enfant n'est pas dans notre crèche, merci de vérifier vos saisies",
            icon="⚠️",
        )
    else:
        child_id = child_id_df.to_pandas()["ID"].values[0]
        session.sql(
            f"""INSERT INTO DAYCARE.PUBLIC.LEAVES (child, start_date, end_date) 
        VALUES ('{child_id}', '{formatted_start_date}', '{formatted_end_date}')"""
        ).collect()
        st.success("Success!", icon="✅")


st.divider()
st.subheader("Délai de prévenance")
st.text("Congé inférieur à une semaine: prévenir 2 jours avant")
st.text("Congé supérieur à une semaine: prévenir 15 jours avant")
