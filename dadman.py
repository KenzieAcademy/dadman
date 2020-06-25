import os
import re
import sys
import requests

"""
A Dad Joke Wheel of Fortune-style Game!

TODO:
- setup:
    - [DONE] initialize number of chances (6)
    - [DONE] obtain a random phrase (https://icanhazdadjoke.com/)
    - [DONE] represent the phrase as a series of underscores
    - [DONE] display the outcome (number of incorrect guesses remaining)
    - [DONE] maintain a list of guessed letters
- game loop:
    - [DONE] prompt user to enter a letter
    - [DONE] determine whether the user's guess is in the phrase
    - provide feedback about the user's guess
        - [DONE] if correct, display letter where it belongs in the phrase
        - [DONE]if incorrect, decrement number of guesses remaining
    - [DONE] display all guessed letters
    - is game over?
        - [DONE] win: phrase is entirely filled
        - [DONE] lose: number of incorrect guesses used
"""
joke_request_attempts = 3
guessed_letters = []


def get_joke():
    headers = {'accept': 'application/json'}
    for _ in range(joke_request_attempts):
        response = requests.get('https://icanhazdadjoke.com/', headers=headers)
        data = response.json()
        text = data['joke']

        # restrict joke format from API response to a
        # joke sentence followed by a punchline sentence
        joke_match = re.search(r'(.+[.?!])(.+[.?!])', text)
        if joke_match:
            joke = joke_match.group(1).strip()
            punchline = joke_match.group(2).strip()
            return joke, punchline

    print('Did not find a well-formatted joke within API limits.')
    sys.exit(1)


def update_blanks(punchline):
    display = []
    for char in punchline.lower():
        if not char.isalpha() or char in guessed_letters:
            display.append(char)
        else:
            display.append('_')
    display[0] = display[0].upper()
    return ' '.join(display)


def main():
    guesses_remaining = 5
    joke = get_joke()
    text, punchline = joke

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{text}")
        unguessed = update_blanks(punchline)
        if '_' not in unguessed:
            print(punchline)
            print('You win! Good job, nerd!')
            break
        print(unguessed)
        print(f"\nGuesses remaining: {guesses_remaining}\n")
        print(f"Previous guesses: {' '.join(guessed_letters)}")
        guess = input("Guess a letter: ").lower()
        if guess not in punchline:
            if guess not in guessed_letters:
                guesses_remaining -= 1
        if guess not in guessed_letters:
            guessed_letters.append(guess)
        if not guesses_remaining:
            print('Game Over!')
            break


if __name__ == '__main__':
    main()
