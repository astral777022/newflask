from flask import Flask, render_template         #За допомогою класу Flack будемо створювати додаток
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)           # Створюємо додаток
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
db = SQLAlchemy(app)

class Post(db.Model):                                   # створюємо таблицю
    id = db.Column(db.Integer, primary_key=True)        #перша колонка 
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    

@app.route("/index")            #Декоратор для головної сторінки
@app.route("/")
def index():
    return render_template('Index.html')

@app.route("/about")            # Декоратор для сторінки про нас
def about():
    return render_template('about.html')

if __name__ == '__main__':      # Если в нашем проекте один файл, то запускаем егоЧВ
    app.run(host="0.0.0.0", port=5000, debug=True)
    