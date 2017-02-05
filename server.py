from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET']


@app.route('/')
def index():

    return render_template('index.html')


if __name__ == '__main__':

    app.debug = True
    # connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')
