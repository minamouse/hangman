from flask import Flask, render_template, jsonify, request, session
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

    guess = request.form.get('guess')
    session['guesses'] = session['guesses'] + [guess]

    letters = check_guess()

    return jsonify({'letters': letters,
                    'all_guesses': session['guesses']})

if __name__ == '__main__':

    app.debug = True
    # connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')
