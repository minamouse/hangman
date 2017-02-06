from model import Word, Type, db, connect_to_db
from server import app


def load_words():

    f = open('words.txt')
    for row in f:
        rank, word, word_type, freq, _ = row.split()

        word = Word(rank=rank, word=word, word_type=word_type, frequency=freq)
        db.session.add(word)

    f.close()

    db.session.commit()


def load_types():

    info = [('a', 'article'),
            ('c', 'conjuction'),
            ('e', 'existential'),
            ('d', 'demonstrative'),
            ('i', 'adverb'),
            ('j', 'adjective'),
            ('m', 'number'),
            ('n', 'noun'),
            ('p', 'pronoun'),
            ('r', 'preposition'),
            ('u', 'interjection'),
            ('t', 'infinite_marker'),
            ('v', 'verb'),
            ('x', 'negation')]

    for type_id, name in info:
        word_type = Type(type_id=type_id, name=name)
        db.session.add(word_type)

    db.session.commit()

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()

    load_types()
    load_words()
