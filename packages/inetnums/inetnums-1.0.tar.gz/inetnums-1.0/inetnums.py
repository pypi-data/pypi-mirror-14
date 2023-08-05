#!/usr/bin/env python3

"""
Copyright © 2016 Mail.Ru Group LLC / Vadim Markovtsev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import argparse
import gzip
import os
import pickle
import pycurl
import shutil
import socket
import struct
import sys


urls = (
    "ftp://ftp.ripe.net/ripe/dbase/ripe.db.gz",
    "ftp://ftp.apnic.net/apnic/whois-data/APNIC/split/apnic.db.inetnum.gz",
    "ftp://ftp.afrinic.net/pub/dbase/afrinic.db.gz",
    "ftp://ftp.arin.net/pub/rr/arin.db"
)


def __get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true",
                        help="Overwrite cached database files")
    parser.add_argument("-c", "--cache", help="Path to the cache directory",
                        default=".cache")
    parser.add_argument(
        "-o", "--output", help="Output path (- for stdout, log will be "
                               "printed to stderr then)",
        required=True)
    parser.add_argument("-t", "--format", help="Output format",
                        default="pickle", choices=("pickle", "print"))
    return parser.parse_args()


def __setup_std_streams(output):
    if output == "-":
        sys.stdout, sys.stderr = sys.stderr, sys.stdout


def __fetch_file(url, where):
    def progress(size, downloaded, *args, **kwargs):
        if size > 0:
            slen = len(str(size))
            width = 80 - (slen * 2 + 3 + 2 + 2 + 4)
            ratio = downloaded / size
            dotp = int(ratio * width)
            sys.stdout.write(("\r%3d%% [%s%s] %" + str(slen) + "d / %d") % (
                int(ratio * 100), "." * dotp, " " * (width - dotp),
                downloaded, size))


    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.XFERINFOFUNCTION, progress)
    curl.setopt(curl.NOPROGRESS, False)
    curl.setopt(curl.FTP_FILEMETHOD, pycurl.FTPMETHOD_NOCWD)
    target = os.path.join(where, os.path.basename(url))
    try:
        with open(target, "wb") as fout:
            curl.setopt(curl.WRITEDATA, fout)
            curl.perform()
    finally:
        curl.close()
    return target


def __download_dbs(cache, force):
    files = []

    def download_gz(url):
        bfn = os.path.basename(url)
        target = os.path.join(cache, bfn[:bfn.find(".db") + 3])
        if not os.path.exists(target) or force:
            print("Downloading %s ..." % url)
            fn = __fetch_file(url, cache)
            print()  # we do not print a new line in the end
            print("Decompressing %s ..." % fn)
            with gzip.open(fn, "rb") as fin:
                with open(target, "wb") as fout:
                    shutil.copyfileobj(fin, fout)
            os.remove(fn)
        assert os.path.getsize(target) > 0
        files.append(target)

    def download_raw(url):
        target = os.path.join(cache, os.path.basename(url))
        if not os.path.exists(target) or force:
            print("Downloading %s ..." % url)
            __fetch_file(url, cache)
            print()  # we do not print a new line in the end
        assert os.path.getsize(target) > 0
        files.append(target)

    if not os.path.exists(cache):
        os.mkdir(cache)
    for url in urls:
        if url.endswith(".gz"):
            download_gz(url)
        else:
            download_raw(url)
    return files


def __ipstr2int(ip):
    try:
        return struct.unpack("!I", socket.inet_aton(ip.strip()))[0]
    except OSError:
        raise ValueError("Invalid IP: \"%s\"" % ip) from None


def __parse(file):
    print("Parsing %s ..." % file)
    crange = None
    cnetname = None
    ccountry = None
    cmntby = None
    step = os.path.getsize(file) // 100
    pos = 0
    rc = 0
    with open(file, "rb") as fin:
        for line in fin:
            pos += len(line)
            if pos == len(line) or (pos // step) > ((pos - len(line)) // step):
                sys.stdout.write("\r%d%%" % (pos // step))
                sys.stdout.flush()
            try:
                line = line.decode()
            except UnicodeDecodeError:
                continue
            try:
                val = line.split(":")[1].strip()
            except IndexError:
                continue
            if line.startswith("inetnum:"):
                if crange is not None:
                    yield (crange, cnetname, ccountry, cmntby)
                    cnetname = None
                    ccountry = None
                    cmntby = None
                    rc += 1
                try:
                    crange = tuple(__ipstr2int(ip) for ip in val.split("-"))
                except ValueError as e:
                    print("\rWarning: invalid inetnum record: %s: %s" %
                          (e, line[:-1]))
                    crange = None
            elif line.startswith("netname:"):
                cnetname = val.upper()
            elif line.startswith("country:"):
                ccountry = val[:2].upper()
            elif line.startswith("mnt-by:"):
                cmntby = val.upper().replace("-MNT", "").replace("MNT-", "")
    print("\r-> %d records" % rc)


def __build_levels(inetnums):
    print("Building levels from %d inetnums. Initial sort..." % len(inetnums))
    levels = []
    ranges = inetnums
    ranges.sort()
    while True:
        if not levels:
            print("Building IP boundary list...")
        ips = [(r[0][ii], "%d%d" % (ii, i))
               for i, r in enumerate(ranges)
               for ii in (0, 1)]
        if not levels:
            print("Sorting IP boundary list...")
        ips.sort()
        specinds = []
        broadinds = []
        if not levels:
            print("First pass...")
        for i, ip in enumerate(ips):
            if ip[1][0] == '0':
                idx = int(ip[1][1:])
                if ips[i + 1][1][0] == '1' and ip[1][1:] == ips[i + 1][1][1:]:
                    specinds.append(idx)
                else:
                    broadinds.append(idx)
        new_ranges = []
        if not levels:
            print("Second pass...")
        for i, bi in enumerate(broadinds):
            this = ranges[bi]
            spec = True
            for j in range(i + 1, len(broadinds)):
                net = ranges[broadinds[j]]
                if net[0][0] > this[0][0]:
                    spec = net[0][0] > this[0][1]
                    break
            if spec:
                specinds.append(bi)
            else:
                new_ranges.append(this)
        if not specinds:
            break
        if not levels:
            print("Sorting level 0 indices...")
        specinds.sort()
        if not levels:
            print("Merging level 0 indices...")
        ll = []
        levels.append(ll)
        ipstart = ranges[specinds[0]][0][0]
        for i in range(len(specinds) - 1):
            r, nr = (ranges[specinds[j]] for j in (i, i + 1))
            if r[1:] != nr[1:]:
                ll.append(((ipstart, r[0][1]),) + r[1:])
            ipstart = nr[0][0]
        ll.append(((ipstart, ranges[specinds[-1]][0][1]),) + ranges[specinds[-1]][1:])

        print("Level %d: %d > %d / %d (%d -> %d)" % (
            len(levels), len(specinds), len(ll), len(broadinds), len(ranges),
            len(new_ranges)))
        ranges = new_ranges
    return levels


def __write_result(levels, output, fmt):
    print("Writing the result (%s)..." % fmt)

    def write(fobj):
        if fmt == "pickle":
            pickle.dump(levels, fobj, protocol=-1)
        elif fmt == "print":
            fobj.write(b"# inetnums\n[\n")
            for lno, level in enumerate(levels):
                fobj.write(("# Level %d\n[\n" % lno).encode("utf-8"))
                for net in level:
                    fobj.write(("%s,\n" % net).encode("utf-8"))
                fobj.write(b"],\n")
            fobj.write(b"]\n")

    if output == "-":
        write(sys.stderr.buffer)
    else:
        with open(output, "wb") as fout:
            write(fout)

def main():
    args = __get_args()
    __setup_std_streams(args.output)
    files = __download_dbs(args.cache, args.force)
    inetnums = list(itertools.chain.from_iterable(__parse(f) for f in files))
    levels = __build_levels(inetnums)
    __write_result(levels, args.output, args.format)

if __name__ == "__main__":
    main()
