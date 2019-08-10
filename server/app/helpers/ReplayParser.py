import sc2reader

class ReplayParser:
    def __init__(self, replay):
        self.replay = sc2reader.load_replay(replay)

    def get_replay_name(self):
        # replay.players: [Player 1 - RoQer(Zerg), Player 2 - A.I. 1(Very Easy) (Terran)]
        # replay.date: datetime.datetime(2019, 7, 28, 15, 10, 14)
        name = self.replay.date.__str__()
        name = name.replace(' ', '_').replace(':', '-')
        name = name + '_' + self.replay.players[0].__str__() + '_vs_' + self.replay.players[1].__str__()
        name = (name.replace('Player 1 - ', '')
                    .replace('Player 2 - ', '')
                    .replace(' (Zerg)', '(Z)')
                    .replace(' (Terran)', '(T)')
                    .replace(' (Protoss)', '(P)')
                    .replace('A.I. 1', 'AI')
                    .replace(' (Very Easy)', '1')
                    .replace(' (Easy)',      '2')
                    .replace(' (Medium)',    '3')
                    .replace(' (Hard)',      '4')
                    .replace(' (Harder)',    '5')
                    .replace(' (Very Hard)', '6')
                    .replace(' (Elite)',     '7')
                )
        return name


    def parse(self):
        print(self.replay.game_length, "seconds")  # 982
        print(self.replay.frames, "frames")  # 22017

        abilities = [i.ability_name for i in self.replay.events if 'TargetPointCommandEvent' in i.name]

        a = [i for i in self.replay.events if 'TargetPointCommandEvent' in i.name]
        print(a[0].second)  # 3
        print(a[-1].second)  # 1370  -> 1 real second ~= 1.4 game seconds?
        b = [i for i in a if 'Tumor' in i.ability_name]
        c = [(i.second, i.ability_name) for i in b]
        print(
            'total tumors: {}, by queens: {}, by tumors: {}'.format(len(c), len([i for i in c if 'Build' not in i[1]]),
                                                                    len([i for i in c if 'Build' in i[1]])))
        for i in c:
            print('{:>4}. {}'.format(i[0], 'tumor by Queen' if 'Build' not in i[1] else 'tumor by tumor'))
