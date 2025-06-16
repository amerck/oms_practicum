import json
import argparse
from itso_ai.parsers import metadata, teams


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in-file', required=True,
                        help='JSON file of Microsoft Teams messages from ms_crawler.py')
    parser.add_argument('-o', '--out-file', required=True,
                        help='JSON file of Microsoft Teams messages flattened')
    args = parser.parse_args()

    fin = open(args.in_file, 'r')
    fout = open(args.out_file, 'w')
    lines = fin.readlines()

    metadata_finder = metadata.MetadataParser()

    for line in lines:
        parser = teams.TeamsParser(line, metadata_finder)
        summary = parser.get_summary()
        body = parser.get_body()
        replies = parser.get_replies()

        fout.write('%s\n' % json.dumps(summary))
        fout.write('%s\n' % json.dumps(body))
        for reply in replies:
            fout.write('%s\n' % json.dumps(reply))

    fin.close()
    fout.close()


if __name__ == '__main__':
    main()
