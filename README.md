# Gangway Monsters English Patch

This is the English patch for the PS1 game, Gangway Monsters.

The translations were done using Google Translate.

## How to apply patch

* Obtain a ROM of the game (it should have one `.bin` file and one `.cue` file).
* [Download the patch here](https://gangway-monsters-english.s3.amazonaws.com/gangway_monsters_english_v0.1.patch.xz).
* Follow the instructions below.

### Windows

* Decompress the patch using [7zip](https://www.7-zip.org/).
* Install [Git for Windows](https://git-scm.com/download/win)
* Apply the patch to the game's `.bin` file by using the `C:\Program Files\Git\usr\bin\patch.exe` utility.

```
"C:\Program Files\Git\usr\bin\patch.exe" --binary "\path\to\game.bin" "\path\to\gangway_monsters_english.patch"
```

* Give it a minute to complete applying the patch.


### Linux/Mac

* Decompress the patch using Archive Utility (Mac) or the `xz` command.
* Apply the patch to the game's `.bin` file.

```
patch /path/to/game.bin < /path/to/gangway_monsters_english.patch
```

* Give it a minute to complete applying the patch.


## Building a Patch

* See `scripts` for scripts used to create the patch. Keep in mind some of them are just one-off scripts used to save some time. The main script is `replace_bytes.py`, which also updates game logic to work with English words.
* `en-ja` contains the Japanese/English pairings for translation.

## Reporting bugs, typos, etc.

Create an issue.

## Contributing

If you happen to know Japanese and want to help correct any translations, please contribute! The least accurate translations are probably the "monbook" ones, and any dialogue with a lot of "emotion" in it.

If you want to contribute by fixing bugs or adding features, see NOTES.md for notes on what parts were changed (it will probably save you some time) and any TODOs related to those changes.