import style
style.setup()

from matplotlib.patches import Polygon
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from matplotlib import ticker
from glob import glob
import tables as tb
import pycurb.analysis as pa
from scipy import stats
import itertools as it
import itertools
from scipy import optimize

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']
markers = itertools.cycle('o^*')
from cycler import cycler

cc = itertools.cycle(plt.cm.spectral(np.linspace(0,1,10)))
#plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def get_omg(w, r):
    gamma = np.arccos(w/2.)
    hc = 0.5*np.tan(np.pi/3.)
    hr = np.tan(gamma)*0.5

    d = (hc - hr)*(0.5 - r)/hc

    beta = np.arctan(hr/(0.5 - d))
    return 2*np.cos(beta)


def get_amp(series):
    n = len(series)/4
    data = series[3*n:]
    A = 0.5*(np.max(data)-np.min(data))
    return A

def main():
    dpath = '/home/upgp/jruebsam/simulations/mai16/week2/move_border'
    rs = np.linspace(0, 0.5, 5)[::-1]
    cdir = os.getcwd()

    f, axes = plt.subplots(len(rs), 2, figsize=style.figsize(1., np.sqrt(2)*0.9),
                            gridspec_kw = {'width_ratios':[3, 1]})
    # build a rectangle in axes coords
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width + 0.5
    top = bottom + height

    l =  0.5*np.tan(np.pi/3.)
    for ax, radius in zip(axes[:, 1], rs):
        r = radius
        hc = 0.5*np.tan(np.pi/3.)
        p00 = (0.5-r, 0)
        p01 = (0.5+r, 0)
        p11 = (1,hc)
        p10 = (0, hc)
        po2= (1, 1)
        po = (0, 1)
        cube_lines = [p00, p01, p11, po2, po, p10]
        x = [p[0] for p in cube_lines]
        y = [p[1] for p in cube_lines]
        d = np.column_stack((x,y))
        p = Polygon(d, alpha=0.5, color='b', hatch='x')
        ax.add_artist(p)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xlabel('x', labelpad = 0.1)
        ax.set_ylabel('z', labelpad = 0.1)
        ax.set_aspect('equal')
        ax.text(right, 0.5*(bottom+top), 'r=%.3f' % (radius),
                horizontalalignment='center',
                verticalalignment='center',
                rotation='vertical',
                transform=ax.transAxes)


    for i, (ax, radius) in enumerate(zip(axes[:, 0], rs[::-1])):

        os.chdir(os.path.join(dpath, 'data', 'wall_%.3f' % radius))

        simpathes =  glob('*/*.ekin')

        omgs = sorted([float((x.split('/')[0]).split('_')[-1]) for x in simpathes])

        a_ekin, a_vz, a_vphi = [], [], []
        omgsn = []

        for j, simpath in enumerate(sorted(simpathes)):
            #print simpath
            data = np.genfromtxt(simpath)
            time = data[:, 0]
            ekin = data[:, 1]
            vz   = data[:, -3]
            vphi = data[:, -1]
            #ax.plot(time, vz, label=simpath)
            #a_ekin.append(get_amp(ekin))

            amp = get_amp(vz)
            #a_vphi.append(get_amp(vphi))

            #plt.plot(time, vz, label=simpath.split('/')[-1])
            a_vz.append(amp)
            omgsn.append(omgs[j])

        if i>0:
            ax.plot(omgsn, a_vz, 'o-',  ms=3, mew=0, alpha=0.8)
        else:
            ax.plot(omgsn, a_vz, 'o-',  ms=3, mew=0, alpha=0.8, label='Spectrum')


        if i>0:
            ax.axvline(2*np.cos(np.pi/2. -np.arctan(radius/l)), color='#e41a1c', lw=0.75)
        else:
            ax.axvline(2*np.cos(np.pi/2. -np.arctan(radius/l)), color='#e41a1c',
                        lw=0.75, label=r' $\omega_c$')

        ax.set_ylabel(radius)
        os.chdir(cdir)

        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-2,-3))
        ax.yaxis.set_major_formatter(formatter)

        ax.set_ylabel(r'$A\left(\left<v_z^2\right>\right)$')
        ax.grid(True)
        ax.set_ylim(0, 1e-3)
        ax.set_xlim(0.2, 2)


    for i, ax in enumerate(axes[:, 1]):
        if i == 0:
            ax.set_title('Setup')

    for i, ax in enumerate(axes[:, 0]):
        if i == 0:
            pass
            #ax.set_title('(a) Spectrum')
        if i < 4:
            labels = [item.get_text() for item in ax.get_xticklabels()]
            empty_string_labels = ['']*len(labels)
            ax.set_xticklabels(empty_string_labels)
        else:
            ax.set_xlabel(r'$\omega$')

    plt.sca(axes[0, 0])
    plt.legend(ncol = 3, fontsize=9, loc='upper center', bbox_to_anchor=(0.5, 1.4),
           fancybox=True, shadow=True)

    plt.subplots_adjust(bottom =0.05, top =0.9)

    plt.savefig('transition.pdf')
    #plt.show()

if __name__=='__main__':
    main()
