import gear.substat as substat
from myexception import GearParseException, MyException

# trim front and back spaces, removes empty strings, parses to list format
def str_to_list(string):
    return list(filter(bool, [str.strip() for str in string.splitlines()]))

# modifies given list to remove substat modification from substat names
# TODO: apply different roll calculation to modified substats
def remove_substat_modification(substat_name_list):
    for i in range(len(substat_name_list)):
        substat_name = substat_name_list[i]
        if not all(chr.isalpha() or chr.isspace() for chr in substat_name):
            substat_name_list[i] = substat_name_list[i].rsplit(' ',1)[0]
            if not substat_name_list[i].isalpha():
                print('Error with substat modification')
            else:
                substat_name_list[i] = substat_name

def parse_substats(substat_name_list, substat_value_list):
    remove_substat_modification(substat_name_list)

    if len(substat_name_list) != len(substat_value_list):
        raise GearParseException("number of substat names =/= number of substat values")

    for i in range(len(substat_name_list)):
        curr_substat_name = substat_name_list[i]
        curr_substat_value = substat_value_list[i]
        if '%' in curr_substat_value and curr_substat_name in substat.FLAT_PERCENT_STATS:
            substat_value_list[i] = remove_character(curr_substat_value, '%')
            substat_name_list[i] = curr_substat_name + ' Percent'
        elif curr_substat_name in substat.FLAT_PERCENT_STATS:
            substat_name_list[i] = curr_substat_name + ' Flat'
        else:
            substat_value_list[i] = remove_character(curr_substat_value, '%')
    return (substat_name_list, substat_value_list)

def remove_character(string, char):
    return string.replace(char, "")

# also removes leading/trailing spaces
def remove_newline(string):
    return string.strip()

def remove_plussign(string):
    return string.replace('+', '')

def parse_gear_type(gear_type):
    return gear_type.split()[0]

def parse_gear_enhance_level(gear_enhance_level):
    if gear_enhance_level.isnumeric():
        gear_enhance_level = int(gear_enhance_level)
        if gear_enhance_level in range(1,16):
            return gear_enhance_level
        else:
            return 0
    elif gear_enhance_level == "":
        return 0
    else:
        print("Error in parse gear enhance level")


# string = "Health\nAttack\n\nSpeed &\nEffectiveness\n"

# string_list = str_to_list(string) 

# remove_substat_modification(string_list)

# print(string_list)