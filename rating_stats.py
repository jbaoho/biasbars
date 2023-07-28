"""
File: rating_stats.py
----------------------
This file defines a program that allows a user to calculate
baseline summary statistics about a datafile of professor review
data. 
"""

def calculate_rating_stats(filename):
    """
    This function analyzes the professor review data in the given
    file to calculate the percentage of reviews for both men and
    women that fall in the "high rating" bucket, which is a numerical
    rating that is greater than 3.5.

    The resulting information is printed to the console.
    """
    women_high_count = 0
    women_count = 0
    men_high_count = 0
    men_count = 0
    # this function works by keeping track of the total counts for each gender as well as high counts all in separate variables
    with open(filename, 'r') as f:
        next(f)
        for line in f:
            line_parts = line.split(',')
            if line_parts[1] == 'M':
                men_count += 1
                if float(line_parts[0]) > 3.5:
                    men_high_count += 1
            else:
                women_count += 1
                if float(line_parts[0]) > 3.5:
                    women_high_count += 1
        print(f"{round(women_high_count / women_count * 100)}% of reviews for women in the dataset are high.")
        print(f"{round(men_high_count / men_count * 100)}% of reviews for men in the dataset are high.")


def main():
    # Ask the user to input the name of a file
    filename = input("Which data file would you like to load? ")

    # Calculate review distribution statistics by gender for
    # that file. This function should print out the results of
    # the analysis to the console.
    calculate_rating_stats(filename)

if __name__ == '__main__':
    main()