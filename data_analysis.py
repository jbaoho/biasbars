"""
File: data_analysis.py
----------------------
This program read in data on cumulative infections of a disease
in different locations, and computes the number of infections
per day at each location.
"""


def load_data(filename):
    """
    The function takes in the name of a datafile (string), which
    contains data on locations and their seven day cumulative number
    of infections.  The function returns a dictionary in which the
    keys are the locations in the data file, and the value associated
    with each key is a list of the (integer) values presenting the
    cumulative number of infections at that location.
    >>> load_data('data/disease1.txt')
    {'Evermore': [1, 1, 1, 1, 1, 1, 1], 'Vanguard City': [1, 2, 3, 4, 5, 6, 7], 'Excelsior': [1, 1, 2, 3, 5, 8, 13]}
    >>> load_data('data/disease2.txt')
    {'Hogwarts': [5, 12, 18, 29, 33, 34, 34], 'Alderaan': [100, 200, 300, 400, 500, 600, 700], "Helm's Deep": [2, 3, 3, 5, 7, 7, 8], 'Mordor': [247, 448, 937, 1370, 2109, 3720, 5268], 'Shire': [1, 1, 1, 1, 1, 1, 1], 'Diagon Alley': [14, 28, 47, 72, 89, 97, 102]}
    """
    dict = {}
    with open(filename, 'r') as f:
        for line in f:
            line_parts = line.split(',')
            for i in range(len(line_parts)):
                if i != 0:
                    line_parts[i] = int(line_parts[i].strip())
            dict[line_parts[0].strip()] = line_parts[1:]
    return dict



def daily_cases(cumulative):
    """
    The function takes in a dictionary of the type produced by the load_data
    function (i.e., keys are locations and values are lists of seven values
    representing cumulative infection numbers).  The function returns a
    dictionary in which the keys are the same locations in the dictionary
    passed in, but the value associated with each key is a list of the
    seven values (integers) presenting the number of new infections each
    day at that location.
    >>> daily_cases({'Test': [1, 2, 3, 4, 4, 4, 4]})
    {'Test': [1, 1, 1, 1, 0, 0, 0]}
    >>> daily_cases({'Evermore': [1, 1, 1, 1, 1, 1, 1], 'Vanguard City': [1, 2, 3, 4, 5, 6, 7], 'Excelsior': [1, 1, 2, 3, 5, 8, 13]})
    {'Evermore': [1, 0, 0, 0, 0, 0, 0], 'Vanguard City': [1, 1, 1, 1, 1, 1, 1], 'Excelsior': [1, 0, 1, 1, 2, 3, 5]}
    """
    daily = {}
    for case in cumulative:
        if case not in daily:
            daily[case] = []
        for i in range(len(cumulative[case])):
            # The first conditional of the if statement if for the first case because their is no previous day
            if i == 0:
                daily[case].append(cumulative[case][0])
            else:
                daily[case].append(cumulative[case][i] - cumulative[case][i - 1])
    return daily


def main():
    filename = 'data/disease1.txt'

    data = load_data(filename)
    print(f"Loaded datafile {filename}:")
    print(data)

    print("Daily infections: ")
    print(daily_cases(data))


if __name__ == '__main__':
    main()
