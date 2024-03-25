#! /usr/bin/env python3

import gzip
import sys
import signal
from itertools import chain

import etsv  # ver. 0.0.2


def hmm2aln(aln, hmm_coord):
    for i, n in enumerate(aln, 1):
        if n == "-" or n.isupper():
            hmm_coord -= 1
        if hmm_coord == 0:
            return i
    raise IndexError(f"HMM coordinate is out of range ({hmm_coord})")


def aln2prot(aln, start, aln_coord, from_coord=True):
    start -= 1
    for n in aln[:aln_coord]:
        if n not in "-.":
            start += 1
    if from_coord and aln[aln_coord-1] in "-.":
        start += 1
    return start


def cut_region(aln, start, hmm_coords):
    aln_frags = []
    prot_coords = []
    for hmm_from, hmm_to in hmm_coords:
        aln_from = hmm2aln(aln, hmm_from)
        aln_to = hmm2aln(aln, hmm_to)
        aln_frags.append(aln[aln_from-1:aln_to])
        prot_from = aln2prot(aln, start, aln_from)
        prot_to = aln2prot(aln, start, aln_to, False)
        if prot_from <= prot_to:
            prot_coords.append(f"{prot_from}-{prot_to}")
    return ",".join(aln_frags), ",".join(prot_coords)


def parse_coords(coords_str):
    coord_from, coord_to = coords_str.split("-", 1)
    return int(coord_from), int(coord_to)


def parse_coordset(coordset_str):
    return [parse_coords(s) for s in coordset_str.split(",")]


def format_coordset(coordset):
    return ",".join(f"{f}-{t}" for f, t in coordset)


def process_alignments(instk, outsv, regions):
    hmmid = None
    reg_coords = None
    process_hmm = True
    alns = dict()
    with instk:
        for line in instk:
            if line.startswith("#"):
                if line.startswith("#=GF ID"):
                    hmmid = line[8:-1]
                    process_hmm = hmmid in regions
                    if process_hmm:
                        reg_coords = regions[hmmid]
                continue
            if line.startswith("//"):
                for seqid, aln in alns.items():
                    nm, coords_str = seqid.split("/", 1)
                    hit_id = ":".join((nm, hmmid, coords_str))
                    prot_from, _prot_to = parse_coords(coords_str)
                    for region, hmm_coords in reg_coords:
                        aln_frags, prot_coords = cut_region(aln, prot_from,
                                                            hmm_coords)
                        outsv.write_entry(vars())
                hmmid = None
                alns = dict()
                continue
            line = line.strip()
            if process_hmm and line:
                seqid, aln = line.split(maxsplit=1)
                alns[seqid] = alns.get(seqid, "") + aln


def load_regions(intsv):
    regions = dict()
    for vals in intsv:
        hmmid = vals["hmmid"]
        region = vals["region"]
        hmm_coordset = vals["coords"]
        regions.setdefault(hmmid, []).append((region, hmm_coordset))
    return regions


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: <script> regions.tsv hmmsearch.stk[.gz]")
        sys.exit(1)

    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass # no signal.SIGPIPE on Windows

    with open(sys.argv[1]) as intsv_obj:
        intsv = etsv.ETSVReader(intsv_obj, [
            etsv.InputField("hmmid", 0),
            etsv.InputField("region", "Region_name"),
            etsv.InputField("coords", "Region_coords_HMM", parse_coordset),
        ])
        regions = load_regions(intsv)
    instk_name = sys.argv[2]
    if instk_name.endswith(".gz"):
        instk = gzip.open(instk_name, 'rt')
    else:
        instk = open(instk_name)
    outsv = etsv.ETSVWriter(sys.stdout, [
        etsv.OutputField("hit_id", "Hit_ID"),
        etsv.OutputField("nm", "REBASE_name"),
        etsv.OutputField("hmmid", "Model_ID"),
        etsv.OutputField("region", "Region_name"),
        etsv.OutputField("coords_str", "Alignment_coords"),
        etsv.OutputField("prot_coords", "Region_coords"),
        etsv.OutputField("hmm_coords", "Region_coords_HMM", format_coordset),
        etsv.OutputField("aln_frags", "Alignment_frags"),
    ])
    process_alignments(instk, outsv, regions)
