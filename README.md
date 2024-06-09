# Introduction

This is a practice project for making predictions on the booking destination for AirBnB users. The problem is taken from a Kaggle dataset, link to which is specified below:
https://www.kaggle.com/competitions/airbnb-recruiting-new-user-bookings/data

The project is structured in a way that the entire source code is present in Analytics/kc-bookings/src/app folder. Below is the description of the subfolders of the source code:

src/app
    backend                           : Contains the python code built using Flask framework
        apps                          : Contains multiple apps/modules in the project
            core                      : This is the core app which contains the api response handlers. It could be used for core functionalities in future                 like logging, connecting to database etc
            predict_booking           : This is the app that contains the api wrapper for making predictions
        data_files
            test_users.csv            : This is the csv files containing the test data
            train_users.csv           : This is the csv files containing the training data
            output                    : This is the folder containing the output of ML model on test data
                output.csv            : This is the csv files containing the output csv i.e. predicted destination against every user id
    frontend                          : This is empty currently and could be used for storing front end codes for the project


Before moving on to the solution understanding, lets quickly understand how to test the app. The project contains an API for file upload where the user can upload test_users.csv file against which predictions are needed. The API can be tested using Thunderclient which is available as an extension in Visual studio code and is mentioned in the steps of 'Getting Started'. Once the test file is uploaded in Thunderclient, the results of the test will be generated in the backend/output folder with the name output.csv.

# Getting Started

Pre-requisites:
    - Linux machine with Ubuntu 18 OS and 16 GB RAM
    - Root access on Linux machine
    - Stable internet connection

Below are the steps needed to run the project.
1. Install Visual Studio Code extensions for Docker and Thunderclient
2. Clone the repo in a local directory of your Linux machine
3. In VS Code do the following:
    Ctrl + Shift + P
    Search for: Dev Container: Open Folder in Container
    select repo folder
4. In the dev container, cd to backend folder and run "python manage.py" command to start the backend.
5. Open Thunderclient extension for VS Code and create a new request.
6. In the request, specify the URL as "http://127.0.0.1:5000/api/predictbooking/PredictBooking/upload". In the body of the request, select "Form" tab and check the "Files" checkbox. In the "Form" tab, in the file section, enter "file" as field name and in field_value, upload the test_users.csv file by selecting it from data_files directory.
7. Change the request type of the request from GET to POST and click on send.
8. The output will get successfully generated in the data_files/output/output.csv file and in thunderclient, you can find the below message.
{
  "status": 200,
  "message": null,
  "data": {
    "data": "Model outputs successfully generated."
  }
}


# Swagger documentation

http://127.0.0.1:5000/api/predictbooking/swagger/

You can choose to see the documentation of any API here.
