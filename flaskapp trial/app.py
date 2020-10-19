from flask import Flask, render_template,request,redirect
from flask_mysqldb import MySQL
import yaml

app=Flask(__name__)

db= yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']= db['mysql_host']
app.config['MYSQL_USER']= db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']= db['mysql_db']

mysql= MySQL(app)

@app.route('/',methods=['GET','POST'])
def login():
	return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
	return render_template('register.html')

@app.route('/user',methods=['POST'])
def user():
	userdetails= request.form
	username= userdetails['username']
	password= userdetails['password']
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO users(username,password) VALUES(%s,%s)",(username,password))
	mysql.connection.commit()
	cur.close()
	return "account created"

@app.route('/home',methods=['POST'])
def home():
    userdetails= request.form
    username= userdetails['username']
    password= userdetails['password']
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM `users` WHERE `username` LIKE '{}' AND `password` LIKE '{}'""".format(username,password))
    #cur.execute("SELECT * FROM users")
    users= cur.fetchall()

    if(len(users)>0):
        return "Success Hi {} welcome back!!".format(username)
    else:
        return "Invalid Username or Password"


if __name__=='__main__':
	app.run(debug=True)