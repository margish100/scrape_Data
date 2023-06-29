# scrape_Data
I have 2 file created for with docker and crud operation 

Create a file named requirements.txt
fastapi
uvicorn
requests
beautifulsoup4
mysql-connector-python


Save the main.py file.
Open a terminal or command prompt and navigate to the docker-fastapi directory.

    Create a user: POST http://localhost:8000/users
    Get a user by ID: GET http://localhost:8000/users/{user_id}
    Update a user by ID: PUT http://localhost:8000/users/{user_id}
    Delete a user by ID: DELETE http://localhost:8000/users/{user_id}
    Scrape and store data: POST http://localhost:8000/scrape-and-store
