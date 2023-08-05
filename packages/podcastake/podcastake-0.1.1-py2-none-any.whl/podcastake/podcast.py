import argparse
import sys

BANNDER="""
my awsome project v1.0
"""

def main():
    if len(sys.argv) == 1:
        print(BANNDER)
        sys.argv.append('--help')
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quality', type=int, default=0, help="download video quality : 1 for the standard-definition; 3 for the super-definition")
    parser.add_argument('-v', '--verbose', default=0, help="print more debuging information")
    parser.add_argument('-s', '--store', help="where to save the downloaded podcasts")
    parser.add_argument('-c', '--config', default=0, help="read config from ~/.{project_name} or your specified file")
    parser.add_argument('urls', metavar='URL', nargs='+', help="album url")
    parser.add_argument('-b', '--banner', type=bool, default=True, help="show banner?")

    args = parser.parse_args()
    for url in args.urls:
        print u'downloading from {}'.format(url)

if __name__ == '__main__':
    main()