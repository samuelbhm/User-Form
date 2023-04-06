### IMPORTING SELECTION ###


#Flask is a back-end framework for Python that allows you to create web applications. 
from flask import Flask, render_template, request, send_file, session, redirect

#mysql.connector is a Python library that allows you to interact with MySQL databases.
import mysql.connector  
from mysql.connector import Error

#hashlib is a Python library that allows you to hash passwords
import hashlib

#secrets is a Python library that allows you to generate secret tokens used for functions such as password_reset
import secrets

#generates a secret token
secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secret_key

#tries to connect to the database
try:
  global conn
  conn = mysql.connector.connect(host="localhost", 
                                 user="root", 
                                 password="", 
                                 database="user_login")
  #if the connection is successful, then the database is connected
  if conn.is_connected():
    global cursor
    cursor = conn.cursor()
    db_info = conn.get_server_info()
    print('Connectedto Mysql server version ', db_info)

#if the connection fails 
except Error as e:  
  print('An Error Occured while connecting to MySQL', e)  


@app.route('/')
def home():
  return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s AND email = %s", (username, hashed_password, email))
    user = cursor.fetchone()
    if user:
      session['username'] = username
      return redirect('/welcome')
    
    else:
      Error = 'Invalid username or password. Please try again.'
      return render_template('register.html', error=Error)
  
  else:
    return render_template('register.html')
  
@app.route('/welcome')
def welcome():
  username = session.get('username')
  return render_template('welcome.html', username=username)

  
@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    pin = request.form['pin']
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("SELECT * FROM accounts WHERE username = %s AND email = %s AND pin = %s", (username, email, pin))
    user = cursor.fetchone()  
    if user:
      error = 'Username, email or recovery pin already exists. Please choose another Username or email.'
      return render_template('register.html', error=error)
    else:
      cursor.execute("INSERT INTO accounts (username, password, email, pin) VALUES (%s, %s, %s, %s)", (username, hashed_password, email, pin))
      conn.commit()
      session['username'] = username  
      return redirect('/')
  else: 
    return render_template('register.html')
  
@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect('/login')

@app.route('/reset')
def reset():
  return render_template('password_reset.html')

@app.route('/confirm_reset', methods=['POST'])
def confirm_reset():  
  username = request.form.get('username')
  new_password = request.form.get('password')
  confirm_password = request.form.get('confirm_password')
  pin = request.form.get('pin')
  
  query = f'SELECT username, pin From accounts'
  cursor.execute(query)
  data = cursor.fetchall()
  print(data)
  
  conf = 0 
  
  for i in range(3):
    if username in data[i][0] and pin == data[i][1]:
      conf = 1
    else:
      conf = 0
  
  if new_password == confirm_password and conf == 1:
    password = confirm_password 
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("UPDATE accounts SET password = %s WHERE username = %s", (hashed_password, username))
    conn.commit()
    return render_template('login.html')
  
  else:
    error = '''something went wrong! \n
               Please try again.
            '''
    return render_template('password_reset.html', error=error)
  
if __name__ == "__main__":
	app.run(debug=True)