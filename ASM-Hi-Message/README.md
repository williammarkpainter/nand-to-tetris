## Flashing HI KAY message in  assembly code only

The file can be loaded on the Hack Platform (using the CPU Emulator), to the falsh the message 'Hi Kay' on the screen. This is a standalone assembly file and does not require the Hack OS or any other supporting system files.

Software can be downloaded from https://www.nand2tetris.org/software

The code in HiKay.asm, print the HI KAY on the Hack Screen by writing to set memory locations. The value of -1 is written to RAM to display 16 pixel wide back line, and the value of 0 is written to clear any pixels.

HI KAY has 20 sections to render the text, each section is written as a column section, with a start memory location and an end memory location. When filling out the column seciton, 32 memory locations are skipped as this is the width of the screen memory location and it takes you to the next line in the same column.

The .asm file start by inputting 20 values into RAM 3000-3019, and 20 values into RAM 4000-4019. These are the start and end memory locations for each character character section.

The code then set -1 as the intial write option in RAM Address 2, then takes the values form 30XX and 40XX into RAM[0] and RAM[1], then writes -1 to these memory locations, skipping 32 memory location each write.

Once complete, there is a delay loop, then the write value in in RAM[2] is flipped to 0, and the process starts again to clear the screen.

This is repeated in an infinate loop.
