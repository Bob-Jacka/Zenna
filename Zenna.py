from flask import Flask

from Wrappers import log

# Global entities:
flask_interface: Flask


@log
def main_cycle():
    global flask_interface
    flask_interface = Flask()


@log
def add_dependencies():
    pass


@log
def update_dependencies():
    pass


if __name__ == '__main__':
    print('Utility started working, v1.0.0')
    main_cycle()
    print('Utility finished working')
