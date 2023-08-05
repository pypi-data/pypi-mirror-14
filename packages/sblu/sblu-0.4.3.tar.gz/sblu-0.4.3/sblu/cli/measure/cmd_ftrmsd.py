import click
import numpy as np
from scipy.spatial.distance import cdist

from prody import parsePDB

from sblu.cli import pass_context
from sblu.ft import (read_rotations, read_ftresults_stream,
                     apply_ftresults_atom_group)
from sblu.rmsd import calc_rmsd


@click.command('ftrmsd', short_help="Calculate RMSDs using an FTFile from PIPER.")
@click.argument("lig_file", type=click.Path(exists=True))
@click.argument("lig_crys", type=click.Path(exists=True))
@click.argument("ftfile", type=click.File(mode='r'))
@click.argument("rotprm", type=click.File(mode='r'))
@click.option("--sort-ftresults/--no-sort-ftresults", default=False)
@click.option('-n', "--nftresults",
              type=click.INT,
              default=None)
@click.option("--only-CA", is_flag=True, help="Only C-alpha atoms")
@click.option("--only-backbone", is_flag=True, help="Only backbone atoms")
@click.option("--only-interface", is_flag=True, default=False,
              help="Only use inteface atoms. Requires --rec.")
@click.option("--interface-radius", type=click.FLOAT, default=10.0,
              help="Radius around receptor to consider.")
@click.option("--rec", type=click.Path(exists=True), default=None,
              help="Receptor file if using interface mode.")
@click.option('-o', "--output", type=click.File(mode='w'),
              default=click.open_file("-", "w"),
              help="Write output to file (default: stdout)")
@pass_context
def cli(ctx,
        lig_file, lig_crys, ftfile, rotprm,
        sort_ftresults, nftresults, only_ca, only_backbone,
        only_interface, interface_radius, rec, output):
    lig = parsePDB(lig_file)
    lig_crys = parsePDB(lig_crys)

    if sort_ftresults:
        ftresults = read_ftresults_stream(ftfile)
        ftresults.sort(order='E', kind='mergesort')  # only mergesort is stable
        ftresults = ftresults[:nftresults]
    else:
        ftresults = read_ftresults_stream(ftfile, limit=nftresults)

    rotations = read_rotations(rotprm)

    transformed = apply_ftresults_atom_group(lig, ftresults, rotations)

    if only_ca:
        transformed = transformed.calpha
        lig_crys = lig_crys.calpha
    elif only_backbone:
        transformed = transformed.backbone
        lig_crys = lig_crys.backbone

    lig_crys_coords = lig_crys.getCoords()

    interface = None
    if rec and only_interface:
        rec = parsePDB(rec)
        rec_coords = rec.getCoords()

        r_sq = interface_radius**2
        dists = cdist(rec_coords, lig_crys_coords, 'sqeuclidean')
        interface = np.any(dists < r_sq, axis=0).nonzero()[0]

    rmsds = calc_rmsd(transformed, lig_crys, interface)
    for rms in rmsds:
        print("{:.2f}".format(rms), file=output)
