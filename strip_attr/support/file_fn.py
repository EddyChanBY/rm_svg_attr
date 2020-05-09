#!/usr/bin/env python

import sys, getopt


def generate_sequential_file(file_name):
    current_squence = 0
    new_sub_str = ""
    new_file_name = ""
    ext_pos = 0
    net_file_str = ""
    ext_str = ""

    # generate a sequential file name
    ext_pos = file_name.find(".")
    net_file_str = file_name[0:ext_pos]
    ext_str = file_name[ext_pos : len(file_name)]
    if (
        net_file_str[len(net_file_str) - 2 :].isnumeric()
        and net_file_str[len(net_file_str) - 3] == "-"
    ):
        # net_file_str is in sequencal number, increment by 1
        current_squence = int(net_file_str[len(net_file_str) - 2 :])
        if current_squence < 9:
            new_sub_str = "-0" + str(current_squence + 1)
        else:
            new_sub_str = "-" + str(current_squence + 1)
        new_file_name = net_file_str[0 : len(net_file_str) - 3] + new_sub_str + ext_str
    else:
        new_file_name = net_file_str[0 : len(net_file_str)] + "-01" + ext_str
    return new_file_name


def open_text_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as filein:
            content = filein.read()
            filein.close()
    except Exception as err_open:
        sys.exit(err_open.args[1])
    return content


def write_text_file(filename, content_str):
    # Write to the output file
    try:
        with open(filename, "w", encoding="utf-8") as fileout:
            fileout.write(content_str)
            fileout.close()
    except Exception as err_newfile:
        sys.exit(err_newfile.args[1])
