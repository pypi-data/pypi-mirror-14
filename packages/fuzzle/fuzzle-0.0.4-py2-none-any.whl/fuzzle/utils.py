def feq(x, y, ε=0.00000001):
    """ Checks if two values are almost the same.

    It's useful (and the only way) to compare two float numbers properly. The
    why is well explained in that video from: Prof. Eric Grimson and Prof. John
    Guttag: https://www.youtube.com/watch?v=Pfo7r6bjSqI.

    :param x: One number to compare.
    :param y: Other number to compare.
    :param ε: The resolution of the comparison. Defaults to 0.00000001.
    :return: True if both numbers are almos the same, False otherwise.
    """
    return abs(x - y) < ε


def frange(stop, start=0.0, step=1.0):
    """ Similar to built-in method range but for float values.

    :param stop: The end of the range. It'll be not included.
    :param step: Each of the steps until the stop value.
    :param start: The begining value for the range. Defaults to 0.
    """
    return (
        start + step * i
        for i in range(int((stop - start) / step))
    )
