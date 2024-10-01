import streamlit as st
import sqlite3
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Initialize database connection
conn = sqlite3.connect('swavlamban24_registration.db')
c = conn.cursor()

# Create table for storing registration data
c.execute('''CREATE TABLE IF NOT EXISTS registrations (org_name TEXT, person_name TEXT, email TEXT)''')
conn.commit()

# Login section
name, authentication_status, username = authenticator.login("Login", 'main')

if authentication_status:
    st.success(f"Welcome {name}")
    
    # Logout button
    authenticator.logout("Logout", "main")
    
    # Number of personnel for this organization (e.g., 5 people)
    num_personnel = 2
    
    # Form for personnel data entry
    st.write(f"Register {num_personnel} personnel for {name}")
    for i in range(num_personnel):
        st.subheader(f"Personnel {i+1}")
        person_name = st.text_input(f"Name of Person {i+1}", key=f"name_{i}")
        email = st.text_input(f"Email of Person {i+1}", key=f"email_{i}")
        role = st.text_input(f"Role of Person {i+1}", key=f"role_{i}")
        if st.button(f"Submit Person {i+1}"):
            c.execute("INSERT INTO registrations (org_name, person_name, email) VALUES (?, ?, ?)", (name, person_name, email))
            conn.commit()
            st.success(f"Details for {person_name} added")

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

# Closing connection
conn.close()

# Saving config file
with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
