# -*- coding: utf-8 -*-
#
# Copyright 2015 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

"""
It contains functions to predict the A/T gear shifting.
"""

from collections import OrderedDict
from itertools import chain
import numpy as np
from copy import deepcopy
from scipy.optimize import fmin
from scipy.interpolate import InterpolatedUnivariateSpline as Spline
from sklearn.tree import DecisionTreeClassifier
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import mean_absolute_error, accuracy_score
import co2mpas.dispatcher.utils as dsp_utl
from functools import partial
from ..utils import median_filter, grouper, clear_fluctuations, reject_outliers
from ..constants import *
from ..gear_box import calculate_gear_box_speeds_in
from ..wheels import calculate_wheel_power


def correct_gear_full_load(
        velocity, acceleration, gear, velocity_speed_ratios, max_engine_power,
        max_engine_speed_at_max_power, idle_engine_speed, full_load_curve,
        road_loads, vehicle_mass, min_gear):
    """
    Corrects the gear predicted according to full load curve.

    :param velocity:
        Vehicle velocity [km/h].
    :type velocity: float

    :param acceleration:
        Vehicle acceleration [m/s2].
    :type acceleration: float

    :param gear:
        Predicted vehicle gear [-].
    :type gear: int

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :param max_engine_power:
        Maximum power [kW].
    :type max_engine_power: float

    :param max_engine_speed_at_max_power:
        Rated engine speed [RPM].
    :type max_engine_speed_at_max_power: float

    :param idle_engine_speed:
        Engine speed idle median and std [RPM].
    :type idle_engine_speed: (float, float)

    :param full_load_curve:
        Vehicle full load curve.
    :type full_load_curve: Spline

    :param road_loads:
        Cycle road loads [N, N/(km/h), N/(km/h)^2].
    :type road_loads: list, tuple

    :param vehicle_mass:
        Vehicle mass [kg].
    :type vehicle_mass: float

    :return:
        A gear corrected according to full load curve.
    :rtype: int
    """

    if velocity > 100:
        return gear

    p_norm = calculate_wheel_power(
        velocity, acceleration, road_loads, vehicle_mass)
    p_norm /= max_engine_power

    r = max_engine_speed_at_max_power - idle_engine_speed[0]

    vsr = velocity_speed_ratios

    def flc(gear):
        x = (velocity / vsr[gear] - idle_engine_speed[0]) / r
        return full_load_curve(x)

    while gear > min_gear and (gear not in vsr or p_norm > flc(gear)):
        # to consider adding the reverse function in the future because the
        # n+200 rule should be applied at the engine not the GB
        # (rpm < idle_speed + 200 and 0 <= a < 0.1) or
        gear -= 1

    return gear


def basic_correct_gear(
        velocity, acceleration, gear, velocity_speed_ratios, idle_engine_speed,
        *args):
    """
    Corrects the gear predicted according to basic drive-ability rules.

    :param velocity:
        Vehicle velocity [km/h].
    :type velocity: float

    :param acceleration:
        Vehicle acceleration [m/s2].
    :type acceleration: float

    :param gear:
        Predicted vehicle gear [-].
    :type gear: int

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :param idle_engine_speed:
        Engine speed idle median and std [RPM].
    :type idle_engine_speed: (float, float)

    :return:
        A gear corrected according to basic drive-ability rules.
    :rtype: int
    """

    if gear == 0 and acceleration > 0:
        gear = min(k for k in velocity_speed_ratios if k > 0)
    elif gear > 1:
        vsr, idle = velocity_speed_ratios, idle_engine_speed[0]
        while gear > 1 and (gear not in vsr or velocity / vsr[gear] < idle):
            gear -=1
    return gear


