from crypt import methods
from pydoc import render_doc
from urllib import request
from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def root():
    loggedIn, first_name = getLogindetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()        
        cur.execute('SELECT * FROM categories')            
        categoryData = cur.fetchall()              
    return render_template('index.html', loggedIn = loggedIn, first_name = first_name, categoryData=categoryData)
  
@app.route('/about us')
def Info():
    return "That page will be avialabe soon"
 
#Login Functions
#Get login credentials
def getLogindetails():
    with sqlite3.connect('database.db') as data:
        connection = data.cursor()
        if 'email' not in session:
            loggedIn = False
            first_name = ""
        else:
            try:
                details = connection.execute("Select * from users where email='"+session['email']+"'") 
                p = details.fetchone()
                first_name = p[3]
                loggedIn = True
            except:
                loggedIn = False
                first_name = ""
                session.pop('email')
    return (loggedIn, first_name)    
       
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Validate user information
def valid(email,password):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select email, password from users where email='"+email+"'")
    user = cur.fetchall()
    try:
        for i in user:
            if email == i[0] and password == i[1]:
                return True
    except:
        return False

#Login
@app.route('/login')
def loginform():
    if request.args.get('email'):
        email = request.args.get('email')
        password = request.args.get('password')
        if valid(email,password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            flash("Invalid credentials")
            return render_template('login.html' )
    else:
        return render_template('login.html')

#Logout 
@app.route('/logout')
def logout():
    session.pop('email')
    return redirect(url_for('root')) 

#Create an account
@app.route('/register',methods=['POST','GET'])   
def register():
    print(app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        return render_template('register.html')  
    elif request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        Re_password = request.form['password2']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']        
        zipcode = request.form['zipcode']
        country = request.form['country']
        phone = request.form['phone']
        if request.files['pic']:
            pic = request.files['pic']
            if not allowed_file(pic.filename):
                return "wrong fie extension"
            filename = secure_filename(pic.filename)
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) 
            a = "Insert into users (password,email,firstname,lastName,address1,address2,zipcode,city,state,country,phone,image) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(password,email,firstName,lastName,address1,address2,zipcode,city,state,country,phone,filename)
    
        else:
            a = "Insert into users (password,email,firstname,lastName,address1,address2,zipcode,city,state,country,phone) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(password,email,firstName,lastName,address1,address2,zipcode,city,state,country,phone)   
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print(a)
            try:                
                cur.execute(a)
                con.commit()
                return redirect('/login')
            except:
                con.rollback()
                flash("Something Went wrong")
                print(flash)
                return redirect(url_for('register'))
        
       
#View Profile Information
@app.route('/profile')
def profile():
    loggedIn, first_name = getLogindetails()
    if loggedIn == False:
        return redirect(url_for('loginform'))
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("select * from users where email='{}'".format(session['email']))  
        user_info = cur.fetchone()
    return render_template('profile.html',loggedIn= loggedIn, first_name=first_name, user_info=user_info)

#Update profile
@app.route('/profile/update',methods=['POST','GET'])
def edit_profile():
    if request.method == "GET":
        loggedIn, first_name = getLogindetails()
        if loggedIn == False:
            return redirect(url_for('loginform'))
        else:
            with sqlite3.connect('database.db') as c:
                conn = c.cursor()
                conn.execute("select * from users where email='{}'".format(session['email']))
                user_info = conn.fetchone()        
            return render_template('update_profile.html',user_info=user_info, loggedIn=loggedIn, first_name=first_name)
    elif request.method == "POST":
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']        
        zipcode = request.form['zipcode']
        country = request.form['country']
        phone = request.form['phone']
        if request.files['pic']:
            pic = request.files['pic']
            if not allowed_file(pic.filename):
                return "wrong fie extension"
            filename = secure_filename(pic.filename)
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) 
            update = "update users set firstname='{}',lastName='{}',address1='{}',address2='{}',zipcode='{}',city='{}',state='{}',country='{}',phone='{}',image='{}' where email='{}'".format(firstName,lastName,address1,address2,zipcode,city,state,country,phone,filename,session['email'])
        else:
            update = "update users set firstname='{}',lastName='{}',address1='{}',address2='{}',zipcode='{}',city='{}',state='{}',country='{}',phone='{}' where email='{}'".format(firstName,lastName,address1,address2,zipcode,city,state,country,phone,session['email'])
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print(update)
            try:
                cur.execute(update)
                con.commit()  
                flash("update succesfull")
                return redirect(url_for('edit_profile'))              
            except:
                flash("Something Went wrong")
                return redirect(url_for('edit_profile'))  
    else:
        return "something went wrong"
             
        

