import sc2reader  # pip install --force-reinstall git+https://github.com/ggtracker/sc2reader.git

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

    def _stats_spread_creep(self):
        point_command_events = [i for i in self.replay.events if 'TargetPointCommandEvent' in i.name]
        tumor_events = [i for i in point_command_events if 'Tumor' in i.ability_name]
        tumors = [(i.second, i.ability_name) for i in tumor_events]
        print('total tumors: {}, by queens: {}, by tumors: {}'.format(
            len(tumors),
            len([i for i in tumors if 'Build' not in i[1]]),
            len([i for i in tumors if 'Build' in i[1]])
        ))
        for i in tumors:
            print('{:>4}. {}'.format(i[0], 'tumor by Queen' if 'Build' not in i[1] else 'tumor by tumor'))

    def parse(self):
        print(self.replay.game_length.total_seconds(), "seconds")  # 982
        print(self.replay.frames, "frames")  # 2201
        '''
        TODOs:
        # army
        1. hydras + 2 * lurkers num in time        
        
        # core buildings
        2. spawning pool ready
        3. lair ready
        4. hydra den ready
        5. lurker den ready
        
        # core upgrades
        6. hydra range ready
        7. hydra speed ready        
        8. missile attack 1 ready        
        9. missile attack 2 ready
        
        # economy
        10. drones num in time
        11. queens num in time
        12. queens mana pool in time
        13. 2nd hatchery ready
        14. 3d hatchery ready
        15. larvas used
        16. hatcheries with 3 larvas alerts
        17. supply used / available        
        18. minerals income
        19. gas income
        
        # def
        20. zerglings ready
        21. spores ready
        22. metabolic boost ready        
        '''

        self._stats_spread_creep()
