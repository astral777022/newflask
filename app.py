#бібла
from flask import Flask, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Створюємо новий додаток Flack
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'  #Налаштовуємо підключення до БД
db = SQLAlchemy(app)                                             #Створюємо об'єкт БД SQLAlchemy

class Post(db.Model):                                              #Створює новий клас Post, який успадковується від db.Model
    id = db.Column(db.Integer, primary_key=True)                   #Створює колонку ID
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")                                                     #Декоратор сторінки Index
@app.route("/index")
def index():
    return render_template('Index.html')

@app.route("/teacher")                                              #Декоратор сторінки вчителя
def teacher():
    return render_template('teacher.html')

@app.route("/parents")                                              #Декоратор сторінки батьків
def parents():
    return render_template('parents.html')

@app.route("/student")                                              #Декоратор сторінки дітей
def student():
    return render_template('student.html')

@app.route("/calendar")                                             #Декоратор сторінки календаря
def calendar():
    return render_template('calendar.html')

@app.route("/api/events", methods=['GET'])                          
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d %H:%M:%S')
    } for event in events])

@app.route("/api/events", methods=['POST'])
def create_event():
    data = request.json
    event = Event(
        title=data['title'],
        description=data.get('description', ''),
        date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route("/api/events/<int:event_id>", methods=['PUT'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.json
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    if 'date' in data:
        event.date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
    db.session.commit()
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route("/api/events/<int:event_id>", methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return '', 204

@app.route('/register', methods=['POST'])
def register():
    # Add your registration logic here
    return "Registered successfully"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        # Add proper authentication logic here
        print(f"Login attempt: {name}")  # For debugging only
        return redirect('parents')
    return render_template('login.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
