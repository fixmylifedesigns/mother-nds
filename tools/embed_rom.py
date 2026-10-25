#!/usr/bin/env python3
"""Write an NES rom into the empty rom slot of nesDS-embed.nds.

usage: python3 embed_rom.py nesDS-embed.nds "Mother (Japan).nes" MOTHER.nds
The rom may also be a .zip containing one .nes file.
"""
import sys, struct, zipfile, os

MAGIC = b"NESDS-EMBED-SLOT"
HEADER_SIZE = 64
SLOT_SIZE = 0x80000

def read_rom(path):
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if n.lower().endswith(".nes")]
            if not names:
                sys.exit("no .nes file inside the zip")
            return os.path.basename(names[0]), z.read(names[0])
    with open(path, "rb") as f:
        return os.path.basename(path), f.read()

def embed(nds, name, rom):
    if rom[:4] != b"NES\x1a":
        sys.exit("not an iNES rom (missing NES header)")
    if len(rom) > SLOT_SIZE:
        sys.exit("rom is %d bytes, the slot holds %d" % (len(rom), SLOT_SIZE))
    pos = nds.find(MAGIC)
    if pos < 0 or nds.find(MAGIC, pos + 1) >= 0:
        sys.exit("could not find exactly one rom slot in the .nds")
    if struct.unpack_from("<I", nds, pos + 16)[0] != 0:
        sys.exit("this .nds already has a rom embedded, use the empty nesDS-embed.nds")
    out = bytearray(nds)
    stem = os.path.splitext(name)[0].encode("ascii", "ignore")[:39] + b".nes"
    struct.pack_into("<I", out, pos + 16, len(rom))
    out[pos + 20:pos + 64] = stem.ljust(44, b"\0")
    out[pos + HEADER_SIZE:pos + HEADER_SIZE + len(rom)] = rom
    return bytes(out)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    with open(sys.argv[1], "rb") as f:
        nds = f.read()
    name, rom = read_rom(sys.argv[2])
    with open(sys.argv[3], "wb") as f:
        f.write(embed(nds, name, rom))
    print("wrote %s with %s (%d bytes)" % (sys.argv[3], name, len(rom)))
