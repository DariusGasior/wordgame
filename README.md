# WordGame CLI
A simple terminal-based word guessing game

*Usage:* wordgame.py [wordlist.txt]
## Options
- `-n, --num-letters` Sets the size of the words used for the game. The word list file must contain words of this length. The default is word length is 5. Cannot be used with `-w`.

- `-w, --word` Sets the secret word for the game. Used for testing. The word list must contain words of the same length. Cannot be used with `-n`.