def correct_gear_v0(
        velocity_speed_ratios, mvl, engine_max_power,
        engine_max_speed_at_max_power, idle_engine_speed, full_load_curve,
        road_loads, vehicle_mass):
    """
    Returns a function to correct the gear predicted according to
    :func:`correct_gear_mvl` and :func:`correct_gear_full_load`.

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :param mvl:
        Matrix velocity limits (upper and lower bound) [km/h].
    :type mvl: OrderedDict

    :param engine_max_power:
        Maximum power [kW].
    :type engine_max_power: float

    :param engine_max_speed_at_max_power:
        Rated engine speed [RPM].
    :type engine_max_speed_at_max_power: float

    :param idle_engine_speed:
        Engine speed idle median and std [RPM].
    :type idle_engine_speed: (float, float)

    :param full_load_curve:
        Vehicle full load curve.
    :type full_load_curve: Spline

    :param road_loads:
        Cycle road loads [N, N/(km/h), N/(km/h)^2].
    :type road_loads: list, tuple

    :param vehicle_mass:
        Vehicle mass [kg].
    :type vehicle_mass: float

    :return:
        A function to correct the predicted gear.
    :rtype: function
    """

    max_gear = max(velocity_speed_ratios)
    min_gear = min(velocity_speed_ratios)

    def correct_gear(velocity, acceleration, gear):
        g = correct_gear_mvl(
            velocity, acceleration, gear, mvl, max_gear, min_gear)

        g = correct_gear_full_load(
            velocity, acceleration, g, velocity_speed_ratios, engine_max_power,
            engine_max_speed_at_max_power, idle_engine_speed, full_load_curve,
            road_loads, vehicle_mass, min_gear)
        return basic_correct_gear(
            velocity, acceleration, g, velocity_speed_ratios, idle_engine_speed)

    return correct_gear


def correct_gear_v1(velocity_speed_ratios, mvl, idle_engine_speed):
    """
    Returns a function to correct the gear predicted according to
    :func:`correct_gear_mvl`.

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :param mvl:
        Matrix velocity limits (upper and lower bound) [km/h].
    :type mvl: OrderedDict

    :return:
        A function to correct the predicted gear.
    :rtype: function
    """

    max_gear, min_gear = max(velocity_speed_ratios), min(velocity_speed_ratios)

    def correct_gear(velocity, acceleration, gear):
        g = correct_gear_mvl(
            velocity, acceleration, gear, mvl, max_gear, min_gear)
        return basic_correct_gear(
            velocity, acceleration, g, velocity_speed_ratios, idle_engine_speed)

    return correct_gear


def correct_gear_v2(
        velocity_speed_ratios, engine_max_power, engine_max_speed_at_max_power,
        idle_engine_speed, full_load_curve, road_loads, vehicle_mass):
    """
    Returns a function to correct the gear predicted according to
    :func:`correct_gear_full_load`.

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :param engine_max_power:
        Maximum power [kW].
    :type engine_max_power: float

    :param engine_max_speed_at_max_power:
        Rated engine speed [RPM].
    :type engine_max_speed_at_max_power: float

    :param idle_engine_speed:
        Engine speed idle median and std [RPM].
    :type idle_engine_speed: (float, float)

    :param full_load_curve:
        Vehicle full load curve.
    :type full_load_curve: Spline

    :param road_loads:
        Cycle road loads [N, N/(km/h), N/(km/h)^2].
    :type road_loads: list, tuple

    :param vehicle_mass:
        Vehicle mass [kg].
    :type vehicle_mass: float

    :return:
        A function to correct the predicted gear.
    :rtype: function
    """

    min_gear = min(velocity_speed_ratios)

    def correct_gear(velocity, acceleration, gear):
        g = correct_gear_full_load(
            velocity, acceleration, gear, velocity_speed_ratios,
            engine_max_power, engine_max_speed_at_max_power, idle_engine_speed,
            full_load_curve, road_loads, vehicle_mass, min_gear)

        return basic_correct_gear(
            velocity, acceleration, g, velocity_speed_ratios, idle_engine_speed)

    return correct_gear


def correct_gear_v3(velocity_speed_ratios, idle_engine_speed):
    """
    Returns a function that does not correct the gear predicted.

    :return:
        A function to correct the predicted gear.
    :rtype: function
    """

    correct_gear = partial(basic_correct_gear,
                           velocity_speed_ratios=velocity_speed_ratios,
                           idle_engine_speed=idle_engine_speed)
    return correct_gear


