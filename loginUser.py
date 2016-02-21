from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
  #from recaptcha import verify
  ## recaptcha_client = recaptcha.client('6LfqyRgTAAAAAEMw_phaQfPjZbLRgnvuk2wkUGWE', '6LfqyRgTAAAAAMdZM4AwZCOoJPuE3DOaZ7SQJnb5')

app = Flask(__name__)
 
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password'] 
        state = saveToDB(email, password)
       
        # private_key = "6LfqyRgTAAAAAEMw_phaQfPjZbLRgnvuk2wkUGWE"
        # remote_ip = request.META['REMOTE_ADDR']
        # challenge = request.POST.get('recaptcha_challenge_field', '')
        # response = request.POST.get('recaptcha_response_field', '')

        # result = verify(private_key, remote_ip, challenge, response)  
        
        return render_template('afterlogin.html', data = 'Good:)) Your email: ' + email + ', password: ' + password + ", state: " + state)
    
    elif request.method == 'GET':
        
        return render_template('login.html')

def saveToDB(email, password):
  db = connectToDB()
  createTableUsersIfNeeded(db)
  saveUser(db, email, password)
  db.close()
  
  return 'OK:))'

def connectToDB():
  return mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='users')

def createTableUsersIfNeeded(db):
  cursor = db.cursor()
  createTableUsers = """CREATE TABLE IF NOT EXISTS `users` (
              `id` int(11) NOT NULL AUTO_INCREMENT, 
              `email` varchar(100) NOT NULL, 
              `password` varchar(100) NOT NULL, 
              PRIMARY KEY (`id`)
            ); """
  cursor.execute(createTableUsers)
  db.commit()

def saveUser(db, email, password):
  cursor = db.cursor()
  saveUsers = """INSERT INTO `users` 
                 (email, password) 
                 VALUES ('%s', '%s') """ % (email, password)

  cursor.execute(saveUsers)
  db.commit()
  cursor.close()

if __name__ == '__main__':
    app.run()
    