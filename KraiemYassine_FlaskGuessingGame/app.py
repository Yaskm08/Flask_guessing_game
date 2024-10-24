"""
Yassine Kraiem
WI2024
Independent Study Final Project
Flask Guessing Game:
The app generates a random number between 1 and 20 (inclusive) and asks the user to guess it.
The user has only 5 guesses. The app should prevent the user from guessing the same number twice
(“You already guessed that! Give me a new guess.”)
and display the number of guesses remaining. If the user guesses the number before running out,
or runs out of guesses before guessing correctly, display a “game over” page that says “You [won/lost]!
Click here if you’d like to play again.” This should be a template where ‘won’ or ‘lost’ is a parameter.
And of course, “Click here” should be a hyperlink that takes the user to a new game. The game's "home page" should be /game
Displaying the number of guesses remaining  as an image like a long green rectangle that gets shorter with each guess
until it's gone.
"""


import base64
import random
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'some_secret_key'


def initialize_game():
    session['number'] = random.randint(1, 20)
    session['remaining_guesses'] = 5
    session['guesses'] = []


@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'number' not in session:
        initialize_game()

    if request.method == 'POST':
        rect_width = session['remaining_guesses'] * 80  # Adjust the width as needed.
        rect_height = 70  # You can adjust the height.
        im = Image.new('RGB', (rect_width, rect_height), color='Darkgreen')
        output = BytesIO()
        im.save(output, format='PNG')
        img_bytes = output.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        remaining_percentage = (session['remaining_guesses'] / 5) * 100
        guess = int(request.form['guess'])
        while guess != session['number']:
            if session['remaining_guesses'] == 1:
                return redirect(url_for('game_over', result='lost'))
            if guess == session['number']:
                break
            if guess in session.get('guesses', []):
                return render_template('game.html', remaining_percentage=remaining_percentage, img_base64=img_base64, message='You already guessed that! Give me a new guess.')
            session['remaining_guesses'] -= 1
            session['guesses'].append(guess)
            rect_width = session['remaining_guesses'] * 80  # Adjust the width as needed.
            rect_height = 70  # You can adjust the height.
            im = Image.new('RGB', (rect_width, rect_height), color='Darkgreen')
            output = BytesIO()
            im.save(output, format='PNG')
            img_bytes = output.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            return render_template('game.html', remaining_percentage=remaining_percentage, img_base64=img_base64, message='Guess a number between 1 and 20.')
        return redirect(url_for('game_over', result='won'))

    #     session['guesses'] = session.get('guesses', []) + [guess]

    # Create an image of a decreasing rectangle based on remaining guesses.
    rect_width = session['remaining_guesses'] * 80  # Adjust the width as needed.
    rect_height = 70  # You can adjust the height.
    im = Image.new('RGB', (rect_width, rect_height), color='Darkgreen')

    # Render the image to a BytesIO object.
    output = BytesIO()
    im.save(output, format='PNG')
    img_bytes = output.getvalue()

    # Encode the image in base64.

    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    remaining_percentage = (session['remaining_guesses'] / 5) * 100

    return render_template('game.html', remaining_percentage=remaining_percentage, img_base64=img_base64, message='')


@app.route('/gameover/<result>', methods=['GET'])
def game_over(result):
    if 'number' in session:
        session.pop('number')
    if 'guesses' in session:
        session.pop('guesses')
    return render_template('gameover.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