def identify_gear_shifting_velocity_limits(gears, velocities):
    """
    Identifies gear shifting velocity matrix.

    :param gears:
        Gear vector [-].
    :type gears: numpy.array

    :param velocities:
        Vehicle velocity [km/h].
    :type velocities: numpy.array

    :return:
        Gear shifting velocity matrix.
    :rtype: dict
    """

    limits = {}

    for v, (g0, g1) in zip(velocities, dsp_utl.pairwise(gears)):
        if v >= VEL_EPS and g0 != g1:
            limits[g0] = limits.get(g0, [[], []])
            limits[g0][g0 < g1].append(v)

    def rjt_out(x, default):
        if x:
            x = np.asarray(x)

            # noinspection PyTypeChecker
            m, (n, s) = np.median(x), (len(x), 1 / np.std(x))

            y = 2 > (abs(x - m) * s)

            if y.any():
                y = x[y]

                # noinspection PyTypeChecker
                m, (n, s) = np.median(y), (len(y), 1 / np.std(y))

            return m, (n, s)
        else:
            return default

    max_gear = max(limits)
    gsv = OrderedDict()
    for k in range(max_gear + 1):
        v0, v1 = limits.get(k, [[], []])
        gsv[k] = [rjt_out(v0, (-1, (0, 0))), rjt_out(v1, (INF, (0, 0)))]

    return correct_gsv(gsv)


def correct_gsv_for_constant_velocities(
        gsv, up_cns_vel=(15, 32, 50, 70), up_limit=3.5, up_delta=-0.5,
        down_cns_vel=(35, 50), down_limit=3.5, down_delta=-1):
    """
    Corrects the gear shifting matrix velocity according to the NEDC velocities.

    :param gsv:
        Gear shifting velocity matrix.
    :type gsv: dict

    :return:
        A gear shifting velocity matrix corrected from NEDC velocities.
    :rtype: dict
    """

    def set_velocity(velocity, const_steps, limit, delta):
        for v in const_steps:
            if v < velocity < v + limit:
                return v + delta
        return velocity

    def fun(v):
        limits = (set_velocity(v[0], down_cns_vel, down_limit, down_delta),
                  set_velocity(v[1], up_cns_vel, up_limit, up_delta))
        return limits

    return gsv.__class__((k, fun(v)) for k, v in gsv.items())


