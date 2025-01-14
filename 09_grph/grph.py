#!/usr/bin/env python3
"""
Author : yanhan <yanhan@localhost>
Date   : 2023-03-19
Purpose: Overlap Graphs
"""

import argparse
from collections import defaultdict
from itertools import product
from iteration_utilities import starfilter
import logging
import operator as op
from pprint import pformat
from typing import List, NamedTuple, TextIO

from Bio import SeqIO


class Args(NamedTuple):
    """Command-line arguments"""

    file: TextIO
    k: int
    debug: bool


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Overlap Graphs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "file",
        metavar="FILE",
        type=argparse.FileType("rt"),
        help="FASTA file",
    )

    parser.add_argument(
        "-k",
        "--overlap",
        help="Size of overlap",
        metavar="size",
        type=int,
        default=3,
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="Debug",
        action="store_true",
    )

    args = parser.parse_args()

    # k will be a positive integer.
    if args.overlap < 1:
        parser.error(f'-k "{args.overlap}" must be > 0')

    return Args(args.file, args.overlap, args.debug)


# --------------------------------------------------
def main() -> None:
    """Run as a Program"""

    args = get_args()

    # This will globally affect all subsequent calls to the logging module's functions.
    logging.basicConfig(
        filename=".log",
        filemode="w",
        level=logging.DEBUG if args.debug else logging.CRITICAL,
    )

    # Create dictionaries with list as default values.
    start, end = defaultdict(list), defaultdict(list)
    # Iterate the FASTA records.
    for rec in SeqIO.parse(args.file, "fasta"):
        # Not sure if it is necessary to coerce the Seq object to string.
        # Experiments are needed later.
        if kmers := find_kmers(str(rec.seq), args.k):
            start[kmers[0]].append(rec.id)
            end[kmers[-1]].append(rec.id)

    logging.debug(f'STARTS\n{pformat(start)}')
    logging.debug(f'ENDS\n{pformat(end)}')

    for kmer in set(start).intersection(set(end)):
        for pair in starfilter(op.ne, product(end[kmer], start[kmer])):
            print(*pair)


def find_kmers(seq: str, k: int) -> List[str]:
    """Find k-mers in string."""

    # If len(seq) - k + 1 <= 0, the list of the range function will return [].
    return [seq[n : n + k] for n in range(len(seq) - k + 1)]


def test_find_kmers() -> None:
    """Test find_kmers."""

    assert find_kmers("", 1) == []
    assert find_kmers("ACTG", 1) == ["A", "C", "T", "G"]
    assert find_kmers("ACTG", 2) == ["AC", "CT", "TG"]
    assert find_kmers("ACTG", 3) == ["ACT", "CTG"]
    assert find_kmers("ACTG", 4) == ["ACTG"]
    assert find_kmers("ACTG", 5) == []


# --------------------------------------------------
if __name__ == "__main__":
    main()
