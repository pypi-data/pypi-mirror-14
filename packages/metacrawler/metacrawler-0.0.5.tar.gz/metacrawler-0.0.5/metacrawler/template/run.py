# coding=utf-8

import json

from elements.handlers import YourHandler

if __name__ == '__main__':
    YourHandler.settings.load_from_file('settings.config')
    data = YourHandler().start()

    with open('output.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
