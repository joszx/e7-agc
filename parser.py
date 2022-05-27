
def str_to_list(string):
    return list(filter(bool, [str.strip() for str in string.splitlines()]))



string = "Health\nAttack\n\nSpeed\nEffectiveness\n"

