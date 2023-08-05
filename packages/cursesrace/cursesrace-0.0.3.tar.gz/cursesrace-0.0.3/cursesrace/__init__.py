import sys
import time
import random
import curses


__version__ = '0.0.3'


class Game(object):
    def __init__(self, initial_size=40, decay=0.995, delay=0.1):
        self.delay = delay
        self.decay = decay

        self.size = initial_size
        self.pos = initial_size // 2
        self.width = curses.COLS
        self.height = curses.LINES

        self.score = 0
        self.player_height = 10
        self.walls = [(0, self.size)]

        for __ in range(self.height - 1):
            self.populate_wall()

    def populate_wall(self):
        last_size = int(round(self.size))
        self.size *= self.decay
        this_size = int(round(self.size))

        left, right = self.walls[-1]
        dir = random.random()

        if this_size < last_size:
            if dir > 0.5:
                # right stays the same, left moves in
                new_left, new_right = right - this_size, right
            else:
                # left stays the same, right moves in
                new_left, new_right = left, left + this_size
        else:
            if (dir > 0.6) and (right < self.width - 1):
                # move right
                new_left, new_right = left + 1, right + 1
            elif (dir < 0.4) and (left > 0):
                # move left
                new_left, new_right = left - 1, right - 1
            else:
                # same
                new_left, new_right = left, right

        self.walls.append((new_left, new_right))

        if len(self.walls) > self.height:
            self.walls.pop(0)

    def explode(self, stdscr):
        for dist in range(5):
            stdscr.clear()
            stdscr.addstr(self.player_height, self.pos, '%')
            stdscr.addstr(self.player_height - dist, self.pos, '^')
            stdscr.addstr(self.player_height + dist, self.pos, 'v')
            stdscr.addstr(self.player_height, max(0, self.pos - dist), '<')
            stdscr.addstr(self.player_height,
                          min(self.width - 1, self.pos + dist), '>')
            stdscr.move(0, 0)
            stdscr.refresh()
            time.sleep(self.delay)

    def loop(self, stdscr):
        stdscr.clear()
        curses.use_default_colors()
        stdscr.nodelay(True)

        while True:
            self.score += 1
            stdscr.clear()

            # handle moves
            ch = stdscr.getch()
            if ch == curses.KEY_LEFT:
                self.pos -= 1
                if self.pos < 0:
                    self.pos = 0
            elif ch == curses.KEY_RIGHT:
                self.pos += 1
                if self.pos >= self.width:
                    self.pos = self.width - 1
            elif ch == ord('q'):
                break

            # check for collision
            left, right = self.walls[self.player_height]
            if (self.pos <= left) or (self.pos >= right):
                self.explode(stdscr)
                break

            # draw player
            stdscr.addstr(self.player_height, self.pos, 'V')

            # draw walls
            for y in range(self.height):
                left, right = self.walls[y]
                stdscr.addstr(y, left, "#")
                stdscr.addstr(y, right, "#")

            # draw score
            score_s = " Score: %d " % self.score
            stdscr.addstr(0, (self.width - len(score_s)) // 2, score_s)

            # paint screen and wait
            stdscr.move(0, 0)
            stdscr.refresh()
            time.sleep(self.delay)
            self.populate_wall()


def wrapped(stdscr):
    game = Game()
    game.loop(stdscr)
    return game.score


def main(args=sys.argv):
    score = curses.wrapper(wrapped)
    print("Score: %d" % score)
