# mother-nds

nesDS ([DS-Homebrew/nesDS](https://github.com/DS-Homebrew/nesDS)) with a built-in ROM slot, so one `.nds` file contains both the emulator and your own NES ROM and boots straight into the game. Made for MOTHER (Famicom), works with most NES ROMs up to 512 KB.

No ROMs are included. The release is an empty `nesDS-embed.nds`; you add your own ROM to it.

## Make your all-in-one .nds

1. Download `nesDS-embed.nds` from [Releases](../../releases).
2. Add your ROM:
   - On a phone: open the web patcher, pick `nesDS-embed.nds` and your `.nes` (or `.zip`), save the result.
   - On a computer: `python3 tools/embed_rom.py nesDS-embed.nds "Mother (Japan).nes" MOTHER.nds`
3. Open the new `.nds` in DraStic, melonDS, or on a DS/DSi flashcard.

If the slot is empty, it behaves like normal nesDS with its file browser.

## Saving

- Real DS / DSi / melonDS with SD access: in-game saves go to a `.sav` next to the `.nds`, as in normal nesDS.
- DraStic: it doesn't give homebrew SD access, so use DraStic's own save states.

The bottom screen is nesDS's touch menu (save states, settings, screen options).

## How it works

`patches/embed-rom.patch` adds a 512 KB slot to nesDS's ARM9 binary, marked with `NESDS-EMBED-SLOT`, and makes nesDS boot from it when it isn't empty. The patcher just writes the ROM's size, name and bytes into that slot. The ROM buffer shrinks from 2.5 MB to 2 MB so memory use stays the same.

GitHub Actions builds it in the official `devkitpro/devkitarm` container on every push to `main` and publishes a release.

## Credits

nesDS by the nesDS team and DS-Homebrew contributors.
