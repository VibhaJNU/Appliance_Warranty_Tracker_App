import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import os
import pandas as pd

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_registration' not in st.session_state:
    st.session_state.show_registration = False
if 'logged_in_username' not in st.session_state:
    st.session_state.logged_in_username = None

# Set page configuration
st.set_page_config(page_title="Appliance Warranty Tracker", page_icon="📝", layout="wide", initial_sidebar_state="expanded")

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }
    
    .main-title {
        color: #2B3467;
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        padding: 30px;
        margin-bottom: 40px;
        background: linear-gradient(135deg, #E3F2FD, #90CAF9);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background-color: #2B3467;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #1a1f3d;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        border: 2px solid #E0E0E0;
    }
    
    .upload-section, .view-section {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    h1, h2, h3 {
        color: #2B3467;
        font-weight: 600;
        margin-bottom: 20px;
        font-size: 32px;
    }
    
    .stMarkdown a {
        color: #2B3467;
        text-decoration: none;
        font-weight: 500;
    }
    
    .stMarkdown a:hover {
        color: #1a1f3d;
        text-decoration: underline;
    }
    
    .sidebar .sidebar-content {
        background-color: #F8F9FA;
        padding: 20px;
    }
    
    .dataframe {
        font-size: 14px;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .st-emotion-cache-1y4p8pa {
        max-width: 1200px;
        padding: 0 20px;
    }
    
    .st-emotion-cache-16idsys p {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #2B3467;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        background-color: #F8F9FA;
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError {
        padding: 16px;
        border-radius: 8px;
        font-weight: 500;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Login/Registration sidebar
with st.sidebar:
    if not st.session_state.logged_in:
        if st.session_state.show_registration:
            st.title("Registration")
            new_username = st.text_input("Username")
            email = st.text_input("Email")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Register"):
                if new_username and email and new_password and new_password == confirm_password:
                    try:
                        path = os.path.join(os.getcwd(), "Database", "Customer_data.db")
                        with sqlite3.connect(path) as conn:
                            cursor = conn.cursor()
                            # Check if username already exists
                            cursor.execute("SELECT * FROM Registration_login WHERE username = ?", (new_username,))
                            if cursor.fetchone():
                                st.error("Username already exists!")
                            else:
                                id = f"{new_username}_{email}".lower().replace(" ", "_")
                                cursor.execute(
                                    "INSERT INTO Registration_login (id, username, email, password) VALUES (?, ?, ?, ?)",
                                    (id, new_username, email, new_password)
                                )
                                conn.commit()
                                st.success("Registration successful! Please login.")
                                st.session_state.show_registration = False
                    except sqlite3.Error as e:
                        st.error(f"Database error: {e}")
                else:
                    st.error("Please fill all fields and ensure passwords match.")

            if st.button("Back to Login"):
                st.session_state.show_registration = False
        else:
            st.title("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login"):
                    try:
                        path = os.path.join(os.getcwd(), "Database", "Customer_data.db")
                        with sqlite3.connect(path) as conn:
                            cursor = conn.cursor()
                            cursor.execute(
                                "SELECT * FROM Registration_login WHERE username = ? AND password = ?",
                                (username, password)
                            )
                            user = cursor.fetchone()
                            if user:
                                st.session_state.logged_in = True
                                st.session_state.logged_in_username = username
                                st.success("Login successful!")
                            else:
                                st.error("Invalid credentials!")
                    except sqlite3.Error as e:
                        st.error(f"Database error: {e}")
            
            with col2:
                if st.button("Register Instead"):
                    st.session_state.show_registration = True
    else:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.success("Logged out successfully!")

        st.markdown("---")
        st.markdown("### Quick Links")
        st.markdown("* [Home](#)")
        st.markdown("* [About](#)")
        st.markdown("* [Contact](#)")

# Main content
if st.session_state.logged_in:
    # Main title
    st.markdown('<h1 class="main-title">Appliance Warranty Tracker</h1>', unsafe_allow_html=True)
    
    # Layout: Two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        # Upload Information
        st.title("Upload Information")

        # Fetch user details from registration
        try:
            path = os.path.join(os.getcwd(), "Database", "Customer_data.db")
            with sqlite3.connect(path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username, email FROM Registration_login WHERE username = ?",
                    (st.session_state.logged_in_username,)
                )
                user_details = cursor.fetchone()
                if user_details:
                    registered_name, registered_email = user_details
                else:
                    registered_name, registered_email = "", ""
        except sqlite3.Error as e:
            st.error(f"Error fetching user details: {e}")
            registered_name, registered_email = "", ""

        # Auto-populated inputs
        name = st.text_input("Enter your name:", value=registered_name, disabled=True)
        cust_name = name

        email_input = st.text_input("Enter your email:", value=registered_email, disabled=True)
        cust_email = email_input

        # Dropdown list for appliance categories
        appliance_categories = [
            "Refrigerator", "Freezer", "Microwave Oven", "Conventional Oven", "Convection Oven", 
            "Built-in Oven", "Gas Stove", "Electric Cooktop", "Induction Cooktop", "Dishwasher", 
            "Mixer", "Hand Blender", "Table Blender", "Toaster", "Sandwich Maker", "Coffee Machine", 
            "Electric Kettle", "Juicer", "Food Processor", "Air Fryer", "Deep Fryer", "Ice Maker", 
            "Rice Cooker", "Washing Machine (Front Load)", "Washing Machine (Top Load)", 
            "Clothes Dryer", "Washer Dryer Combo", "Steam Iron", "Dry Iron", "Garment Steamer", 
            "Heated Drying Rack", "Window Air Conditioner", "Split Air Conditioner", 
            "Portable Air Conditioner", "Air Cooler", "Oil Heater", "Fan Heater", "Infrared Heater", 
            "Ceiling Fan", "Table Fan", "Tower Fan", "Wall Fan", "Pedestal Fan", "Dehumidifier", 
            "Humidifier", "Geyser", "Instant Water Heater", "Vacuum Cleaner", "Wet & Dry Vacuum Cleaner", 
            "Robot Vacuum Cleaner", "Steam Cleaner", "Pressure Washer", "Carpet Cleaner", 
            "Hair Dryer", "Hair Straightener", "Hair Curler", "Electric Shaver", "Beard Trimmer", 
            "Epilator", "Electric Toothbrush", "Facial Steamer", "Body Massager", "LED TV", 
            "Smart TV", "Home Theatre System", "Bluetooth Speaker", "Music System", "Set-Top Box", 
            "Smart Speaker (Alexa, Google Home)", "Smart Thermostat", "Smart Security Camera", 
            "Smart Doorbell", "Water Purifier (RO, UV, etc.)", "Water Dispenser", "Sewing Machine", 
            "Air Freshener/Diffuser", "Insect Killer Lamp", "Pest Repeller"
        ]

        appliance = st.selectbox("Select the appliance name:", appliance_categories)

        date = st.date_input("Select a date:")
        purchase_date = date.strftime("%Y-%m-%d")

        warranty_period_input = st.number_input("Enter the warranty period (in years): ")
        warranty_period = warranty_period_input

        #Create a unique ID for the customer based on their name and emailid
        id = cust_name +"_"+ cust_email
        id = id.replace(" ", "_")  # Replace spaces with underscores for the ID
        id = id.lower()  # Convert to lowercase for consistency


        # Create button where customer can upload therir bill (image /PDF)
        uploaded_file = st.file_uploader("Upload your bill (image/PDF)", type=["jpg", "jpeg", "png", "pdf"])

        folder_path = os.path.join(os.getcwd(), "Customer_Bills", id)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if uploaded_file is not None:
            # Save the uploaded file to the folder_path
            file_path = os.path.join(folder_path, appliance + "_" + purchase_date + "_" + uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File uploaded and saved to {file_path}")


        # Calculate warranty end date
        if purchase_date:
            purchase_date_date = datetime.strptime(purchase_date, "%Y-%m-%d")
            warranty_end_date = purchase_date_date + timedelta(days=float(warranty_period) * 365)
            warranty_expiry_date = warranty_end_date.strftime("%Y-%m-%d")

        # Submit button
        if st.button("Submit"):
            if cust_name and cust_email and appliance and purchase_date and warranty_period:
                
                path = os.path.join(os.getcwd(),"Database", "Customer_data.db")
                connection = sqlite3.connect(path)
                cursor = connection.cursor()

                try:
                    cursor.execute('''
                        INSERT INTO Customer_info (id, name, email_id, Appliance_name, Purchase_date, warranty_period, warranty_expiry_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (id, cust_name, cust_email, appliance, purchase_date, warranty_period, warranty_expiry_date))
                    connection.commit()
                except sqlite3.Error as e:
                    print(f"An error occurred: {e}")
                finally:
                    connection.close()  # Ensure the connection is closed     
                
                
                st.success("Your information has been saved successfully!") 
                st.balloons() 
            
            else:
                st.error("Please fill in all fields before submitting.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Initialize session states for view section
        if 'customer_dataframe' not in st.session_state:
            st.session_state.customer_dataframe = None
        if 'customer_id' not in st.session_state:
            st.session_state.customer_id = None

        st.markdown('<div class="view-section">', unsafe_allow_html=True)
        st.title("View your information")

        # Add custom styling to inputs in the view section
        st.markdown("""
            <style>
            .view-section .stTextInput > div > div > input {
                font-size: 16px !important;
                padding: 12px !important;
            }
            
            .view-section .dataframe {
                font-size: 16px !important;
                padding: 10px !important;
            }
            
            .view-section h1 {
                color: #2B3467;
                font-size: 32px;
                font-weight: 600;
                margin-bottom: 25px;
            }
            </style>
        """, unsafe_allow_html=True)

        # Input fields for name and email with consistent styling
        name_customer = st.text_input("Enter your name:", key="name1", 
                                    help="Enter the name used during registration")
        cust_name_input = name_customer

        email_input_customer = st.text_input("Enter your email:", key="email1",
                                           help="Enter the email used during registration")
        cust_email_input = email_input_customer

        if st.button("Enter your details"):
            if not cust_name_input or not cust_email_input:
                st.error("Please enter both name and email to view your information.")
            else:
                # Store id_input in session state
                st.session_state.customer_id = cust_name_input + "_" + cust_email_input
                st.session_state.customer_id = st.session_state.customer_id.replace(" ", "_").lower()
                
                # Database query for appliance info
                path = os.path.join(os.getcwd(), "Database", "Customer_data.db")
                connection = sqlite3.connect(path)
                cursor = connection.cursor()

                try:
                    cursor.execute("SELECT * FROM Customer_info WHERE id=?", (st.session_state.customer_id,))
                    rows = cursor.fetchall()
                    if rows:
                        # Store dataframe in session state
                        st.session_state.customer_dataframe = pd.DataFrame(
                            rows, 
                            columns=['id', 'name', 'email_id', 'Appliance_name', 'Purchase_date', 'warranty_period', 'warranty_expiry_date']
                        )
                        
                    else:
                        st.error("No records found for the given name and email.")
                        st.session_state.customer_dataframe = None
                except sqlite3.Error as e:
                    st.error(f"Database error: {e}")
                finally:
                    connection.close()

        # Display dataframe outside the button click handler
        if st.session_state.customer_dataframe is not None:
            st.dataframe(st.session_state.customer_dataframe[['Appliance_name', 'Purchase_date', 'warranty_period', 'warranty_expiry_date']])
            
            # Add download section for bills
            st.subheader("Download Bills")
            bills_folder = os.path.join(os.getcwd(), "Customer_Bills", st.session_state.customer_id)
            if os.path.exists(bills_folder):
                files = os.listdir(bills_folder)
                if files:
                    for file in files:
                        file_path = os.path.join(bills_folder, file)
                        with open(file_path, "rb") as f:
                            file_bytes = f.read()
                        st.download_button(
                            label=f"⬇️ {file}",
                            data=file_bytes,
                            file_name=file,
                            mime="application/octet-stream"
                        )
                else:
                    st.info("No bills uploaded yet.")
            else:
                st.info("No bills uploaded yet.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px;">
            <h1>Welcome to Appliance Warranty Tracker</h1>
            <p>Please login to access the application.</p>
        </div>
        """,
        unsafe_allow_html=True
    )




