from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
import requests
import json

app = Flask(__name__)
database_name = 'users'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password'] 
        recaptcha_response = request.form['g-recaptcha-response']

        if validate_recaptcha_response(recaptcha_response) == True:
            save_to_db(email, password)

        return render_template('afterlogin.html', data='Good:)) Your email: '+email+', password: '+password)
    
    elif request.method == 'GET':
        
        return render_template('login.html')


def validate_recaptcha_response(recaptcha_response):
    private_key = "6LfqyRgTAAAAAEMw_phaQfPjZbLRgnvuk2wkUGWE"
    google_recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
    params = {'response': recaptcha_response, 'secret': private_key}
    response = requests.post(google_recaptcha_url, params=params)
    recaptcha_data = json.loads(response.text)
    success = recaptcha_data["success"]

    return success


def save_to_db(email, password):
  db = connect_to_db(database_name)
  create_table_users_if_needed(db)
  save_user(db, email, password)
  db.close()


def connect_to_db(database_name):
  return mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database=database_name)


def create_table_users_if_needed(db):
  cursor = db.cursor()
  create_table_users = """CREATE TABLE IF NOT EXISTS `users` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `email` varchar(100) NOT NULL,
              `password` varchar(100) NOT NULL,
              PRIMARY KEY (`id`)
            ); """
  cursor.execute(create_table_users)
  db.commit()


def save_user(db, email, password):
  cursor = db.cursor()
  save_users = """INSERT INTO `users`
                 (email, password)
                 VALUES ('%s', '%s') """ % (email, password)
  cursor.execute(save_users)
  db.commit()
  cursor.close()


if __name__ == '__main__':
    app.run()
