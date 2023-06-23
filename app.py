from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    dateCreated = db.Column(db.DateTime, default = datetime.utcnow) 

    def __repr__(self):
        return f'{self.sno} - {self.title}'


@app.route('/',  methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        if len(request.form['title']) > 0:
            todo = Todo(title = request.form['title'], desc = request.form['desc'])
            db.session.add (todo)
            db.session.commit()
    all_todo = Todo.query.all()
    return render_template('index.html', all_todo = all_todo)


@app.route('/delete/<int:sno_>')
def delete_todo(sno_):
    todo = Todo.query.filter_by(sno = sno_).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:sno_>', methods = ['POST', 'GET'])
def update_todo(sno_):
    if request.method == 'POST':
        todo = Todo.query.filter_by(sno = sno_).first()
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.date = datetime.utcnow
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    else:
        todo = Todo.query.filter_by(sno = sno_).first()
        return render_template('update.html', todo = todo)


if __name__ == '__main__':
    app.run(debug=True)