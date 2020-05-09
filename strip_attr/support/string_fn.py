#!/usr/bin/env python


def ensure_UTF8(value):
    try:
        return str(value, errors="ignore", encoding="utf-8")
    except TypeError:  # Wasn't a bytes object, no need to decode
        return str(value)


def insert_xml_tag(input_str):
    # Force utf-8 encoded
    input_content = ensure_UTF8(input_str)

    if input_content.find("<?xml") == -1:
        # no xml at all, add UFT-8 tag
        input_content = '<?xml version="1.0" encoding="UTF-8"?>' + input_content
        xml_status = "added"
    elif input_content.find('encoding="UTF-8"') != -1:
        xml_status = "is there already"
    else:
        # xml tag found but no UTF-8 attribute, add it back
        mark_pos = input_content.find("?>")
        input_content = (
            input_content[:mark_pos] + ' encoding="UTF-8"' + input_content[mark_pos:]
        )
        xml_status = "is inserted into existing xml tag"

    return input_content, xml_status


def strip_attr(attr_to_strip, input_content):
    # Strip the extra attribute
    from_pos = 0
    to_pos = 0
    new_str = ""
    strip_counter = 0
    xml_status = ""
    quotation_mark = ""
    illegit_count = 0

    while True:
        # establish exit condition when the substr cannot be found.
        if input_content.find(attr_to_strip, from_pos) == -1:
            # check before adding the xml tag before writing to file
            xml_done = insert_xml_tag(input_content)
            input_content = xml_done[0]
            xml_status = xml_done[1]
            break
        from_pos = input_content.find(attr_to_strip, from_pos)
        # check if the character infront of from_pos is a space
        if input_content[from_pos - 1] == " ":
            # from_pos - 1 to capture the space character infront.
            from_pos = from_pos - 1
        # check single or double quotation marks are used
        if (
            input_content.find('"', from_pos + 1, from_pos + len(attr_to_strip) + 6)
            != -1
        ):
            # it is double quotation mark
            quotation_mark = '"'
        elif (
            input_content.find("'", from_pos + 1, from_pos + len(attr_to_strip) + 6)
            != -1
        ):
            quotation_mark = "'"
        else:
            illegit_count = illegit_count + 1
            from_pos = from_pos + len(attr_to_strip) + 1
            quotation_mark = ""
        # do the stripping only when legit
        if quotation_mark != "":
            to_pos = input_content.find(quotation_mark, from_pos + 1)
            # to_pos + 1 to include the last character.
            to_pos = input_content.find(quotation_mark, to_pos + 1)
            # in python 3, replace alway give a new copy of the str.
            # # need a new str to capture the replaced str.
            new_str = input_content.replace(input_content[from_pos : to_pos + 1], "")
            strip_counter = strip_counter + 1
            input_content = new_str
    return strip_counter, input_content, xml_status, illegit_count
