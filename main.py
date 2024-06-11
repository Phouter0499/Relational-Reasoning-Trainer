import webview
from time import time, sleep
import random

def destroy(window: webview.Window):
    print('Destroying window...')
    window.destroy()
    print('Destroyed!')

def checkAnswer(window: webview.Window, button_pressed: str):
    global ANSWER
    button_text = window.dom.get_element(f'#{button_pressed}').text
    user_answer = True if button_text == "True" else False
    if ANSWER == user_answer:
        window.dom.get_element('#message_p').text = "Correct!"
    else:
        window.dom.get_element('#message_p').text = "Wrong!"

def setupSyllogism(window: webview.Window, syllogism: tuple[str, str, str, bool]):
    p1 = window.dom.get_element('#p1')
    p1.text = syllogism[0]
    p2 = window.dom.get_element('#p2')
    p2.text = syllogism[1]
    c = window.dom.get_element('#c')
    c.text = syllogism[2]
    global ANSWER
    ANSWER = syllogism[-1]

def generateSimpleSyllogism() -> tuple[str, str, str, bool]:
    p1skl = "{} is opposite of {}."
    p2skl = "{} is opposite of {}."
    cskl = "{} is same as {}."
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chosen_ones = random.sample(letters, 3)
    variant = random.randint(0, 1)
    # variant 0 will be the true ones
    if variant == 0:
        return (p1skl.format(chosen_ones[0], chosen_ones[1]), p2skl.format(chosen_ones[1], chosen_ones[2]), cskl.format(chosen_ones[0], chosen_ones[2]), True)
    else:
        return (p1skl.format(chosen_ones[0], chosen_ones[1]), p2skl.format(chosen_ones[0], chosen_ones[2]), cskl.format(chosen_ones[1], chosen_ones[2]), False)

def init(window: webview.Window):
    quit_button = window.dom.get_element('#quitButton')
    quit_button.on('click', lambda x: destroy(window))

    syllogism = generateSimpleSyllogism()
    setupSyllogism(window, syllogism)

    left_button = window.dom.get_element('#left')
    left_button.on('click', lambda x: checkAnswer(window, "left"))

    right_button = window.dom.get_element('#right')
    right_button.on('click', lambda x: checkAnswer(window, "right"))

    regenerate_button = window.dom.get_element('#regenerate')
    regenerate_button.on('click', lambda x: setupSyllogism(window, generateSimpleSyllogism()))

if __name__ in '__main__':
    window = webview.create_window('Relational Reasoning Trainer', url='game_page.html')
    webview.start(func=init, args=window, debug=False)