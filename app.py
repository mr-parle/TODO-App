  
from flask import Flask, render_template,flash, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
db=SQLAlchemy(app)

class PendingTask(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    task = db.Column(db.String(200), nullable=False)
    
class CompletedTask(db.Model):
    id=db.Column(db.Integer, primary_key= True)
    task = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        new_task = request.form['task']
        pending_task = PendingTask(task= new_task)
        db.session.add(pending_task)
        db.session.commit()
        return redirect(url_for('index'))
    pending_task= PendingTask.query.all()
    completed_task= CompletedTask.query.all()
    return render_template('index.html', pending_task= pending_task, completed_task = completed_task)

@app.route('/complete/<int:id>')
def complete(id):
    task_to_complete = PendingTask.query.get_or_404(id)
    completed_task = CompletedTask(task = task_to_complete.task)
    db.session.add(completed_task)
    db.session.delete(task_to_complete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_all', methods=['POST'])
def delete_all():
    CompletedTask.query.delete()
    PendingTask.query.delete()
    db.session.commit()
    return redirect(url_for('index'))

def create_db_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_db_tables()  # Call the function to create the database tables
    app.run(debug=True)