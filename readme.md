🚀 **Overview**
This application allows users to:

    Register and login to a secure account
    
    Upload appliance purchase receipts (bills, invoices, documents)
    
    Store details like appliance type, purchase date, warranty duration
    
    Automatically calculate and display warranty expiry dates
    
    Download saved receipts or view warranty status via the dashboard

✅** Getting Started**
1. Clone the Repo
git clone https://github.com/VibhaJNU/Appliance_Warranty_Tracker_App.git
cd Appliance_Warranty_Tracker_App

2. Setup Environment
python -m venv venv
source venv/bin/activate           # macOS/Linux
.\venv\Scripts\activate            # Windows
pip install -r src/requirements.txt

3. Configure Database
Create your database (e.g. SQLite, PostgreSQL, MySQL)

Update connection settings in src/database.py

4. Run the App Locally
streamlit run src/app.py

Your app will be available at:
http://localhost:8501

📦 **App Features**
User Authentication: Secure registration and login (e.g. via auth.py)

Appliance Entry: Add purchase date, warranty period, and upload bill

Dashboard: View ongoing warranties, expiry warnings

Receipt Management: Download previously uploaded bills

Warranty Expiry Logic: Automatically computes expiry date in database.py


⚙️ **Usage Flow**
Start the Streamlit app (app.py)

Register or log into your user account

Navigate to “Upload Appliance” section

Provide appliance details + upload receipt

View dashboard for warranty details and download invoices

📂 **Docker Deployment (Optional)**
A Dockerfile exists in the root folder. To build and run:

docker build -t warranty_tracker_app .
docker run -p 8501:8501 warranty_tracker_app
Access the app in your browser at http://localhost:8501

🙌 What’s Next?
Integrate email reminders for upcoming warranty expiries

Extend support to multi-user roles (admin, standard)

Add receipt validation (e.g. via OCR or manual tagging)

Deploy using Docker Compose on a cloud platform (e.g., DigitalOcean, AWS)








Developed an Appliance Warranty Tracker application to efficiently store, manage, and track warranty information for household appliances. The app enables users to upload and securely save appliance bills, monitor warranty periods, and conveniently download stored bills for future reference.

🏗️ **Application Building Steps**
Requirements:
    Create a database and tables:
    
    registration_login table
    
    customer_info table
    
    Take user input:
    
    Login/Registration: Name, Email ID, Password
    
    Appliance Category: Provide a dropdown list of appliance types
    
    Purchase Date
    
    Warranty Period (data type: float)
    
    Store all input data in the created database tables.
    
    Add a column in the customer_info table to calculate the warranty expiry date.

🎯 **Streamlit App Design**
Two sections:

    Upload Information
    
    View Your Information

Sidebar for user login and registration.

In the Upload Information section:

    Option to upload appliance bills.
    
    Uploaded bills are saved in a designated folder.

In the View Information section:

    Input: Name and Email ID.
    
    Extract and display all relevant information from the customer_info table.
    
    Option to download uploaded bills.

🐳 **Dockerization**
1. Creating Docker Image and Container
a. Create a blank Dockerfile (outside the src folder).
b. Add the following Dockerfile content:

dockerfile
FROM python:<version>
WORKDIR /app
ADD src/ /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]

c. Run the Docker build command from the same directory as the Dockerfile:
    docker build -t vibha0908/streamlite_app:01 .
    (Here, vibha0908 is the Docker Hub username)

d. To rebuild the image without cache:
docker build --no-cache -t vibha0908/streamlite_app:01 .
e. After a successful build, run the container:
docker run -p 8501:8501 vibha0908/streamlite_app:01
The application will now be live locally at: http://localhost:8501

☁️ **Deployment on AWS EC2**
Refer to this YouTube tutorial for guidance:
🔗 Deploy Dockerized Streamlit App on AWS EC2

Steps:
Push the Docker image to Docker Hub:
docker push vibha0908/streamlite_app:01
Create an AWS Account at aws.amazon.com
(Note: Requires valid card details)

Navigate to EC2 Instance in AWS Console.

Follow the video tutorial to set up the EC2 instance.

Important: Streamlit apps run by default on port 8501.

Ensure to customize your security group settings to allow inbound traffic on port 8501.



