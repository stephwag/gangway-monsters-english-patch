Notes on what parts of the game's logic has been changed.

## Battle Text

The way the monsters' names are rendered in the VS screen had to be updated for it to show up.

battle_text_address.png

* `11B500` is the address location (see register `s7`) of the asset that is used to render text.
* `C1A74` is when it updates the pointer to the the Japanese character it will render.

battle_text_change_command.png

* `B1C6C` - game will jump here after loading the monster names in memory. Change it from `lbu v0, 0x0000(a0)` to `ori v0, 0x0083` 
* `B1C70` - Change it from `lbu v1, 0x0001(a0)` to `lbu v1, 0x0000(a0)`

This changes it to load only the first and current byte. The or-ing with `0x83` is to fake a shift-jis character.

battle_text_swap_command.png

* `C1A1C` - Change this to `addiu a0, s1, 0x0008`
* `C1A20` - Change this to `sll s0, s1, 0x1`

The shifting is the game's way to iterate through names at two bytes at a time. It adds 8 because that's how many "slots" each name gets in memory. By changing it to shift after the addition, it will go through each byte one at a time, but shifting later will allow the game's math to work when choosing which Japanese character to render.

Keep in mind the new rendered text is not real Japanese. It is just associating each character with an equivalent shift-jis code (e.g. `A`, which is `0x41`, becomes linked with `0x83 0x41`, which is `ア`). This is fine though, because after applying these changes, making the VS screen show English characters would just be a matter of updating the image itself.

#### TODO's

* The name may be aligned weirdly if the name has an odd number of bytes.
* Some default names of the monsters are more than 8 bytes in English. This may cause the name not to fit completely in the VS screen (and only render the first 8 bytes).

## Name Input

See `replace_bytes.py`. The updates made in `replace_asm` when updating the SLPS file is all related to the name input. It basically changes it to only read/write 1 byte instead of 2, and updates the way the cursor moves so that it will hover over the character in the right spot.

#### TODO's

* The text in the input box looks kind of squished. There is a way to update the spacing of each character (located in roughly the same location as the updated input code), but it will change the spacing of characters throughout the game.

## Workflow

Workflow for finding and patching game logic

### Steps

* Use Bizhawk to filter what memory addresses are getting read/written to
* Go on Mednafen or pSX, step through disassembled code in debugger. Add read/write memory breakpoints to find where the code is.
* When found, dump memory and open it in IDA Pro. Click on the area where the code is, which IDA will find all the references to and show a nice map that makes life somewhat easier
* Dump the results to an ASM file
* Repeat above steps until it's figured out

### Tools

* [binviz](https://binvis.io) is also useful for figuring out if files are compressed, and how (e.g. like how offsets/window size is used, which affects structure of the file).
* psximager for rebuilding images
* This [documentation on how PlayStation works](http://www.raphnet.net/electronique/psx_adaptor/Playstation.txt) which was a very useful reference throughout development of the patch.



