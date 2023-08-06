Measurement Statistics
======================

A statistical package for measurement and population statistics that
incorporate measurement uncertainties and error propagation.

Installation::

    pip install measurement_stats


Error Propagation
-----------------

Say, for example, that we have measured a rectangle to be 11 +/- 0.4 centimeters
wide and 8 +/- 0.3 centimeters long. We can then calculate the area with
uncertainty as follows::

    from measurement_stats import value

    width = value.ValueUncertainty(11, 0.4)
    length = value.ValueUncertainty(8, 0.3)

    area = length * width

    print('AREA:', area.label)
    # $ AREA: 88 +/- 5


For a more complicated example, consider the canonical physics 101 experiment
of trying to calculate the acceleration due to gravity using a pendulum. If a
student has setup a pendulum with a measured length of 92.95 centimeters and an
uncertainty of 0.1 centimeters and measured a period of that pendulum to be
1.936 seconds with an uncertainty of 0.004 seconds, the acceleration due to
gravity, with propagated uncertainty, can be determined as follows::

    l = value.ValueUncertainty(92.95, 0.1)
    T = value.ValueUncertainty(1.936, 0.004)

    g = 4.0 * (math.pi ** 2) * l / (T ** 2)

    print('Acceleration Due To Gravity:', g.label)
    # $ Acceleration Due To Gravity: 979 +/- 4


