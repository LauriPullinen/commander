def parse(string):
    parts = string.split(' ')
    type, *payload = parts
    return { 'type': validate_type(type), 'payload': payload }

def validate_type(type):
    if type in ['list', 'join', 'create', 'quit']:
        return type
    elif type == 'l':
        return 'list'
    elif type == 'j':
        return 'join'
    elif type == 'c':
        return 'create'
    elif type == 'q':
        return 'quit'
    else:
        return None

def is_valid(command):
    return 'type' in command and command['type'] != None
