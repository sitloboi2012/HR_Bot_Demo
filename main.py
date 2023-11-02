# -*- coding: utf-8 -*-
import streamlit as st
import openai
from client.interface import main_interface

openai.api_key = st.secrets["OPENAI_API_KEY"]

main_interface()
