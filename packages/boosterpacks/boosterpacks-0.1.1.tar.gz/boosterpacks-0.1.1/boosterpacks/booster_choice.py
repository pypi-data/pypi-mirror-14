from bisect import bisect
from random import random, choice, shuffle

__all__ = ('BoosterGenerator',)

class Quality(object):
    REGULAR = '1'
    CONSCRIPT = '2'
    ELITE = '3'
    HEROIC = '4'
    PARAGON = '5'

    human_readable = {'1': 'regular', '2': 'conscript', '3': 'elite', '4': 'heroic', '5': 'paragon'}


class Chance(object):
    NORMAL_CHANCE = [(Quality.CONSCRIPT, 80), (Quality.ELITE, 8), (Quality.HEROIC, 7), (Quality.PARAGON, 5)]
    ELITE_CHANCE = [(Quality.CONSCRIPT, 0), (Quality.ELITE, 88), (Quality.HEROIC, 7), (Quality.PARAGON, 5)]
    EPIC_CHANCE = [(Quality.CONSCRIPT, 0), (Quality.ELITE, 0), (Quality.HEROIC, 95), (Quality.PARAGON, 5)]
    PARAGON_CHANCE = [(Quality.CONSCRIPT, 0), (Quality.ELITE, 0), (Quality.HEROIC, 0), (Quality.PARAGON, 100)]

    rules = {

        'default': (NORMAL_CHANCE, ELITE_CHANCE),
        'donators': (EPIC_CHANCE, PARAGON_CHANCE),
        'legendary': (PARAGON_CHANCE, PARAGON_CHANCE),
    }

    @classmethod
    def resolve(cls, rule):
        return cls.rules.get(rule, 'default')


class BoosterGenerator(object):
    def __init__(self, objects_list):
        """
        :param objects_list: list of tuples eq [(uniquestrinqid, quality), ...]
        """
        self.objects_list = objects_list

    def _random_select(self, total, cum_weights, values):
        x = random() * total
        i = bisect(cum_weights, x)
        return choice([key for key, rarity in self.objects_list if rarity == values[i]])

    @staticmethod
    def _weighted_choice(choices):
        values, weights = zip(*choices)
        total = 0
        cum_weights = []
        for weight in weights:
            total += weight
            cum_weights.append(total)
        return total, cum_weights, values

    def rule_selector(self, selector):
        total, cum_weights, values = self._weighted_choice(selector)
        return total, cum_weights, values

    def generate_cards(self, rule, count, unique_count):
        """
        :rtype : list of uniquestringid
        """
        regular_rule, fifth_card_rule = Chance.resolve(rule)
        regular_total, regular_cum_weights, regular_values = self.rule_selector(regular_rule)
        regular = [self._random_select(regular_total, regular_cum_weights, regular_values) for _ in range(count)]

        total, cum_weights, values = self.rule_selector(fifth_card_rule)
        unique = [self._random_select(total, cum_weights, values) for _ in range(unique_count)]

        return regular + unique

    def generate(self, rule='default', count=5, unique_count=1):
        cards = self.generate_cards(rule=rule, count=count, unique_count=unique_count)
        return cards


if __name__ == '__main__':
    cards = [(u'neut_u_modulehealer', u'1'), (u'terr_t_PrecisionStrike', u'2'),
             (u'terr_t_PulseBarrage', u'3'), (u'terr_t_NuclearStrike', u'4'),
             (u'shan_u_NaninteSwarm', u'3'), (u'shan_t_CorruptTransform', u'3'),
             (u'shan_u_ParasiticThrall', u'5'), (u'shan_t_Infestation', u'2')
             ]
    boosterpack = BoosterGenerator(cards)
    print (boosterpack.generate())
