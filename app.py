from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def choose_word():
    words = ["python", "programming", "hangman", "computer", "developer", "coding", "challenge"]
    return random.choice(words)

def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += " _ "
    return display

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hangman', methods=['GET', 'POST'])
def hangman():
    if request.method == 'POST':
        if 'reset' in request.form:
            session.clear()
            return redirect(url_for('index'))

        if 'secret_word' not in session:
            session['secret_word'] = choose_word()
            session['guessed_letters'] = []
            session['incorrect_attempts'] = 0
            session['max_attempts'] = 6

        secret_word = session['secret_word']
        guessed_letters = session['guessed_letters']
        incorrect_attempts = session['incorrect_attempts']
        max_attempts = session['max_attempts']

        if 'guess' in request.form:
            guess = request.form['guess'].lower()

            if len(guess) == 1 and guess.isalpha() and guess not in guessed_letters:
                guessed_letters.append(guess)

                if guess not in secret_word:
                    session['incorrect_attempts'] += 1

        current_display = display_word(secret_word, guessed_letters)

        if current_display == secret_word:
            result_message = 'Congratulations! You guessed the word.'
            session.clear()  # Reset the session after the game is over
            return render_template('result.html', result=result_message)

        if incorrect_attempts == max_attempts:
            result_message = f"Sorry, you've run out of attempts. The word was: {secret_word}"
            session.clear()  # Reset the session after the game is over
            return render_template('result.html', result=result_message)

        session['current_display'] = current_display
        session['guessed_letters'] = guessed_letters  # Update guessed letters in the session
        return render_template('hangman.html', current_word=current_display, max_attempts=max_attempts, incorrect_attempts=incorrect_attempts, guessed_letters=guessed_letters)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
