# coding=utf-8

import json

from elements.handlers import CustomHandler

if __name__ == '__main__':
    data = CustomHandler().start()

    with open('output.json', 'w') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
