#!/usr/bin/python3

# Get file names input
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
        if current_squence >= 9:
            new_sub_str = "-0" + str(current_squence + 1)
        else:
            new_sub_str = "-" + str(current_squence + 1)
            new_file_name = (
                net_file_str[0 : len(net_file_str) - 3] + new_sub_str + ext_str
            )
    else:
        new_file_name = net_file_str[0 : len(net_file_str)] + "-01" + ext_str
    return new_file_name


def strip_attr(attr_to_strip, input_content):
    # Strip the extra attribute
    from_pos = 0
    to_pos = 0
    new_str = ""
    strip_counter = 0

    while True:
        # establish exit condition when the substr cannot be found.
        if input_content.find(attr_to_strip) == -1:
            # add the xml tag before writing to file
            input_content = '<?xml version="1.0" encoding="UTF-8"?>' + input_content
            break
        from_pos = input_content.find(attr_to_strip, from_pos)
        # from_pos + 1 to capture the space character infront.
        to_pos = input_content.find('"', from_pos + 1)
        # to_pos + 1 to include the last character.
        to_pos = input_content.find('"', to_pos + 1)
        # in python 3, replace alway give a new copy of the str.
        # # need a new str to capture the replaced str.
        new_str = input_content.replace(input_content[from_pos - 1 : to_pos + 1], "")
        strip_counter = strip_counter + 1
        input_content = new_str
    return strip_counter, input_content


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


def parse_user_input(argv):
    number_of_input = 2
    usage_string = "Usage: conv.py -a <attr_to_strip> -i <inputfile>"
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
    print("and one xml utf-8 tag added.")
    print("Results outputed to file ", outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
