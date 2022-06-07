from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer, default=0)
    data_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"<Task {self.id}>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = TODO(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Issue in adding task"
    else:
        tasks = TODO.query.order_by(TODO.data_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')    
def delete(id):
    task_to_delete = TODO.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except :
        return "There was an error in deleting that task"


@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = TODO.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception:
            return "Error while updating"
    else:
        return render_template('update.html',task=task)


if __name__ == '__main__':
    app.run(debug=True)