#!/usr/bin/env python3

from sklearn.cluster import DBSCAN
import sys
import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging
import glob

__author__ = 'Devansh Agarwal'
__email__ = 'da0017@mix.wvu.edu'


parser = ArgumentParser(description='Perform dbscan clustering of heimdall cands. Usage heimdbs.py 2*cand',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Be verbose')
parser.add_argument('-t', '--tdist', type=int, help='Sample distance', default=256)
parser.add_argument('-d', '--ddist', type=int, help='Idt distance', default=20)
parser.add_argument('-p', '--plot', action='store_true', help='Show plots', default=False)
parser.add_argument('-w', '--wmax', type=int, help='Maxium width (in number of samples) to consider', default=4096)
parser.add_argument('-m', '--minsamp', type=int, help='Minimum samples in cluster (Use -m 1 for friends of friends)',
                    default=2)
parser.add_argument('-s', '--snmin', type=float, help='Minimum S/N to conside', default=8.)
parser.add_argument('--dmmin', type=float, help='Minimum DM to consider (pc/cm3)', default=0.)
#parser.add_argument('--memmin', type=int, help='Minimum Members to consider', default=1)
parser.add_argument('--njobs', type=int, help='The number of parallel jobs to run (-1 for all cores)', default=1)
parser.add_argument(dest='files', nargs="+", help="eg 2018*cands")
parser.set_defaults(verbose=False)
values = parser.parse_args()
if values.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

cand_file = values.files
tsamp_cluster_size = values.tdist
dm_cluster_size = values.ddist
min_samples = values.minsamp
plot_cand = values.plot
sn_min = values.snmin
width_max = int(round(np.log2(values.wmax)))
dm_min = values.dmmin
n_jobs = values.njobs
#min_mem = values.memmin

# load candidates
arrays = [np.loadtxt(f, comments="#") for f in cand_file]
all_cands = np.concatenate(arrays)

cand_nos = all_cands.shape[0]

if values.verbose:
    logging.debug('loaded %d candidates', cand_nos)

if cand_nos == 0:
    logging.info('%s is empty', cand_file)
    sys.exit(0)

# only take those candidates where number of memebers are >=1
#all_cands = all_cands[all_cands[:, 6] >= min_mem, :]

#if values.verbose:
#    logging.debug('%d candiates with members > %d', all_cands.shape[0], min_mem)

#if all_cands.shape[0] == 0:
#    logging.info('No candidates with > %d members', min_mem)
#    sys.exit(0)

# take time samples and dm index values

if plot_cand:
    if values.verbose:
        logging.info('Initating plotting')
    import matplotlib.pyplot as plt

    plt.figure(figsize=(15, 10))
    plt.xlabel("Time (s)")
    plt.ylabel("DM")
    a = plt.scatter(all_cands[:, 2], (all_cands[:, 0]), s=10 * all_cands[:, 1], facecolors='none', edgecolor='k',
                    alpha=0.15, marker='.')

data = np.array((all_cands[:, 5], all_cands[:, 4]), dtype=np.float32).T

# rescale before clustering

if values.verbose:
    logging.info('rescaling clusters')

data[:, 0] /= tsamp_cluster_size
data[:, 1] /= dm_cluster_size

# dbs!

if values.verbose:
    logging.info('running DBSCAN with %d min. samples, %d jobs', min_samples, n_jobs)
db = DBSCAN(eps=np.sqrt(2), min_samples=min_samples, n_jobs=n_jobs).fit(data)

# get the clusters!
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
core_samples_mask = np.zeros_like(labels, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
logging.info('Reduced from %d to %d candidates', cand_nos, n_clusters_)
# that's our output file
outfile = cand_file[0] + '.dbs'

with open(outfile, 'w') as file:
    file.write(('#snr,sample,time,logwidth,idt,dm,ncand\n'))
    for k in set(labels):
        # for each cluster, put data in xy
        class_member_mask = (labels == k)
        cluster_mask = class_member_mask & core_samples_mask
        # if not noise, make replace the cluster with candidate of max S/N.
        if k >= 0:
            snr_max_arg = np.argmax(all_cands[cluster_mask][:, 1])  # .T)
            cand = all_cands[cluster_mask][snr_max_arg]
            if plot_cand:
                b = plt.plot(all_cands[:, 2][cluster_mask], (all_cands[:, 0][cluster_mask]), 'g*-', alpha=0.5)
#            if cand[1] >= sn_min and cand[3] <= width_max and cand[0] >= dm_min:
            file.write('{:f},{:d},{:f},{:d},{:d},{:f},{:d}\n'.format(cand[1], int(cand[5]), cand[2], int(cand[3]), int(cand[4]), cand[0], cluster_mask.sum()))
            if plot_cand:
                c = plt.scatter(cand[2], (cand[0]), s=10 * cand[1], facecolors='none', edgecolor='r', alpha=1, marker='o')

if plot_cand:
    plt.legend([a, b, c], ['All', 'Cluster Members', 'Cluster Head'])
    plt.savefig(cand_file[0] + '.png', bbox_inches='tight')
    plt.show()

