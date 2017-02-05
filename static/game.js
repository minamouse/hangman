'use strict';

var guessBtn = $('#guess_input');
$.post('/guess.json', {}, updateGame);

guessBtn.on('submit', function (evt) {
    evt.preventDefault();

    var guess = $('#guess_input_text').val();
    var data = {'guess': guess};

    $.post('/guess.json', data, updateGame);
});

function updateVictory(victory) {
    if (victory) {
        $('#victory_status').html('You Win!!!');
    } else {
        $('#victory_status').html('You Lose!!!');
        showWord();
    }
    $('#guess_input_text').attr('disabled', true);
    $('#submit_button').attr('disabled', true);
}

function resetGame() {

    $('#victory_status').html('');
    $('#guess_input_text').attr('disabled', false);
    $('#submit_button').attr('disabled', false);

}

function showWord() {
    $.get('/get_word', function(response){
        var word = response.word.split('');
        var guesses = $('#current_word').html().split(' ');
        console.log(guesses);
        var coloredLetters = [];
        for (var i = 0; i < word.length; i++) {
            if (word[i] === guesses[i]) {
                coloredLetters.push(word[i]);
            } else {
                coloredLetters.push('<span class="incorrect">' + word[i] + '</span>');
            }
        }
        $('#current_word').html(coloredLetters.join(' '));
    });
}

function updateGame(response) {
    $('#guess_input_text').val('');

    updateGuessedLetters(response.bad_guesses);
    updateWord(response.letters);
    if (response.finished) {
        updateVictory(response.victory);
    }
    updateAscii(response.bad_guesses.length);
    if (response.message) {
        $('#message').html(response.message);
    } else {
        $('#message').html('');
    }
}

function updateGuessedLetters(guesses) {
    $('#all_guesses').html(guesses.join(' '));
}

function updateAscii(qty) {
    var id_num = '#n' + qty;
    console.log(id_num);
    $('pre').attr('hidden', true);
    $(id_num).attr('hidden', false);
}

function updateWord(letters) {
    $('#current_word').html(letters.join(' '));
}