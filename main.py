from random import choice


class TTTGame:
    GAME_PARAMS = ['medium', 'easy', 'user', 'hard']

    def __init__(self):
        self.table = ['_', '_', '_',
                      '_', '_', '_',
                      '_', '_', '_']
        self.sign = 'X'
        self.bot_1 = None
        self.bot_2 = None
        self.game_mode = None
        self.menu()

    def menu(self):
        self.reset_game()
        command = input('Input command: ')
        if command == 'exit':
            pass
        else:
            try:
                cmd, p1, p2 = command.split()
                if cmd == 'start' and all(param in self.GAME_PARAMS for param in {p1, p2}):
                    if p1 == p2 == 'user':
                        self.game_mode = 'pvp'  # player vs player
                    elif p1 != p2 and 'user' in (p1, p2):
                        self.game_mode = 'pvb'  # player vs bot
                        if p1 == 'user':
                            self.set_bots(bot1=p2)
                        else:
                            self.set_bots(bot1=p1)
                    else:
                        self.game_mode = 'bvb'
                        self.set_bots(p1, p2)
                    self.game()
                else:
                    raise ValueError

            except ValueError:
                print('Bad parameters!')
                self.menu()

    def set_bots(self, bot1=None, bot2=None):
        bot_list = {'easy': self.EasyBot(),
                    'medium': self.MediumBot()}
        if all([bot1, bot2]):
            self.bot_1 = bot_list[bot1]
            self.bot_2 = bot_list[bot2]
        else:
            self.bot_1 = bot_list[bot1]

    def reset_game(self):
        self.table = ['_', '_', '_',
                      '_', '_', '_',
                      '_', '_', '_']
        self.sign = 'X'

    def game(self):
        self.print_table(self.table)
        if self.game_mode == 'pvp':
            self.enter_cords()

        elif self.game_mode == 'bvb':
            if self.sign == 'X':
                self.update_table(self.bot_1.make_move(self.table))
            elif self.sign == 'O':
                self.update_table(self.bot_2.make_move(self.table))

        elif self.game_mode == 'pvb':
            if self.sign == 'X':
                self.enter_cords()
            else:
                self.update_table(self.bot_1.make_move(self.table))

        self.check_game_state()

    def enter_cords(self):
        try:
            x, y = input('Enter the coordinates: ').split()
            if x.isdigit() is False or y.isdigit() is False:
                print('You should enter numbers!')
                self.enter_cords()
            elif x not in '123' or y not in '123':
                print('Coordinates should be from 1 to 3!')
                self.enter_cords()
            else:
                index = self.transfer_cord(x, y)
                if self.table[index] == '_':
                    self.update_table(index)
                else:
                    print('This cell is occupied! Choose another one!')
                    self.enter_cords()
        except ValueError:
            print('You should enter numbers!')
            self.enter_cords()

    def update_table(self, index):
        self.table[index] = self.sign
        self.sign = self.sign_change(current_sign=self.sign)

    def check_game_state(self):
        vertical_win = [''.join(self.table[i: i + 3]) for i in range(0, 8, 3)]
        horizontal_win = [''.join(self.table[i: 9:3]) for i in range(3)]
        cross_win = [''.join(self.table[0:9:4]), ''.join(self.table[2:7:2])]

        win = vertical_win + horizontal_win + cross_win
        if any(['XXX' in win, 'OOO' in win, '_' not in self.table]):
            if 'XXX' in win:
                self.print_table(self.table)
                print('X wins')
            elif 'OOO' in win:
                self.print_table(self.table)
                print('O wins')
            elif '_' not in self.table:
                self.print_table(self.table)
                print('Draw')
            self.menu()
        else:
            self.game()

    @staticmethod
    def sign_change(current_sign):
        return 'X' if current_sign == 'O' else 'O'

    @staticmethod
    def transfer_cord(x, y):
        return 3 * (int(x) - 1) + (int(y) - 1)

    @staticmethod
    def print_table(table):
        print('---------')
        for i in range(0, 8, 3):
            print('| ' + ' '.join(table[i: i + 3]) + ' |')
        print('---------')

    class EasyBot:

        @staticmethod
        def get_emptycells(table):
            return [index for index, sign in enumerate(table) if sign == '_']

        def make_move(self, table):
            empty_cells = self.get_emptycells(table)
            print('Making move level "easy"')
            return choice(empty_cells)

    class MediumBot:

        @staticmethod
        def get_emptycells(table):
            return [index for index, sign in enumerate(table) if sign == '_']

        def make_move(self, table):
            empty_cells = self.get_emptycells(table)
            print('Making move level "medium"')

            return choice(empty_cells)


TTTGame()
