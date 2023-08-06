import numpy as np

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.artist import setp
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import colors, cm


def plot_correlation(hist, title="Hit correlation", xlabel=None, ylabel=None, filename=None):
    fig = Figure()
    FigureCanvas(fig)
    ax = fig.add_subplot(1, 1, 1)
    cmap = cm.get_cmap('cool')
    extent = [hist[2][0] - 0.5, hist[2][-1] + 0.5, hist[1][-1] + 0.5, hist[1][0] - 0.5]
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    im = ax.imshow(hist[0], extent=extent, cmap=cmap, interpolation='nearest')
    ax.invert_yaxis()
    # add colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    z_max = np.max(hist[0])
    bounds = np.linspace(start=0, stop=z_max, num=255, endpoint=True)
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig.colorbar(im, boundaries=bounds, cmap=cmap, norm=norm, ticks=np.linspace(start=0, stop=z_max, num=9, endpoint=True), cax=cax)
    if not filename:
        fig.show()
    elif isinstance(filename, PdfPages):
        filename.savefig(fig)
    else:
        fig.savefig(filename)


def cartesian(arrays, out=None):  # http://stackoverflow.com/questions/1208118/using-numpy-to-build-an-array-of-all-combinations-of-two-arrays
    """
    Generate dut_one cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(dut_one_hits_x_combinations) for dut_one_hits_x_combinations in arrays]
    dtype = arrays[0].dtype

    n = np.prod([dut_one_hits_x_combinations.size for dut_one_hits_x_combinations in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:, 0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m, 1:])
        for j in xrange(1, arrays[0].size):
            out[j * m:(j + 1) * m, 1:] = out[0:m, 1:]
    return out

# Fake data
dut_one = np.zeros(shape=(100, 100))
for i in range(dut_one.shape[0]):
    dut_one[i, i] = i + 1
# dut_one = np.array([[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]])  #np.random.randint(0, 10, 10 * 10).reshape((10, 10))
dut_two = dut_one

# Hit position info from 2D position histogram
dut_one_hits_x = np.where(dut_one > 8)[0]
dut_two_hits_x = np.where(dut_two > 8)[0]
dut_one_hits_y = np.where(dut_one > 8)[1]
dut_two_hits_y = np.where(dut_two > 8)[1]


def get_cartesian_combinations(array_one, array_two):
    ''' Creates all combinations of elements in array one against elements in array two.
    Parameters: array_one, array_two: array_like, 1 dimension
    e.g.: array_one = [1, 2, 3]; array_two = [4, 5, 6]
          result: [1, 2, 3, 1, 2, 3, 1, 2, 3], [4, 5, 6, 6, 4, 5, 5, 6, 4]
          '''
    array_one_comb = np.tile(array_one, array_two.shape[0])
    array_two_comb = np.tile(array_two, array_two.shape[0])

    array_two_comb_reshaped = array_two_comb.reshape(array_two_comb.shape[0] / array_two.shape[0], array_two.shape[0])
    for shifts in range(array_two_comb_reshaped.shape[1]):  # Shift each tile by shift vector [0, 1, 2, array_two_comb_reshaped.shape[1]]
        array_two_comb_reshaped[shifts] = np.roll(array_two_comb_reshaped[shifts], shifts)

    return array_one_comb, array_two_comb_reshaped.reshape(array_two_comb.shape)


# array_one = np.array([1, 2, 3])
# array_two = np.array([4, 5, 6])

# print get_cartesian_combinations(array_one, array_two)

combinations_x = get_cartesian_combinations(dut_one_hits_x, dut_two_hits_x)
combinations_y = get_cartesian_combinations(dut_one_hits_y, dut_two_hits_y)


print dut_one_hits_x
print combinations_x[0]
print combinations_x[1]

print np.amax(dut_one)

H, xedges, yedges = np.histogram2d(combinations_x[0], combinations_x[1], bins=[100, 100])#, range=([0, np.amax(dut_one[0])], [0, np.amax(dut_two[0])]))

print H

plt.imshow(H.T, origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], interpolation='nearest', aspect='auto')
plt.colorbar()
plt.show()

# im = plt.imshow(x_correlation.astype(np.int), cmap='hot')

# print dut_one_hits_x, dut_two_hits_x, dut_one_hits_x.shape
# print combinations_x, combinations_x[0].shape
#
# print dut_one_hits_x_combinations.shape
# print dut_two_hits_x_combination.shape
# print dut_one_hits_x_combinations
#
#
# plt.plot()
