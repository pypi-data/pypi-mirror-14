""" Determine calibration values for data

This module can be used to determine calibration values from data.

Determine timing offsets for detectors and stations to correct arrival times.
Determine the PMT response curve to correct the detected number of MIPs.

"""
from ..utils import gauss

from numpy import (arange, histogram, percentile, linspace, std, nan, isnan,
                   sqrt, abs, sum, power)
from scipy.optimize import curve_fit
from sapphire.utils import round_in_base


def determine_detector_timing_offsets(events, station=None):
    """Determine the timing offsets between station detectors.

    :param events: events table of processed events.
    :param station: :class:`~sapphire.clusters.Station` object, to determine
        number of detectors and relative altitudes.
    :return: list of detector offsets.

    """
    offsets = [nan, nan, nan, nan]
    if not events.nrows:
        return offsets

    t = []
    filters = []
    if station is not None:
        n_detectors = len(station.detectors)
        station.cluster.set_timestamp(events[0]['timestamp'])
        z = [d.get_coordinates()[2] for d in station.detectors]
    else:
        n_detectors = 4
        z = [0., 0., 0., 0.]

    for id in range(n_detectors):
        t.append(events.col('t%d' % (id + 1)))
        filters.append((events.col('n%d' % (id + 1)) > .3) & (t[id] >= 0.))

    if n_detectors == 2:
        ref_id = 1
    else:
        ref_id = determine_best_reference(filters)

    for id in range(n_detectors):
        if id == ref_id:
            offsets[id] = 0.
            continue
        dt = (t[id] - t[ref_id]).compress(filters[id] & filters[ref_id])
        dz = z[id] - z[ref_id]
        offsets[id], _ = determine_detector_timing_offset(dt, dz)

    # If all except reference are nan, make reference nan.
    if sum(isnan(offsets)) == 3:
        offsets = [nan, nan, nan, nan]

    # Try to make detector 2 the reference point, if it is not nan.
    if not isnan(offsets[1]):
        ref = offsets[1]
        offsets = [o - ref for o in offsets]

    return offsets


def determine_detector_timing_offset(dt, dz=0):
    """Determine the timing offset between station detectors.

    :param dt: a list of time differences between detectors (t - t_ref).
    :param dz: height difference between the detector (z - z_ref).
    :return: mean of a gaussian fit to the data corrected for height.

    """
    if not len(dt):
        return nan, nan
    c = .3
    p = round_in_base(percentile(dt.compress(abs(dt) < 100), [0.5, 99.5]), 2.5)
    bins = arange(p[0] + 1.25, p[1], 2.5)
    detector_offset, rchi2 = fit_timing_offset(dt, bins)
    detector_offset += dz / c
    if abs(detector_offset) > 100:
        detector_offset = nan
    return detector_offset, rchi2


def determine_station_timing_offset(dt, dz=0):
    """Determine the timing offset between stations.

    :param dt: a list of time differences between stations (t - t_ref).
    :param dz: height difference between the stations (z - z_ref).
    :return: mean of a gaussian fit to the data corrected for height.

    """
    if not len(dt):
        return nan, nan
    c = .3
    p = percentile(dt, [0.5, 99.5])
    bins = linspace(p[0], p[1], min(int(p[1] - p[0]), 200))
    station_offset, rchi2 = fit_timing_offset(dt, bins)
    station_offset += dz / c
    if abs(station_offset) > 1000:
        return nan, nan
    return station_offset, rchi2


def fit_timing_offset(dt, bins):
    """Fit the time difference distribution.

    :param dt: a list of time differences between stations (t - t_ref).
    :param bins: bins edges to use for the histogram.
    :return: mean of a gaussian fit to the data corrected for height.

    """
    y, bins = histogram(dt, bins=bins)
    x = (bins[:-1] + bins[1:]) / 2
    sigma = sqrt(y + 1)
    try:
        popt, pcov = curve_fit(gauss, x, y, p0=(len(dt), 0., std(dt)),
                               sigma=sigma, absolute_sigma=False)
        offset = popt[1]
        y_fit = gauss(x, *popt)
        n_dof = len(x) - len(popt)
        rchi2 = sum(power((y - y_fit) / sigma, 2)) / n_dof
    except RuntimeError:
        offset, rchi2 = nan, nan
    return offset, rchi2


def determine_best_reference(filters):
    """Find which detector has most events in common with the others

    :param filters: list of filters for each detector, selecting rows
                    where that detector has data.
    :return: index for the detector that has most rows in common with
             the other detectors.

    """
    lengths = []
    ids = range(len(filters))

    for id in ids:
        idx = [j for j in ids if j != id]
        lengths.append(sum(filters[id] & (filters[idx[0]] |
                                          filters[idx[1]] | filters[idx[2]])))
    return lengths.index(max(lengths))
