# -*- coding: utf-8 -*-
#
import math
import numpy


def show(scheme):
    from matplotlib import pyplot as plt
    ax = plt.gca()
    # change default range so that new circles will work
    plt.axis('equal')
    ax.set_xlim((-1.5, 1.5))
    ax.set_ylim((-1.5, 1.5))

    circle1 = plt.Circle((0, 0), 1, color='k', fill=False)
    ax.add_artist(circle1)

    for tp, weight in zip(scheme.points, scheme.weights):
        color = 'b' if weight >= 0 else 'r'
        # highlight circle center
        plt.plot([tp[0]], [tp[1]], '.' + color)
        # choose radius such that sum(pi * radius**2) = pi
        radius = numpy.sqrt(abs(weight)/sum(scheme.weights))
        circ = plt.Circle((tp[0], tp[1]), radius, color=color, alpha=0.5)
        ax.add_artist(circ)
    return


def integrate(f, scheme):
    x = scheme.points.T
    return math.fsum(scheme.weights * f(x).T)


class Peirce(object):
    '''
    W.H. Peirce,
    Numerical integration over the planer annulus,
    J. Soc. Indust. Appl. Math.,
    Vol. 5, No. 2, June, 1957.
    '''
    def __init__(self, m):
        k = 4*m + 3
        self.degree = k
        theta = 2*numpy.pi * numpy.arange(1, k+2) / (k+1)
        p, w = numpy.polynomial.legendre.leggauss(m+1)
        # scale points to [r0, r1] (where r0 = 0, r1 = 1 for now)
        p = numpy.sqrt(0.5*(p + 1.0))
        p_theta = numpy.dstack(numpy.meshgrid(p, theta)).reshape(-1, 2).T
        self.points = numpy.column_stack([
            p_theta[0] * numpy.cos(p_theta[1]),
            p_theta[0] * numpy.sin(p_theta[1]),
            ])

        # When integrating between 0 and 1, the weights are exactly the
        # Gauss-Legendre weights, scaled according to the circle area.
        self.weights = numpy.tile(0.5 * numpy.pi / (k+1) * w, k+1)
        return


class Lether(object):
    '''
    Frank G. Lether,
    A Generalized Product Rule for the Circle,
    SIAM Journal on Numerical Analysis,
    Vol. 8, No. 2 (Jun., 1971), pp. 249-253,
    <http://www.jstor.org/stable/2949473>.
    '''
    def __init__(self, n):
        p, w = numpy.polynomial.legendre.leggauss(n)

        mu = numpy.arange(1, n+1)
        self.points = numpy.column_stack([
            numpy.tile(numpy.cos(mu * numpy.pi / (n+1)), n),
            numpy.outer(p, numpy.sin(mu * numpy.pi / (n+1))).flatten(),
            ])

        self.weights = numpy.pi/(n+1) \
            * numpy.outer(w, numpy.sin(mu*numpy.pi/(n+1))**2).flatten()

        self.degree = 2*n - 1
        return