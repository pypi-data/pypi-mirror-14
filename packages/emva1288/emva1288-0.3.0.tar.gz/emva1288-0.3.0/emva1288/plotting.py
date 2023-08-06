# -*- coding: utf-8 -*-
# Copyright (c) 2014 The EMVA1288 Authors. All rights reserved.
# Use of this source code is governed by a GNU GENERAL PUBLIC LICENSE that can
# be found in the LICENSE file.

"""Plot the results
This class takes a results.Results1288 object and produces all the plots
needed to create a reference datasheet of the EMVA1288 test

"""

from __future__ import print_function
# from matplotlib.figure import Figure
# from matplotlib.backend import new_figure_manager_given_figure
# import matplotlib.pyplot as plt
import numpy as np
import os

from . import routines


class Emva1288Plot(object):
    """Base class for emva plots

    The only mandatory attribute is name, the rest are for use in
    setup_figure
    """
    name = ""
    title = None
    xlabel = None
    ylabel = None
    xscale = None
    yscale = None

    def __init__(self, figure):
        self.figure = figure
        self.setup_figure()

    def setup_figure(self):
        """Simple wrapper for one plot per figure

        Takes the name, xlabel, ylabel, xscale and yscale
        for one plot case

        If more than one plot, just overwrite as you wish
        """
        ax = self.figure.add_subplot(111)
        if self.title:
            ax.set_title(self.title)
        else:
            ax.set_title(self.name)
        if self.xlabel:
            ax.set_xlabel(self.xlabel)
        if self.ylabel:
            ax.set_ylabel(self.ylabel)
        if self.xscale:
            ax.set_xscale(self.xscale)
        if self.yscale:
            ax.set_yscale(self.yscale)

        self.ax = ax

    def plot(self, test):
        raise NotImplementedError

    def set_legend(self, ax):
        '''
        Shortcut to add legend
        '''
        ax.legend(loc='best')
        legend = ax.get_legend()
        if legend is not None:
            if getattr(legend, 'draggable', False):
                legend.draggable(True)


class PlotSensitivity(Emva1288Plot):
    name = 'Sensitivity'
    xlabel = '$\mu_p$ [mean number of photons/pixel]'
    ylabel = '$\mu_y - \mu_{y.dark}$ [DN]'

    def plot(self, test):
        ax = self.ax
        ax.plot(test.temporal['u_p'],
                test.temporal['u_y'] - test.temporal['u_ydark'],
                label='Data',
                gid='%d:data' % test.id)

        ax.plot(test.temporal['u_p'],
                test.R * test.temporal['u_p'], '--',
                label='Fit',
                gid='%d:fit' % test.id)

        xi = test.temporal['u_p'][test.index_sensitivity_min]
        xf = test.temporal['u_p'][test.index_sensitivity_max]
        yi = (test.temporal['u_y'] -
              test.temporal['u_ydark'])[test.index_sensitivity_min]
        yf = (test.temporal['u_y'] -
              test.temporal['u_ydark'])[test.index_sensitivity_max]

        ax.plot((xi, xf), (yi, yf),
                label='Fit range',
                linestyle='None',
                marker='o',
                gid='%d:marker' % test.id)

        # Todo : Standard EMVA3 asks to print on graph $\mu_{y.dark}$.
        self.set_legend(ax)


class PlotUyDark(Emva1288Plot):
    '''Create $\mu_{y.dark}$ plot'''

    name = 'Mean gray value in dark'
    title = '$\mu_{y.dark}$'
    xlabel = 'exposure time [ns]'
    ylabel = '$\mu_{y.dark}$ [DN]'

    def plot(self, test):
        ax = self.ax

        if np.mean(test.temporal['texp']) == test.temporal['texp'][0]:
            ax.plot(test.temporal['texp'],
                    test.temporal['u_ydark'],
                    'o',
                    markersize=5,
                    label='Data',
                    gid='%d:data' % test.id)
        else:
            ax.plot(test.temporal['texp'],
                    test.temporal['u_ydark'],
                    label='Data',
                    gid='%d:data' % test.id)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(1, 4))
        self.set_legend(ax)


