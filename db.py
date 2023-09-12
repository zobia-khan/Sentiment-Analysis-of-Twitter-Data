import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="postgres",
        port="5432",
        password="1234")

# Open a cursor to perform database operations
cur = conn.cursor()

# # Execute a command: this creates a new table
# cur.execute('''CREATE TABLE signup (
#     id serial PRIMARY KEY,
#     username varchar(50) NOT NULL,
#     email varchar(100) NOT NULL,
#     password varchar(100) NOT NULL,
#     created_at timestamp DEFAULT current_timestamp
# );''')

# cur.execute('''INSERT INTO signup (username, email, password)
# VALUES ('JohnDoe', 'johndoe@example.com', 'password123'),
#        ('JaneSmith', 'janesmith@example.com', 'letmein456'),
#        ('RobertJohnson', 'robertjohnson@example.com', 'securepass789');''')

conn.commit()

cur.close()
conn.close()



