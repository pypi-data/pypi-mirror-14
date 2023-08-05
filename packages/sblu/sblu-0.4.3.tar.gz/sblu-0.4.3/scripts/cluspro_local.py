#!/usr/bin/python
from __future__ import print_function
import os
import sys
import shutil
from glob import glob
from argparse import ArgumentParser, ArgumentTypeError, FileType
import subprocess
import logging
"""Run CLUSPRO on a local machine"""

LOG = logging.getLogger("cluspro_local")


# Function to see if executable exists in $PATH
# borrowed from user "Jay" at stackoverflow.com
# https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


# Function to check if given chains exist in file, or, if no chains are given, list all chains
# Assumes PDBPREP has already run in cwd
def checkchains(pdb, chainlist):
    LOG.info(os.getcwd())
    cmd = "ls " + str(pdb) + "-?.*"
    files = subprocess.check_output(cmd, shell=True).split()

    chains = set()
    for f in files:
        chains.add(f.split("-")[1][0].upper())

    if chainlist:
        chainlist = [c.upper() for c in chainlist]
        for c in chainlist:
            if c not in chains:
                LOG.error("Chain " + c + " not found in given " + pdb + " file!")
                raise Exception()
    else:
        chainlist = chains

    return sorted(list(chainlist))


def validate_args(args):
    pass