class PlotPTC(Emva1288Plot):
    '''Create Photon Transfer plot'''

    name = 'Photon Transfer'
    xlabel = '$\mu_y - \mu_{y.dark}$ [DN]'
    ylabel = '$\sigma^2_y - \sigma^2_{y.dark}$ [DN$^2$]'

    def plot(self, test):
        ax = self.ax

        X = test.temporal['u_y'] - test.temporal['u_ydark']
        Y = test.temporal['s2_y'] - test.temporal['s2_ydark']
        ax.plot(X, Y,
                label='Data',
                gid='%d:data' % test.id)

        ax.plot(X, test.K * X,
                linestyle='--',
                label='Fit',
                gid='%d:fit' % test.id)

        ax.plot((X[test.index_u_ysat], ), (Y[test.index_u_ysat], ),
                marker='o',
                linestyle='None',
                label='Saturation',
                gid='%d:marker' % test.id)

        ax.plot((X[test.index_sensitivity_min],
                 X[test.index_sensitivity_max]),
                (Y[test.index_sensitivity_min],
                 Y[test.index_sensitivity_max]),
                linestyle='None',
                marker='o',
                label='Fit range',
                gid='%d:marker' % test.id)

        # Todo : Standard EMVA3 asks to print on graph
        # $\sigma^2_{y.dark}$ and K with its one-sigma statistical
        # uncertainty.
        self.set_legend(ax)


class PlotSNR(Emva1288Plot):
    '''Create SNR plot '''

    name = 'SNR'
    xlabel = '$\mu_{p}$ [mean number of photons/pixel]'
    ylabel = 'SNR'

    def setup_figure(self):
        super(PlotSNR, self).setup_figure()
        self.ax.loglog()
        max_ideal = []
        self.max_ideal = max_ideal

    def plot(self, test):
        ax = self.ax

        X = np.arange(test.u_p_min, test.u_p_sat,
                      (test.u_p_sat - test.u_p_min) / 100.0)

        # remove the zeros on the denominator, at saturation the temporal
        # noise is zero!
        nz = np.nonzero(test.temporal['s2_y'])
        ax.plot(test.temporal['u_p'][nz],
                (test.temporal['u_y'] - test.temporal['u_ydark'])[nz] /
                np.sqrt(test.temporal['s2_y'][nz]),
                label='Data',
                gid='%d:data' % test.id)

        ax.plot(X,
                ((test.QE / 100) * X) /
                np.sqrt((test.sigma_d) ** 2 +
                        (test.s2q / (test.K) ** 2) +
                        ((test.QE / 100) * X)),
                linestyle='--',
                label='Theoretical',
                gid='%d:fit' % test.id)

        ideal = np.sqrt(X)
        self.max_ideal.append(ideal[-1])
        ax.plot((X),
                ideal,
                linestyle='--',
                label='Ideal',
                gid='%d:fit' % test.id)

        ax.axvline(test.u_p_min,
                   linestyle='--',
                   label='$\mu_{p.min} = %.1f[p]$' % test.u_p_min,
                   gid='%d:marker' % test.id)

        ax.axvline(test.u_p_sat,
                   linestyle='--',
                   label='$\mu_{p.sat} = %.1f[p]$' % test.u_p_sat,
                   gid='%d:marker' % test.id)

        ax.plot(X,
                ((test.QE / 100) * X) /
                np.sqrt((test.sigma_d) ** 2 +
                        (test.s2q / (test.K) ** 2) +
                        ((test.QE / 100) * X) +
                        (test.DSNU1288 ** 2) +
                        (((test.PRNU1288 / 100) *
                          (test.QE / 100.) * X) ** 2)),
                linestyle='--',
                label='Total SNR',
                gid='%d:fit' % test.id)

        ax.set_ylim(1, max(self.max_ideal))
        self.set_legend(ax)


class PlotLinearity(Emva1288Plot):
    '''Create Linearity plot'''

    name = 'Linearity'
    xlabel = '$\mu_{p}$ [mean number of photons/pixel]'
    ylabel = '$\mu_y - \mu_{y.dark}$ [DN]'

    def plot(self, test):
        ax = self.ax

        X = test.temporal['u_p']
        Y = test.temporal['u_y'] - test.temporal['u_ydark']
        ax.plot(X, Y,
                label='Data',
                gid='%d:data' % test.id)

        ax.plot(X,
                test.linearity()['fit_slope'] *
                X + test.linearity()['fit_offset'],
                linestyle='--',
                label='Fit',
                gid='%d:fit' % test.id)

        ax.plot((X[test.index_linearity_min], X[test.index_linearity_max]),
                (Y[test.index_linearity_min], Y[test.index_linearity_max]),
                label='Fit range',
                linestyle='None',
                marker='o',
                gid='%d:marker' % test.id)

        self.set_legend(ax)


