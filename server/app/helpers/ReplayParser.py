import sc2reader

class ReplayParser:
    def __init__(self):
        pass

    def parse(self, filename):
        replay = sc2reader.load_replay(filename)

        print(replay.game_length, "seconds")  # 982
        print(replay.frames, "frames")  # 22017

        abilities = [i.ability_name for i in replay.events if 'TargetPointCommandEvent' in i.name]

        a = [i for i in replay.events if 'TargetPointCommandEvent' in i.name]
        a[0].second  # 3
        a[-1].second  # 1370  -> 1 real second ~= 1.4 game seconds?
        b = [i for i in a if 'Tumor' in i.ability_name]
        c = [(i.second, i.ability_name) for i in b]
        print(
            'total tumors: {}, by queens: {}, by tumors: {}'.format(len(c), len([i for i in c if 'Build' not in i[1]]),
                                                                    len([i for i in c if 'Build' in i[1]])))
        for i in c:
            print('{:>4}. {}'.format(i[0], 'tumor by Queen' if 'Build' not in i[1] else 'tumor by tumor'))