# Command line argument handling
def create_parser():
    def executable(path):
        exe = which(path)
        if exe is None:
            raise ArgumentTypeError("{} not found".format(path))
        return exe

    parser = ArgumentParser(description="Run CLUSPRO docking on local machine")
    parser.add_argument("rec_file", type=FileType('r'),
                        help="Receptor pdb file")
    parser.add_argument("lig_file", type=FileType('r'),
                        help="Ligand pdb file")

    parser.add_argument("--prm", type=FileType('r'),
                        default=os.path.expanduser("~/prms/parm.prm"),
                        help="Atom parameter file")
    parser.add_argument("--rtf", type=FileType('r'),
                        default=os.path.expanduser("~/prms/pdbamino.rtf"),
                        help="RTF parameter file")
    parser.add_argument("--rotprm", type=FileType('r'), metavar='<rots>',
                        default=os.path.expanduser("~/prms/rotsets/rot70k.0.0.6.jm.prm"),
                        help="Use <rots> as the rotations parameter file")

    parser.add_argument("--working_dir", default=".", help="working directory")
    parser.add_argument("--others-mode", default=False, action="store_true",
                        help="Run in others mode.")

    parser_prep = parser.add_argument_group("Preparation")
    parser_prep.add_argument("--pdbprep", type=executable,
                                default="pdbprep.pl",
                                help="Path to pdbprep.pl script")

    parser_prep.add_argument("--pdbnmd", type=executable,
                               default="pdbnmd.pl",
                               help="path to pdbnmd.pl script")
    parser_prep.add_argument("--nmin", type=executable,
                               help="Path to nmin executable")
    parser_prep.add_argument("--psfgen", type=executable,
                               help="Path to psfgen executable")

    parser_prep.add_argument("--pdbnmd_rec_link",
                               help="type,seg1,res1,seg2,res2,...")
    parser_prep.add_argument("--pdbnmd_rec_first",
                               help="n_term,chain1,chain2,...")
    parser_prep.add_argument("--pdbnmd_rec_smod", default="R",
                               help="pdbnmd rec segment_prefix")
    parser_prep.add_argument("--pdbnmd_rec_chains", nargs="*",
                               help="pdbnmd rec chains")
    parser_prep.add_argument("--pdbnmd_rec_nsteps",
                               type=int, help="pdbnmd rec nsteps")
    parser_prep.add_argument("--pdbnmd_rec_dont_clean", action="store_true",
                               help="pdbnmd rec dont-clean")
    parser_prep.add_argument("--pdbnmd_rec_dont_minimize", action="store_true",
                               help="pdbnmd rec dont-minimize")

    parser_prep.add_argument("--pdbnmd_lig_link",
                               help="type,seg1,res1,seg2,res2,...")
    parser_prep.add_argument("--pdbnmd_lig_first",
                               help="n_term,chain1,chain2,...")
    parser_prep.add_argument("--pdbnmd_lig_smod",
                               default="L", help="pdbnmd lig segment_prefix")
    parser_prep.add_argument("--pdbnmd_lig_chains",
                               nargs="*", help="pdbnmd lig chains")
    parser_prep.add_argument("--pdbnmd_lig_nsteps", type=int,
                               help="pdbnmd lig nsteps")
    parser_prep.add_argument("--pdbnmd_lig_dont_clean", action="store_true",
                               help="pdbnmd lig dont-clean")
    parser_prep.add_argument("--pdbnmd_lig_dont_minimize", action="store_true",
                               help="pdbnmd lig dont-minimize")

    parser_concat = parser.add_argument_group("concat")
    parser_concat.add_argument("--concat", type=executable,
                               default="pdb_psf_concat",
                               help="path to pdb_psf_concat")
    parser_concat.add_argument("--concat_prefix", default="reclig",
                               help="concat prefix")

    parser_piper = parser.add_argument_group("PIPER")
    parser_piper.add_argument("--piper", type=executable,
                              default="piper", help="path to PIPER program")
    parser_piper.add_argument("--piper_f", type=FileType('r'), metavar='<coeffs>',
                              default=os.path.expanduser("~/prms/coeffs/coeffs.0.0.6.cs1.0.serverdemo"),
                              help="Use <coeffs> as the coefficient parameter file")
    parser_piper.add_argument("--piper_p", type=FileType('r'), metavar='<atom>',
                              default=os.path.expanduser("~/prms/atoms.0.0.4.prm.ms.3cap+0.5ace.Hr0rec"),
                              help="Use <atom> as atom parameter file")
    parser_piper.add_argument("--piper_n", type=int, metavar='<N>',
                              help="Output the top <N> ftresults (default: all)")
    parser_piper.add_argument("--piper_v", action="count", default=2,
                              help="Increase verbosity. Multiple -v options increase the verbosity. The maximum is 2.")
    parser_piper.add_argument("--piper_a", action="store_true", default=False,
                              help="Use antibody functions")
    parser_piper.add_argument("--piper_c", type=float, metavar='<cellsize>',
                              help="Use <cellsize> as grid cell size (default: 1.0)")
    parser_piper.add_argument("--piper_grid_pad", type=int, default=2, metavar='<pad>',
                              help="Use <pad> as fft grid padding (default: 2)")
    parser_piper.add_argument("--piper_k", default=4, type=int, metavar='<k>',
                              help="Use first <k> eigenvalues from prm file (default: 4)")
    parser_piper.add_argument("--piper_R", default=70000, type=int, metavar='<nrots>',
                              help="Use first <nrots> rotation matrices from rotation file (default: 70000)")
    parser_piper.add_argument("--piper_surface_potential", default=False,
                              action="store_true",
                              help="Place pairwise potential only on surface atoms.")
    parser_piper.add_argument("--piper_T", metavar='<plan_type>',
                              default="FFTW_EXHAUSTIVE", choices=["FFTW_EXHAUSTIVE", "FFTW_ESTIMATE"],
                              help="Use <plan_type> as planning type rigor for fftw. (default: FFTW_EXHAUSTIVE)")
    parser_piper.add_argument("--piper_d", type=float, default=5.0, metavar='<radius>',
                              help="Use <radius> as the angstrom radius of the top hit per rotation to be marked. (default: 5.0)")
    parser_piper.add_argument("--piper_t", type=int, default=1, metavar='<N>',
                              help="Save the top <N> results from each rotation. (default: 1)")
    parser_piper.add_argument("--piper_pb", type=FileType('r'), metavar='FILE',
                              help="Read poisson boltzmann grid from FILE")
    parser_piper.add_argument("--piper_pbt", type=float, metavar='t',
                              help="Use <t> for poisson boltzmann extrema threshold (default: 40.0)")
    parser_piper.add_argument("--piper_cavity", action="store_true", help="Use cavity function")
    parser_piper.add_argument("--piper_water_sigma", type=float, help="Use <sigma> for gaussian water sphere (default: 10.0)")
    parser_piper.add_argument("--piper_enative", action="store_true", help="Print energies for given input structures")
    parser_piper.add_argument("--piper_maskrec", type=FileType('r'),
                              metavar='<FILE>', help="Mask receptor with <FILE>")
    parser_piper.add_argument("--piper_masklig", type=FileType('r'),
                              metavar='<FILE>', help="Mask ligand with FILE")
    parser_piper.add_argument("--piper_maskr", default=1.0, type=float, help="Mask all atoms within <k> angstroms of mask atoms")
    parser_piper.add_argument("--piper_axis",  type=FileType('r'),
                              metavar='<FILE>', help="Enforce symmetric docking. Use axis file <FILE>.")
    parser_piper.add_argument("--piper_smooth_elec", type=int, help="Smooth the elec grids N times (default: 3)")
    parser_piper.add_argument("--piper_smooth_pot", type=int, help="Smooth the pairwise potential grids N times (default: 0)")
    parser_piper.add_argument("--piper_scale_radii", type=float, help="Use <k> for prms radii scaling (default: 1.0)")
    parser_piper.add_argument("--piper_msur_k", type=float, help="Use <k> for msur solvent and prms radii scaling (default: 1.0)")
    parser_piper.add_argument("--piper_rvdw_sa_scale", type=float, help="Repulsive vdw sa scale (default: 0.9)")
    parser_piper.add_argument("--piper_rvdw_nsa_scale", type=float, help="Repulsive vdw not sa scale (default: 1.2)")
    parser_piper.add_argument("--piper_avdw_sa_scale", type=float, help="Attractive vdw sa scale (default: 0.0)")
    parser_piper.add_argument("--piper_avdw_sa_inc", type=float, help="Attractive vdw sa increment (default: 6.5)")
    parser_piper.add_argument("--piper_avdw_nsa_scale", type=float, help="Attractive vdw not sa scale (default: 0.0)")
    parser_piper.add_argument("--piper_avdw_nsa_inc", type=float, help="Attractive vdw not sa increment (default: 6.5)")

    parser_cluster = parser.add_argument_group("Clustering")
    parser_cluster.add_argument("--pwrmsd", default="pwrmsd.py", type=executable,
                               help="Path to pwrmsd")
    parser_cluster.add_argument("--pwrmsd-n", default=1000, type=int,
                               help="Number of results to cluster")
    parser_cluster.add_argument("--cluster-bin", default="cluster.py", type=executable,
                                help="Path to cluster bin")
    parser_cluster.add_argument("--cluster-radius", default=9.0, type=float,
                                help="Radius for clustering")
    parser_cluster.add_argument("--cluster-min-size", default=10, type=int,
                                help="Minimum cluster size")
    parser_cluster.add_argument("--max-clusters", default=50, type=int,
                                help="Maximum number of clusters per coefficient")
    parser_cluster.add_argument("--gen-cluster-models", default="gen_pdb_cluster_models.py", type=executable,
                                help="Path to gen_pdb_cluster_models")
    parser_cluster.add_argument("--minimize-clusters", default=False, action="store_true",
                                help="Minimize the clusters")
    parser_cluster.add_argument("--minimize-bin", default="complex_refine", type=executable,
                                help="Path to refinement binary.")

    return parser


