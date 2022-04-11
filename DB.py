import sqlite3

#Open database
conn = sqlite3.connect('database.db')

#Create table
try:
    conn.execute('''CREATE TABLE users 
                (userId integer primary key autoincrement,
  		password TEXT,
		email TEXT unique,
		firstName TEXT,
		lastName TEXT,
		address1 TEXT,
		address2 TEXT,
		zipcode TEXT,
		city TEXT,
		state TEXT,
		country TEXT, 
		phone TEXT,
                image TEXT
		)''')
except:
    pass
try:
    conn.execute('''CREATE TABLE products
                (productId INTEGER primary key autoincrement,
		name TEXT,
		price REAL,
		description TEXT,
		image TEXT,
		stock INTEGER,
		categoryId INTEGER,
		FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
		)''')
except:
    pass
try:
    conn.execute('''CREATE TABLE kart
		(userId Integer primary key,
		productId INTEGER,
                quantity integer,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')
except:
    pass
try:
    conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT,
        image TEXT
		)''')
except:
    pass
try:
	conn.execute('''CREATE TABLE orders (
		orderId integer primary key,
		status varchar,
		userId integer,
		FOREIGN KEY (userId) REFERENCES users(userId)
		)''')
except:         
	pass
try:
	conn.execute('''CREATE TABLE order_detail (
		userId integer,
		productId varchar(10) NOT NULL,
		orderId int(11) NOT NULL,
		quantity integer,
		price REAL,
		FOREIGN KEY (price) REFERENCES products(price),
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')
except:
	pass
try:
	conn.execute('''CREATE TABLE feedbacks (
	email TEXT unique,
	rating varchar,
	comments varchar(140),
	FOREIGN KEY (email) REFERENCES users(email)
	)''')
except:
	pass
try:
	cur = conn.cursor()
	cur.execute('''INSERT INTO orders (orderId, status, userId) VALUES (1, 'Delivered', 1)''')
	conn.commit()
	print('success')
except:
	pass