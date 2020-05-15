#!/usr/bin/env python

import sys, getopt


def parse_user_input(argv):
    number_of_input = 2
    usage_string = "Usage: strip_attr.py -a <attr_to_strip> -i <inputfile>"
    inputfile = ""
    attr_to_strip = ""
    errorwarning = ""
    try:
        opts, args = getopt.getopt(argv, "ha:i:", ["attr=", "ifile="])
        # error handlling:
        # 1. standard errors, this handle when user input has -x syntax but not one of -h, -i and -o.
        #     Or with -i and -o with no argument.
        #  ***The except: block must follow the try: block imediately***
    except getopt.GetoptError as err:
        # sys.exit onlt take one argument and err here cannot cat to another string.
        print(err, "\n", usage_string)
        sys.exit(2)
        # capture if user put in file names with space
    if len(argv) >= number_of_input * 2 + 1:
        errorwarning = (
            "It seems that you are using multi words file names."
            + "\ntry using underscore to make the file name as a single word."
            + "\n"
            + usage_string
        )
        sys.exit(errorwarning)
    # 2. no valid file entry, the getopt would just get a null list, that will not be catched by 1 above
    if len(opts) == 0:
        errorwarning = "Error: no valid input." + "\n" + usage_string
        sys.exit(errorwarning)
    # 3. only one name is captured.
    elif len(opts) == 1:
        if opts[0][0] == "-i":
            usage_string = (
                "Error: attribute to strip not specified." + "\n" + usage_string
            )
            sys.exit(usage_string)
        elif opts[0][0] == "-a":
            usage_string = "Error: input file not specified." + "\n" + usage_string
            sys.exit(usage_string)
    # valid entries, record in variables
    for opt, arg in opts:
        if opt == "-h":
            print(usage_string)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-a", "--attr"):
            attr_to_strip = arg
    return [attr_to_strip, inputfile]
