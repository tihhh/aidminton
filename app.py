from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
import os
from os import environ
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = environ.get('FLASK_SECRET_KEY')  
app.config['DATABASE'] = os.path.join(app.root_path, 'aidminton.db')

# Database Helper Functions
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        with open('schema.sql') as f:
            db.executescript(f.read())
        db.commit()
        db.close()

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_nickname'] = user['nickname']
            session['user_email'] = user['email']
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data based on the step
        step = int(request.form.get('step', 1))
        
        if step == 3:  # Final step
            name = request.form.get('name', '')
            nickname = request.form.get('nickname', '')
            email = request.form.get('email', '')
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            phone_number = request.form.get('phone_number', '')
            
            if not all([name, nickname, email, password, confirm_password, phone_number]):
                flash('All fields are required', 'error')
                return render_template('signup.html', step=3, 
                                      name=name, nickname=nickname, 
                                      email=email, password=password, 
                                      confirm_password=confirm_password)
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template('signup.html', step=2, 
                                      name=name, nickname=nickname, 
                                      email=email)
            
            # Check if email already exists
            conn = get_db_connection()
            existing_user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
            
            if existing_user:
                conn.close()
                flash('Email already registered', 'error')
                return render_template('signup.html', step=2, 
                                      name=name, nickname=nickname)
            
            # Create new user
            hashed_password = generate_password_hash(password)
            try:
                conn.execute(
                    'INSERT INTO users (name, nickname, email, password, phone_number) VALUES (?, ?, ?, ?, ?)',
                    (name, nickname, email, hashed_password, phone_number)
                )
                conn.commit()
                conn.close()
                
                flash('Account created successfully! Please log in.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                conn.close()
                flash(f'Error creating account: {str(e)}', 'error')
                return render_template('signup.html', step=3, 
                                      name=name, nickname=nickname, 
                                      email=email, password=password, 
                                      confirm_password=confirm_password)
            
        # Just render the next step
        return render_template('signup.html', step=step+1, **request.form)
    
    return render_template('signup.html', step=1)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form['name']
        nickname = request.form['nickname']
        phone_number = request.form['phone_number']
        
        conn = get_db_connection()
        conn.execute(
            'UPDATE users SET name = ?, nickname = ?, phone_number = ? WHERE id = ?',
            (name, nickname, phone_number, session['user_id'])
        )
        conn.commit()
        conn.close()
        
        # Update session data
        session['user_name'] = name
        session['user_nickname'] = nickname
        
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

@app.route('/injuries')
@login_required
def injuries():
    return render_template('injuries.html')

@app.route('/injury-log')
@login_required
def injury_log():
    conn = get_db_connection()
    injuries = conn.execute(
        'SELECT * FROM injury_logs WHERE user_id = ? ORDER BY date DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    
    return render_template('injury_log.html', injuries=injuries)

@app.route('/add-injury', methods=['GET', 'POST'])
@login_required
def add_injury():
    if request.method == 'POST':
        try:
            title = request.form.get('title', '')
            description = request.form.get('description', '')
            date = request.form.get('date', '')
            pain_level = request.form.get('pain_level', '5')
            
            if not all([title, description, date, pain_level]):
                flash('All fields are required', 'error')
                return render_template('add_injury.html')
            
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO injury_logs (user_id, title, description, date, pain_level) VALUES (?, ?, ?, ?, ?)',
                (session['user_id'], title, description, date, pain_level)
            )
            conn.commit()
            conn.close()
            
            flash('Injury log added successfully', 'success')
            return redirect(url_for('injury_log'))
        except Exception as e:
            flash(f'Error adding injury log: {str(e)}', 'error')
            return render_template('add_injury.html')
    
    return render_template('add_injury.html')

@app.route('/medical-experts')
def medical_experts():
    conn = get_db_connection()
    experts = conn.execute('SELECT * FROM medical_experts').fetchall()
    conn.close()
    
    return render_template('medical_experts.html', experts=experts)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q', '')
    results = []
    
    if query:
        conn = get_db_connection()
        # Search in injuries
        injuries = conn.execute(
            "SELECT * FROM common_injuries WHERE title LIKE ? OR description LIKE ?",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        
        # Search in experts
        experts = conn.execute(
            "SELECT * FROM medical_experts WHERE name LIKE ? OR specialty LIKE ?",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        
        conn.close()
        
        results = {
            'injuries': injuries,
            'experts': experts
        }
    
    return render_template('search.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)