def setup_working_dir(working_dir, rec, lig):
    subdirectories = ("inputs", "prepped", "piper", "clusters", "logs")
    for subdirectory in subdirectories:
        subdir = os.path.join(working_dir, subdirectory)
        if os.path.exists(subdir):
            if not os.path.isdir(subdir):
                LOG.error("Path {} already exists and is not a directory".format(subdir))
        else:
            try:
                os.makedirs(subdir)
            except Exception as e:
                LOG.error("Could not create directory {}".format(subdir),
                          exc_info=True)
                raise e

    LOG.info("Copying input files...")
    shutil.copy(rec.name,
                os.path.join(working_dir, "inputs", "rec.pdb"))
    shutil.copy(lig.name,
                os.path.join(working_dir, "inputs", "lig.pdb"))


def prepare_pdbs(args):
    try:
        # pdbprep
        os.chdir("prepped")
        for prefix in ('rec', 'lig'):
            os.symlink("../inputs/{}.pdb".format(prefix), "{}.pdb".format(prefix))
            cmd = [args.pdbprep, "{}.pdb".format(prefix)]
            subprocess.call(cmd)

        # pdbnmd
        cmd = [args.pdbnmd, "--xplor-psf"]
        if args.pdbnmd_rec_smod:
            cmd += ["--smod={}".format(args.pdbnmd_rec_smod)]
        if args.pdbnmd_rec_link:
            cmd += ["--link", args.pdbnmd_rec_link]
        if args.pdbnmd_rec_first:
            cmd += ["--first", args.pdbnmd_rec_first]
        if args.psfgen:
            cmd += ["--psfgen", args.pdbnmd_rec_psfgen]
        if args.nmin:
            cmd += ["--nmin", args.pdbnmd_rec_nmin]
        if args.pdbnmd_rec_dont_minimize:
            cmd += ["--dont-minimze "]
        elif args.pdbnmd_rec_nsteps:
            cmd += ["--nsteps", str(args.pdbnmd_rec_nsteps)]
        if args.pdbnmd_rec_dont_clean:
            cmd += ["--dont-clean"]

        cmd += ["--osuffix={}".format("_prepped")]
        cmd += ["--rtf", args.rtf.name]
        cmd += ["--prm", args.prm.name]
        cmd += ["rec"] + checkchains("rec", args.pdbnmd_rec_chains)
        LOG.info(" ".join(cmd))
        subprocess.call(cmd)

        cmd = [args.pdbnmd, "--xplor-psf"]
        if args.pdbnmd_lig_smod:
            cmd += ["--smod={}".format(args.pdbnmd_lig_smod)]
        if args.pdbnmd_lig_link:
            cmd += ["--link", args.pdbnmd_lig_link]
        if args.pdbnmd_lig_first:
            cmd += ["--first", args.pdbnmd_lig_first]
        if args.psfgen:
            cmd += ["--psfgen", args.pdbnmd_lig_psfgen]
        if args.nmin:
            cmd += ["--nmin", args.pdbnmd_lig_nmin]
        if args.pdbnmd_lig_dont_minimize:
            cmd += ["--dont-minimze "]
        elif args.pdbnmd_lig_nsteps:
            cmd += ["--nsteps", str(args.pdbnmd_lig_nsteps)]
        if args.pdbnmd_lig_dont_clean:
            cmd += ["--dont-clean"]

        cmd += ["--osuffix={}".format("_prepped")]
        cmd += ["--rtf", args.rtf.name]
        cmd += ["--prm", args.prm.name]
        cmd += ["lig"] + checkchains("lig", args.pdbnmd_lig_chains)
        LOG.info(" ".join(cmd))
        subprocess.call(cmd)

        # pdb_psf_concat
        cmd = [args.concat]
        cmd += ["--rtf={}".format(args.rtf.name)]
        cmd += ["--prefix={}".format(args.concat_prefix)]
        cmd += ["rec_prepped_xplor.psf", "rec_prepped.pdb", "lig_prepped_xplor.psf", "lig_prepped.pdb"]
        LOG.info(" ".join(cmd))
        subprocess.call(cmd)

        rec = os.path.join(args.working_dir, "prepped", "rec_prepped.pdb")
        lig = os.path.join(args.working_dir, "prepped", "lig_prepped.pdb")

        return rec, lig
    finally:
        os.chdir(args.working_dir)  # End in working directory


