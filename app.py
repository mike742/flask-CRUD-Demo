from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "flash message"

app.config['MYSQL_HOST'] = '127.0.0.1' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

@app.route('/')
def Index():
    c = mysql.connection.cursor()
    c.execute("SELECT * FROM jokes")
    data = c.fetchall()
    c.close()

    return render_template('index.html', jokes=data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash('Data inserted successfully')
        firstSentence = request.form['firstSentence']
        secondSentence = request.form['secondSentence']
        c = mysql.connection.cursor()
        c.execute("INSERT INTO jokes (firstSentence, secondSentence) VALUES (%s, %s)", (firstSentence, secondSentence))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/update', methods = ['POST'])
def update():
    if request.method == "POST":
        flash('Data updated successfully')
        jokeId = request.form['id']
        firstSentence = request.form['firstSentence']
        secondSentence = request.form['secondSentence']
        c = mysql.connection.cursor()
        c.execute("UPDATE jokes SET firstSentence=%s, secondSentence=%s WHERE id=%s", (firstSentence, secondSentence, jokeId))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete//<string:jokeId>', methods = ['GET'])
def delete(jokeId):
    flash('Data deleted successfully')
    c = mysql.connection.cursor()
    c.execute("DELETE FROM jokes WHERE id=%s", (jokeId))
    mysql.connection.commit()
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
    
    