class CMV(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(CMV, self).__init__(*args, **kwargs)
        self.velocity_speed_ratios = {}

    def fit(self, correct_gear, gears, engine_speeds_out, velocities,
            accelerations, velocity_speed_ratios):
        self.clear()
        self.velocity_speed_ratios = velocity_speed_ratios
        self.update(identify_gear_shifting_velocity_limits(gears, velocities))

        gear_id, velocity_limits = zip(*list(sorted(self.items()))[1:])

        _inf = float('inf')

        def update_gvs(vel_limits):
            self[0] = (0, vel_limits[0])

            limits = np.append(vel_limits[1:], _inf)
            self.update(dict(zip(gear_id, grouper(limits, 2))))

        def error_fun(vel_limits):
            update_gvs(vel_limits)

            g_pre = self.predict(np.array([velocities, accelerations]).T,
                                 correct_gear=correct_gear)

            speed_predicted = calculate_gear_box_speeds_in(
                g_pre, velocities, velocity_speed_ratios)

            return mean_absolute_error(engine_speeds_out, speed_predicted)

        x0 = [self[0][1]].__add__(list(chain(*velocity_limits))[:-1])

        x = fmin(error_fun, x0, disp=False)

        update_gvs(x)

        self.update(correct_gsv_for_constant_velocities(self))

        return self

    def plot(self):
        import matplotlib.pylab as plt
        for k, v in self.items():
            kv = {}
            for (s, l), x in zip((('down', '--'), ('up', '-')), v):
                if x < INF:
                    kv['label'] = 'Gear %d:%s-shift' % (k, s)
                    kv['linestyle'] = l
                    kv['color'] = plt.plot([x] * 2, [0, 1], **kv)[0]._color
        plt.legend(loc='best')
        plt.xlabel('Velocity [km/h]')

    def predict(self, X, correct_gear=lambda v, a, g: g, previous_gear=None,
                times=None):

        gear = previous_gear or min(self)

        min_gear, max_gear = min(self), max(self)

        gears = np.zeros(shape=len(X))

        for i, (velocity, acceleration) in enumerate(X):
            down, up = self[gear]

            if not down <= velocity < up:
                add = 1 if velocity >= up else -1
                while min_gear <= gear <= max_gear:
                    gear += add
                    if gear in self:
                        break
                gear = max(min_gear, min(max_gear, gear))

            g = correct_gear(velocity, acceleration, gear)

            if g in self:
                gear = g

            gears[i] = gear = max(MIN_GEAR, gear)

        if times is not None:
            gears = median_filter(times, gears, TIME_WINDOW)
            gears = clear_fluctuations(times, gears, TIME_WINDOW)

        return gears

    def convert(self, velocity_speed_ratios):
        if velocity_speed_ratios != self.velocity_speed_ratios:

            vsr, n_vsr = self.velocity_speed_ratios, velocity_speed_ratios
            it = [(vsr[k], v[0], v[1]) for k, v in self.items()]

            K, X = zip(*[(k, v) for k, v in sorted(n_vsr.items())])

            L, U = _convert_limits(it, X)

            self.clear()

            for k, l, u in sorted(zip(K, L, U), reverse=it[0][0] > it[1][0]):
                self[k] = (l, u)

            self.velocity_speed_ratios = n_vsr

        return self


def _convert_limits(it, X):
    it = sorted(it)
    x, l, u = zip(*it[1:])

    _inf = u[-1]
    x = np.asarray(x)
    l, u = np.asarray(l) / x, np.asarray(u) / x

    L = Spline(x, l, k=1)(X) * X
    U = np.append(Spline(x[:-1], u[:-1], k=1)(X[:-1]) * X[:-1], [_inf])
    L[0], U[0] = it[0][1:]

    return L, U


def calibrate_gear_shifting_cmv(
        correct_gear, gears, engine_speeds_out, velocities, accelerations,
        velocity_speed_ratios):
    """
    Calibrates a corrected matrix velocity to predict gears.

    :param gears:
        Gear vector [-].
    :type gears: numpy.array

    :param engine_speeds_out:
        Engine speed vector [RPM].
    :type engine_speeds_out: numpy.array

    :param velocities:
        Vehicle velocity [km/h].
    :type velocities: numpy.array

    :param accelerations:
        Vehicle acceleration [m/s2].
    :type accelerations: numpy.array, float

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :returns:
        A corrected matrix velocity to predict gears.
    :rtype: dict
    """

    cmv = CMV().fit(correct_gear, gears, engine_speeds_out, velocities,
                    accelerations, velocity_speed_ratios)

    return cmv


def calibrate_gear_shifting_cmv_hot_cold(
        correct_gear, times, gears, engine_speeds, velocities, accelerations,
        velocity_speed_ratios, time_cold_hot_transition):
    """
    Calibrates a corrected matrix velocity for cold and hot phases to predict
    gears.

    :param gears:
        Gear vector [-].
    :type gears: numpy.array

    :param engine_speeds:
        Engine speed vector [RPM].
    :type engine_speeds: numpy.array

    :param velocities:
        Vehicle velocity [km/h].
    :type velocities: numpy.array

    :param accelerations:
        Vehicle acceleration [m/s2].
    :type accelerations: numpy.array, float

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :param time_cold_hot_transition:
        Time at cold hot transition phase [s].
    :type time_cold_hot_transition: float

    :returns:
        Two corrected matrix velocities for cold and hot phases.
    :rtype: dict
    """

    cmv = {}

    b = times <= time_cold_hot_transition

    for i in ['cold', 'hot']:
        cmv[i] = calibrate_gear_shifting_cmv(
            correct_gear, gears[b], engine_speeds[b], velocities[b],
            accelerations[b], velocity_speed_ratios)
        b = np.logical_not(b)

    return cmv


def calibrate_gear_shifting_decision_tree(gears, *params):
    """
    Calibrates a decision tree classifier to predict gears.

    :param gears:
        Gear vector [-].
    :type gears: numpy.array

    :param params:
        Time series vectors.
    :type params: (np.array, ...)

    :returns:
        A decision tree classifier to predict gears.
    :rtype: DecisionTreeClassifier
    """

    previous_gear = [gears[0]]

    previous_gear.extend(gears[:-1])

    tree = DecisionTreeClassifier(random_state=0)

    tree.fit(np.array((previous_gear,) + params).T, gears)

    return tree


def correct_gsv(gsv):
    """
    Corrects gear shifting velocity matrix from unreliable limits.

    :param gsv:
        Gear shifting velocity matrix.
    :type gsv: dict

    :return:
        Gear shifting velocity matrix corrected from unreliable limits.
    :rtype: dict
    """

    gsv[0] = [0, (VEL_EPS, (INF, 0))]

    for v0, v1 in dsp_utl.pairwise(gsv.values()):
        up0, down1 = (v0[1][0], v1[0][0])

        if down1 + VEL_EPS <= v0[0]:
            v0[1] = v1[0] = up0
        elif up0 >= down1:
            v0[1], v1[0] = (up0, down1)
            continue
        elif v0[1][1] >= v1[0][1]:
            v0[1] = v1[0] = up0
        else:
            v0[1] = v1[0] = down1

        v0[1] += VEL_EPS

    gsv[max(gsv)][1] = INF

    return gsv


class GSPV(dict):
    def __init__(self):
        super(GSPV, self).__init__()
        self.cloud = {}

    def fit(self, gears, velocities, wheel_powers, velocity_speed_ratios):
        self.clear()

        self.velocity_speed_ratios = velocity_speed_ratios

        it = zip(velocities, wheel_powers, dsp_utl.pairwise(gears))

        for v, p, (g0, g1) in it:
            if v > VEL_EPS and g0 != g1:
                x = self.get(g0, [[], [[], []]])
                if g0 < g1 and p >= 0:
                    x[1][0].append(p)
                    x[1][1].append(v)
                elif g0 > g1 and p <= 0:
                    x[0].append(v)
                else:
                    continue
                self[g0] = x

        self[0] = [[0.0], [[0.0], [VEL_EPS]]]

        self[max(self)][1] = [[0, 1], [INF] * 2]

        self.cloud = deepcopy(self)

        self._fit_cloud()

        return self

    def _fit_cloud(self):
        def line(k, v, i):
            x = np.mean(np.asarray(v[i])) if v[i] else None
            k_p = k - 1
            while k_p > 0 and k_p not in self:
                k_p -= 1
            x_up = self[k_p][not i](0) if k_p >= 0 else x

            if x is None or x > x_up:
                x = x_up
            return Spline([0, 1], [x] * 2, k=1)

        def mean(x):
            if x:
                x = np.asarray(x)
                return np.mean(x)
            else:
                return np.nan

        self.clear()
        self.update(deepcopy(self.cloud))

        for k, v in sorted(self.items()):
            v[0] = line(k, v, 0)

            if len(v[1][0]) > 2:
                v[1] = _gspv_interpolate_cloud(*v[1])
            else:
                v[1] = [mean(v[1][1])] * 2
                v[1] = Spline([0, 1], v[1], k=1)

    @property
    def limits(self):
        limits = {}
        X = [INF, 0]
        for v in self.cloud.values():
            X[0] = min(min(v[1][0]), X[0])
            X[1] = max(max(v[1][0]), X[1])
        X = list(np.linspace(*X))
        X = [0] + X + [X[-1] * 1.1]
        for k, func in self.items():
            limits[k] = [(f(X), X) for f, x in zip(func, X)]
        return limits

    def plot(self):
        import matplotlib.pylab as plt
        for k, v in self.limits.items():
            kv = {}
            for (s, l), (x, y) in zip((('down', '--'), ('up', '-')), v):
                if x[0] < INF:
                    kv['label'] = 'Gear %d:%s-shift' % (k, s)
                    kv['linestyle'] = l
                    kv['color'] = plt.plot(x, y, **kv)[0]._color
            cy, cx = self.cloud[k][1]
            if cx[0] < INF:
                kv.pop('label')
                kv['linestyle'] = ''
                kv['marker'] = 'o'
                plt.plot(cx, cy, **kv)
        plt.legend(loc='best')
        plt.xlabel('Velocity [km/h]')
        plt.ylabel('Power [kW]')

    def predict(self, X, correct_gear=lambda v, a, g: g, previous_gear=None,
                times=None):

        gear = previous_gear or min(self)

        min_gear, max_gear = min(self), max(self)

        gears = np.zeros(shape=len(X))

        for i, (velocity, acceleration, wheel_power) in enumerate(X):
            down, up = [func(wheel_power) for func in self[gear]]

            if not down <= velocity < up:
                add = 1 if velocity >= up else -1
                while min_gear <= gear <= max_gear:
                    gear += add
                    if gear in self:
                        break
                gear = max(min_gear, min(max_gear, gear))

            g = correct_gear(velocity, acceleration, gear)

            if g in self:
                gear = g

            gears[i] = gear = max(MIN_GEAR, gear)

        if times is not None:
            gears = median_filter(times, gears, TIME_WINDOW)
            gears = clear_fluctuations(times, gears, TIME_WINDOW)

        return gears

    def convert(self, velocity_speed_ratios):
        if velocity_speed_ratios != self.velocity_speed_ratios:

            vsr, n_vsr = self.velocity_speed_ratios, velocity_speed_ratios

            limits = [INF, 0]

            for v in self.cloud.values():
                limits[0] = min(min(v[1][0]), limits[0])
                limits[1] = max(max(v[1][0]), limits[1])

            K, X = zip(*[(k, v) for k, v in sorted(n_vsr.items())])
            cloud = self.cloud = {}

            for p in np.linspace(*limits):
                it = [[vsr[k]] + [func(p) for func in v]
                      for k, v in self.items()]

                L, U = _convert_limits(it, X)

                for k, l, u in zip(K, L, U):
                    c = cloud[k] = cloud.get(k, [[], [[], []]])
                    c[0].append(l)
                    c[1][0].append(p)
                    c[1][1].append(u)

            cloud[0] = [[0.0], [[0.0], [VEL_EPS]]]
            cloud[max(cloud)][1] = [[0, 1], [INF] * 2]

            self._fit_cloud()

            self.velocity_speed_ratios = n_vsr

        return self


def calibrate_gspv(gears, velocities, wheel_powers, velocity_speed_ratios):
    """
    Identifies gear shifting power velocity matrix.

    :param gears:
        Gear vector [-].
    :type gears: numpy.array

    :param velocities:
        Vehicle velocity [km/h].
    :type velocities: numpy.array

    :param wheel_powers:
        Power at wheels vector [kW].
    :type wheel_powers: numpy.array

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :return:
        Gear shifting power velocity matrix.
    :rtype: dict
    """

    gspv = GSPV()

    gspv.fit(gears, velocities, wheel_powers, velocity_speed_ratios)

    return gspv


def _gspv_interpolate_cloud(powers, velocities):

    regressor = IsotonicRegression().fit(powers, velocities)

    min_p, max_p = min(powers), max(powers)
    x = np.linspace(min_p, max_p)
    y = regressor.predict(x)
    y = np.append(np.append(y[0], y), [y[-1]])
    x = np.append(np.append([0.0], x), [max_p * 1.1])
    return Spline(x, y, k=1)


def calibrate_gspv_hot_cold(
        times, gears, velocities, wheel_powers, time_cold_hot_transition,
        velocity_speed_ratios):
    """
    Identifies gear shifting power velocity matrices for cold and hot phases.

    :param times:
        Time vector [s].
    :type times: numpy.array

    :param gears:
        Gear vector [-].
    :type gears: numpy.array

    :param velocities:
        Vehicle velocity [km/h].
    :type velocities: numpy.array

    :param wheel_powers:
         Power at wheels vector [kW].
    :type wheel_powers: numpy.array

    :param time_cold_hot_transition:
        Time at cold hot transition phase [s].
    :type time_cold_hot_transition: float

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :return:
        Gear shifting power velocity matrices for cold and hot phases.
    :rtype: dict
    """

    gspv = {}

    b = times <= time_cold_hot_transition

    for i in ['cold', 'hot']:
        gspv[i] = calibrate_gspv(gears[b], velocities[b], wheel_powers[b],
                                 velocity_speed_ratios)
        b = np.logical_not(b)

    return gspv


def prediction_gears_decision_tree(correct_gear, decision_tree, times, *params):
    """
    Predicts gears with a decision tree classifier [-].

    :param correct_gear:
        A function to correct the gear predicted.
    :type correct_gear: function

    :param decision_tree:
        A decision tree classifier to predict gears.
    :type decision_tree: DecisionTreeClassifier

    :param times:
        Time vector [s].
    :type times: numpy.array

    :param params:
        Time series vectors.
    :type params: (nx.array, ...)

    :return:
        Predicted gears.
    :rtype: numpy.array
    """

    gear = [MIN_GEAR]

    predict = decision_tree.predict

    def predict_gear(*args):
        g = predict([gear + list(args)])[0]
        gear[0] = correct_gear(args[0], args[1], g)
        return gear[0]

    gear = np.vectorize(predict_gear)(*params)

    gear[gear < MIN_GEAR] = MIN_GEAR

    gear = median_filter(times, gear, TIME_WINDOW)

    return clear_fluctuations(times, gear, TIME_WINDOW)


def prediction_gears_gsm(
        correct_gear, gsm, velocities, accelerations, times=None,
        wheel_powers=None):
    """
    Predicts gears with a gear shifting matrix (cmv or gspv) [-].

    :param correct_gear:
        A function to correct the gear predicted.
    :type correct_gear: function

    :param gsm:
        A gear shifting matrix (cmv or gspv).
    :type gsm: GSPV, CMV

    :param velocities:
        Vehicle velocity [km/h].
    :type velocities: numpy.array

    :param accelerations:
        Vehicle acceleration [m/s2].
    :type accelerations: numpy.array

    :param times:
        Time vector [s].

        If None gears are predicted with cmv approach, otherwise with gspv.
    :type times: numpy.array, optional

    :param wheel_powers:
        Power at wheels vector [kW].

        If None gears are predicted with cmv approach, otherwise with gspv.
    :type wheel_powers: numpy.array, optional

    :return:
        Predicted gears.
    :rtype: numpy.array
    """

    X = [velocities, accelerations]

    if wheel_powers is not None:
        X.append(wheel_powers)

    return gsm.predict(np.array(X).T, correct_gear=correct_gear, times=times)


def prediction_gears_gsm_hot_cold(
        correct_gear, gsm, time_cold_hot_transition, times, velocities,
        accelerations, wheel_powers=None):
    """
    Predicts gears with a gear shifting matrix (cmv or gspv) for cold and hot
    phases [-].

    :param correct_gear:
        A function to correct the gear predicted.
    :type correct_gear: function

    :param gsm:
        A gear shifting matrix (cmv or gspv).
    :type gsm: dict

    :param time_cold_hot_transition:
        Time at cold hot transition phase [s].
    :type time_cold_hot_transition: float

    :param times:
        Time vector [s].
    :type times: numpy.array

    :param velocities:
        Vehicle velocity [km/h].
    :type velocities: numpy.array

    :param accelerations:
        Vehicle acceleration [m/s2].
    :type accelerations: numpy.array

    :param wheel_powers:
        Power at wheels vector [kW].

        If None gears are predicted with cmv approach, otherwise with gspv.
    :type wheel_powers: numpy.array, optional

    :return:
        Predicted gears [-].
    :rtype: numpy.array
    """

    b = times <= time_cold_hot_transition

    gear = []

    for i in ['cold', 'hot']:
        args = [correct_gear, gsm[i], velocities[b], accelerations[b], times[b]]
        if wheel_powers is not None:
            args.append(wheel_powers[b])

        gear = np.append(gear, prediction_gears_gsm(*args))
        b = np.logical_not(b)

    return gear


def calculate_error_coefficients(
        identified_gears, gears, engine_speeds, predicted_engine_speeds,
        velocities):
    """
    Calculates the prediction's error coefficients.

    :param engine_speeds:
        Engine speed vector [RPM].
    :type engine_speeds: numpy.array

    :param predicted_engine_speeds:
        Predicted Engine speed vector [RPM].
    :type predicted_engine_speeds: numpy.array

    :param velocities:
        Vehicle velocity [km/h].
    :type velocities: numpy.array

    :return:
        Correlation coefficient and mean absolute error.
    :rtype: dict
    """

    b = velocities > VEL_EPS

    x = engine_speeds[b]
    y = predicted_engine_speeds[b]

    res = {
        'mean_absolute_error': mean_absolute_error(x, y),
        'correlation_coefficient': np.corrcoef(x, y)[0, 1],
        'accuracy_score': accuracy_score(identified_gears, gears)
    }

    return res


def calibrate_mvl(gears, velocities, velocity_speed_ratios, idle_engine_speed):
    """
    Calibrates the matrix velocity limits (upper and lower bound) [km/h].

    :param gears:
        Gear vector [-].
    :type gears: numpy.array

    :param velocity_speed_ratios:
        Constant velocity speed ratios of the gear box [km/(h*RPM)].
    :type velocity_speed_ratios: dict

    :param idle_engine_speed:
        Engine speed idle median and std [RPM].
    :type idle_engine_speed: (float, float)

    :return:
        Matrix velocity limits (upper and lower bound) [km/h].
    :rtype: MVL
    """

    mvl = MVL().fit(gears, velocities, velocity_speed_ratios, idle_engine_speed)

    return mvl


def correct_gear_mvl_v1(
        velocity, acceleration, gear, mvl, max_gear, min_gear):
    """
    Corrects the gear predicted according to upper and lower bound velocity
    limits.

    :param velocity:
        Vehicle velocity [km/h].
    :type velocity: float

    :param acceleration:
        Vehicle acceleration [m/s2].
    :type acceleration: float

    :param gear:
        Predicted vehicle gear [-].
    :type gear: int

    :param max_gear:
        Maximum gear [-].
    :type max_gear: int

    :param min_gear:
        Minimum gear [-].
    :type min_gear: int

    :param mvl:
        Matrix velocity limits (upper and lower bound) [km/h].
    :type mvl: OrderedDict

    :return:
        A gear corrected according to upper bound engine speed [-].
    :rtype: int
    """

    if abs(acceleration) < ACC_EPS:

        while mvl[gear][1] < velocity and gear < max_gear:
            gear += 1

        while mvl[gear][0] > velocity and gear > min_gear:
            gear -= 1

    return gear


def correct_gear_mvl(velocity, acceleration, gear, mvl, *args):
    """
    Corrects the gear predicted according to upper and lower bound velocity
    limits.

    :param velocity:
        Vehicle velocity [km/h].
    :type velocity: float

    :param acceleration:
        Vehicle acceleration [m/s2].
    :type acceleration: float

    :param gear:
        Predicted vehicle gear [-].
    :type gear: int

    :param mvl:
        Matrix velocity limits (upper and lower bound) [km/h].
    :type mvl: MVL

    :return:
        A gear corrected according to upper bound engine speed [-].
    :rtype: int
    """

    return mvl.predict(velocity, acceleration, gear)


class MVL(CMV):
    def fit(self, gears, velocities, velocity_speed_ratios, idle_engine_speed):
        self.velocity_speed_ratios = velocity_speed_ratios
        idle = idle_engine_speed
        mvl = [np.array([idle[0] - idle[1], idle[0] + idle[1]])]
        for k in range(1, int(max(gears)) + 1):
            l, on, vsr = [], None, velocity_speed_ratios[k]

            for i, b in enumerate(chain(gears == k, [False])):
                if not b and not on is None:
                    v = velocities[on:i]
                    l.append([min(v), max(v)])
                    on = None

                elif on is None and b:
                    on = i

            if l:
                min_v, max_v = zip(*l)
                l = [sum(reject_outliers(min_v)), sum(reject_outliers(max_v))]
                mvl.append(np.array([max(idle[0], l / vsr) for l in l]))
            else:
                mvl.append(mvl[-1].copy())

        mvl = [[k, tuple(v * velocity_speed_ratios[k])]
               for k, v in reversed(list(enumerate(mvl[1:], 1)))]
        mvl[0][1] = (mvl[0][1][0], INF)
        mvl.append([0, (0, mvl[-1][1][0])])

        self.clear()
        self.update(correct_gsv_for_constant_velocities(
                OrderedDict(mvl), up_cns_vel=[35, 50],
                down_cns_vel=[15, 32, 50, 70])
        )
        return self

    def predict(self, velocity, acceleration, gear):

        if abs(acceleration) < ACC_EPS:
            g = next((k for k, v in self.items() if velocity - v[0] > 0), gear)
            gear = gear if g < gear and self[gear][1] > velocity else g

        return gear
