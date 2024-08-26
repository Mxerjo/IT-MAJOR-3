from fastapi import FastAPI
import pymysql

route = FastAPI()

# Database configuration
def db_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="fruits_db",
    )
@route.get("/")
def read_fruit():
    conn = db_conn()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tbl_fruits")
        rows = cursor.fetchall()
    conn.close()
    return [{data[1], data[0]} for data in rows]

@route.get("/add/{fruitN}")
def add_fruit(fruitN: str):
    conn = db_conn()
    with conn.cursor() as cursor:
        query = "INSERT INTO tbl_fruits (fruitName) VALUES (%s)"
        cursor.execute(query, (fruitN,))
        conn.commit()
    conn.close()
    return {"Successfully Added"}

@route.get("/update/{fruitId}/{new_name}")
def update_fruit(fruitId: int, new_name: str):
    conn = db_conn()
    with conn.cursor() as cursor:
        query = "UPDATE tbl_fruits SET fruitName = %s WHERE fruit_ID = %s"
        cursor.execute(query, (new_name, fruitId))
        conn.commit()
    conn.close()
    return {"Successfully Updated"}

@route.get("/delete/{fruitId}")
def delete_fruit(fruitId: int):
    conn = db_conn()
    with conn.cursor() as cursor:
        query = "DELETE FROM tbl_fruits WHERE fruit_ID= %s"
        cursor.execute(query, (fruitId,))
        conn.commit()
    conn.close()
    return {"Successfully Deleted"}
