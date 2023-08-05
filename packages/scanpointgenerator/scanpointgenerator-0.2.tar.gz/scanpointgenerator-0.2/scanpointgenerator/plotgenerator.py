MARKER_SIZE = 10


def plot_generator(gen):
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import interpolate

    # points for spline generation
    x, y = [], []
    # capture points and indexes
    capx, capy, capi = [], [], []
    # segment start for colour changing
    starts = []
    for point in gen.iterator():
        # If lower is different from last then include it
        xlower = point.lower["x"]
        ylower = point.lower.get("y", 0)
        if len(x) == 0 or x[-1] != xlower or y[-1] != ylower:
            if len(x) != 0:
                # add in a tiny fractional distance
                xneg = x[-1] - xlower > 0
                yneg = y[-1] - ylower > 0
                xdiff = (x[-1] - x[-2]) * 0.01
                ydiff = (y[-1] - y[-2]) * 0.01
                for i in range(3):
                    x.append(x[-1] + xdiff)
                    y.append(y[-1] + ydiff)
                # add the padding on the input
                if xneg:
                    xdiff *= -1
                if yneg:
                    ydiff *= -1
                for i in reversed(range(3)):
                    x.append(xlower + xdiff * (i + 1))
                    y.append(ylower + ydiff * (i + 1))
            starts.append(len(x))
            x.append(xlower)
            y.append(ylower)
        # Add in capture points
        xpos = point.positions["x"]
        ypos = point.positions.get("y", 0)
        x.append(xpos)
        y.append(ypos)
        capx.append(xpos)
        capy.append(ypos)
        capi.append(point.indexes)
        # And upper point
        starts.append(len(x))
        x.append(point.upper["x"])
        y.append(point.upper.get("y", 0))

    # Define curves parametrically
    x = np.array(x)
    y = np.array(y)
    t = np.zeros(len(x))
    t[1:] = np.sqrt((x[1:] - x[:-1])**2 + (y[1:] - y[:-1])**2)
    t = np.cumsum(t)
    t /= t[-1]
    tck, _ = interpolate.splprep([x, y], s=0)

    # Plot each line
    for i, start in enumerate(starts):
        if i + 1 < len(starts):
            end = starts[i+1]
        else:
            end = len(x) - 1
        tnew = np.linspace(t[start], t[end], num=1001, endpoint=True)
        sx, sy = interpolate.splev(tnew, tck)
        plt.plot(sx, sy, linewidth=2)

    # And the capture points
    plt.plot(capx, capy, linestyle="", marker="x", color="k",
             markersize=MARKER_SIZE)

    # And a start position
    plt.plot([x[0]], [y[0]], 'o')
    plt.annotate("Start", (x[0], y[0]), xytext=(MARKER_SIZE/2, MARKER_SIZE/2),
                 textcoords='offset points')

    # And the indexes
    for i, x, y in zip(capi, capx, capy):
        plt.annotate(i, (x, y), xytext=(MARKER_SIZE/2, MARKER_SIZE/2),
                     textcoords='offset points')

    plt.show()
