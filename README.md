# URL Shortener

## Overview 
Create a web service that shortens URLs akin to 'tinyurl' and 'bit.ly', and provides statistics on their usage.

## Technologies

- Flask 2.2.2
- flask-marshmallow 0.14.0
- Flask-SQLAlchemy 3.0.2
- marshmallow 3.18.0
- marshmallow-sqlalchemy 0.28.1

## How to Run 
clone the repository (if using git)

     git clone https://github.com/soheila-askarzadeh/url-shortener.git

Navigate to the project directory

     cd /path-to-project

Create a virtual environment

     python -m venv venv

Activate a virtual environment

     source venv/bin/activate  (MacOS\Linux)
      
     .\venv\Scripts\activate   (Windows)  

Install the dependencies from `requirements.txt`

    (venv) pip install -r requirements.txt 

Navigate to the /shortener folder

     cd shortener

Then run the main Python script

     python app.py

## API documentation

### Base URL

The base URL for all endpoints is: `http://localhost:8000`

### Endpoints

#### 1. Create Shortened URL

- **URL**: `/shorten`
- **Method**: `POST`
- **Description**: Create a new shortened URL.
- **Request Body**:
  ```json
  {
    "url": "Original_URL",
    "shortcode": "Custom_Shortcode (Optional)"
  }
- **Response**:
- **Status Code**: `201 Created`
- **Body**:
  ```json
  {
    "shortcode": "Shortened_Code"
  }
- **Additional Requirement**: The `shortcode` should have a length of 6 characters and contain only alphanumeric characters or underscores.

#### 2. Retrieve Original URL

- **URL**: `/<shortcode>`
- **Method**: `GET`
- **Description**: Retrieve the original URL associated with the provided shortcode.
- **Parameters**:
  - `shortcode`: The shortcode generated during URL shortening.
- **Response**: Redirects to the original URL.
     - **Status Code**: `302` 

#### 3. Retrieve Statistics for Shortened URL

- **URL**: `/<shortcode>/stats`
- **Method**: `GET`
- **Description**: Retrieve statistics for the specified shortened URL.
- **Parameters**:
  - `shortcode`: The shortcode generated during URL shortening.
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**:
    ```json
    {
      "created": "Creation_Date",
      "lastRedirect": "Last_Redirection_Date",
      "redirectCount": "Redirect_Count"
    }
    ```

### Example

#### Create a Shortened URL

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.example.com", "shortcode": "exmpl1"}' http://localhost:8000/shorten
```
#### Retrieve the Original URL

```bash
curl -L http://localhost:8000/exmpl1
```

#### Retrieve Statistics

```bash
curl http://localhost:8000/exmpl1/stats
```
### Errors

- **400 Bad Request**: If the URL is not provided or is invalid.
- **404 Not Found**: If the provided shortcode is not found.
- **409 Conflict**: If the provided shortcode is already in use.
- **412 Precondition Failed**: If the URL or shortcode provided is invalid.

## List of Shortcodes
Upon running the project and inserting a new shortcode, you can view a list of items by navigating to http://localhost:8000/

## Author
   Soheila Askarzadeh 