def run_piper(args, rec, lig):
    try:
        os.chdir("piper")
        cmd = [args.piper]
        if args.piper_f:
            cmd += ["-f", args.piper_f.name]
        if args.piper_p:
            cmd += ["-p", args.piper_p.name]
        if args.rotprm:
            cmd += ["-r", args.rotprm.name]
        if args.piper_n:
            cmd += ["-n ", str(args.piper_n)]
        if args.piper_v > 0:
            cmd += ["-" + "v"*args.piper_v]
        if args.piper_a:
            cmd += ["-a"]
        if args.piper_c:
            cmd += ["-c", str(args.piper_c)]
        if args.piper_grid_pad:
            cmd += ["--grid-pad={}".format(args.piper_grid_pad)]
        if args.piper_k:
            cmd += ["-k", str(args.piper_k)]
        if args.piper_R:
            cmd += ["-R", str(args.piper_R)]
        if args.piper_surface_potential:
            cmd += ["--surface-potential"]
        if args.piper_T:
            cmd += ["-T", args.piper_T]
        if args.piper_d:
            cmd += ["-d", str(args.piper_d)]
        if args.piper_t:
            cmd += ["-t", str(args.piper_t)]
        if args.piper_pb:
            cmd += ["--pb={}".format(args.piper_pb)]
        if args.piper_pbt:
            cmd += ["--pbt={}".format(args.piper_pbt)]
        if args.piper_cavity:
            cmd += ["--cavity"]
        if args.piper_water_sigma:
            cmd += ["--water_sigma={}".format(args.piper_water_sigma)]
        if args.piper_enative:
            cmd += ["--enative"]
        if args.piper_maskrec:
            cmd += ["--maskrec={}".format(args.piper_maskrec.name)]
        if args.piper_masklig:
            cmd += ["--masklig={}".format(args.piper_masklig.name)]
        if args.piper_maskr:
            cmd += ["--maskr={}".format(args.piper_maskr)]
        if args.piper_axis:
            cmd += ["--axis={}".format(args.piper_axis.name)]
        if args.piper_smooth_elec:
            cmd += ["--smooth-elec={}".format(args.piper_smooth_elec)]
        if args.piper_smooth_pot:
            cmd += ["--smooth-pot={}".format(args.piper_smooth_pot)]
        if args.piper_scale_radii:
            cmd += ["--scale_radii={}".format(args.piper_scale_radii)]
        if args.piper_msur_k:
            cmd += ["--msur_k={}".format(args.piper_msur_k)]
        if args.piper_rvdw_sa_scale:
            cmd += ["--rvdw_sa_scale={}".format(args.piper_rvdw_sa_scale)]
        if args.piper_rvdw_nsa_scale:
            cmd += ["--rvdw_nsa_scale={}".format(args.piper_rvdw_nsa_scale)]
        if args.piper_avdw_sa_scale:
            cmd += ["--avdw_sa_scale={}".format(args.piper_avdw_sa_scale)]
        if args.piper_avdw_sa_inc:
            cmd += ["--avdw_sa_inc={}".format(args.piper_avdw_sa_inc)]
        if args.piper_avdw_nsa_scale:
            cmd += ["--avdw_nsa_scale={}".format(args.piper_avdw_nsa_scale)]
        if args.piper_avdw_nsa_inc:
            cmd += ["--avdw_nsa_inc={}".format(args.piper_avdw_nsa_inc)]

        cmd += [rec, lig]
        LOG.info(" ".join(cmd))
        print(cmd)

        with open("../logs/piper.log", "w") as piper_log:
            subprocess.check_call(cmd, stdout=piper_log, stderr=piper_log)
    finally:
        os.chdir(args.working_dir)


