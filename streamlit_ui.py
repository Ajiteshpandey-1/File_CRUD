# streamlit_crud.py

import streamlit as st
import os
from pathlib import Path

st.set_page_config(page_title="CRUD File Manager", page_icon="📁", layout="centered")

st.title("📁 CRUD File & Folder Manager")

# -----------------------------
# SHOW FILES AND FOLDERS
# -----------------------------
def readfileandfolder():
    p = Path('.')
    items = list(p.rglob('*'))

    if items:
        st.subheader("📂 Files & Folders")
        for index, file in enumerate(items):
            st.write(f"{index+1} - {file}")
    else:
        st.info("No files or folders found.")

# -----------------------------
# CREATE FILE
# -----------------------------
def create_file():
    st.subheader("📝 Create File")

    file_name = st.text_input("Enter file name")

    content = st.text_area("Enter file content")

    if st.button("Create File"):

        p = Path(file_name)

        if p.exists():
            st.error("File already exists")
        else:
            with open(file_name, 'w') as file:
                file.write(content)

            st.success("File created successfully")

# -----------------------------
# READ FILE
# -----------------------------
def read_file():
    st.subheader("📖 Read File")

    file_name = st.text_input("Enter file name to read")

    if st.button("Read File"):

        p = Path(file_name)

        if p.exists():
            with open(file_name, 'r') as file:
                st.text(file.read())
        else:
            st.error("File not found")

# -----------------------------
# UPDATE FILE
# -----------------------------
def update_file():
    st.subheader("✏️ Update File")

    file_name = st.text_input("Enter file name to update")

    option = st.radio(
        "Choose update type",
        ("Overwrite Content", "Append Content")
    )

    content = st.text_area("Enter new content")

    if st.button("Update File"):

        p = Path(file_name)

        if p.exists():

            if option == "Overwrite Content":
                with open(file_name, 'w') as file:
                    file.write(content)

                st.success("Content overwritten successfully")

            elif option == "Append Content":
                with open(file_name, 'a') as file:
                    file.write(content)

                st.success("Content appended successfully")

        else:
            st.error("File does not exist")

# -----------------------------
# DELETE FILE
# -----------------------------
def delete_file():
    st.subheader("🗑️ Delete File")

    file_name = st.text_input("Enter file name to delete")

    if st.button("Delete File"):

        p = Path(file_name)

        if p.exists():
            os.remove(p)
            st.success("File deleted successfully")
        else:
            st.error("File does not exist")

# -----------------------------
# RENAME FILE
# -----------------------------
def rename_file():
    st.subheader("🔄 Rename File")

    file_name = st.text_input("Enter current file name")

    new_file = st.text_input("Enter new file name")

    if st.button("Rename File"):

        p = Path(file_name)

        if p.exists():
            p.rename(new_file)
            st.success("File renamed successfully")
        else:
            st.error("File does not exist")

# -----------------------------
# CREATE FOLDER
# -----------------------------
def create_folder():
    st.subheader("📁 Create Folder")

    folder_name = st.text_input("Enter folder name")

    if st.button("Create Folder"):

        p = Path(folder_name)

        if p.exists():
            st.error("Folder already exists")
        else:
            p.mkdir()
            st.success("Folder created successfully")

# -----------------------------
# REMOVE FOLDER
# -----------------------------
def remove_folder():
    st.subheader("❌ Remove Folder")

    folder_name = st.text_input("Enter folder name")

    if st.button("Remove Folder"):

        p = Path(folder_name)

        if p.exists():
            p.rmdir()
            st.success("Folder removed successfully")
        else:
            st.error("Folder does not exist")

# -----------------------------
# SIDEBAR MENU
# -----------------------------
menu = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Show Files & Folders",
        "Create File",
        "Read File",
        "Update File",
        "Delete File",
        "Rename File",
        "Create Folder",
        "Remove Folder"
    ]
)

# -----------------------------
# MENU LOGIC
# -----------------------------
if menu == "Show Files & Folders":
    readfileandfolder()

elif menu == "Create File":
    create_file()

elif menu == "Read File":
    read_file()

elif menu == "Update File":
    update_file()

elif menu == "Delete File":
    delete_file()

elif menu == "Rename File":
    rename_file()

elif menu == "Create Folder":
    create_folder()

elif menu == "Remove Folder":
    remove_folder()