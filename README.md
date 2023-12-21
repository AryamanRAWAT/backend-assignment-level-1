Assignment_datapeace

The project is a Django-based web application that provides API endpoints to manage user details. It includes functionality to create, retrieve, update, and delete user information. The project utilizes Django's ORM for database operations, allowing users to interact with a database of user details through API calls.

Setup and Installation:

1. Clone the Repository:

   ```bash
   git clone https://github.com/AryamanRAWAT/Assignment_datapeace.git
   cd Assignment_datapeace
   ```

2. Create Virtual Environment:

   ```bash
   python -m venv venv
   ```

3. Activate Virtual Environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```


5. Apply Database Migrations:

   ```bash
   python manage.py migrate
   ```

6. Run the Development Server:

   ```bash
   python manage.py runserver
   ```

   The server will be running at aryamanrawat2000.pythonanywhere.com/.

API DOCUMENTATION AT: https://documenter.getpostman.com/view/26169620/2s9Ykoe2Hh

## API Endpoints

### 1. Create a New User

Endpoint:

- Method: `POST`
- URL: `/api/post-user/`
- Request Body:

  ```json
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "XYZ Corp",
    "age": 30,
    "city": "Cityville",
    "state": "Stateville",
    "zip": 12345,
    "email": "john.doe@example.com",
    "web": "http://example.com"
  }
  ```

- Responses:

  - Successful Creation:
    - Status: 201 Created
    - Body: "New User Created!"

  - Email Already Taken:
    - Status: 400 Bad Request
    - Body:
      ```json
      {
        "status": "Email already taken",
        "email_taken": ["john.doe@example.com"],
        "id_taken": [1]
      }
      ```

### 2. Get All Users

Endpoint:

- Method: `GET`
- URL: `/api/get-all-users/`

- Query Parameters:
  - `page` (default: 1): Page number for paginated results.
  - `limit` (default: 5): Number of entries per page.
  - `name` (default: ""): Search users by name (substring match in first or last name).
  - `sort` (default: ""): Sort users by attribute (e.g., "age" or "-age" for descending).

- Responses:

  - Successful Response:
    - Status: 200 OK
    - Body: List of user details in JSON format.

  - Empty Page:
    - Status: 500 Internal Server Error
    - Body: "Empty Page."

### 3. Get User by ID

Endpoint:

- Method: `GET`
- URL: `/api/get-user/{uid}/`

- Path Parameter:
  - `{uid}`: The unique identifier of the user.

- Responses:

  - Successful Response:
    - Status: 200 OK
    - Body: User details in JSON format.

  - User Not Found:
    - Status: 500 Internal Server Error
    - Body: "User Does Not Exist."

### 4. Update User by ID

Endpoint:

- Method: `PUT`
- URL: `/api/update-user/{uid}/`

- Path Parameter:
  - `{uid}`: The unique identifier of the user.

- Request Body:

  ```json
  {
    "first_name": "Updated",
    "last_name": "User",
    "company_name": "New Corp",
    "age": 25,
    "city": "New City",
    "state": "New State",
    "zip": 54321,
    "email": "updated.user@example.com",
    "web": "http://newexample.com"
  }
  ```

- Responses:

  - Successful Update:
    - Status: 200 OK
    - Body: "Entry Updated!"

  - User Not Found:
    - Status: 400 Bad Request
    - Body: "User Does Not Exist."

### 5. Delete User by ID

Endpoint:

- Method: `DELETE`
- URL: `/api/delete-user/{uid}/`

- Path Parameter:
  - `{uid}`: The unique identifier of the user.

- Responses:

  - Successful Deletion:
    - Status: 200 OK
    - Body: "Entry Deleted!"

  - User Not Found:
    - Status: 500 Internal Server Error
    - Body: "User Does Not Exist."

### 6. Delete Users with Filters

Endpoint:

- Method: `DELETE`
- URL: `/api/delete-all/`

- Query Parameters:
  - `first_name` (default: ""): Filter users by first name.
  - `last_name` (default: ""): Filter users by last name.
  - `age_start` (default: 0): Minimum age for filtering.
  - `age_end` (default: 0): Maximum age for filtering.
  - `start_id` (default: 0): Minimum user ID for filtering
