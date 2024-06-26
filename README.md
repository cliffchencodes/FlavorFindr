# FlavorFindr

## Team 29: Kelly Chung, Rodrigo Ugarte, Cliff Chen

### Introduction 
FlavorFindr is a web application that allows users to easily access the nutritional information of their favorite foods from popular fast food chains. Today, consumers can be overwhelmed by an abundance of food options - with many of them being cheap and unhealthy. FlavorFindr’s goal is to make food nutrition accurate, accessible, and interactive... to make food fun! Our goal with FlavorFindr is to create a streamline product for both the user and database administrator to grab and aggregate the available information, as well as create simple pie chart visualizations for macronutrient information of each food.

### 'api' Folder 
The ‘api’ folder contains a folder called ‘src’, a folder called ‘templates’, and a python file called ‘run.py’. The ‘src’ folder contains the python files that handle the backend functions. 

### 'src' Folder 
Within ‘src’, there is an ‘__init__.py’ that initializes the instance of the Flask app. There are several intermediate files that contain functions that perform calculations, cleaning, and formatting. 

The ‘userAPI_noDjango.py’ file handles requests from two ends, the frontend HTML and response from the database. 

### 'templates' Folder 
The ‘templates’ folder contains .html files that configure views for the user and admin. The folder contains views for admin, user, errors, and successful pages. 

### 'run.py' File 
Lastly, the ‘run.py’ file runs the Flask application. 

### Code Flow 
As it comes together, ‘run.py’ is run first to open up the application. The user then completes a sample operation such as an add. The data is parsed from the HTML and processed by ‘userAPI_noDjango.py’ and formatted into a JSON. The JSON is then passed to a request that is sent to the firebase to be appended to the database. Lastly, a success message is received by ‘userAPI_noDjango.py’ and the message routes the user to either a successful or failed view. A back button is available on the resulting pages to bring the admin or user back to the main page so further actions can be taken. The firebase databases are hashed on the first letter of the food's name, and there are 5 available databases. 

### To Run the Program
To run the program, simply run 'run.py' and the app will run locally!
