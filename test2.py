from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import pymysql

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

host = "localhost"
user = "root"
password = "test123"
database = "mydatabase"

connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    cursorclass=pymysql.cursors.DictCursor,
)

@app.post("/users")
async def create_user(user: User):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO user (name, email) VALUES (%s, %s)"
            cursor.execute(sql, (user.name, user.email))
            connection.commit()

            user_id = cursor.lastrowid

            return {"message": "User created successfully", "user_id": user_id}
    except Exception as e:
        return {"message": "Error creating user", "error": str(e)}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE id = %s"
            cursor.execute(sql, user_id)
            user = cursor.fetchone()

            if user:
                return user
            else:
                return {"message": "User not found"}
    except Exception as e:
        return {"message": "Error retrieving user", "error": str(e)}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE user SET name = %s, email = %s WHERE id = %s"
            cursor.execute(sql, (user.name, user.email, user_id))
            connection.commit()

            return {"message": "User updated successfully"}
    except Exception as e:
        return {"message": "Error updating user", "error": str(e)}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM user WHERE id = %s"
            cursor.execute(sql, user_id)
            connection.commit()

            return {"message": "User deleted successfully"}
    except Exception as e:
        return {"message": "Error deleting user", "error": str(e)}

@app.post("/scrape-and-store")
async def scrape_and_store_data():
    try:
        
        url = "https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        
        with connection.cursor() as cursor:
        
            table = soup.find("table", {"id": "BulkDeal"})
            rows = table.find_all("tr")[1:] 

            for row in rows:
                columns = row.find_all("td")
                deal_date = columns[0].text.strip()
                security_code = columns[1].text.strip()
                security_name = columns[2].text.strip()
                client_name = columns[3].text.strip()
                deal_type = columns[4].text.strip()
                quantity = columns[5].text.strip()
                price = columns[6].text.strip()

                sql = "INSERT INTO user (deal_date, security_code, security_name, client_name, deal_type, quantity, price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (deal_date, security_code, security_name, client_name, deal_type, quantity, price))

            connection.commit()

        return {"message": "Data scraped and stored successfully"}
    except Exception as e:
        return {"message": "Error scraping data", "error": str(e)}
