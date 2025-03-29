# Online-Store-website

An online store website built using Python, JavaScript, HTML, and CSS. This project is designed to provide a seamless shopping experience for users with a variety of features such as product browsing, shopping cart, and checkout process.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Libraries and Dependencies](#libraries-and-dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Introduction
The Online-Store-website is a fully functional web application that simulates an online shopping experience. Users can browse products, add them to their cart, and proceed to checkout. The website is built using a combination of Python for the backend, JavaScript for interactivity, and HTML/CSS for the front-end design.

## Features
- User authentication and authorization with separate customer and manager logins.
- Customer login leads to a static web page that is not yet completed.
- Manager login leads to an admin dashboard showing statistics.
- Admin dashboard allows managers to view and modify all tables.
- Managers can purchase products from suppliers.
- Product listing and detail pages.
- Shopping cart functionality.
- Checkout process.
- Order management.
- Responsive design.

## Technologies Used
- **Python**: Backend logic and server-side operations
- **JavaScript**: Client-side interactivity
- **HTML**: Structuring the web pages
- **CSS**: Styling the web pages

## Libraries and Dependencies
### Backend
- Flask: A lightweight WSGI web application framework
- SQLAlchemy: An ORM for handling database operations

### Frontend
- Bootstrap: CSS framework for responsive design
- jQuery: JavaScript library for DOM manipulation and AJAX requests

## Installation
1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/yazan6546/Online-Store-website.git
    cd Online-Store-website/Project_files
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    - Note: This may take a while

4. Create a `.flaskenv` file in the project root directory and define the following environment variables:
    ```dotenv
    DATABASE_URL=mysql://<username>:<password>@127.0.0.1:3306/store # Replace `<username>` and `<password>` with your username and password respectively.
    FLASK_APP=store.py
    FLASK_ENV=development
    FLASK_RUN_PORT=5000
    FLASK_DEBUG=1
    ```

5. Create a `.env` file in the root directory of the project for testing purposes and if you want to insert fake database data:
    ```dotenv
    DATABASE_URL_TEST=mysql://<username>:<password>@127.0.0.1:3306/store # Replace `<username>` and `<password>` with your username and password respectively.
    FLASK_APP=store.py
    ```

6. Generate tables by running the `store.sql` script located in the `Project_files` directory. Execute the following command in your MySQL interface:
    ```sql
    source Project_files/store.sql;
    ``` 

7. Generate tables from the included scripts in the `utils` directory. Run the following command:
    ```bash
    python utils/db_generator.py
    ```

## Usage
1. Run the Flask development server:
    ```bash
    flask run
    ```

2. Open your web browser and navigate to http://127.0.0.1:5000.

3. Register a new user account or log in with an existing account:
    - **Customer login**: Leads to a static web page that is not yet completed.
    - **Manager login**: Leads to an admin dashboard showing statistics and allows managers to view and modify all tables, as well as purchase products from suppliers.

## Contributing
Contributions are welcome! Please fork this repository and submit pull requests to add new features or fix bugs.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Disclaimer
Please note that the customer side of this project is static and incomplete.

## Team
- [Yazan Abualoun](https://github.com/yazan6546)
- [Osaid Nour](https://github.com/osaidnur)
- [Lana Musaffer](https://github.com/Lanamahd)
