# -*- coding: utf-8 -*-
from __future__ import annotations

import streamlit as st

from client.partials import material_sidebar


def main_interface():
    st.title("HR ChatBot")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-16k"

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    with st.sidebar:
        temperature = material_sidebar.display_temperature_slider()
