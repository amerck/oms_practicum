import re
import argparse


REGEX = '(TASK|INC|RITM)\d{6,}'


def main():
    parser = argparse.ArgumentParser(description='Find ServiceNow ticket numbers in text file.')
    parser.add_argument('-i', '--input', required=True,
                        help='Text file to search for ServiceNow ticket numbers')
    parser.add_argument('-o', '--output', required=True,
                        help='Output file to write the found ticket numbers')
    args = parser.parse_args()

    fin = open(args.input, 'r')
    fout = open(args.output, 'w')

    for line in fin:
        m = re.search(REGEX, line)
        if m:
            fout.write('%s\n' % m.group(0))
    fin.close()
    fout.close()
    return


if __name__ == '__main__':
    main()
