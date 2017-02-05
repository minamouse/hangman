'use strict';

var guessBtn = $('#guess_input');

guessBtn.on('submit', function (evt) {
    evt.preventDefault();

    var guess = $('#guess_input_text').val();
    var data = {'guess': guess};

    $.post('/guess.json', data, updateGame);
});

function updateGame(response) {
    $('#guess_input_text').val('');

    updateGuessedLetters(response.all_guesses);
    updateWord(response.letters);
}

function updateGuessedLetters(guesses) {
    $('#all_guesses').html(guesses.join(' '));
}

function updateWord(letters) {
    $('#current_word').html(letters.join(' '));
}