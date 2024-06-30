# KitniRoti API

KitniRoti is an API for managing meal planning and tracking the number of rotis each user will eat. It includes functionalities for user registration, login, meal creation, and filtering meals by date, date range, and meal type.

## Project Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/divyesh1099/kitniroti.git
    cd kitniroti
    ```

2. **Create a virtual environment and activate it:**
    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On macOS/Linux
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Setup environment variables:**
    Create an `instance` folder and a `config.py` file inside it. Add your configurations like secret key and database URI in `config.py`.

5. **Initialize the database:**
    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6. **Run the application:**
    ```sh
    flask run
    ```

## API Endpoints

### User Routes

#### Register a new user
- **URL:** `/register`
- **Method:** `POST`
- **Body:**
    ```json
    {
      "username": "divya",
      "email": "email@example.com",
      "password": "Motiee0987654321#",
      "confirm_password": "Motiee0987654321#"
    }
    ```
- **Response:**
    ```json
    {
      "message": "Account created for divya!"
    }
    ```

#### Login a user
- **URL:** `/login`
- **Method:** `POST`
- **Body:**
    ```json
    {
      "email": "email@example.com",
      "password": "Motiee0987654321#"
    }
    ```
- **Response:**
    ```json
    {
      "message": "Login successful"
    }
    ```

#### Logout the current user
- **URL:** `/logout`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
    ```json
    {
      "message": "Logged out successfully"
    }
    ```

### Meal Routes

#### Create a new meal
- **URL:** `/meal/new`
- **Method:** `POST`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
    ```json
    {
      "meal_type": "Breakfast",
      "rotis": 4,
      "sabjis": "Paneer",
      "rice": "Basmati",
      "special_dish": "Gulab Jamun",
      "milk": "200ml"
    }
    ```
- **Response:**
    ```json
    {
      "message": "Meal has been added!"
    }
    ```

#### View all meals
- **URL:** `/meals`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
    ```json
    [
      {
        "id": 1,
        "date": "2024-06-30",
        "meal_type": "Breakfast",
        "rotis": 4,
        "sabjis": "Paneer",
        "rice": "Basmati",
        "special_dish": "Gulab Jamun",
        "milk": "200ml",
        "chef": "divya",
        "created_at": "2024-06-30T05:00:00",
        "updated_at": "2024-06-30T05:00:00"
      }
    ]
    ```

#### View the current meal
- **URL:** `/meals/current`
- **Method:** `GET`
- **Response:**
    ```json
    {
      "meal_type": "Lunch",
      "rotis": 4,
      "sabjis": "Paneer",
      "rice": "Basmati",
      "special_dish": "Gulab Jamun",
      "milk": "200ml",
      "chef": "divya"
    }
    ```

#### Get a single meal by ID
- **URL:** `/meal/<meal_id>`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
    ```json
    {
      "id": 1,
      "date": "2024-06-30",
      "meal_type": "Breakfast",
      "rotis": 4,
      "sabjis": "Paneer",
      "rice": "Basmati",
      "special_dish": "Gulab Jamun",
      "milk": "200ml",
      "chef": "divya",
      "created_at": "2024-06-30T05:00:00",
      "updated_at": "2024-06-30T05:00:00"
    }
    ```

#### Update a meal
- **URL:** `/meal/<meal_id>`
- **Method:** `PUT`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
    ```json
    {
      "meal_type": "Lunch",
      "rotis": 3,
      "sabjis": "Aloo Gobi",
      "rice": "Brown Rice",
      "special_dish": "Kheer",
      "milk": "250ml"
    }
    ```
- **Response:**
    ```json
    {
      "message": "Meal has been updated!"
    }
    ```

#### Delete a meal
- **URL:** `/meal/<meal_id>`
- **Method:** `DELETE`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
    ```json
    {
      "message": "Meal has been deleted!"
    }
    ```

#### Add user meal (register the number of rotis a user will eat)
- **URL:** `/user_meal/<meal_id>`
- **Method:** `POST`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
    ```json
    {
      "rotis": 3
    }
    ```
- **Response:**
    ```json
    {
      "message": "User meal has been added!"
    }
    ```

#### Update user meal (update the number of rotis a user will eat)
- **URL:** `/user_meal/<meal_id>`
- **Method:** `PUT`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
    ```json
    {
      "rotis": 4
    }
    ```
- **Response:**
    ```json
    {
      "message": "User meal has been updated!"
    }
    ```

#### Get total number of rotis for a meal (chef only)
- **URL:** `/chef/rotis/<meal_id>`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
    ```json
    {
      "total_rotis": 25
    }
    ```

### Filtering Meals

#### Filter meals with various parameters
- **URL:** `/meals/filter`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <access_token>`
- **Query Parameters:**
  - `date`: Specific date to filter meals (e.g., `2024-06-30`).
  - `start_date`: Start date of the date range to filter meals.
  - `end_date`: End date of the date range to filter meals.
  - `meal_type`: Type of meal to filter (e.g., `Breakfast`, `Lunch`, `Dinner`).

#### Example Requests

##### Get Meals by Specific Date
- **URL:** `http://localhost:5000/meals/filter?date=2024-06-30`
- **Method:** `GET`

##### Get Meals by Date Range
- **URL:** `http://localhost:5000/meals/filter?start_date=2024-06-01&end_date=2024-06-30`
- **Method:** `GET`

##### Get Meals by Type
- **URL:** `http://localhost:5000/meals/filter?meal_type=Lunch`
- **Method:** `GET`

##### Get Meals by Date Range and Type
- **URL:** `http://localhost:5000/meals/filter?start_date=2024-06-01&end_date=2024-06-30&meal_type=Dinner`
- **Method:** `GET`

## Database Models

### User
- `id`: Integer, primary key
- `username`: String, unique, required
- `email`: String, unique, required
- `password`: String, required
- `meals`: Relationship with `Meal`
- `user_meals`: Relationship with `UserMeal`

### Meal
- `id`: Integer, primary key
- `date`: Date, required
- `meal_type`: String, required (Breakfast, Lunch, Dinner)
- `rotis`: Integer, required
- `sabjis`: String
- `rice`: String
- `special_dish`: String
- `milk`: String
- `user_id`: Integer, foreign key to `User`, required
- `created_at`: DateTime, default current time
- `updated_at`: DateTime, default current time, updates on modification
- `user_meals`: Relationship with `UserMeal`

### UserMeal
- `id`: Integer, primary key
- `user_id`: Integer, foreign key to `User`, required
- `meal_id`: Integer, foreign key to `Meal`, required
- `rotis`: Integer, required
- `created_at`: DateTime, default current time
- `updated_at`: DateTime, default current time, updates on modification

## Running Tests

To run tests for the API, you can use any testing framework such as `pytest` or `unittest`. Ensure to set up a separate testing environment and database.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Flask documentation
- Flask-SQLAlchemy documentation
- Flask-Login documentation
- Flask-Migrate documentation
