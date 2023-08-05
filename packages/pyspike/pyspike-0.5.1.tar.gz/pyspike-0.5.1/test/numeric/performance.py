""" performance runs

Copyright 2016, Mario Mulansky <mario.mulansky@gmx.net>

Distributed under the BSD License
"""
from __future__ import print_function

import pyspike as spk
import timeit


spk.disable_backend_warning = True


setup = """
import pyspike as spk
N = 1000
spike_trains = []
for i in xrange(N):
    spike_trains.append(spk.generate_poisson_spikes(1.0, 500.0))
print "Spike trains generated"
"""

run_isi_distance = """
isi = spk.isi_distance_multi(spike_trains)
"""

run_isi_profile = """
isi = spk.isi_profile_multi(spike_trains).avrg()
"""

run_spike_distance = """
spike = spk.spike_distance_multi(spike_trains)
"""

run_spike_profile = """
spike = spk.spike_profile_multi(spike_trains).avrg()
"""

run_spike_sync = """
spike = spk.spike_sync_multi(spike_trains)
"""

run_spike_sync_profile = """
spike = spk.spike_sync_profile_multi(spike_trains).avrg()
"""


N = 5

# timing = timeit.timeit(run_isi_distance, setup=setup, number=N) / N
# print("ISI:", timing, "sec")

# timing = timeit.timeit(run_isi_profile, setup=setup, number=N) / N
# print("ISI from prof:", timing, "sec")

# timing = timeit.timeit(run_spike_distance, setup=setup, number=N) / N
# print("SPIKE:", timing, "sec")

timing = timeit.timeit(run_spike_profile, setup=setup, number=N) / N
print("SPIKE from prof:", timing, "sec")

timing = timeit.timeit(run_spike_sync, setup=setup, number=N) / N
print("SPIKE-SYNC:", timing, "sec")

timing = timeit.timeit(run_spike_sync_profile, setup=setup, number=N) / N
print("SPIKE-SYNC from prof:", timing, "sec")
