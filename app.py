from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
def create_table():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="restaurant_db"
        )
        if conn.is_connected():
            print('Connected to MySQL database')

        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS restaurants (
                restaurant_ID INT PRIMARY KEY,
                name VARCHAR(255),
                type VARCHAR(255),
                distance INT,
                rating FLOAT,
                UNIQUE (name, type) 
            )
        ''')
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()

def create_restaurant():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="restaurant_db"
        )
        if conn.is_connected():
            print('Connected to MySQL database for creation')

        cursor = conn.cursor()

        restaurant_query = (
            "INSERT IGNORE INTO restaurants (restaurant_ID, name, type, distance, rating) "
            "VALUES (%s, %s, %s, %s, %s)"
        )

        restaurant_data = [
            (1, "Kenshin", "Japanese", 72, 4.2),
            (2, "Starbucks", "Cafe", 200, 4.3),
            (3,"Rodic's Diner", "Filipino", 6, 4.4),
            (4, "Uncle John's", "Filipino", 6, 4.5),
            (5, "Jollibee", "Fast Food", 450, 4),
            (6, "Seven Eleven", "Filipino", 120, 1),
            (7, "Teriyaki Boy", "Japanese", 450, 3.7),
            (8, "Wendy's", "Fast Food", 2800, 3.7),
            (9, "Uncle Moe's Shawarma", "Middle Eastern", 6, 3.8),
            (10, "Burger King", "Fast Food", 400, 4.6)
        ]

        cursor.executemany(restaurant_query, restaurant_data)
        conn.commit()
        print("Restaurant data inserted successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    types = request.form.get('type')
    distance = request.form.get('distance')
    rating = request.form.get('rating')

    query = "SELECT * FROM restaurants WHERE 1=1"
    params = []

    if types:
        query += " AND type LIKE %s"
        params.append(f"%{types}%")
    if distance:
        query += " AND distance <= %s"
        params.append(distance)
    if rating:
        query += " AND rating >= %s"
        params.append(rating)

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='restaurant_db'
        )
        if conn.is_connected():
            print('Connected to MySQL database for search')

        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        results = []
    finally:
        if conn.is_connected():
            conn.close()

    return render_template('results.html', results=results)

if __name__ == '__main__':
    create_table()
    create_restaurant()
    app.run(debug=True)






