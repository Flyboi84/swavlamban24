import streamlit as st
import sqlite3
from streamlit_authenticator import Authenticate

# Initialize database connection
conn = sqlite3.connect('swavlamban24_registration.db')
c = conn.cursor()

# Create table for storing registration data
c.execute('''CREATE TABLE IF NOT EXISTS registrations
             (org_name TEXT, person_name TEXT, email TEXT)''')
conn.commit()

# Sample credentials (you can use a more secure system)
credentials = {"IA": "ZAQ1zaq1", "IAF": "xsw2XSW2"}

authenticator = Authenticate(credentials)

# Login section
org_name = authenticator.login("Login", "main")

if org_name:
    st.success(f"Welcome {org_name}")

    # Number of personnel for this organization (e.g., 5 people)
    num_personnel = 2

    # Form for personnel data entry
    st.write(f"Register {num_personnel} personnel for {org_name}")
    
    for i in range(num_personnel):
        st.subheader(f"Personnel {i+1}")
        person_name = st.text_input(f"Name of Person {i+1}", key=f"name_{i}")
        email = st.text_input(f"Email of Person {i+1}", key=f"email_{i}")
        role = st.text_input(f"Role of Person {i+1}", key=f"role_{i}")
        
        if st.button(f"Submit Person {i+1}"):
            c.execute("INSERT INTO registrations (org_name, person_name, email, role) VALUES (?, ?, ?, ?)", 
                      (org_name, person_name, email, role))
            conn.commit()
            st.success(f"Details for {person_name} added")

# Closing connection
conn.close()

