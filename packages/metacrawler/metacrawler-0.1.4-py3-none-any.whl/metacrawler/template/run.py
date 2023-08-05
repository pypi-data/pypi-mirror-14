# coding=utf-8

from elements.handlers import CustomHandler

if __name__ == '__main__':
    handler = CustomHandler()
    handler.start()
    handler.output(compact=False)
