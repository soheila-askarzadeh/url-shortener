# Shortner

## Overview 
Create a web service that shortens URLs akin to 'tinyurl' and 'bit.ly', and provides statistics on their usage.

## Technologies

- Python 3.9.6
- Flask 2.2.2
- flask-marshmallow 0.14.0
- Flask-SQLAlchemy 3.0.2
- marshmallow 3.18.0
- marshmallow-sqlalchemy 0.28.1
- SQLAlchemy 1.4.42

## How to Run 
clone the repository

     git clone https://github.com/soheila-askarzadeh/url-shortener.git

Navigate to the project directory

     cd /path-to-project

Create a virtual environment

     python -m venv venv

Activate a virtual environment

     source venv/bin/activate  (MacOS\Linux)
      
     .\venv\Scripts\activate   (Windows)  

Install the dependencies from `requirements.txt`

    (vevn) pip install -r requirements.txt 

Navigate to the /shortener folder

     cd shortener

To build a database run

     python build_db.pyx

Then run the main Python script

     python app.py

## How to Run test 
To test the app, run the app.py script first, then execute the test_shortener script

     python test_shortener.py

## API documentation
After running the project, browse http://localhost:7006/api/ui

## List of Shortcodes
Upon running the project and inserting a new shortcode, you can view a list of items by navigating to http://localhost:7006/

## Author
   Soheila Askarzadeh 
