from substat import Substat 
import gear_calc

class Gear:
    def __init__(self, gear_level, gear_type, enhance_level, substat_name_list, substat_value_list):
        self.gear_level = gear_calc.get_gear_level(gear_level)
        self.gear_type = gear_calc.get_gear_type(gear_type)
        self.enhance_level = int(enhance_level)
        self.substat_list = []
        for i in range(len(substat_name_list)): 
            curr_substat_name = substat_name_list[i]
            curr_substat_value = int(substat_value_list[i])
            self.substat_list.append(Substat(curr_substat_name, curr_substat_value))
        self.num_rolls_list = gear_calc.calc_num_gear_rolls(self.gear_level, self.gear_type, self.enhance_level, self.substat_list)
        self.gear_score = gear_calc.calc_gear_score(self.substat_list)
        self.gear_score_potential = gear_calc.calc_gear_score_potential(self.gear_level, self.substat_list, self.gear_type, self.num_rolls_list)
        if self.gear_level != gear_calc.LVL85:
            self.reforge_substat_list = []
            self.reforge_gear_score = 0
        else:
            self.reforge_substat_list = gear_calc.calc_reforge_stats(self.substat_list, self.num_rolls_list)
            self.reforge_gear_score = gear_calc.calc_gear_score(self.reforge_substat_list)

    def __str__(self):
        gear_level_txt = "Gear level: " + str(self.gear_level)
        gear_type_txt = "Gear type: " + str(self.gear_type)
        gear_enhance_lvl_txt = "Gear enhance lvl: " + str(self.enhance_level)
        gear_substat_txt = ""
        reforge_gear_substat_txt = ""
        for i in range(len(self.substat_list)):
            substat = self.substat_list[i]
            reforge_substat = self.reforge_substat_list[i]
            gear_substat_txt += "Substat: {0} - {1}, rolled {2} times\n".format(substat.name, substat.value, self.num_rolls_list[i])
            reforge_gear_substat_txt += "Substat: {0} - {1}, rolled {2} times\n".format(reforge_substat.name, reforge_substat.value, self.num_rolls_list[i])
        gear_score_txt = "Gear score: " + str(self.gear_score)
        gear_score_potential_txt = "Gear score potential: " + str(self.gear_score_potential)
        reforge_gear_score_txt = "Reforged gear score: " + str(self.reforge_gear_score)
        return  "{0} \n{1} \n{2} \n{3} \n{4} \n{5} \n{6} \n{7}".format(gear_level_txt, gear_type_txt, gear_enhance_lvl_txt, gear_substat_txt, gear_score_txt, gear_score_potential_txt, reforge_gear_substat_txt, reforge_gear_score_txt)
    

test_gear1 = Gear("85", "Epic", "15", ["Speed", "Critical Hit Chance", "Effect Resistance", "Health Percent"], ["2", "19", "13", "8"])
test_gear2 = Gear("85", "Epic", "15", ["Defense Percent", "Effectiveness", "Critical Hit Chance", "Effect Resistance"], ["16", "7", "7", "20"])
test_gear3 = Gear("85", "Epic", "15", ["Critical Hit Chance", "Critical Hit Damage", "Health Percent", "Effectiveness"], ["9", "9", "20", "13"])
test_gear4 = Gear("85", "Rare", "15", ["Attack Percent", "Defense Percent", "Health Percent", "Effectiveness"], ["18", "11", "5", "5"])
test_gear5 = Gear("85", "Epic", "15", ["Health Percent", "Health Flat", "Critical Hit Damage", "Attack Flat"], ["8", "379", "12", "114"])
test_gear6 = Gear("85", "Heroic", "15", ["Speed", "Defense Percent", "Effect Resistance", "Effectiveness"], ["4", "13", "15", "5"])
test_gear7 = Gear("85", "Heroic", "15", ["Effect Resistance", "Defense Percent", "Defense Flat", "Effectiveness"], ["12", "10", "85", "4"])
test_gear8 = Gear("85", "Heroic", "15", ["Defense Percent", "Speed", "Critical Hit Chance", "Defense Flat"], ["15", "8", "3", "58"])
test_gear9 = Gear("88", "Epic", "15", ["Health Percent", "Attack Percent", "Speed", "Effectiveness"], ["26", "9", "8", "21"])
test_gear10 = Gear("88", "Epic", "15", ["Health Percent", "Attack Percent", "Speed", "Critical Hit Chance"], ["9", "32", "8", "10"])
test_gear11 = Gear("85", "Heroic", "15", ["Attack Flat", "Critical Hit Damage", "Speed", "Effectiveness"], ["70", "10", "10", "5"])


print(test_gear7)