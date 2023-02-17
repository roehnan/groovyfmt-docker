#!/usr/bin/env python3

from hashlib import blake2b
from pathlib import Path
from subprocess import call, DEVNULL
from sys import argv, exit

FORMAT_CMD = ['/app/format/bin/format']

if __name__ == '__main__':
    if len(argv[1:]) == 0:
        print('no files specified')
        exit(0)
    
    # grab our list of files
    files = [Path(f) for f in argv[1:]]
    # calculate hashes before formatting, for change detection
    hashes = {f:blake2b(f.read_bytes()).hexdigest() for f in files}

    # now format the files
    try:
        _ = call(FORMAT_CMD + files, stderr=DEVNULL, stdout=DEVNULL)
        # strip the erroneous newlines the formatter adds
        for f in files:
            data = f.read_text()
            data = data.rstrip()
            f.write_text(data + '\n')

        # now calc new hashes
        new_hashes = {f:blake2b(f.read_bytes()).hexdigest() for f in files}

        if new_hashes == hashes:
            exit(0)
        
        for f in files:
            if new_hashes[f] != hashes[f]:
                print(f'{f}: formatted')
        exit(1)

    except:
        exit(1)