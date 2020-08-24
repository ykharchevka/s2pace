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

    def _stats_hydra_lur_born_and_dead_time(self):
        born_hydra = [(i.second, i.unit_type_name) for i in self.replay.events
                      if i.name == 'UnitBornEvent' and i.unit_type_name == 'Hydralisk'
                      and i.unit_upkeeper.name == 'yehor']
        born_lur = [(i.second, i.unit_type_name) for i in self.replay.events
                    if i.name == 'UnitTypeChangeEvent'
                    and 'Lurker' == [j.name for j in i.unit.type_history.values()][-1]
                    and i.unit.owner.name == 'yehor']  # TODO: need to debug as too many lurs
        dead = [(i.second, i.unit.name) for i in self.replay.events
                if i.name == 'UnitDiedEvent' and i.unit.name in ('Hydralisk', 'Lurker')
                and i.unit.owner.name == 'yehor']
        print('born hydra', born_hydra)
        print('born lur', born_lur)
        print('dead hydra and lur', dead)

    def _stats_buildings_and_creep_init_time(self):
        init = [(i.second, i.unit.name) for i in self.replay.events
                if i.name == 'UnitInitEvent' and i.unit.owner.name == 'yehor']
        print(init)

    def _stats_buildings_and_creep_ready_time(self):
        done = [(i.second, i.unit.name) for i in self.replay.events
                if i.name == 'UnitDoneEvent' and i.unit.owner.name == 'yehor']
        print(done)

    def _stats_upgrades_ready_time(self):
        upg_names = ('zerglingmovementspeed',
                     'ZergMissileWeaponsLevel1', 'ZergMissileWeaponsLevel2',
                     'EvolveMuscularAugments', 'EvolveGroovedSpines',
                     'ZergGroundArmorsLevel1', 'ZergGroundArmorsLevel2', 'ZergGroundArmorsLevel3',
                     'ZergMissileWeaponsLevel3',
                     'overlordspeed', 'ZergFlyerWeaponsLevel1')
        done = [(i.second, i.upgrade_type_name) for i in self.replay.events
                if i.name == 'UpgradeCompleteEvent' and i.upgrade_type_name in upg_names
                and i.player.name == 'yehor']
        print(done)

    def parse(self):
        print(self.replay.game_length.total_seconds(), "seconds")  # 982
        print(self.replay.frames, "frames")  # 2201
        '''
        TODOs:
        1. Decide how to visualize, e.g.: https://observablehq.com/@d3/gallery .
        2. Prepare necessary charts (tutor: https://observablehq.com/@d3/learn-d3).
        3. Store data to Pg to avoid parsing all replays to show performance comparison.
        4. Integrate solution and put it to rqdev.com
        5. Automate code delivery to prod.
        
        VISUALIZE:
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
        self._stats_hydra_lur_born_and_dead_time()
        self._stats_buildings_and_creep_init_time()
        self._stats_buildings_and_creep_ready_time()
        self._stats_upgrades_ready_time()
        self._stats_spread_creep()
