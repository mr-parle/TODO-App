# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
db = SQLAlchemy(app)

# Define models
class IncompleteTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

class CompletedTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_task = request.form['task']
        incomplete_task = IncompleteTask(task=new_task)
        db.session.add(incomplete_task)
        db.session.commit()
        return redirect(url_for('index'))
    incomplete_tasks = IncompleteTask.query.all()
    completed_tasks = CompletedTask.query.all()
    return render_template('index.html', incomplete_tasks=incomplete_tasks, completed_tasks=completed_tasks)

@app.route('/complete/<int:id>')
def complete(id):
    task_to_complete = IncompleteTask.query.get_or_404(id)
    completed_tasks = CompletedTask(task=task_to_complete.task)
    db.session.add(completed_tasks)
    db.session.delete(task_to_complete)
    db.session.commit()
    return redirect(url_for('index'))

def create_db_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db_tables()  # Call the function to create the database tables
    app.run(debug=True)
  
  
 