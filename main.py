#!/usr/bin/env python3
import random
import sys
import os
import time
from colorama import init, AnsiToWin32, Fore  # , Back, Style
init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream


class Tile(object):
    """docstring for Tile"""
    def set_mine(x=12):
        if(random.randint(1, 100) * 100 % x == 0):
            return True
        else:
            return False

    def __init__(self):
        super(Tile, self).__init__()
        self.flag = False
        self.mine = Tile.set_mine(x=24)
        self.value = None
        self.closed = True
        self.signal = 0

    def set_flag(self):
        self.flag = True
        pass

    def has_mine(self):
        return self.mine

    def is_closed(self):
        return self.closed


class Field(object):
    """docstring for Field"""

    def __init__(self, size=8):
        super(Field, self).__init__()
        self.size = size
        self.tiles = [Tile() for x in range(size**2)]
        # for tile in self.tiles:
        #     print(tile.has_mine())

    def get_signals(self):
        for row in range(self.size):
            for column in range(self.size):
                signal = 0
                neighbours2 = []
                neighbours = [[row, column + 1], [row, column - 1], [row + 1, column],
                              [row - 1, column], [row - 1, column - 1], [row + 1, column + 1],
                              [row + 1, column - 1], [row - 1, column + 1]]
                for neighbour in neighbours:
                    if neighbour[0] > -1:
                        if neighbour[0] < self.size:
                            if neighbour[1] > -1:
                                if neighbour[1] < self.size:
                                    neighbours2.append(neighbour)
                for neighbour in neighbours2:
                    if self.tiles[self.size * neighbour[0] + neighbour[1]].has_mine():
                        signal += 1
                self.tiles[self.size * row + column].signal = signal
        pass

    def show0(self, persistance=0.1):
        os.system("cls")
        print()
        for row in range(self.size):
            print("  ", end="")
            for column in range(self.size):
                if self.tiles[self.size * row + column].closed:
                    # if self.tiles[self.size * row + column].has_mine():
                    #     print(Fore.LIGHTRED_EX + "*" + "*", end=" " * 2 + Fore.LIGHTBLUE_EX)
                    # else:
                    if self.tiles[self.size * row + column].flag is True:
                        print(Fore.LIGHTRED_EX + ("0", "")[len(str(8 * row + column)) > 1] + str(8 * row + column), end=" " * 2 + Fore.LIGHTBLUE_EX)
                    else:
                        print(("0", "")[len(str(8 * row + column)) > 1] + str(8 * row + column), end=" " * 2)
                else:
                    if self.tiles[self.size * row + column].signal == 0:
                        print("  ", end="  ")
                    else:
                        print(Fore.LIGHTGREEN_EX + "0" + str(self.tiles[self.size * row + column].signal), end=" " * 2 + Fore.LIGHTBLUE_EX)
            print("\n")
        time.sleep(persistance)
        pass

    def show(self):
        os.system("cls")
        print()
        for row in range(self.size):
            print("  ", end="")
            for column in range(self.size):
                if self.tiles[self.size * row + column].closed:
                    print(("0", "")[len(str(8 * row + column)) > 1] + str(8 * row + column), end=" " * 2)
                else:
                    print(Fore.LIGHTGREEN_EX + "0" + str(self.tiles[self.size * row + column].signal), end=" " * 2 + Fore.LIGHTBLUE_EX)
            print("\n")
        pass


class Game(object):
    """docstring for Game"""

    def __init__(self):
        super(Game, self).__init__()
        self.in_progress = True
        self.level = 1
        self.field = Field(size=8)
        self.field.get_signals()

    def flag(self, tile):
        self.field.tiles[tile].set_flag()
        pass

    def move(self, tile):
        if tile >= self.field.size**2:
            return
        if self.field.tiles[tile].has_mine():
            self.in_progress = False
            for each_tile in self.field.tiles:
                each_tile.closed = False
        else:
            self.field.tiles[tile].closed = False
            row = int(tile / self.field.size)
            column = int(tile % self.field.size)
            neighbours2 = []
            neighbours = [[row, column + 1], [row, column - 1], [row + 1, column],
                          [row - 1, column], [row - 1, column - 1], [row + 1, column + 1],
                          [row + 1, column - 1], [row - 1, column + 1]]
            for neighbour in neighbours:
                if neighbour[0] > -1:
                    if neighbour[0] < self.field.size:
                        if neighbour[1] > -1:
                            if neighbour[1] < self.field.size:
                                neighbours2.append(neighbour)
            for neighbour in neighbours2:
                if self.field.tiles[self.field.size * neighbour[0] + neighbour[1]].signal == 0:
                    if not self.field.tiles[self.field.size * neighbour[0] + neighbour[1]].has_mine():
                        if self.field.tiles[self.field.size * neighbour[0] + neighbour[1]].closed:
                            self.move(self.field.size * neighbour[0] + neighbour[1])
                            self.field.show0(0.0)

            for neighbour in neighbours2:
                if not self.field.tiles[self.field.size * neighbour[0] + neighbour[1]].has_mine():
                    if self.field.tiles[self.field.size * neighbour[0] + neighbour[1]].closed:
                        self.field.tiles[self.field.size * neighbour[0] + neighbour[1]].closed = False
                        self.field.show0(0.0)
            pass

    def main_loop(self):
        while self.in_progress:
            os.system("mode con cols=37 lines=18")
            self.field.show0()
            choice = input()
            if choice[0] == 'f' or choice[0] == 'F':
                choice = int(choice[1:])
                self.flag(choice)
            else:
                choice = int(choice)
                self.move(choice)
            pass
        while True:
            self.field.show()
            pass
        pass


def main():
    os.system("title Mine_Sweeper")
    game = Game()
    game.main_loop()
    pass


if __name__ == '__main__':
    main()
