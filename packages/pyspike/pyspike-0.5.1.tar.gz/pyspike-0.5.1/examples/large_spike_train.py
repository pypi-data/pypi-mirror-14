""" Compute distances of large sets of spike trains for performance tests
"""

from __future__ import print_function

import pyspike as spk
from datetime import datetime
import cProfile

r = 1.0    # rate of Poisson spike times
T = 1E6    # length of spike trains

print("Spike trains with %d spikes" % (int(r*T)))

t_start = datetime.now()
spike_train1 = spk.generate_poisson_spikes(r, T)
spike_train2 = spk.generate_poisson_spikes(r, T)
t_end = datetime.now()
runtime = (t_end-t_start).total_seconds()

print("Spike generation runtime: %.3fs" % runtime)

cProfile.run('for i in xrange(100): \
spk.spike_distance(spike_train1, spike_train2)')
