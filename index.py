# -*- coding: utf-8 -*-
import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("SmaHR - SmartDev's HR Assistant")

st.write("__SmaHR is an assistant bot that helps the HR teams to support candidate whenever they need.__")


st.header("SmaHR Usage")
st.markdown(
    """
        SmaHR can use to support the HR team in the following tasks:
        - Answer candidate's question related to current hiring job description
        - Support candidate in understanding company background, culture, policy, etc.
         """
)

st.header("How to use ?")
st.markdown(
    """
            On this platform, SmaHR can be divide into two parts:
            - HR Page (Replicate the HR's Experience)
            - Candidate Chat Page (Replicate the Candidate's Experience)

            You can start with the HR Page to upload the job description and company documents. \n
            Then move to the Candidate Chat Page to test the chat functionality.
            """
)
