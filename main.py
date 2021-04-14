from random import choice


class TicTacToe:
    GAME_PARAMS = ['medium', 'easy', 'user', 'hard']

    def __init__(self):
        self.table = None
        self.player_1 = None
        self.player_2 = None
        self.turn = 1
        self.menu()

    def menu(self):
        command = input('Input command: ')
        if command == 'exit':
            pass
        else:
            try:
                cmd, player1, player2 = command.split()
                if cmd == 'start' and all(param in self.GAME_PARAMS for param in [player1, player2]):
                    self.setup_game(player1=player1, player2=player2)
                else:
                    raise ValueError
            except ValueError:
                print('Bad parameters!')
                self.menu()

    def setup_game(self, player1, player2):
        self.table = self.Table()
        self.player_1 = self.setup_player(player1, sign='X', opp='O')
        self.player_2 = self.setup_player(player2, sign='O', opp='X')
        self.turn = 1
        self.game()

    def setup_player(self, player_type, sign, opp):
        if player_type == 'user':
            return self.HumanPlayer(sign=sign)
        else:
            return self.Bot(level=player_type, table=self.table, sign=sign, opp=opp)

    def game(self):
        self.table.print_table()
        self.table.update_table(*self.move())
        self.check_game_state()
        self.game()

    def move(self):
        if self.turn == 1:
            self.turn = 2
            return self.player_1.make_move(self.table.get_empty())
        else:
            self.turn = 1
            return self.player_2.make_move(self.table.get_empty())

    def check_game_state(self):
        win = self.table.get_win_cells()
        x_win = ['X'] * 3 in win
        o_win = ['O'] * 3 in win
        if any([x_win, o_win, self.table.get_empty() is None]):
            self.table.print_table()
            if x_win:
                print('X wins')
            elif o_win:
                print('O wins')
            else:
                print('Draw')
            self.menu()

    class Table:
        def __init__(self):
            self.table = ['_', '_', '_',
                          '_', '_', '_',
                          '_', '_', '_']

        def update_table(self, *params):
            index, sign = params
            self.table[index] = sign

        def get_positions(self):
            num_table = [index if sign == '_' else sign for index, sign in enumerate(self.table)]
            return self.get_win_cells(num_table)

        def get_empty(self):
            empty = [index for index, sign in enumerate(self.table) if sign == '_']
            return empty if empty else None

        def get_win_cells(self, table=None):
            if table is None:
                table = self.table
            vertical_win = [table[i: i + 3] for i in range(0, 8, 3)]
            horizontal_win = [table[i: 9:3] for i in range(3)]
            cross_win = [table[0:9:4], table[2:7:2]]
            return vertical_win + horizontal_win + cross_win

        def print_table(self):
            print('---------')
            for i in range(0, 8, 3):
                print('| ' + ' '.join(self.table[i: i + 3]) + ' |')
            print('---------')

    class _Player:
        def make_move(self, empty_cells):
            pass

    class HumanPlayer(_Player):

        def __init__(self, sign):
            self.own_sign = sign

        def make_move(self, empty_cells):
            try:
                x, y = input('Enter the coordinates: ').split()
                if x.isdigit() is False or y.isdigit() is False:
                    print('You should enter numbers!')

                elif x not in '123' or y not in '123':
                    print('Coordinates should be from 1 to 3!')

                else:
                    index = self.transfer_cord(x, y)
                    if index in empty_cells:
                        return index, self.own_sign
                    else:
                        print('This cell is occupied! Choose another one!')

                return self.make_move(empty_cells)

            except ValueError:
                print('You should enter numbers!')
                return self.make_move(empty_cells)

        @staticmethod
        def transfer_cord(x, y):
            return 3 * (int(x) - 1) + (int(y) - 1)

    class Bot(_Player):

        def __init__(self, level, table, sign, opp):
            self.level = level
            self.table = table
            self.own_sign = sign
            self.opp_sign = opp

        def make_move(self, empty_cells):
            print(f'Making move level "{self.level}"')
            move = choice(empty_cells)
            if self.level == 'easy':
                pass

            elif self.level == 'medium':
                best_move = self.analyze_table()
                if best_move:
                    move = choice(best_move)

            return move, self.own_sign

        def analyze_table(self):

            positions = self.table.get_positions()
            to_win_pos = self.filter_pos(sign=self.own_sign, pos=positions)
            to_block_pos = self.filter_pos(sign=self.opp_sign, pos=positions)
            return to_win_pos if to_win_pos else to_block_pos

        @staticmethod
        def filter_pos(sign, pos):
            pos_list = list(filter(
                lambda x: x.count(sign) == 2, pos))
            positions = [item for item_list in pos_list for item in item_list if type(item) == int]

            return positions


TicTacToe()