def cluster_ftresults(args, rec, lig):
    try:
        os.chdir("piper")

        # Generate cluster centers
        for ftfile in glob("ft.???.??"):
            coeff = ftfile.split(".")[1]
            pwrmsd_file = ftfile+".clustermat"
            cluster_file = ftfile+".cluster"

            cmd = [args.pwrmsd]
            cmd += ["-n", str(args.pwrmsd_n)]
            cmd += ["-m", "1"]
            cmd += ["--only-CA"]
            cmd += ["-o", pwrmsd_file]
            cmd += [rec, lig, ftfile, args.rotprm.name]
            LOG.info(" ".join(cmd))
            subprocess.call(cmd)

            cmd = [args.cluster_bin]
            cmd += ["-r", str(args.cluster_radius)]
            cmd += ["-s", str(args.cluster_min_size)]
            cmd += ["-l", str(args.max_clusters)]
            cmd += ["-o", cluster_file]
            cmd += [pwrmsd_file]
            LOG.info(" ".join(cmd))
            subprocess.call(cmd)

            cmd = [args.gen_cluster_models]
            cmd += ['-m', str(30)]
            cmd += [cluster_file, ftfile, args.rotprm.name,
                    lig, "../clusters/lig."+coeff]
            LOG.info(" ".join(cmd))
            subprocess.call(cmd)

        os.chdir(args.working_dir)
        os.chdir("clusters")

        # Concatenate with receptor to produce model files
        with open(rec, "r") as f:
            rec_lines = f.readlines()

        LOG.info("Generating concatenated model files")
        for cluster_center in glob("lig.???.??.pdb"):
            coeff, model_index = cluster_center.split(".")[1:3]
            model_file = "model.{}.{}.pdb".format(coeff, model_index)

            with open(cluster_center, "r") as lig_file:
                lig_lines = lig_file.readlines()

            with open(model_file, "w") as output:
                output.write("HEADER rec.pdb\n")
                output.writelines(rec_lines)
                output.write("HEADER {}\n".format(cluster_center))
                output.writelines(lig_lines)

    finally:
        os.chdir(args.working_dir)


