# HLPR backend demo

This is a demonstration of some of the backend functionality inside of HLPR - our computing AT3 group project. This also includes two demonstration frontend pages to show how this could intergrate with a frontend too.

## How to run/test for yourself

### initial setup - MongoDB

To begin, you need to set up a MongoDB server, the two simplest ways are to use the MongoDB community server to host it locally, or create a free MongoDB atlas account.

Next you need to connect to your MongoDB, and create a new database with the name HLPR

Inside of that database create collections with the names "posts", "schools", "subjects", and "users"

You then need to set the URL of the db you have created inside of functions/db.py (if you have used community server it should be the same as the value that has already been set)

### Initial setup - python

You will can install the requirements with the following command:
`pip install flask pymongo requests`

### How to run

Once you have set everything up, you can run the project from the root of the project with the following command: `py main.py`

This should host it locally on `127.0.0.1:5000` / `localhost:5000` (the flask default url)

### How to test routes

You can test the routes using any app that can generate post requests, I personally use [Insomnia](https://github.com/Kong/insomnia)

## A rundown of the system of the code files

### /api

the api folder contains all the api routes, these are all the backend functionalty, and are stored in the routes on the website you go to take them

the folders inside are

- admin
  - contains functions that are limited to admins or HLPR
- user
  - contains functions that require user authentication

(the root folder just contains other functions)

### /functions

This just contains some general python functions that are used across the code

### /routing

Routing just contains the routes.py file which contains the python code for returning the frontend pages and files

### /public

This contains all the frontend code and assets, included as a demonstration of how a frotend could be intergrated
