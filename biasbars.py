"""
File: biasbars.py
---------------------
Add your comments here
"""

import tkinter
import biasbarsdata
import biasbarsgui as gui


# Provided constants to load and plot the word frequency data
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

FILENAME = "data/full-data.txt"

VERTICAL_MARGIN = 30
LEFT_MARGIN = 60
RIGHT_MARGIN = 30
LABELS = ["Low Reviews", "Medium Reviews", "High Reviews"]
LABEL_OFFSET = 10
BAR_WIDTH = 75
LINE_WIDTH = 2
TEXT_DX = 2
NUM_VERTICAL_DIVISIONS = 7
TICK_WIDTH = 15

def get_centered_x_coordinate(width, idx):
    """
    Given the width of the canvas and the index of the current review
    quality bucket to plot, returns the x coordinate of the centered
    location for the bars and label to be plotted relative to.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current label in the LABELS list
    Returns:
        x_coordinate (float): The centered x coordinate of the horizontal line 
                              associated with the specified label.
    >>> round(get_centered_x_coordinate(1000, 0), 1)
    211.7
    >>> round(get_centered_x_coordinate(1000, 1), 1)
    515.0
    >>> round(get_centered_x_coordinate(1000, 2), 1)
    818.3
    """
    plot_width = width - LEFT_MARGIN - RIGHT_MARGIN
    return LEFT_MARGIN + plot_width * (1 + idx * 2) / 6





def draw_fixed_content(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background border and x-axis labels on it.

    Input:
        canvas (tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing content from the canvas
    width = canvas.winfo_width()    # get the width of the canvas
    height = canvas.winfo_height()  # get the height of the canvas
    # this draws the plotting region based on the margin values
    canvas.create_rectangle(LEFT_MARGIN, VERTICAL_MARGIN, width - 1 - RIGHT_MARGIN, height - 1 - VERTICAL_MARGIN, width=LINE_WIDTH)
    # this creates the text labels for the bins based on the get_centered helper function
    for i in range(3):
        canvas.create_text(get_centered_x_coordinate(width, i), height - 1 - VERTICAL_MARGIN  + LABEL_OFFSET, text=LABELS[i], anchor=tkinter.N)


def plot_word(canvas, word_data, word):
    """
    Given a dictionary of word frequency data and a single word, plots
    the distribution of the frequency of this word across gender and 
    rating category.

    Input:
        canvas (tkinter Canvas): The canvas on which we are drawing.
        word_data (dictionary): Dictionary holding word frequency data
        word (str): The word whose frequency distribution you want to plot
    """

    draw_fixed_content(canvas)
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    plot_height = height - VERTICAL_MARGIN - 1

        # We have provided code to calculate the maximum frequency for the specified
    # word from the provided dict 
    gender_data = word_data[word]
    max_frequency = max(max(gender_data[biasbarsdata.KEY_WOMEN]), max(gender_data[biasbarsdata.KEY_MEN]))

    # Note: You find it helpful to use the KEY_WOMEN and KEY_MEN constants
    # defined in the biasbarsdata file. To see how to use these constants, 
    # reference the example above.

    # this first for loop will loop through the number of tick marks and draw the tick mark and its corresponding value
    # at the appropriate spot
    for i in range(NUM_VERTICAL_DIVISIONS):
        x_value = LEFT_MARGIN - TICK_WIDTH // 2
        y_value = round(plot_height - ((i / (NUM_VERTICAL_DIVISIONS - 1)) * (plot_height - VERTICAL_MARGIN)))
        canvas.create_line(x_value, y_value, x_value + TICK_WIDTH, y_value, width=LINE_WIDTH)
        label = round(max_frequency * (i / NUM_VERTICAL_DIVISIONS))
        canvas.create_text(LEFT_MARGIN - LABEL_OFFSET, y_value, text=label, anchor=tkinter.E)

    # this nested for loop is used to draw the two boxes three times by assigning variables that are specific for men's
    # and women's boxes as well as defining a variable for the separate heights
    # by doing it this way the mod function allows for the create_rectangle function to take in different parameters 
    for j in range(3):
        for k in range(2):
            if k % 2 == 0:
                left = get_centered_x_coordinate(width, j) - BAR_WIDTH
                gender_key = biasbarsdata.KEY_WOMEN
                color = 'cyan'
                gender_label = 'W'
            else:
                left = get_centered_x_coordinate(width, j)
                gender_key = biasbarsdata.KEY_MEN
                color = 'magenta'
                gender_label = 'M'
            bar_height = round((plot_height - VERTICAL_MARGIN) / max_frequency * word_data[word][gender_key][j])
            canvas.create_rectangle(left, plot_height - bar_height, left + BAR_WIDTH, plot_height, fill=color)
            canvas.create_text(left + TEXT_DX, plot_height - bar_height, text=gender_label, anchor=tkinter.NW)


def convert_counts_to_frequencies(word_data):
    """
    This code is provided to you! 

    It converts a dictionary 
    of word counts into a dictionary of word frequencies by 
    dividing each count for a given gender by the total number 
    of words found in reviews about professors of that gender.
    """ 
    K = 1000000
    total_words_men = sum([sum(counts[biasbarsdata.KEY_MEN]) for word, counts in word_data.items()])
    total_words_women = sum([sum(counts[biasbarsdata.KEY_WOMEN]) for word, counts in word_data.items()])
    for word in word_data:
        gender_data = word_data[word]
        for i in range(3):
            gender_data[biasbarsdata.KEY_MEN][i] *= K / total_words_men
            gender_data[biasbarsdata.KEY_WOMEN][i] *= K / total_words_women


# main() code is provided for you
def main():
    import sys
    args = sys.argv[1:]
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    if len(args) == 2:
        WINDOW_WIDTH = int(args[0])
        WINDOW_HEIGHT = int(args[1])

    # Load data
    word_data = biasbarsdata.read_file(FILENAME)
    convert_counts_to_frequencies(word_data)

    # Make window
    top = tkinter.Tk()
    top.wm_title('Bias Bars')
    canvas = gui.make_gui(top, WINDOW_WIDTH, WINDOW_HEIGHT, word_data, plot_word, biasbarsdata.search_words)

    # draw_fixed once at startup so we have the borders and labels
    # even before the user types anything.
    draw_fixed_content(canvas)

    # This needs to be called just once
    top.mainloop()


if __name__ == '__main__':
    main()