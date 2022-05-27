import substat
import math

# Constants
MIN = 0
MAX = 1
EPIC = 0
HEROIC = 1
RARE = 2
LVL85 = 0
LVL88 = 1
LVL90 = 2

lvl85_speed_range = ((2,4), (1,4), (1,4)) # epic 5 max but very low chance
lvl85_cdmg_range = ((4,7), (4,7), (4,6))
lvl85_cchance_range = ((3,5), (3,5), (3,5))
lvl85_atkper_range = lvl85_defper_range = lvl85_eff_range = lvl85_effres_range = lvl85_hpper_range = ((4,8),(4,8),(4,7))
lvl85_atkflat_range = ((33,46), (31, 44), (29, 42))
lvl85_defflat_range = ((28,34), (26,33), (25,31)) # epic 35 max but very low chance
lvl85_hpflat_range = ((157, 202), (149,192), (141,182))

lvl88_speed_range = ((3,5), (2,4), (2,4))
lvl88_cdmg_range = ((4,8), (4,8), (4,7))
lvl88_cchance_range = ((3,6), (3,6), (3,5))
lvl88_atkper_range = lvl88_defper_range = lvl88_eff_range = lvl88_effres_range = lvl88_hpper_range = ((5,9),(5,9),(5,8))
lvl88_atkflat_range = ((37,53), (36, 50), (34, 48))
lvl88_defflat_range = ((32,39), (30,37), (28,35)) # epic 40 max but very low chance
lvl88_hpflat_range = ((178, 229), (169,218), (160,206))

range_dict = {"Speed": (lvl85_speed_range, lvl88_speed_range), 
              "Critical Hit Damage": (lvl85_cdmg_range, lvl88_cdmg_range), 
              "Critical Hit Chance": (lvl85_cchance_range, lvl88_cchance_range),
              "Attack Percent": (lvl85_atkper_range, lvl88_atkper_range),
              "Defense Percent": (lvl85_defper_range, lvl88_defper_range),
              "Effectiveness": (lvl85_eff_range, lvl88_eff_range),
              "Effect Resistance": (lvl85_effres_range, lvl88_effres_range),
              "Health Percent": (lvl85_hpper_range, lvl88_hpper_range),
              "Attack Flat": (lvl85_atkflat_range, lvl88_atkflat_range),
              "Defense Flat": (lvl85_defflat_range, lvl88_defflat_range),
              "Health Flat": (lvl85_hpflat_range, lvl88_hpflat_range)}

avg_dict = {"Speed": (3,3.5), 
              "Critical Hit Damage": (5.5,6), 
              "Critical Hit Chance": (4,4.5),
              "Attack Percent": (6,7),
              "Defense Percent": (6,7),
              "Effectiveness": (6,7),
              "Effect Resistance": (6,7),
              "Health Percent": (6,7),
              "Attack Flat": (39,45),
              "Defense Flat": (31,36),
              "Health Flat": (174,203)}



def calc_num_gear_rolls(gear_level, gear_type, enhance_level, substat_list):
    minmax_roll_list = []
    num_rolls_list = []
    avg_rolls_list = []
    for substat in substat_list:
        min_rolls = calc_min_rolls(gear_level, substat, gear_type)
        max_rolls = calc_max_rolls(gear_level, substat, gear_type)
        minmax_roll_list.append((min_rolls,max_rolls))
        num_rolls_list.append(min_rolls)
        avg_rolls_list.append(avg_dict[substat.name][gear_level])

    sum_min_rolls = sum(num_rolls_list)

    num_starting_rolls = 0
    if gear_type == EPIC:
        num_starting_rolls = 4
    elif gear_type == HEROIC:
        num_starting_rolls = 3
    elif gear_type == RARE:
        num_starting_rolls = 2
    else:
        print('Gear type not expected')

    total_rolls = num_starting_rolls + math.floor(enhance_level/3)
    missing_rolls = total_rolls - sum_min_rolls

    scale_diff_list = [None] * len(substat_list)

    for i in range(missing_rolls):
        for j in range(len(substat_list)):
            if num_rolls_list[j] >= minmax_roll_list[j][MAX]:
                scale_diff_list[j] = 0
                continue
            scale_diff_list[j] = calc_scaled_diff(substat_list[j], avg_rolls_list[j], num_rolls_list[j])

        max_scale_diff = max(scale_diff_list)
        max_scale_diff_index = scale_diff_list.index(max_scale_diff)

        num_rolls_list[max_scale_diff_index] += 1

    # for k in range(len(substat_list)):
    #     substat_list[k].num_rolls = num_rolls_list[k]

    return num_rolls_list



