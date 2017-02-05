from flask import Flask, render_template, jsonify, request, session, redirect, flash
import os
import random

app = Flask(__name__)
app.secret_key = os.environ['SECRET']

WORDS = ['blue', 'zebra', 'potato']


@app.route('/')
def index():

    if 'word' not in session:
        session['word'] = random.choice(WORDS)
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

    return jsonify({'letters': letters,
                    'bad_guesses': session['bad_guesses'],
                    'victory': victory,
                    'finished': session['finished'],
                    'message': message})


@app.route('/reset', methods=['POST'])
def reset():

    session.pop('word')
    session.pop('guesses')
    session.pop('qty_guesses')

    return redirect('/')


@app.route('/get_word')
def get_word():

    if session['finished']:
        return jsonify({'word': session['word']})
    else:
        return 'none of your business'

if __name__ == '__main__':

    app.debug = True
    # connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')
