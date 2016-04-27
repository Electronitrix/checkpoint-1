"""Greeter.

Usage:
  greeter.py hello [<name> <last>]
  greeter.py goodbye <name>
  greeter.py (-h | --help)

Options:
  -h --help     Show this screen.

"""
from docopt import docopt


def hello(name,last):
    print('Hello, {0}'.format(name))
    print('last, {0}'.format(last))



def goodbye(name):
    print('Goodbye, {0}'.format(name))

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print arguments

    # if an argument called hello was passed, execute the hello logic.
    if arguments['hello']:
        hello(arguments['<name>'],arguments['<last>'])
    elif arguments['goodbye']:
        goodbye(arguments['<name>']) 