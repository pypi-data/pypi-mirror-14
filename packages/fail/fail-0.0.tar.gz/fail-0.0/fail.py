#!/usr/bin/env python

"""
run a program until it fails
"""

# imports
import argparse
import subprocess
import sys
import time

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', help="command to run")
    parser.add_argument('--code', dest='codes', default=(0,), nargs='+',
                        help="allowed exit codes")
    parser.add_argument('-s', '--sleep', dest='sleep',
                        type=float, default=1.,
                        help="sleep between iterations [DEFAULT: %(default)]")
    options = parser.parse_args(args)

    try:

        ctr = 0
        while True:

            print ("Iteration {}".format(ctr))
            ctr += 1

            # run it
            process = subprocess.Popen(options.command, shell=True)
            _, _ = process.communicate()

            # test it
            if process.returncode not in options.codes:
                sys.exit(process.returncode)

            # loop control
            time.sleep(options.sleep)


    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
