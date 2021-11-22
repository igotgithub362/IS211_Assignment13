

from flask import Flask, render_template, request, redirect, g, url_for, abort, session, flash
from contextlib import closing
import time, os, sqlite3, re

DATABASE = 'hw13.db'
DEBUG = True
SECRET_KEY = 'dd50b560b1ba65dadefbcb6e35963715ed92a79643677744'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resources('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
		
@app.before_request
def before_request():
	g.db = connect_db()
	
@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'hw13.db', None)
	if db is not None:
		db.close()
		
@app.route('/')
def index():
	return redirect(url_for('login'))
		
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['username']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['password']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect('/dashboard')
	return render_template('login.html', error=error)
	
@app.route('/dashboard', methods=['GET'])
def dashboard():
		cur = g.db.execute('SELECT id, first_name, last_name FROM students')
		students = [dict(ID=row[0], first_name=row[1], last_name=row[2])
					for row in cur.fetchall()]
		cur1 = g.db.execute('SELECT id, subject, num_questions, quiz_date FROM quizzes')
		quizzes = [dict(ID=row[0], subject=row[1], num_questions=row[2], quiz_date=row[3])
					for row in cur1.fetchall()]
		return render_template('dashboard.html', students=students, quizzes=quizzes)
		
@app.route('/student/add', methods=['GET', 'POST'])
def add_students():
	if request.method =='GET':
		return render_template('addstudent.html')
	elif request.method =='POST':
		if not session.get('logged_in'):
			abort(401)
		g.db.execute('INSERT into students (first_name, last_name) VALUES (?, ?)', 
					[request.form['first_name']. request.form['last_name']])
		g.db.commit()
	flash('New student successfully added')
	return redirect(url_for('dashboard'))
	
@app.route('/quiz.add', methods=['GET', 'POST'])
def add_quiz():
	if request.method =='GET':
		return render_template('addquiz.html')
	elif request.method =='POST':
		if not session.get('logged_in'):
			abort(401)
		g.db.execute('INSERT INTO quizzes (subject, num_questions, quiz_date) '
					'VALUES (?, ?, ?)', [request.form['subject'], request.form['num_questions'], request.form['quiz_date']])
		gb.db.commit()
	flash('New quiz successfully added')
	return redirect(url_for('dashboard'))
	
@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
	if request.method == 'GET':
		cur4 = g.db.execute('SELECT id, subject FROM quizzes')
		quizzes = [dict(quiz_id=row[0], subject=row[1]) for row in cur4.fetchall()]
		cur5 = g.db.execute('SELECT id, first_name, last_name FROM students')
		students = [dict(student_id=row[0], student_name='{} {}'.format(row[1], row[2])) for row in cur5.fetchall()]
		return render_template('addresults.html', quizzes=quizzes, students=students)
	elif request.method == 'POST':
		g.db.execute('INSERT INTO results (stu_id, quiz_id, score) VALUES '
					'(?, ?, ?)', (request.form['stu_id'], request.form['quiz_id']. request.form['score']))
		g.db.commit()
		flash('Quiz results successfully added')
		return redirect('/dashboard')
	else:
		flash('Could not successfully update results')
		return redirect('/results/add')
		
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You are logged out')
	return redirect(url_for('login'))
	
if __name__ == '__main__':
	app.run()
