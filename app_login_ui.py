import streamlit
import json
import pathlib
import datetime
import uuid
import time

streamlit.set_page_config(page_title="Course Manager", layout="centered")
# Initialize users.json file path
json_file = pathlib.Path("users.json")

# Load or initialize users list
if json_file.exists():
    with open(json_file, "r") as f:
        users = json.load(f)
else:
    users = [
        {
            "id": "1",
            "email": "admin@school.edu",
            "full_name": "System Admin",
            "password": "123ssag@43AE",
            "role": "Admin",
            "registered_at": datetime.datetime.now().isoformat()
        }
    ]

# Function to save users to JSON file
def save_users():
    with open(json_file, "w") as f:
        json.dump(users, f, indent=4)

# Sidebar Navigation
streamlit.sidebar.title("🎓 Course Manager")
page = streamlit.sidebar.radio("Select an Option", ["Login", "Register"])

# Main container
main_container = streamlit.container()

if page == "Login":
    with main_container:
        streamlit.title("Login")
        
        login_container = streamlit.container()
        with login_container:
            col1, col2, col3 = streamlit.columns([1, 2, 1])
            with col2:
                streamlit.markdown("---")
                email = streamlit.text_input("Email Address", key="login_email")
                password = streamlit.text_input("Password", type="password", key="login_password")
                
                if streamlit.button("Log In", key="login_btn"):
                    with streamlit.spinner("Verifying credentials..."):
                        time.sleep(1)  # Simulate authentication delay
                        
                        # Check if user exists
                        logged_in_user = None
                        for user in users:
                            if user["email"] == email and user["password"] == password:
                                logged_in_user = user
                                break
                        
                        if logged_in_user:
                            streamlit.success(f"✅ Welcome, {logged_in_user['full_name']}!")
                            streamlit.info(f"📧 Email: {logged_in_user['email']}\n\n🔖 Role: {logged_in_user['role']}\n\n📅 Registered: {logged_in_user['registered_at']}")
                        else:
                            streamlit.error("Invalid email or password.")
                
                streamlit.markdown("---")
    
    # User Database Display below login form
    streamlit.markdown("---")
    streamlit.subheader("📊 User Database")
    if users:
        # Create a display-friendly dataframe without password
        display_users = []
        for user in users:
            display_users.append({
                "Full Name": user["full_name"],
                "Email": user["email"],
                "Role": user["role"],
                "Registered At": user["registered_at"]
            })
        streamlit.dataframe(display_users, use_container_width=True)
    else:
        streamlit.info("No users registered yet.")

elif page == "Register":
    with main_container:
        streamlit.title("New Instructor Account")
        
        register_container = streamlit.container()
        with register_container:
            col1, col2, col3 = streamlit.columns([1, 2, 1])
            with col2:
                streamlit.markdown("---")
                email = streamlit.text_input("Email Address", key="register_email")
                
                col_first, col_last = streamlit.columns(2)
                with col_first:
                    first_name = streamlit.text_input("First Name", key="register_first_name")
                with col_last:
                    last_name = streamlit.text_input("Last Name", key="register_last_name")
                
                password = streamlit.text_input("Password", type="password", key="register_password")
                confirm_password = streamlit.text_input("Confirm Password", type="password", key="register_confirm_password")
                
                role = streamlit.selectbox("Role", ["Instructor"], key="register_role")
                
                if streamlit.button("Create Account", key="register_btn"):
                    # Validation
                    if not email or not first_name or not last_name or not password or not confirm_password:
                        streamlit.error("❌ Please fill in all fields.")
                    elif password != confirm_password:
                        streamlit.error("❌ Passwords do not match.")
                    else:
                        # Check if email already exists
                        email_exists = any(user["email"] == email for user in users)
                        if email_exists:
                            streamlit.error("❌ Email already registered. Please try another email.")
                        else:
                            with streamlit.spinner("Creating account..."):
                                time.sleep(1)  # Simulate registration delay
                                
                                full_name = f"{first_name} {last_name}"
                                new_user = {
                                    "id": str(uuid.uuid4()),
                                    "email": email,
                                    "full_name": full_name,
                                    "password": password,
                                    "role": role,
                                    "registered_at": datetime.datetime.now().isoformat()
                                }
                                users.append(new_user)
                                save_users()
                                streamlit.success("✅ Account created successfully! You can now login.")
                
                streamlit.markdown("---")
