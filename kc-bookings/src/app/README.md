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

Below are the steps needed to run the project.


# Swagger documentation

http://127.0.0.1:5000/api/predictbooking/swagger/

# Swagger backend

http://127.0.0.1:5000/api/predictbooking/swagger/

