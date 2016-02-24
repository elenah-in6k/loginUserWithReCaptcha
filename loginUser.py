from flask import Flask
from flask import render_template
from flask import request

import requests

from MySQLdb import connect

# from recaptcha import RecaptchaClient

app = Flask(__name__)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password'] 
        state = save_to_db(email, password)
        # recaptcha_client = RecaptchaClient('6LfqyRgTAAAAAEMw_phaQfPjZbLRgnvuk2wkUGWE', '6LfqyRgTAAAAAMdZM4AwZCOoJPuE3DOaZ7SQJnb5')
        # recaptcha_response = request.form['g-recaptcha-response']
        # private_key = "6LfqyRgTAAAAAEMw_phaQfPjZbLRgnvuk2wkUGWE"
        # remote_ip = request.remote_addr
        # data = {'secret': private_key, 'response': recaptcha_response ,'remoteip': remote_ip}
        # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        #
        return render_template('afterlogin.html', data='Good:)) Your email: '+email+', password: '+password)
    
    elif request.method == 'GET':
        
        return render_template('login.html')


def save_to_db(email, password):
  db = connect_to_db()
  create_table_users_if_needed(db)
  save_user(db, email, password)
  db.close()
  return 'OK:))'


def connect_to_db():
  return connect(user='root', password='root',
                              host='127.0.0.1',
                              database='users')


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
