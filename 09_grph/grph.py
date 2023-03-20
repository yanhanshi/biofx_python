#!/usr/bin/env python3
"""
Author : yanhan <yanhan@localhost>
Date   : 2023-03-19
Purpose: Overlap Graphs
"""

import argparse
import logging
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

    logging.debug('input file = "%s"', args.file.name)

    for rec in SeqIO.parse(args.file, "fasta"):
        print(rec.id, rec.seq)


def find_kmers(seq: str, k: int) -> List[str]:
    """Find k-mers in string."""

    return []


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
