from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    des = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(80) , nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, des = desc, date=datetime.now())
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all()
    return render_template('todo.html', allTodo=allTodo)

@app.route('/cal')
def cal():
    return render_template('calculator.html')

@app.route('/todo/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todo')

@app.route('/todo/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc'] 
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.des = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/todo')
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)