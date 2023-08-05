""" Computes the regression results and stores them in
PySpike_benchmark.txt

Copyright 2016, Mario Mulansky <mario.mulansky@gmx.net>

Distributed under the BSD License
"""
from __future__ import print_function

from scipy.io import loadmat
import pyspike as spk

from numpy.testing import assert_almost_equal

spk.disable_backend_warning = True


spike_file = "regression_random_spikes.mat"
spikes_name = "spikes"
result_name = "Distances"
result_file = "regression_random_results_cSPIKY.mat"

output_file = "PySpike_benchmark.txt"

spike_train_sets = loadmat(spike_file)[spikes_name][0]
results_cSPIKY = loadmat(result_file)[result_name]

out = open(output_file, 'w')

for i, spike_train_data in enumerate(spike_train_sets):
    spike_trains = []
    for spikes in spike_train_data[0]:
        spike_trains.append(spk.SpikeTrain(spikes.flatten(), 100.0))

    isi = spk.isi_distance_multi(spike_trains)
    spike = spk.spike_distance_multi(spike_trains)
    spike_sync = spk.spike_sync_multi(spike_trains)
    # spike_sync = spk.spike_sync_profile_multi(spike_trains).avrg()

    assert_almost_equal(isi, results_cSPIKY[i][0], decimal=14,
                        err_msg="Index: %d, ISI" % i)

    assert_almost_equal(spike, results_cSPIKY[i][1], decimal=14,
                        err_msg="Index: %d, SPIKE" % i)

    out.write("%.16f\t%.16f\t%.16f\n" % (isi, spike, spike_sync))

out.close()
