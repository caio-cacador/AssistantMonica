from constants import WHAT_IS_INTERPRETER, WHO_IS_INTERPRETER, CONVERSATION_INTERPRETER, COMPLIMENT


def what_is_interpreter(phrase):
    for item in WHAT_IS_INTERPRETER:
        if item in phrase:
            theme = phrase.replace(item, '')
            return theme.strip()


def who_is_interpreter(phrase):
    for item in WHO_IS_INTERPRETER:
        if item in phrase:
            theme = phrase.replace(item, '')
            return theme.strip()


def is_what_is_question(msg: str):
    for item in WHAT_IS_INTERPRETER:
        if item in msg:
            return True
    return False


def is_who_is_question(msg: str):
    for item in WHO_IS_INTERPRETER:
        if item in msg:
            return True
    return False


def is_it_a_conversation(msg: str):
    msg = msg.replace('voce', 'vc')
    for item in CONVERSATION_INTERPRETER:
        if item in msg:
            return True
    return False


def is_it_a_compliment(msg: str):
    for item in COMPLIMENT:
        if item in msg:
            return True
    return False