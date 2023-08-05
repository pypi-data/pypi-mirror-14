from collections import OrderedDict

from sblu.pdb import split_segments


def _splitsegs(records, renum, smod="", output_prefix="segment"):
    outputs = OrderedDict()
    for (segid, chain, segment) in split_segments(records):
        out_file = "{}-{}.{:04d}.pdb".format(output_prefix, chain, segid)
        outputs[(segid, chain)] = out_file

        with open(out_file, "w") as ofp:
            for record in segment:
                record.segment = smod + chain + str(segid)
                ofp.write(str(record).strip()+"\n")
            ofp.write("END\n")

    return outputs
