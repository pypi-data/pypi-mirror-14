import numpy as np
from scipy.spatial.distance import cdist
from path import path
from prody import parsePDB

from . import CONFIG
from .job import Job

FTMAP_LOCAL_PATH = None
if CONFIG['ftmap']['local_path'] is not None:
    FTMAP_LOCAL_PATH = path(CONFIG['ftmap']['local_path'])


class FTmapJob(Job):
    def __init__(self, jobid):
        self.jobid = jobid
        self.job_dir = FTMAP_LOCAL_PATH / str(jobid)
        self._receptor = None
        self._probes = None
        self._minimized_probes = None
        self._counts = None

    def receptor(self):
        "Get receptor AtomGroup object"
        if self._receptor is None:
            self._receptor = parsePDB(self.job_dir / "probes/rec/1rec.pdb")

        return self._receptor

    def probes(self):
        "Get list of probe names"
        if self._probes is None:
            with open(self.job_dir / "complexs", "r") as f:
                self._probes = [l.strip() for l in f]

        return self._probes

    def minimized_probes(self):
        "Get list of minimized probe AtomGroups"
        if self._minimized_probes is None:
            self._minimized_probes = [parsePDB(
                self.job_dir / "probes/cluster/{}.min.pdb".format(probe))
                                      for probe in self.probes()]

        return self._minimized_probes

    def counts(self, no_hydrogen=True):
        if self._counts is None:
            rec = self.receptor()
            minimized_probes = self.minimized_probes()

            if no_hydrogen:
                rec = rec.select("not hydrogen")
                minimized_probes = [p.select("not hydrogen")
                                    for p in minimized_probes]

        return self._counts


def brute_count(rec, minimized_probes, radius):
    rec_coords = rec.getCoords()
    counts = np.zeros((len(minimized_probes), len(rec)), dtype=np.int64)
    r_sq = radius * radius

    for i, probe in enumerate(minimized_probes):
        dists = cdist(rec_coords,
                      probe.getCoordsets().reshape(-1, 3),
                      metric='sqeuclidean')
        np.add(counts[i], (dists < r_sq).sum(axis=1), counts[i])

    return counts