def minimize_clusters(args):
    try:
        os.chdir("clusters")

        pass  # Do minimization
    finally:
        os.chdir(args.working_dir)


def main():
    if os.isatty(sys.stderr.fileno()):
        try:
            from colorama import init, Fore
            init()

            COLOR_DICT = {
                "INFO": Fore.GREEN,
                "WARNING": Fore.MAGENTA,
                "ERROR": Fore.RED,
                "CRITICAL": Fore.RED
            }

            class ColorStreamHandler(logging.StreamHandler):

                def emit(self, record):
                    record.levelcolor = COLOR_DICT.get(record.levelname, "")
                    logging.StreamHandler.emit(self, record)

            LOG.setLevel(logging.INFO)
            ch = ColorStreamHandler()
            ch.setLevel(logging.INFO)
            color_format = logging.Formatter("%(levelcolor)s%(levelname)s" +
                                             Fore.RESET +
                                             ":%(name)s:%(message)s")
            ch.setFormatter(color_format)
            LOG.addHandler(ch)
        except:
            logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    try:
        parser = create_parser()
        args = parser.parse_args()
        validate_args(args)

        setup_working_dir(args.working_dir, args.rec_file, args.lig_file)

        args.working_dir = os.path.abspath(args.working_dir)
        os.chdir(args.working_dir)  # Rest of script assumes we always start in working_dir

        handler = logging.FileHandler('logs/docking.log')
        LOG.addHandler(handler)

        rec, lig = prepare_pdbs(args)
        run_piper(args, rec, lig)

        if args.others_mode:
            # TODO: Merge ft.{000..002}.00 into ft.003.00, run pwrmsd on that
            pass

        cluster_ftresults(args, rec, lig)

        if args.minimize_clusters:
            minimize_clusters(args)

    except KeyboardInterrupt:
        LOG.error("Program interrupted")
    finally:
        logging.shutdown()

    return 0

if __name__ == "__main__":
    sys.exit(main())
