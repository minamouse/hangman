from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Word(db.Model):

    __tablename__ = 'words'

    rank = db.Column(db.Integer, autoincrement=True, primary_key=True)
    word = db.Column(db.String(30), nullable=False)
    word_type = db.Column(db.String(1), db.ForeignKey('types.type_id'), nullable=True)
    frequency = db.Column(db.Integer, nullable=True)

    def __repr__(self):

        return '<%s - %s>' % (self.word, self.word_type)


class Type(db.Model):

    __tablename__ = 'types'

    type_id = db.Column(db.String(1), primary_key=True)
    name = db.Column(db.String(20), nullable=True)

    def __repr__(self):

        return '<%s - %s>' % (self.type_id, self.name)


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    wins = db.Column(db.Integer, nullable=True)
    games_played = db.Column(db.Integer, nullable=True)

    def __repr__(self):

        return '<%s - %s - %s>' % (self.user_id, self.username, self.email)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hangman'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