def calc_max_rolls(gear_level, substat, gear_type):
    return math.floor(int(substat.value)/int(range_dict[substat.name][gear_level][gear_type][MIN]))
    
def calc_min_rolls(gear_level, substat, gear_type):
    return math.ceil(int(substat.value)/int(range_dict[substat.name][gear_level][gear_type][MAX]))

def calc_scaled_diff(substat, avg_roll, num_rolls):
    return (float(substat.value) - float(avg_roll) * float(num_rolls))/float(avg_roll)


# gear score formula following fribbels
def calc_gear_score(substat_list):  
        total_gear_score = 0
        for stat in substat_list:
            stat_name = stat.name
            stat_value = stat.value
            if substat.is_normal_stat(stat):
                total_gear_score += stat_value
            elif stat_name == 'Speed':
                total_gear_score += stat_value * (8/4)
            elif stat_name == 'Critical Hit Damage':
                total_gear_score += stat_value * (8/7)
            elif stat_name == 'Critical Hit Chance':
                total_gear_score += stat_value * (8/5)
            elif stat_name == 'Attack Flat':
                total_gear_score += stat_value * (3.46/39)
            elif stat_name == 'Defense Flat':
                total_gear_score += stat_value * (4.99/31)
            elif stat_name == 'Health Flat':
                total_gear_score += stat_value * (3.09/174)
        
        return total_gear_score

        
def calc_minmax_gear_score(gear_level, substat_list, gear_type, stat_rolls, minmax):

    total_gear_score = 0
    for i in range(len(substat_list)):
        stat = substat_list[i]
        stat_name = stat.name
        stat_value = stat.value
        curr_roll = stat_rolls[i]
        if substat.is_normal_stat(stat):
            total_gear_score += range_dict[stat_name][gear_level][gear_type][minmax] * curr_roll
        elif stat_name == 'Speed':
            total_gear_score += range_dict[stat_name][gear_level][gear_type][minmax] * (8/4) * curr_roll
        elif stat_name == 'Critical Hit Damage':
            total_gear_score += range_dict[stat_name][gear_level][gear_type][minmax] * (8/7) * curr_roll
        elif stat_name == 'Critical Hit Chance':
            total_gear_score += range_dict[stat_name][gear_level][gear_type][minmax] * (8/5) * curr_roll
        elif stat_name == 'Attack Flat':
            total_gear_score += range_dict[stat_name][gear_level][gear_type][minmax] * (3.46/39) * curr_roll
        elif stat_name == 'Defense Flat':
            total_gear_score += range_dict[stat_name][gear_level][gear_type][minmax] * (4.99/31) * curr_roll
        elif stat_name == 'Health Flat':
            total_gear_score += range_dict[stat_name][gear_level][gear_type][minmax] * (3.09/174) * curr_roll
    
    return total_gear_score

def calc_gear_score_potential(gear_level, substat_list, gear_type, stat_rolls):
    min_gear_score = calc_minmax_gear_score(gear_level, substat_list, gear_type, stat_rolls, MIN)
    max_gear_score = calc_minmax_gear_score(gear_level, substat_list, gear_type, stat_rolls, MAX)
    curr_gear_score = calc_gear_score(substat_list)
    return ((curr_gear_score - min_gear_score)/(max_gear_score - min_gear_score)) * 100


def get_gear_type(gear_type):
    if gear_type == 'Rare':
        return RARE
    elif gear_type == 'Heroic':
        return HEROIC
    else:
        return EPIC

def get_gear_level(gear_level):
    if gear_level == '85':
        return LVL85
    elif gear_level == '88':
        return LVL88
    elif gear_level == '90':
        return LVL90
    else:
        print('Error gear level not supported')