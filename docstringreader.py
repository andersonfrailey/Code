# Reads a python file and writes all of the doc strings into a text file
import argparse


def build_string(file_used, line):
    """
    Write the function contents
    """
    four = '    '
    s = line.strip() + '\n'
    quotes = 0
    line = file_used.readline()
    split_line = line.split()
    if split_line != []:
        if split_line[0] != '"""':
            quotes = 2
        else:
            s += four + line.strip() + '\n'
            quotes += 1
    while quotes < 2:
        line = file_used.readline()
        split_line = line.split()
        s += four + line.strip() + '\n'
        if split_line != []:
            if split_line[0] == '"""':
                quotes += 1
    s += '\n\n'
    return s


def check_line(line):
    """
    Determine if a line is the start of a function
    """
    try:
        if line[0] == 'def':
            return True
        else:
            return False
    except IndexError:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='path to file you want read')
    parser.add_argument('-o', '--output', help='prefered output file name')
    args = parser.parse_args()
    if args.file is None:
        msg = 'You must specify a file path'
        raise ValueError(msg)
    if args.output is None:
        msg = 'You must name the output file'
        raise ValueError(msg)
    file_path = args.file
    # Read specified file
    code = open(file_path, 'r')
    end_of_file = False
    final_string = ''  # Empty string to hold the total string
    blank_count = 0  # Counts number of consecutive blank lines
    while not end_of_file:
        line = code.readline()
        split_line = line.split()
        if check_line(split_line):
            final_string += build_string(code, line)
            blank_count = 0
        if split_line == []:
            blank_count += 1
            if blank_count == 1000:
                end_of_file = True
    code.close()
    final_file = open(args.output, 'w+')
    final_file.write(final_string)
    final_file.close()


if __name__ == '__main__':
    main()