class PlotDeviationLinearity(Emva1288Plot):
    '''Create Deviation Linearity plot'''

    name = 'Deviation linearity'
    xlabel = '$\mu_{p}$ [mean number of photons/pixel]'
    ylabel = 'Linearity error LE [%]'

    def plot(self, test):
        ax = self.ax

        X = test.temporal['u_p'][test.index_linearity_min:
                                 test.index_linearity_max]
        deviation = test.linearity()['relative_deviation']
        Y = deviation[test.index_linearity_min: test.index_linearity_max]
        ax.plot(X, Y,
                label='Data',
                gid='%d:data' % test.id)

        ax.plot((X[0], X[-1]),
                (Y[0], Y[-1]),
                label='Fit range',
                linestyle='None',
                marker='o',
                gid='%d:marker' % test.id)

        self.set_legend(ax)


class PlotHorizontalSpectrogramPRNU(Emva1288Plot):
    '''Create Horizontal spectrogram PRNU plot'''

    name = 'Horizontal spectrogram PRNU'
    xlabel = 'cycles [periods/pixel]'
    ylabel = 'Standard deviation and\nrelative presence of each cycle [DN]'
    yscale = 'log'

    def plot(self, test):
        ax = self.ax

        # In Release 3.2, there is no subtraction of the residue.
        spectrogram = routines.FFT1288(test.spatial['avg'][0] -
                                       test.spatial['avg_dark'][0])

        ax.plot(routines.GetFrecs(spectrogram[:(np.shape(spectrogram)[0] //
                                                2)]),
                (np.sqrt(spectrogram[:(np.shape(spectrogram)[0] // 2)])),
                label='Data',
                gid='%d:data' % test.id)

        ax.axhline(test.PRNU1288,
                   label='$PRNU_{1288}$',
                   linestyle='--',
                   color='r',
                   gid='%d:marker' % test.id)

        ax.axhline(np.sqrt(test.sigma_2_y_stack),
                   label='$\sigma^2_{y.stack}$',
                   linestyle='--',
                   color='g',
                   gid='%d:marker' % test.id)

        # TODO: Standard EMVA3 asks to print on graph s_w and F.
        self.set_legend(ax)


class PlotHorizontalSpectrogramDSNU(Emva1288Plot):
    '''Create Horizontal spectrogram DSNU plot'''

    name = 'Horizontal spectrogram DSNU'
    xlabel = 'cycles [periods/pixel]'
    ylabel = 'Standard deviation and\nrelative presence of each cycle [DN]'
    yscale = 'log'

    def plot(self, test):
        ax = self.ax

        spectrogram = routines.FFT1288(test.spatial['avg_dark'][0])
        ax.plot(routines.GetFrecs(spectrogram[:(np.shape(spectrogram)[0] //
                                                2)]),
                np.sqrt(spectrogram[:(np.shape(spectrogram)[0] // 2)]),
                label='Data',
                gid='%d:data' % test.id)

        ax.axhline(np.sqrt(test.sigma_2_y_stack_dark),
                   label='$\sigma^2_{y.stack.dark}$',
                   linestyle='--',
                   color='g',
                   gid='%d:marker' % test.id)

        ax.axhline(test.DSNU1288_DN(),
                   label='$DSNU_{1288.DN}$',
                   linestyle='--',
                   color='r',
                   gid='%d:marker' % test.id)

        self.set_legend(ax)


class PlotVerticalSpectrogramPRNU(Emva1288Plot):
    '''Create Vertical spectrogram PRNU plot'''

    name = 'Vertical spectrogram PRNU'
    xlabel = 'cycles [periods/pixel]'
    ylabel = 'Standard deviation and\nrelative presence of each cycle [DN]'
    yscale = 'log'

    def plot(self, test):
        ax = self.ax

        spectrogram = routines.FFT1288(test.spatial['avg'][0] -
                                       test.spatial['avg_dark'][0],
                                       rotate=True)

        ax.plot((routines.GetFrecs(spectrogram[:(np.shape(spectrogram)[0] //
                                                 2)])),
                (np.sqrt(spectrogram[:(np.shape(spectrogram)[0] // 2)])),
                label='Data',
                gid='%d:data' % test.id)

        ax.axhline(test.PRNU1288,
                   label='$PRNU_{1288}$',
                   linestyle='--',
                   color='r',
                   gid='%d:marker' % test.id)

        ax.axhline(np.sqrt(test.sigma_2_y_stack),
                   label='$\sigma^2_{y.stack}$',
                   linestyle='--',
                   color='g',
                   gid='%d:marker' % test.id)

        self.set_legend(ax)


class PlotVerticalSpectrogramDSNU(Emva1288Plot):
    '''Create Vertical spectrogram DSNU plot'''

    name = 'Vertical spectrogram DSNU'
    xlabel = 'Cycles [periods/pixel]'
    ylabel = 'Standard deviation and\nrelative presence of each cycle [DN]'
    yscale = 'log'

    def plot(self, test):
        ax = self.ax

        spectrogram = routines.FFT1288(test.spatial['avg_dark'][0],
                                       rotate=True)
        ax.plot(routines.GetFrecs(spectrogram[:(np.shape(spectrogram)[0] //
                                                2)]),
                np.sqrt(spectrogram[:(np.shape(spectrogram)[0] // 2)]),
                label='Data',
                gid='%d:data' % test.id)

        ax.axhline(test.DSNU1288_DN(),
                   label='$DSNU_{1288.DN}$',
                   linestyle='--',
                   color='r',
                   gid='%d:marker' % test.id)

        ax.axhline(np.sqrt(test.sigma_2_y_stack_dark),
                   label='$\sigma^2_{y.stack.dark}$',
                   linestyle='--',
                   color='g',
                   gid='%d:marker' % test.id)

        self.set_legend(ax)


class PlotLogarithmicHistogramDSNU(Emva1288Plot):
    '''Create Logarithmic histogram DSNU plot'''

    name = 'Logarithmic histogram DSNU'
    xlabel = 'Deviation from the mean [DN]'
    ylabel = 'Number of pixels'
    yscale = 'log'

    def plot(self, test):
        ax = self.ax

        hist = test.histogram_DSNU

        ax.plot(hist['bins'], hist['values'],
                gid='%d:data' % test.id,
                label='Data')
        ax.plot(hist['bins'], hist['model'],
                '--',
                gid='%d:fit' % test.id,
                label='Model')

        self.set_legend(ax)

        ax.axis(ymin=1.0)


class PlotLogarithmicHistogramPRNU(Emva1288Plot):
    '''Create Logarithmic histogram PRNU plot'''

    name = 'Logarithmic histogram PRNU'
    xlabel = 'Deviation from the mean [%]'
    ylabel = 'Number of pixels'
    yscale = 'log'

    def plot(self, test):
        ax = self.ax
        hist = test.histogram_PRNU

        ax.plot(hist['bins'], hist['values'],
                gid='%d:data' % test.id,
                label='Data')
        ax.plot(hist['bins'], hist['model'], '--',
                gid='%d:fit' % test.id,
                label='Model')

        self.set_legend(ax)
        ax.axis(ymin=0.5)


class PlotAccumulatedLogHistogramDSNU(Emva1288Plot):
    '''Create Accumulated log histogram DSNU plot'''

    name = 'Accumulated log histogram DSNU'
    xlabel = 'Minimal deviation from the mean [DN]'
    ylabel = 'Percentage of pixels\ndeviating from the mean at least of : '
    yscale = 'log'

    def plot(self, test):
        ax = self.ax
        hist = test.histogram_DSNU_accumulated

        ax.plot(hist['bins'], hist['values'],
                gid='%d:data' % test.id,
                label='Data')

        self.set_legend(ax)


class PlotAccumulatedLogHistogramPRNU(Emva1288Plot):
    '''Create Accumulated log histogram PRNU plot'''

    name = 'Accumulated log histogram PRNU'
    xlabel = 'Minimal deviation from the mean [%]'
    ylabel = 'Percentage of pixels\ndeviating from the mean at least of : '
    yscale = 'log'

    def plot(self, test):
        ax = self.ax

        hist = test.histogram_PRNU_accumulated

        ax.plot(hist['bins'], hist['values'],
                gid='%d:data' % test.id,
                label='Data')

        self.set_legend(ax)


class ProfileBase(Emva1288Plot):
    def __init__(self, *args, **kwargs):
        Emva1288Plot.__init__(self, *args, **kwargs)
        # Dict to keep track of max and min values to adjust the
        # limit of the axis
        self.axis_limits = {'bright': {'max': [], 'min': [], 'length': []},
                            'dark': {'max': [], 'min': [], 'length': []}}

    def _get_extremes(self, mean_, min_, max_):
        min_min_i = np.argmax(mean_ - min_)
        min_min = min_[min_min_i]
        min_perc = np.abs(100. - (min_min * 100. / mean_[min_min_i]))
        min_label = 'Min ({:.1f} {:.1f}%)'.format(min_min,
                                                  min_perc)

        max_max_i = np.argmax(max_ - min_)
        max_max = max_[max_max_i]
        max_perc = np.abs(100. - (max_max * 100. / mean_[max_max_i]))
        max_label = 'Max ({:.1f} {:.1f}%)'.format(max_max,
                                                  max_perc)

        return {'min_deviation': min_min, 'min_precentage': min_perc,
                'min_label': min_label, 'max_label': max_label,
                'max_deviation': max_max, 'max_percentage': max_perc}

    def _get_image_profiles(self, image, transpose):
        if transpose:
            img = np.transpose(image)
        else:
            img = image
        profile = np.mean(img, axis=0)
        profile_min = np.min(img, axis=0)
        profile_max = np.max(img, axis=0)

        mid_i = np.shape(img)[0]
        profile_mid = img[mid_i // 2, :]
        length = np.shape(profile)[0]

        d = {'mean': profile,
             'min': profile_min,
             'max': profile_max,
             'length': length,
             'mid': profile_mid}
        return d

    def get_profiles(self, bright, dark, transpose):
        b_p = self._get_image_profiles(bright, transpose)
        b_mean = np.mean(b_p['mean'])
        self.axis_limits['bright']['length'].append(b_p['length'])
        self.axis_limits['bright']['min'].append(0.9 * b_mean)
        self.axis_limits['bright']['max'].append(1.1 * b_mean)

        d_p = self._get_image_profiles(dark, transpose)
        self.axis_limits['dark']['length'].append(d_p['length'])
        self.axis_limits['dark']['min'].append(0.9 * np.mean(d_p['min']))
        self.axis_limits['dark']['max'].append(1.1 * np.mean(d_p['max']))

        return {'bright': b_p, 'dark': d_p}

    def reduce_ticks(self, ax, axis, n=4):
        ax.locator_params(axis=axis, nbins=n)


class PlotHorizontalProfile(ProfileBase):
    '''Create Horizontal profile plot
    Profile is done with spatial images.
    '''

    name = 'Horizontal profile'

    def setup_figure(self):
        self.ax = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)
        self.figure.suptitle(self.name)
        self.ax.set_title('PRNU')
        self.ax.set_ylabel('Vertical line [DN]')
        self.ax2.set_title('DSNU')
        self.ax2.set_xlabel('Index of the line')
        self.ax2.set_ylabel('Vertical line [DN]')

    def plot(self, test):
        ax = self.ax
        ax2 = self.ax2

        bimg = test.spatial['avg'][0] - test.spatial['avg_dark'][0]
        dimg = test.spatial['avg_dark'][0]
        profiles = self.get_profiles(bimg, dimg, False)

        x = np.arange(profiles['bright']['length'])
        lmid = ax.plot(x, profiles['bright']['mid'],
                       label='Mid',
                       gid='%d:marker' % test.id)[0]
        lmin = ax.plot(x, profiles['bright']['min'],
                       label='Min',
                       gid='%d:marker' % test.id)[0]
        lmax = ax.plot(x, profiles['bright']['max'],
                       label='Max',
                       gid='%d:marker' % test.id)[0]
        lmean = ax.plot(x, profiles['bright']['mean'],
                        label='Mean',
                        gid='%d:marker' % test.id)[0]
        ax.set_xticks([])

        x_dark = np.arange(profiles['dark']['length'])
        ax2.plot(x_dark, profiles['dark']['mid'],
                 label='Mid',
                 gid='%d:data' % test.id)
        ax2.plot(x_dark, profiles['dark']['min'],
                 label='Min',
                 gid='%d:data' % test.id)
        ax2.plot(x_dark, profiles['dark']['max'],
                 label='Max',
                 gid='%d:data' % test.id)
        ax2.plot(x_dark, profiles['dark']['mean'],
                 label='Mean',
                 gid='%d:data' % test.id)

        ax.axis(ymin=min(self.axis_limits['bright']['min']),
                ymax=max(self.axis_limits['bright']['max']),
                xmax=max(self.axis_limits['bright']['length']))
        ax2.axis(ymin=min(self.axis_limits['dark']['min']),
                 ymax=max(self.axis_limits['dark']['max']),
                 xmax=max(self.axis_limits['dark']['length']))

        self.figure.legend((lmid, lmin, lmax, lmean),
                           ('Mid', 'Min', 'Max', 'Mean'),
                           'upper right')

        self.reduce_ticks(ax2, 'y')
        self.reduce_ticks(ax, 'y')


class PlotVerticalProfile(ProfileBase):
    '''Create Vertical profile plot.
    Profile is done with spatial images.
    '''

    name = 'Vertical profile'

    def setup_figure(self):
        self.ax = self.figure.add_subplot(121)
        self.ax2 = self.figure.add_subplot(122)
        self.figure.suptitle(self.name)
        self.ax.set_title('DSNU')
        self.ax.set_xlabel('Vertical line [DN]')
        self.ax.set_ylabel('Index of the line')
        self.ax2.set_title('PRNU')
        self.ax2.set_xlabel('Vertical line [DN]')

    def plot(self, test):
        ax = self.ax
        ax2 = self.ax2

        bimg = test.spatial['avg'][0] - test.spatial['avg_dark'][0]
        dimg = test.spatial['avg_dark'][0]
        profiles = self.get_profiles(bimg, dimg, True)

        y = np.arange(profiles['bright']['length'])
        lmid = ax2.plot(profiles['bright']['mid'], y,
                        label='Mid',
                        gid='%d:marker' % test.id)[0]
        lmin = ax2.plot(profiles['bright']['min'], y,
                        label='Min',
                        gid='%d:marker' % test.id)[0]
        lmax = ax2.plot(profiles['bright']['max'], y,
                        label='Max',
                        gid='%d:marker' % test.id)[0]
        lmean = ax2.plot(profiles['bright']['mean'], y,
                         label='Mean',
                         gid='%d:marker' % test.id)[0]

        ax2.set_yticks([])

        y_dark = np.arange(profiles['dark']['length'])
        ax.plot(profiles['dark']['mid'], y_dark,
                label='Mid',
                gid='%d:marker' % test.id)
        ax.plot(profiles['dark']['min'], y_dark,
                label='Min',
                gid='%d:marker' % test.id)
        ax.plot(profiles['dark']['max'], y_dark,
                label='Max',
                gid='%d:marker' % test.id)
        ax.plot(profiles['dark']['mean'], y_dark,
                label='Mean',
                gid='%d:marker' % test.id)

        ax2.axis(xmin=min(self.axis_limits['bright']['min']),
                 xmax=max(self.axis_limits['bright']['max']),
                 ymax=max(self.axis_limits['bright']['length']))
        ax.axis(xmin=min(self.axis_limits['dark']['min']),
                xmax=max(self.axis_limits['dark']['max']),
                ymax=max(self.axis_limits['dark']['length']))

        self.figure.legend((lmid, lmin, lmax, lmean),
                           ('Mid', 'Min', 'Max', 'Mean'),
                           'upper right')

        self.reduce_ticks(ax2, 'x')
        self.reduce_ticks(ax, 'x')


EVMA1288plots = [PlotPTC,
                 PlotSNR,
                 PlotSensitivity,
                 PlotUyDark,
                 PlotLinearity,
                 PlotDeviationLinearity,
                 PlotHorizontalSpectrogramPRNU,
                 PlotHorizontalSpectrogramDSNU,
                 PlotVerticalSpectrogramPRNU,
                 PlotVerticalSpectrogramDSNU,
                 PlotLogarithmicHistogramDSNU,
                 PlotLogarithmicHistogramPRNU,
                 PlotAccumulatedLogHistogramDSNU,
                 PlotAccumulatedLogHistogramPRNU,
                 PlotHorizontalProfile,
                 PlotVerticalProfile]


class Plotting1288(object):
    def __init__(self, test):
        '''
        Creates and shows all plots necessary to prepare a camera or sensor
        descriptive report compliant with EMVA Standard 1288 version 3.1.
        '''

        if not getattr(test, 'id', False):
            test.id = id(test)
        self.test = test

    def plots_to_plot(self, *plots):
        p = []
        if not plots:
            plots = range(len(EVMA1288plots))
        for i in plots:
            if i not in range(len(EVMA1288plots)):
                print('Error ', i, 'is not valid index')
                print('Plot has to be integer in ', range(len(EVMA1288plots)))
                continue
            p.append(i)
        return p

    def plot(self, *ids):
        import matplotlib.pyplot as plt
        plots = self.plots_to_plot(*ids)
        for i in plots:
            figure = plt.figure(i)
            plot = EVMA1288plots[i](figure)
            plot.plot(self.test)
            figure.canvas.set_window_title(plot.name)
        plt.show()
