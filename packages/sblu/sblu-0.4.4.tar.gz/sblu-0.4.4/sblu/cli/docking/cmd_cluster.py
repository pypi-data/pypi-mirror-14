import click
import numpy as np
import json as _json

from sblu.cli import pass_context


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


@click.command("cluster", short_help="Cluster PIPER results.")
@click.argument("pwrmsds")
@click.option('-r', "--radius", default=9.0, type=click.FLOAT)
@click.option('-s', "--min-cluster-size", default=10, type=click.INT)
@click.option('-l', "--max-clusters", default=50, type=click.INT)
@click.option('-o', "--output", type=click.File(mode='w'),
              default=click.open_file('-', 'w'))
@click.option('--json/--no-json', default=False)
@pass_context
def cli(ctx, pwrmsds, radius, min_cluster_size, max_clusters,
        output, json):
    pwrmsds = np.loadtxt(pwrmsds)
    pwrmsds = pwrmsds.reshape(np.sqrt(len(pwrmsds)), -1)
    assert pwrmsds.shape[0] == pwrmsds.shape[1]

    clusters = cluster(pwrmsds, radius, min_cluster_size, max_clusters)

    if json:
        data = {
            "radius": args.radius,
            "min_cluster_size": args.min_cluster_size,
            "max_clusters": args.max_clusters,
            "clusters": [
                {"center": center, "members": members}
                    for center, members in clusters
            ]
        }
        _json.dump(data, output)
    else:
        print("Radius\t{:f}".format(radius), file=output)
        for cluster_center, members in clusters:
            print("Center {}".format(cluster_center+1), file=output)
            for member in members:
                print(member+1, file=output)
