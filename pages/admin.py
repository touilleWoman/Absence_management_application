import streamlit as st

conn = st.connection("snowflake")
session = conn.session()
df_children = session.sql(
    """SELECT * FROM DAYCARE.PUBLIC.CHILDREN"""
).to_pandas()
st.dataframe(df_children, use_container_width=True)

df_leaves = session.sql(
    """SELECT * FROM DAYCARE.PUBLIC.LEAVES"""
).to_pandas()
st.dataframe(df_leaves, use_container_width=True)