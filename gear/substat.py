
class Substat:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        # self.num_rolls = None








NORMAL_STATS = ['Attack Percent', 'Defense Percent', 'Health Percent', 'Effectiveness', 'Effect Resistance']
NORMAL_STATS_UNEDITED = ['Attack', 'Defense', 'Health', 'Effectiveness', 'Effect Resistance', 'Critical Hit Chance', 'Critical Hit Damage', 'Speed']
FLAT_PERCENT_STATS = ['Attack', 'Defense', 'Health']


def is_normal_stat(stat):
    return stat.name in NORMAL_STATS
