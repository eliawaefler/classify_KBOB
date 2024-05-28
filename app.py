# /classify_KBOB/app.py

from myutils.version_check import check_version
import streamlit as st

def main():
    files = st.fileuploader()
    


if __name__ == "__main__":
    check_version()
    main()
