from flask import Flask, render_template, flash, jsonify, request, session, redirect
import os
import random
from model import connect_to_db, Word, User, db

app = Flask(__name__)
app.secret_key = os.environ['SECRET']


def pick_word():

    words = Word.query.all()
    return random.choice(words).word


@app.route('/')
def index():

    if 'word' not in session:
        session['word'] = pick_word()
        session['guesses'] = []
        session['bad_guesses'] = []
        session['qty_guesses'] = 6
        session['finished'] = False

    return render_template('index.html')


def check_guess():

    letters = []
    for l in session['word']:
        if l in session['guesses']:
            letters.append(l)
        else:
            letters.append('_')
    return letters


@app.route('/guess.json', methods=['POST'])
def guess():

    guess = request.form.get('guess', None)
    message = None
    if guess:
        guess = guess.lower()
        session['guesses'] = session['guesses'] + [guess]
        if guess not in session['word']:
            if guess in session['bad_guesses']:
                message = 'You already guessed that letter!'
            else:
                session['bad_guesses'] = session['bad_guesses'] + [guess]

    letters = check_guess()
    victory = ''.join(letters) == session['word']
    if session['qty_guesses'] == len(session['bad_guesses']) or victory:
        session['finished'] = True
        if 'user' in session:
            user = User.query.filter_by(username=session['user']).one()
            user.games_played += 1
        if victory:
            if 'user' in session:
                user.wins += 1
            session.pop('word')
        db.session.commit()

    return jsonify({'letters': letters,
                    'bad_guesses': session['bad_guesses'],
                    'victory': victory,
                    'finished': session['finished'],
                    'message': message})


@app.route('/reset', methods=['POST'])
def reset():

    if 'word' in session:
        session.pop('word')
    session.pop('guesses')
    session.pop('qty_guesses')

    return redirect('/')


@app.route('/get_word')
def get_word():

    if session['finished']:
        word = session['word']
        session.pop('word')
        return jsonify({'word': word})
    else:
        return 'none of your business'


@app.route('/leaderboard')
def leaderboard():
    leaders = User.query.order_by('wins desc').limit(5).all()
    data = []
    for leader in leaders:
        data.append((leader.wins, leader.username))
    return render_template('leaderboard.html', data=data)


@app.route('/login', methods=['GET'])
def login():

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def process_login():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user:
        if user.password != password:
            flash('Incorrect password!')
            return redirect('/login')
    else:
        user = User(username=username, password=password, wins=0, games_played=0)
        db.session.add(user)
        db.session.commit()

    session['user'] = user.username

    return redirect('/')


@app.route('/logout')
def logout():

    session.pop('user')
    return redirect('/')


@app.route('/profile')
def profile():
    user = User.query.filter_by(username=session['user']).one()

    return render_template('profile.html',
                           games_won=user.wins,
                           games_played=user.games_played)

if __name__ == '__main__':

    app.debug = True
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')
