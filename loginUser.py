from flask import Flask
from flask import render_template
from flask import request
import mysql.connector

app = Flask(__name__)
 
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password'] 
        db = connectToDB()
        db.close()
        return 'Good:)) Your email: ' + email + ', password: ' + password 

    elif request.method == 'GET':
        return render_template('login.html')


def connectToDB():
	return mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='users')
def createTableUsersIfNeeded():
	return """CREATE TABLE IF NOT EXISTS `users` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `email` varchar(100) NOT NULL,
              `password` varchar(100) NOT NULL,
              PRIMARY KEY (`id`)
            )"""

if __name__ == '__main__':
    app.run()
    