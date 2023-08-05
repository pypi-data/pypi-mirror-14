#!/usr/bin/env python3
#
# Copyright (c) 2015-2016 Lapis Lazuli Texts
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" Convert EDICT1 dictionary text into CSV. """


import getopt
import io
import signal
import sys
import unicodedata


USAGE = """Usage: edict1-to-csv [options]

Reformat EDICT1 dictionary entries as simple CSV.

Options:
  -h, --help       print this help message and exit
  -v, --verbose    include information useful for debugging

"""


def set_stdio_utf8():
    """
    Set standard I/O streams to UTF-8.

    Attempt to reassign standard I/O streams to new streams using UTF-8.
    Standard input should discard any leading BOM. If an error is raised,
    assume the environment is inflexible but correct (IDLE).

    """
    try:
        sys.stdin = io.TextIOWrapper(
            sys.stdin.detach(), encoding='utf-8-sig', line_buffering=True)
        sys.stdout = io.TextIOWrapper(
            sys.stdout.detach(), encoding='utf-8', line_buffering=True)
        sys.stderr = io.TextIOWrapper(
            sys.stderr.detach(), encoding='utf-8', line_buffering=True)
    except io.UnsupportedOperation:
        pass


def edict_to_csv(line):
    """
    Convert an EDICT dictionary entry into CSV.

    Given a line from an EDICT-format dictionary, attempt to convert it
    into CSV format using the "|" character. If no alternate form or
    pronunciation is available in square brackets, then it will default to
    an empty string in the corresponding CSV column. The basic format
    returned is 'term1|term2|alternate|gloss', where term1 and term2 are
    the terms, alternate is the transliteration (e.g. Pinyin or kana), and
    gloss is the set of meanings or definitions for the entry.

    """
    alt = ''
    if ' [' in line and '] ' in line and line.index(' [') < line.index('] '):
        alt = line[line.index(' [')+2:line.index('] ')]
    if alt:
        term = line[:line.index(' [')]
    else:
        term = line[:line.index(' /')]
    gloss = line[line.index('/')+1:line.rindex('/')].replace('/', '; ')
    if gloss[-1] != '.':
        gloss += '.'
    entry = []
    term = term.replace('|', '/')
    alt = alt.replace('|', '/')
    gloss = gloss.replace('|', '/')
    return '%s||%s|%s\n' % (term, alt, gloss)


def main(argv):
    """
    Run as a portable command-line program.

    This program will attempt to handle data through standard I/O streams
    as UTF-8 text. Input text will have a leading byte-order mark stripped
    out if one is found. Broken pipes and SIGINT are handled silently.

    """
    set_stdio_utf8()
    if 'SIGPIPE' in dir(signal):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    try:
        verbose = False
        opts, args = getopt.getopt(
            argv[1:], 'hv', ['help', 'verbose'])
        for option, _ in opts:
            if option in ('-h', '--help'):
                print(USAGE, end='')
                return 0
            if option in ('-v', '--verbose'):
                verbose = True
        if len(args) > 0:
            sys.stderr.write(USAGE)
            return 1
        for line in sys.stdin:
            print(edict_to_csv(unicodedata.normalize('NFC', line)), end='')
        return 0
    except KeyboardInterrupt:
        print()
        return 1
    except Exception as err:
        if verbose:
            raise
        else:
            sys.stderr.write('edict1-to-csv: ' + str(err) + '\n')
            return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