@app.route('/passwordchange')
def Password_change():
    return render_template("password_change.html")

#SHOPPING FUNCTIONS
#View categories of items
@app.route('/shop_by_category')
def category():
    loggedIn, first_name = getLogindetails()
    category = request.args.get('category')
    print(category)
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("select products.*, categories.name from products, categories where products.categoryId=categories.categoriesId and categories.name='{}'".format(category))
        products = cur.fetchall()
        print(products)
    return render_template('category.html', category = category,loggedIn=loggedIn, first_name=first_name, products=products)

#View Products and Add item to shopping cart
@app.route("/product", methods=['GET','POST'])
def product():
    if request.method == "GET":
        loggedIn, first_name = getLogindetails()
        product_name = request.args.get('product') 
        with sqlite3.connect('database.db') as c:
            conn = c.cursor()
            conn.execute("select * from products where name='{}'".format(product_name))
            product_info = conn.fetchone()        
        return render_template('product_description.html', loggedIn=loggedIn, first_name=first_name, product_info=product_info)
    elif request.method == "POST":
        loggedIn, first_name = getLogindetails()
        if not loggedIn:
            return redirect(url_for('loginform'))
        else:
            Product_name = request.args.get('product')
            quantity = request.form['quantity']
            with sqlite3.connect('database.db') as c:
                conn = c.cursor()
                conn.execute("select userId from users where email='{}'".format(session['email']))
                userId = conn.fetchone()
                conn.execute("select productId from products where name='{}'".format(Product_name))
                productId = conn.fetchone()
                conn.execute("insert into kart values('{}','{}','{}')".format(userId[0],productId[0],quantity))
                c.commit()
            return redirect(url_for('Cart'))

#View shopping cart
@app.route('/cart', methods=['POST','GET'])
def Cart ():
    loggedIn, first_name = getLogindetails()
    if loggedIn == False:
        return redirect(url_for('loginform'))
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("select * from products inner join kart on products.productId = kart.productId where kart.userId = (select userId from users where email = '{}')".format(session['email']))
        kart_info = cur.fetchone()
    return render_template('kart.html', loggedIn = loggedIn, first_name = first_name, kart_info = kart_info)

#Place an Order
@app.route('/placeorder')
def placeorder():
    loggedIn, first_name = getLogindetails()
    if loggedIn == False:
        return redirect(url_for('loginform'))
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("select * from products inner join kart on products.productId = kart.productId where kart.userId = (select userId from users where email = '{}')".format(session['email']))
    return redirect(url_for('trackorders'))

#View Order Details/Invoice
@app.route('/viewinvoice')
def viewinvoice():
    loggedIn, first_name = getLogindetails()
    if loggedIn == False:
        return redirect(url_for('loginform'))
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("select * from invoice where userId='{}'".format(session['email']))  
        user_info = cur.fetchone()
    return render_template('invoice.html',loggedIn= loggedIn, first_name=first_name, user_info=user_info)

#Track order status
@app.route('/trackorders', methods=['POST','GET'])
def trackorders():   
    loggedIn, first_name = getLogindetails()
    if loggedIn == False:
        return redirect(url_for('loginform'))
    with sqlite3.connect('database.db') as con:
        if request.method== 'GET':
            cur = con.cursor()
            cur.execute("select * from  orders inner join users on orders.userId = users.userId where email = '{}'".format(session['email']))
            order_info = cur.fetchone()
    return render_template('trackorders.html', loggedIn = loggedIn, first_name = first_name, order_info = order_info)

#Leave Feedback on service                     
@app.route('/feedback', methods=['POST','GET'])
def feedback():   
    loggedIn, first_name = getLogindetails()
    if loggedIn == False:
        return redirect(url_for('loginform'))
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("select * from users where email='{}'".format(session['email'])) 
        user_info = cur.fetchone()
        if request.method == 'POST':
            rating = request.form['rating']
            comments = request.form['comments']
            cur.execute("insert into feedbacks(email, rating, comments) values ('{}', '{}','{}')".format(session['email'], rating, comments))
    return render_template('feedback.html', loggedIn = loggedIn, first_name = first_name, user_info = user_info)


if __name__ == "__main__":
    app.run(debug=True,port=4000)                
