#!/usr/bin/env python3
import argparse
import os
import random
import string
import sys


def get_small_words():
    words = [
        "about", "board", "brain", "brave", "bright", "bring", "catch", "chalk",
        "class", "clean", "climb", "dance", "dream", "drink", "earth", "every",
        "found", "fresh", "giant", "grand", "grass", "green", "happy", "laugh",
        "learn", "light", "lucky", "never", "paper", "place", "plant", "quick",
        "rhyme", "right", "rules", "scale", "share", "shine", "small", "smile",
        "story", "study", "sweet", "teach", "thank", "think", "under", "water",
        "write", "young",
    ]
    return [word.upper() for word in set(words)]


class WordGame:
    def __init__(self, args):
        self.word_file = 'words.txt'
        self._init_system()
        self._init_colors()
        self._init_keyboard()
        self.win = False
        self.hint = False
        self.qwerty = True
        self.forced_word = ''
        self._set_prefs(args)
        self.words = self.get_words()
        self.new_game()

    def get_words(self, word_len=5):
        fname = self.word_file
        if not os.path.isfile(fname):
            sys.exit(f"Word file not found {fname}")
        with open(fname, 'r') as f:
            words = [line.strip() for line in f.readlines()
                     if len(line.strip()) == word_len]
        return [word.upper() for word in set(words)]

    def new_game(self):

        os.system(self.clear_cmd)
        print()
        self.playing = True
        self.history = set()
        self.game_state = []

        self.word = random.choice(self.words)

        if self.forced_word:
            if len(self.forced_word) == len(self.words[0]):
                self.word = self.forced_word
                self.words.append(self.forced_word)
                self.hint = True

    def new_round(self):
        hint = ''
        if self.hint:
            hint = f'({self.word}) '
        guess = input(f"{hint}Enter your word: ").strip().upper()

        if guess == '?':
            self.hint = True
            return (None, "You're cheating")
        if len(guess) == 0:
            self.playing = False
            return (None, "Thank you for playing")

        if len(guess) != len(self.word):
            return (None, f"Words must be {len(self.word)} letters long")

        if guess not in self.words:
            return (None, "Word not in wordlist")

        if guess in self.history:
            return (None, f"You already tried {guess}")

        self.process(guess)
        self.history.add(guess)
        if guess == self.word:
            self.win = True
            self.playing = False
            return (None, "You Win!")
        return (None, "")

    def process(self, guess):
        round = {'char': [], 'status': []}
        letters = list(guess)
        word = list(self.word)
        for i, c in enumerate(letters):
            if c == word[i]:
                status = self.correct
                self.keyboard[c] = self.correct
                word[i] = ' '
            elif c in word:
                status = self.matched
                word[word.index(c)] = ' '
            else:
                status = self.notthere
            if self.keyboard[c] != self.correct:
                self.keyboard[c] = status
            round['char'].append(c)
            round['status'].append(status)
        self.game_state.append(round)

    def display(self):
        padding = ' ' * ((26 - len(self.word)) // 2)
        for row in self.game_state:
            print(padding, end='')
            for i, c in enumerate(list(row['char'])):
                print(f"{row['status'][i]}{c}{self.reset} ", end='')
            print('')
        for _ in range((len(self.word) + 1) - len(self.game_state)):
            print(padding + ' '.join(['-'] * len(self.word)))
        print('')
        self.draw_keyboard()
        print('')

    def draw_keyboard(self):
        layout = string.ascii_uppercase
        pad_sz = 0
        if self.qwerty:
            layout = "Q W E R T Y U I O P\n A S D F G H J K L\n  Z X C V B N M"
            pad_sz = 5
        output = ['']
        for c in list(layout):
            if c in self.keyboard:
                output[-1] += f"{self.keyboard[c]}{c}{self.reset}"
            elif c == '\n':
                output.append('')
            else:
                output[-1] += c

        for line in output:
            padding = " " * pad_sz
            print(f"{padding}{line}")

    def lose(self):
        print(f"Sorry, you didn't win. The word was {
              self.correct}{self.word}{self.reset}")

    def play(self):
        while self.playing:
            self.display()
            result, msg = self.new_round()
            os.system(self.clear_cmd)
            if len(self.game_state) == len(self.word) + 1:
                if not self.win:
                    self.lose()
                break
            print(msg)
        self.display()

    def _init_colors(self):
        self.green = "\033[32;1m"
        self.yellow = "\033[38;2;201;180;88;40m"
        self.yellow = "\033[38;2;223;194;64;40m"
        self.dkgray = "\033[38;5;244;40m"
        self.ltgray = "\033[37m"
        self.reset = "\033[0m"

        self.correct = self.green
        self.matched = self.yellow
        self.unused = self.ltgray
        self.notthere = self.dkgray

    def _init_keyboard(self):
        self.keyboard = {}
        for c in list(string.ascii_uppercase):
            self.keyboard[c] = self.unused

    def _init_system(self):
        platform = sys.platform
        self.clear_cmd = 'clear'
        if 'win' in platform:
            self.clear_cmd = 'cls'

    def _set_prefs(self, args):
        if args.words_file:
            if not os.path.isfile(args.words_file):
                sys.exit(f"Word file not found: {args.words_file}")
            self.word_file = args.words_file

        if args.word:
            if not all([c in string.ascii_uppercase for c in args.word.upper()]):
                sys.exit("Forced words must only contain letters")
            self.forced_word = args.word.upper()


def play_wordgame():
    args = get_args()
    game = WordGame(args)
    game.play()


def get_args():
    parser = argparse.ArgumentParser(
        description="A terminal-based word guessing game"
    )

    parser.add_file = parser.add_argument(
        "words_file",
        nargs="?",
        default="words.txt",
        help="The path to the file which contains the word list to play with"
    )

    parser.add_argument(
        "-w", "--word",
        type=str,
        help=("Force the word to use for the game. "
              "Word list file must contain words of the same length.")
    )
    return parser.parse_args()


def main():
    play_wordgame()


if __name__ == "__main__":
    main()
