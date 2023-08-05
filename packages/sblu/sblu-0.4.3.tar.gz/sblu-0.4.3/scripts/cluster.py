#!/usr/bin/env python
from __future__ import print_function
import numpy as np


def cluster(pwrmsds, cluster_radius, min_clust_size, max_clusters):
    marked = set()

    cluster_indices = [set(np.where(row <= cluster_radius)[0]) for
                       row in pwrmsds]
    cluster_centers = list()

    # Find clusters
    for _ in range(max_clusters):
        max_index = None
        max_size = 0

        for j, cluster in enumerate(cluster_indices):
            if j in marked:
                continue

            cluster_size = len(cluster)
            if cluster_size >= min_clust_size and cluster_size > max_size:
                max_index = j
                max_size = cluster_size

        if max_index is None:
            break

        cluster_centers.append(max_index)
        marked.update(cluster_indices[max_index])

    # Reclustering
    final_cluster_assignments = pwrmsds[cluster_centers].argmin(axis=0)
    cluster_members = [[] for _ in range(len(cluster_centers))]

    # Select the members which are a member of at least one cluster
    s2 = set()
    for c in cluster_centers:
        s2 = s2 | cluster_indices[c]

    # Assign those members to the correct cluster
    for i in sorted(s2):
        cluster_members[final_cluster_assignments[i]].append(i)

    return sorted(zip(cluster_centers, cluster_members),
                  key=lambda x: len(x[1]), reverse=True)


if __name__ == "__main__":
    import argparse
    import json
    import sys
    from contextlib import closing

    parser = argparse.ArgumentParser(description="Cluster ftresults")
    parser.add_argument("--radius", "-r", default=9.0, type=float)
    parser.add_argument("--min_cluster_size", "-s", default=10, type=int)
    parser.add_argument("--max_clusters", "-l", default=50, type=int)
    parser.add_argument("--output", "-o", default=None)
    parser.add_argument("--json", default=False, action="store_true")
    parser.add_argument("pwrmsds")

    args = parser.parse_args()

    if args.output is None:
        args.output = "{}.clusters".format(args.pwrmsds)
        if args.json:
            args.output += ".json"

    pwrmsds = np.loadtxt(args.pwrmsds)
    pwrmsds = pwrmsds.reshape(np.sqrt(len(pwrmsds)), -1)
    assert pwrmsds.shape[0] == pwrmsds.shape[1]

    clusters = cluster(pwrmsds, args.radius,
                       args.min_cluster_size, args.max_clusters)

    if args.output == "-":
        outf = sys.stdout
    else:
        outf = open(args.output, "w")

    with closing(outf) as out:
        if args.json:
            data = {
                "radius": args.radius,
                "min_cluster_size": args.min_cluster_size,
                "max_clusters": args.max_clusters,
                "clusters": [
                    {"center": center, "members": members}
                    for center, members in clusters
                ]
            }
            json.dump(data, out)
        else:
            print("Radius\t{:f}".format(args.radius), file=out)
            for cluster_center, members in clusters:
                print("Center {}".format(cluster_center+1), file=out)
                for member in members:
                    print(member+1, file=out)
