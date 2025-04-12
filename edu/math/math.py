# coding=utf-8
import curses
import random
import time
from sys import exit, stderr, stdout

text = "Hi there"
import numpy as np
from PIL import Image, ImageDraw, ImageFont

myfont = ImageFont.truetype("verdanab.ttf", 12)
size = myfont.getsize(text)
img = Image.new("1",size,"black")
draw = ImageDraw.Draw(img)
draw.text((0, 0), text, "white", font=myfont)
pixels = np.array(img, dtype=np.uint8)
chars = np.array([' ','#'], dtype="U1")[pixels]
strings = chars.view('U' + str(chars.shape[1])).flatten()
print( "\n".join(strings))

counts = 5
delay_time = 2.5
alist = []
sum = 0
for i in range(counts):
    alist.append(random.randint(1, 9))
    print(f"\033[1;31m{alist[i]}\033[0m")
    time.sleep(delay_time)
    sum = sum + int(alist[i])

time.sleep(5)
print(f"{sum=}")

def draw_text(stdscr, text, color=0, fallback=None, title=None, no_figlet_y_offset=-1, end=None):
    """
    Draws text in the given color. Duh.
    """
    if fallback is None:
        fallback = text
    y, x = stdscr.getmaxyx()
    effective_y = (y if no_figlet_y_offset < 0 else 1)
    y_delta = (0 if no_figlet_y_offset < 0 else no_figlet_y_offset)
    if title:
        title = pad_to_size(title, x, 1)
        if "\n" in title.rstrip("\n"):
            # hack to get more spacing between title and body for figlet
            title += "\n" * 5
        text = title + "\n" + pad_to_size(text, x, len(text.split("\n")))
    if end:
        end = pad_to_size(end, x, 1)
        text = pad_to_size(text, x, len(text.split("\n"))) + "\n" + end
    lines = pad_to_size(text, x, effective_y).rstrip("\n").split("\n")

    try:
        for i, line in enumerate(lines):
            stdscr.insstr(i + y_delta, 0, line, curses.color_pair(color))
    except:
        lines = pad_to_size(fallback, x, effective_y).rstrip("\n").split("\n")
        try:
            for i, line in enumerate(lines[:]):
                stdscr.insstr(i + y_delta, 0, line, curses.color_pair(color))
        except:
            pass
    stdscr.refresh()

def pad_to_size(text, x, y):
    """
    Adds whitespace to text to center it within a frame of the given
    dimensions.
    """
    input_lines = text.rstrip().split("\n")
    longest_input_line = max(map(len, input_lines))
    number_of_input_lines = len(input_lines)
    x = max(x, longest_input_line)
    y = max(y, number_of_input_lines)
    output = ""

    padding_top = int((y - number_of_input_lines) / 2)
    padding_bottom = y - number_of_input_lines - padding_top
    padding_left = int((x - longest_input_line) / 2)

    output += padding_top * (" " * x + "\n")
    for line in input_lines:
        output += padding_left * " " + line + " " * (x - padding_left - len(line)) + "\n"
    output += padding_bottom * (" " * x + "\n")

    return output

draw_text(stdscr, "E")
