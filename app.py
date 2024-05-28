# /classify_KBOB/app.py

from MyUtils.version_check import *
import streamlit as st

def main():
    files = st.fileuploader()
    


if __name__ == "__main__":
    check_version()
    main()
