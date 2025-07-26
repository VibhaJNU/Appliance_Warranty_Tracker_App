Building Application:

    What we need :
    1. Create database and tables - Registration_login table, Customer_info table
    2. Take user input:
        1. login credential/ Registration : Name, email-id, password
        2. Appliances category - we need to provide drop down list of appliances name
        3. Purchase date
        4. Warranty Period (data type should float)
    3. We need to store all these data into created table in database
    4. Add another col in customer_info table where we calculate warranty expiry date
    5. Streamlit app building:
        1. Two section : Upload information, view your information
        2. side bar for login and registration
        3. In upload info section, there will be bill upload option and we will store bills in new folder
        4. In view Info section: take name and email id and based on that extract all info from customer_info table
        5. Provide bills download optiion also

After application build:

1. Created Docker Image and container:

a. Create blank docker file outside of src folder
b. Add flowings: FROM python version, WORKDIR /app , ADD src/app , RUN pip install...., EXPORT 8501 CMD used commands
c. Run docker file from same adress where docker file is stored. Command: docker build -t vibha0908/streamlite_app:01 .   // here vibha0908 is docker hub account id
If i have made any changes and want to rerun from starting then command is: docker build --no-cache -t vibha0908/streamlite_app:01 .
d.After succesfully image build, we create container by using this command:docker run -p 8501:8501 streamlite_app:01
So, after successful docker run we will get the application live in local sytem at port 8501.


2. Now, we deploye docker image into EC2 AWS services.

follow the below link for deployement:
https://www.youtube.com/watch?v=wHy0JNwrB9k&ab_channel=MPrashant

a. For deployment, first we need to push docker image into docker hub. Used command: docker push vibha0908/streamlite_app:01
b. Then we will create aws account (aws.amazon.com -> console) (required card information)
b. Go to EC2 Instance services
c. And follow the youtube steps.
d. important point to note, streamlit app run only in 8501 port. So we will need to customize http port number to 8501

