import numpy as np


def curve_handler(raw_x, raw_y, frequency):
    start = raw_x[0]
    end = raw_x[-1]

    # get linear interpolation and 400-resampling done on irregular series
    resampling_points_x = np.linspace(start, end, frequency)
    resampling_points_y = np.interp(resampling_points_x, raw_x, raw_y)

    # get q_max representing maximum instantaneous flow
    q_max = np.max(resampling_points_y)
    normalized_y = resampling_points_y / q_max

    # get u_total representing total urine output via calculus
    time_interval = (end - start) / float(frequency - 1)
    u_total = u_total_calculus(time_interval, resampling_points_y)

    u_average = u_total / end

    return normalized_y, end, q_max, u_total, u_average


def u_total_calculus(time_interval, y):
    u_total = 0
    for i in range(len(y) - 1):
        average = (y[i] + y[i+1]) / 2.
        u_total += average * time_interval
    return u_total
