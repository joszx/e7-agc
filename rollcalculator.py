
import math

speed_range = (2,4) # 5 max but very low chance
cdmg_range = (3,7)
cchance_range = (3,5)
atkper_range = defper_range = eff_range = effres_range = hpper_range = (4,8)
atkflat_range = (33,46)
defflat_range = (28,34) # 35 max but very low chance
hpflat_range = (157, 202)

MIN = 0
MAX = 1

range_dict = {"Speed": speed_range, 
              "Critical Hit Damage": cdmg_range, 
              "Critical Hit Chance": cchance_range,
              "Attack Percent": atkper_range,
              "Defense Percent": defper_range,
              "Effectiveness": eff_range,
              "Effect Resistance": effres_range,
              "Health Percent": hpper_range,
              "Attack Flat": atkflat_range,
              "Defense Flat": defflat_range,
              "Health Flat": hpflat_range}

avg_dict = {"Speed": 3, 
              "Critical Hit Damage": 5.5, 
              "Critical Hit Chance": 4,
              "Attack Percent": 6,
              "Defense Percent": 6,
              "Effectiveness": 6,
              "Effect Resistance": 6,
              "Health Percent": 6,
              "Attack Flat": 39,
              "Defense Flat": 31,
              "Health Flat": 174}


stat1 = 6
stat2 = 6
stat3 = 6
stat4 = 6

testinput1_substat_names = ["Attack Percent", "Defense Percent", "Health Percent", "Effectiveness"]
testinput1_substat_rolls = ["8", "6", "5", "36"]

testinput2_substat_names = ["Speed", "Critical Hit Chance", "Effect Resistance", "Health Percent"]
testinput2_substat_rolls = ["2", "19", "13", "8"]

testinput3_substat_names = ["Defense Percent", "Effectiveness", "Critical Hit Chance", "Effect Resistance"]
testinput3_substat_rolls = ["16", "7", "7", "20"]

testinput4_substat_names = ["Critical Hit Chance", "Critical Hit Damage", "Health Percent", "Effectiveness"]
testinput4_substat_rolls = ["9", "9", "20", "13"]

# Rare gear, 7 total rolls
testinput5_substat_names = ["Attack Percent", "Defense Percent", "Health Percent", "Effectiveness"]
testinput5_substat_rolls = ["18", "11", "5", "5"]

# flat stats test
testinput6_substat_names = ["Health Percent", "Health Flat", "Critical Hit Damage", "Attack Flat"]
testinput6_substat_rolls = ["8", "379", "12", "114"]

# Heroic gear, 8 total rolls
testinput7_substat_names = ["Speed", "Defense Percent", "Effect Resistance", "Effectiveness"]
testinput7_substat_rolls = ["4", "13", "15", "5"]

testinput8_substat_names = ["Effect Resistance", "Defense Percent", "Defense Flat", "Effectiveness"]
testinput8_substat_rolls = ["12", "10", "85", "4"]

# Heroic gear, 8 rolls
testinput9_substat_names = ["Defense Percent", "Speed", "Critical Hit Chance", "Defense Flat"]
testinput9_substat_rolls = ["15", "8", "3", "58"]

def calc_num_rolls(substat_names, substat_rolls): 
    stat1 = substat_names[0]
    stat2 = substat_names[1]
    stat3 = substat_names[2]
    stat4 = substat_names[3]
    stat1_roll = substat_rolls[0]
    stat2_roll = substat_rolls[1]
    stat3_roll = substat_rolls[2]
    stat4_roll = substat_rolls[3]
    stat_roll_list = [stat1_roll, stat2_roll, stat3_roll, stat4_roll]

    stat1_max_rolls = calc_max_rolls(stat1, stat1_roll)
    stat2_max_rolls = calc_max_rolls(stat2, stat2_roll)
    stat3_max_rolls = calc_max_rolls(stat3, stat3_roll)
    stat4_max_rolls = calc_max_rolls(stat4, stat4_roll)
    max_rolls_list = [stat1_max_rolls, stat2_max_rolls, stat3_max_rolls, stat4_max_rolls]

    stat1_min_rolls = calc_min_rolls(stat1, stat1_roll)
    stat2_min_rolls = calc_min_rolls(stat2, stat2_roll)
    stat3_min_rolls = calc_min_rolls(stat3, stat3_roll)
    stat4_min_rolls = calc_min_rolls(stat4, stat4_roll)
    stat1_avg = avg_dict[stat1]
    stat2_avg = avg_dict[stat2]
    stat3_avg = avg_dict[stat3]
    stat4_avg = avg_dict[stat4]
    avg_value_list = [stat1_avg, stat2_avg, stat3_avg, stat4_avg]

    stat1_num_rolls = stat1_min_rolls
    stat2_num_rolls = stat2_min_rolls
    stat3_num_rolls = stat3_min_rolls
    stat4_num_rolls = stat4_min_rolls
    num_rolls_list = [stat1_num_rolls, stat2_num_rolls, stat3_num_rolls, stat4_num_rolls]

    sum_min_rolls = stat1_min_rolls + stat2_min_rolls + stat3_min_rolls + stat4_min_rolls

    # Assume epic gear +15, total 9 rolls
    missing_rolls = 9 - sum_min_rolls
    
    stat1_scaled_diff = calc_scaled_diff(stat1_roll, stat1_avg, stat1_num_rolls)
    stat2_scaled_diff = calc_scaled_diff(stat2_roll, stat2_avg, stat2_num_rolls)
    stat3_scaled_diff = calc_scaled_diff(stat3_roll, stat3_avg, stat3_num_rolls)
    stat4_scaled_diff = calc_scaled_diff(stat4_roll, stat4_avg, stat4_num_rolls)

    scale_diff_list = [stat1_scaled_diff, stat2_scaled_diff, stat3_scaled_diff, stat4_scaled_diff]
    
    for i in range(missing_rolls):
        for j in range(4):
            if (num_rolls_list[j] >= max_rolls_list[j]):
                scale_diff_list[j] = 0
                continue
            scale_diff_list[j] = calc_scaled_diff(stat_roll_list[j], avg_value_list[j], num_rolls_list[j])
    
        max_scale_diff = max(scale_diff_list)
        max_scale_diff_index = scale_diff_list.index(max_scale_diff)

        num_rolls_list[max_scale_diff_index] += 1

    print("Num of rolls into stat 1: " + str(num_rolls_list[0]))
    print("Num of rolls into stat 2: " + str(num_rolls_list[1]))
    print("Num of rolls into stat 3: " + str(num_rolls_list[2]))
    print("Num of rolls into stat 4: " + str(num_rolls_list[3]))


        
        
    



def calc_max_rolls(substat_name, substat_roll):
    return math.floor(int(substat_roll)/int(range_dict[substat_name][MIN]))

def calc_min_rolls(substat_name, substat_roll):
    return math.ceil(int(substat_roll)/int(range_dict[substat_name][MAX]))

def calc_scaled_diff(substat_roll, avg_roll, num_rolls):
    return (float(substat_roll) - float(avg_roll) * float(num_rolls))/float(avg_roll)



calc_num_rolls(testinput8_substat_names, testinput8_substat_rolls)