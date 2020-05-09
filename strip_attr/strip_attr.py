#!/usr/bin/env python

import sys, getopt
from support.user_input import parse_user_input
from support.string_fn import ensure_UTF8, insert_xml_tag, strip_attr
from support.file_fn import generate_sequential_file, open_text_file, write_text_file


def main(argv):
    user_input = []
    strip_str = ""
    inputfile = ""
    outputfile = ""
    svg_content = ""

    # parse user input
    user_input = parse_user_input(argv)
    strip_str = user_input[0]
    inputfile = user_input[1]
    # open and read file
    svg_content = open_text_file(inputfile)
    # stripping attribute
    final_content = strip_attr(strip_str, svg_content)
    svg_content = final_content[1]
    # generate squencial file name
    outputfile = generate_sequential_file(inputfile)
    # write file
    write_text_file(outputfile, svg_content)
    print(final_content[0], " instances of <", strip_str, "> stripped.")
    if final_content[3] != 0:
        print(
            final_content[3],
            " instances of <",
            strip_str,
            "> NOT stripped because they don't have legit delimiters.",
        )
    print("xml utf-8 tag", final_content[2])
    print("Results outputed to file", outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
