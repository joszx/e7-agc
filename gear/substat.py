
class Substat:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        # self.num_rolls = None








NORMAL_STATS = ['Attack Percent', 'Defense Percent', 'Health Percent', 'Effectiveness', 'Effect Resistance']


def is_normal_stat(stat):
    return stat.name in NORMAL_STATS
