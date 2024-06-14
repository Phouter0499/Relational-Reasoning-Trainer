import webview
from time import time, sleep
import random
import generation_helper as syg
import threading
import os
import json

def destroy(window: webview.Window):
    print('Destroying window...')
    window.destroy()
    print('Destroyed!')

def reset_score(window: webview.Window):
    element = window.dom.get_element('#score')
    element.text = '0/0'
    element = window.dom.get_element('#percentage')
    element.text = '0%'

def check(direction, window: webview.Window):
    global ANSWER, ARGUMENT
    if not ANSWER:
        return
    button = window.dom.get_element(f'#{direction}')
    user_answer = button.text
    score_element = window.dom.get_element('#score')
    ncorrect, ntotal = (int(x) for x in score_element.text.split('/'))
    if ANSWER == user_answer:
        ncorrect += 1
    ntotal += 1
    score_element.text = f'{ncorrect}/{ntotal}'
    percentage_element = window.dom.get_element('#percentage')
    percentage_element.text = f'{ncorrect/ntotal*100:.2f}%'
    # save argument, correct answer, and user answer to json list file called 'history.json'
    with open('history.json', 'r') as f:
        history = json.load(f)
    history.append({
        'argument': ARGUMENT,
        'correct_answer': ANSWER == user_answer,
        'user_answer': user_answer
    })
    with open('history.json', 'w') as f:
        json.dump(history, f, indent=4)
    ANSWER = None     
    regenerate(window)   

def regenerate(window: webview.Window):
    # Reset argument_container
    argument_container = window.dom.get_element('#argument_container')
    argument_container.empty()
    # Reset message_p
    element = window.dom.get_element('#message_p')
    element.text = ''
    # Get level desired
    level = window.dom.get_element('#DSlevel').value
    # Get options selected
    global OPTIONS
    selected_options = [option for option in OPTIONS if OPTIONS[option]]
    # Choose and execute
    chosen_option = random.choice(selected_options) if selected_options else None
    if chosen_option == 'DS' and level and level.isdigit():
        global NAMES
        argument, answer = syg.generateOppositeSameQuestions(int(level), NAMES)
        setup_question(argument, answer, window)
    else:
        element = window.dom.get_element('#message_p')
        element.text = 'Please select at least one option, level, and then select regenerate. There\\\'s also a history.json file that you can view.'
        global ANSWER
        ANSWER = None

def setup_question(argument, answer, window: webview.Window):
    argument_container = window.dom.get_element('#argument_container')
    for proposition in argument:
        argument_container.append(html = f'<p>{proposition}</p>')
    global ANSWER
    ANSWER = answer
    global ARGUMENT
    ARGUMENT = argument

def init(window: webview.Window):
    if not os.path.exists('history.json'):
        with open('history.json', 'w') as f:
            json.dump([], f)

    global OPTIONS
    OPTIONS = {
        'DS': False
    }
    global NAMES
    NAMES = syg.get_four_letter_names()
    global ANSWER
    ANSWER = None

    left_button = window.dom.get_element('#left')
    left_button.on('click', lambda x: check('left', window))
    right_button = window.dom.get_element('#right')
    right_button.on('click', lambda x: check('right', window))
    checkbox = window.dom.get_element('#include_different_same')
    checkbox.on('change', lambda x: exec('OPTIONS["DS"] = not OPTIONS["DS"]'))
    quit_button = window.dom.get_element('#quit_button')
    quit_button.on('click', lambda x: destroy(window))
    regenerate_button = window.dom.get_element('#regenerate')
    regenerate_button.on('click', lambda x: regenerate(window))
    reset_score_button = window.dom.get_element('#reset_button')
    reset_score_button.on('click', lambda x: reset_score(window))

    regenerate(window)

if __name__ in '__main__':
    window = webview.create_window('Relational Reasoning Trainer', url='game_page.html')
    webview.start(func=init, args=window, debug=False)