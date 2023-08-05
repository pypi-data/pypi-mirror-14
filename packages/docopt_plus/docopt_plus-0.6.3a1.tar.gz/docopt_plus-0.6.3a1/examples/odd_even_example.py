"""Usage: odd_even_example.py [-h | --help] (ODD EVEN)...

Example, try:
  odd_even_example.py 1 2 3 4

Options:
  -h, --help

"""
from docopt_plus import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
