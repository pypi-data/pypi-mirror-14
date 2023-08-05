from __future__ import print_function

import pyspike as spk
from pyspike import SpikeTrain


def print_distances(st1, st2):
    print("Spike train 1:", st1.spikes)
    print("Spike train 2:", st2.spikes)
    print("ISI-distance: %.16f" % spk.isi_distance(st1, st2))
    print("Spike-distance: %.16f" % spk.spike_distance(st1, st2))
    print("Spike-Sync: %.16f" % spk.spike_sync(st1, st2))
    print()


print("Spike train interval: [0.0, 1.0]")
print()

print_distances(SpikeTrain([], edges=(0.0, 1.0)),
                SpikeTrain([], edges=(0.0, 1.0)))

print_distances(SpikeTrain([], edges=(0.0, 1.0)),
                SpikeTrain([0.4, ], edges=(0.0, 1.0)))

print_distances(SpikeTrain([0.6, ], edges=(0.0, 1.0)),
                SpikeTrain([0.4, ], edges=(0.0, 1.0)))

print_distances(SpikeTrain([0.2, ], edges=(0.0, 1.0)),
                SpikeTrain([0.8, ], edges=(0.0, 1.0)))
