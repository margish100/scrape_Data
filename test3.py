from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import mysql.connector

app = FastAPI()

@app.get("/")
def read_root():
    return {"margish": "test"}

@app.on_event("startup")
async def startup_event():
    url = "https://www.bseindia.com/markets/equity/EQReports/bulk_deals.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    cnx = mysql.connector.connect(
        host="mysql",
        user="root",
        password="mysecretpassword",
        database="mydatabase",
    )
    cursor = cnx.cursor()

   
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        deal_date DATE,
        security_code VARCHAR(255),
        security_name VARCHAR(255),
        client_name VARCHAR(255),
        deal_type VARCHAR(1),
        quantity INT,
        price FLOAT
    );
    """
    cursor.execute(create_table_query)
    cnx.commit()


    insert_query = """
    INSERT INTO user (
        deal_date,
        security_code,
        security_name,
        client_name,
        deal_type,
        quantity,
        price
    )
    VALUES (
        '2023-06-28',
        '542580',
        'AARTECH',
        'VEENA RAJESH SHAH',
        'B',
        168000,
        109.70
    );
    """
    cursor.execute(insert_query)
    cnx.commit()

    cursor.close()
    cnx.close()


@app.on_event("shutdown")
async def shutdown_event():
    pass
