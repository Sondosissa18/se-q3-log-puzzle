#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
__author__ = "sondos got help from gabby, Jt and joseph"

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    puzzleURLs = []
    with open(filename) as f:
        s = filename.find('_')
        url = filename[s + 1::]
        for lines in f:
            urls_search = re.search(r"GET\s(\S*)", lines)
            # if urls_search:
            #     print(urls_search.group(1))
            if '/puzzle' in urls_search.group(1):
                url_ = f'http://{url}{urls_search.group(1)}'
                if url_ not in puzzleURLs:
                    puzzleURLs.append(f'{url_}')
    return sorted(puzzleURLs, key=lambda u: u[-8:-4])


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # img_urls = []
    with open("index.html", "w") as f:
        f.write('<html><body>')
        for i, url in enumerate(img_urls):
            urllib.request.urlretrieve(
                url, os.path.join(dest_dir, "img" + str(i) + ".jpg"))
            # f.write(f'<img src="{url}">')
            f.write(f'<img src="./{dest_dir}/img{str(i)}.jpg">')
        f.write('</body></html>')
        # f.write("<html><body>{0}</body></html>".format(''.join(img_)))


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument(
        'logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])


# Demo Notes:
# TODO: PART A: to trun the log files into url's.
# we "read through the log file", we "found the pieace of information that points to the image slice"
# and then we need to build a URL out of it.
# Todo: Part B: Download those images from the internet
# we need to check README file, to check the tips of how we should name them.
# Ultimate Goal is to end up with index.html file ,that we create with the code.
# that populates " your code" with a punch of <img> tags.
# <html>
# <body>
# <img src="/edu/python/exercises/img0"><img src="/edu/python/exercises/img1"><img src="/edu/python/exercises/img2">...
# </body>
# </html>
# ....so go to the logfile find the information that going to get to the image slice locations ,
# .. then build urls out of them so u can download them and piece them back together, in an index.html file.
# Todo:Part C - Image Slice Descrambling:
# we need to sort them since everything is scrambling:
# then we should to decode the second puzzle which shows the famous place.
#

# https://www.programcreek.com/python/?CodeExample=read%20urls
