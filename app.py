from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# Register Blueprints
from tasks import tasks_bp
from mood import mood_bp

app.register_blueprint(tasks_bp, url_prefix='/tasks')
app.register_blueprint(mood_bp, url_prefix='/mood')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
