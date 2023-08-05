import numpy as np
from matplotlib import pyplot as plt
import pyspike as spk
import pyspike.directionality


st1 = spk.generate_poisson_spikes(1.0, [0, 100])
st2 = spk.generate_poisson_spikes(1.0, [0, 100])

a = spk.directionality.spike_delay_asymmetry(st1, st2)

print a

M = 20

spike_trains = [spk.generate_poisson_spikes(1.0, [0, 100]) for m in xrange(M)]

D = spk.directionality.spike_delay_asymmetry_matrix(spike_trains)

plt.imshow(D)
plt.show()
