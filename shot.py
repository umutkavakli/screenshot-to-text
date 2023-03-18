import argparse
from converter import Converter
from pynput import keyboard

parser = argparse.ArgumentParser()

parser.add_argument('-l', '--lang', nargs='+', default=['en'])
parser.add_argument('-o', '--output-type', default='print', choices=['print', 'file'])
parser.add_argument('-p', '--path', default='./text')

args = parser.parse_args()
converter = Converter(
    args.lang,
    args.output_type,
    args.path
)

listener = keyboard.Listener(on_press=converter.on_press)
listener.start()
listener.join()

