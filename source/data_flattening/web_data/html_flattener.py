import glob
import argparse
import markdownify


def get_filenames(directory):
    """
    Get list of HTML filenames recursively from directory
    :param directory: directory to search for HTML files
    :return: list of filenames
    """
    files = glob.glob(directory + "/**/*.html", recursive=True)
    return files


def flatten_file(filename):
    """
    Flatten HTML file into Markdown

    :param filename: Filename of HTML file to flatten
    :return: Markdown string
    """
    fin = open(filename, 'r')
    html = fin.read()
    md = markdownify.markdownify(html)
    fin.close()
    return md


def main():
    parser = argparse.ArgumentParser(description="HTML Archive Flattener")
    parser.add_argument('-d', '--in-directory', required=True,
                        help='Directory of HTML files to flatten')
    parser.add_argument('-o', '--output', required=True,
                        help='Output filename')
    args = parser.parse_args()

    fout = open(args.output, 'w')
    filenames = get_filenames(args.in_directory)
    for filename in filenames:
        print(filename)
        md = flatten_file(filename)
        fout.write(md + "\n\n")
    fout.close()

if __name__ == '__main__':
    main()
