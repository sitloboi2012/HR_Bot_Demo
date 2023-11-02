# -*- coding: utf-8 -*-
import streamlit as st


def display_temperature_slider():
    return st.slider("Temperature", 0.0, 1.0, 0.1, 0.1)


def display_model_to_choose():
    pass
