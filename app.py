from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moodboard.db'
db = SQLAlchemy(app)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/mood', methods=['POST'])
def create_mood_entry():
    data = request.get_json()
    user_id = data['user_id']
    mood = data['mood']
    description = data.get('description', '')
    
    new_entry = MoodEntry(user_id=user_id, mood=mood, description=description)
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify({'message': 'Mood entry created'}), 201

@app.route('/api/mood/<int:user_id>', methods=['GET'])
def get_mood_entries(user_id):
    entries = MoodEntry.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': entry.id,
        'mood': entry.mood,
        'description': entry.description,
        'created_at': entry.created_at.isoformat()
    } for entry in entries]), 200

def generate_random_moods(user_id, num_days=30):
    moods = ['sad', 'normal', 'happy']
    start_date = datetime.utcnow() - timedelta(days=num_days-1)
    
    for i in range(num_days):
        mood = random.choice(moods)
        date = start_date + timedelta(days=i)
        entry = MoodEntry(user_id=user_id, mood=mood, created_at=date)
        db.session.add(entry)
    
    db.session.commit()

@app.route('/api/generate-moods/<int:user_id>', methods=['POST'])
def generate_moods(user_id):
    generate_random_moods(user_id)
    return jsonify({'message': 'Random mood entries generated'}), 201

if __name__ == '__main__':
    app.run(debug=True)
