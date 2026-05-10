import streamlit as st
try:
    print(f"st.html exists: {hasattr(st, 'html')}")
    print(f"st.iframe exists: {hasattr(st, 'iframe')}")
except Exception as e:
    print(f"Error: {e}")
