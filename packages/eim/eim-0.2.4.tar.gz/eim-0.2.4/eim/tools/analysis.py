import numpy as np
import scipy.interpolate

def bioemo_readings_to_volts(readings):
    """
    Convert readings from the BioEmo sensor range to voltages.

    Parameters
    ----------
    readings : array_like
        The readings to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted reading(s) as voltage(s)

    Raises
    ------
    TypeError
        If ``readings`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> midrange = bioemo_readings_to_volts(512)
    >>> np.abs(midrange - 2.5024437927663734) < 0.001
    True
    """

    return (np.asarray(readings) / 1023.) * 5.


def bioemo_volts_to_ohms(volts):
    """
    Convert voltages from the BioEmo sensor to resistances in ohms. This mapping was empirically verified and is
    governed by the relationship:

    .. math::

        \\begin{eqnarray}
            \\ln{V} &=& -1.17 \\times 10^{-3} R + 0.861 \\\\
            \\ln{V} - 0.861 &=& -0.00117R \\\\
            R &=& \\frac{\ln{V} - 0.861}{-0.00117} \\\\
            R &=& \\frac{0.861 - \ln{V}}{0.00117} \\\\
            R &=& \\frac{0.861}{0.00117} - \\frac{\\ln{V}}{0.00117}
        \\end{eqnarray}

    Parameters
    ----------
    volts : array_like
        The voltages to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted voltage(s) as resistance(s)

    Raises
    ------
    TypeError
        If ``volts`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> two_volts = bioemo_volts_to_ohms(2)
    >>> np.abs(two_volts - 143463.94823936306) < 0.001
    True
    """

    volts = np.asarray(volts)
    # left = 0.861 / 0.00117
    # right = 1. / 0.00117
    # right = right * np.log(volts)
    # return (left - right) * 1000
    num = 1000 * np.log(volts) - 861
    denom = -0.00117
    return num / denom


def bioemo_volts_to_siemens(volts):
    """
    Convert voltages from the BioEmo sensor to conductances in siemens.

    Parameters
    ----------
    volts : array_like
        The voltages to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted voltage(s) as conductance(s)

    Raises
    ------
    TypeError
        If ``volts`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> two_volts = bioemo_volts_to_siemens(2)
    >>> np.abs(two_volts - 6.9703922990572208e-06) < 0.001
    True
    """

    ohms = bioemo_volts_to_ohms(volts)
    siemens = ohms_to_siemens(ohms)
    return siemens


def bioemo_readings_to_siemens(readings):
    """
    Convert readings from the BioEmo sensor to conductances in siemens.

    Parameters
    ----------
    readings : array_like
        The voltages to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted reading(s) as conductance(s)

    Raises
    ------
    TypeError
        If ``readings`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> midrange = bioemo_readings_to_siemens(512)
    >>> np.abs(midrange - -2.0793430561630236e-05) < 0.001
    True
    """

    readings = np.asarray(readings)
    volts = bioemo_readings_to_volts(readings)
    return bioemo_volts_to_siemens(volts)


def ohms_to_siemens(ohms):
    """
    Convert resistances in ohms to conductances in siemens.

    Parameters
    ----------
    ohms : array_like
        The resistances to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted resistance(s) as conductance(s)

    Raises
    ------
    TypeError
        If ``ohms`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> ohms_to_siemens(512) == 1. / 512
    True
    """

    return 1. / np.asarray(ohms)


def siemens_to_ohms(siemens):
    """
    Convert conductances in siemens to resistances in ohms.

    Parameters
    ----------
    siemens : array_like
        The conductances to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted conductance(s) as resistance(s)

    Raises
    ------
    TypeError
        If ``siemens`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> siemens_to_ohms(512) == 1. / 512
    True
    """

    return ohms_to_siemens(siemens)

def unit_to_kilounit(measure):
    """
    Convert measures in whole units to thousands of units.

    Parameters
    ----------
    measure : array_like
        The measure(s) to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted measure(s)

    Raises
    ------
    TypeError
        If ``measure`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> unit_to_kilounit(1) == 1. / 1000
    True
    """

    return measure / 1000.


def unit_to_megaunit(measure):
    """
    Convert measures in whole units to millions of units.

    Parameters
    ----------
    measure : array_like
        The measure(s) to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted measure(s)

    Raises
    ------
    TypeError
        If ``measure`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> unit_to_megaunit(1) == 1. / 1000000
    True
    """

    return measure / 1000000.


def unit_to_gigaunit(measure):
    """
    Convert measures in whole units to billions of units.

    Parameters
    ----------
    measure : array_like
        The measure(s) to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted measure(s)

    Raises
    ------
    TypeError
        If ``measure`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> unit_to_gigaunit(1) == 1. / 1000000000
    True
    """

    return measure / 1000000000.

def unit_to_milliunit(measure):
    """
    Convert measures in whole units to thousandths of units.

    Parameters
    ----------
    measure : array_like
        The measure(s) to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted measure(s)

    Raises
    ------
    TypeError
        If ``measure`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> unit_to_milliunit(1) == 1. * 1000
    True
    """

    return measure * 1000.


def unit_to_microunit(measure):
    """
    Convert measures in whole units to millionths of units.

    Parameters
    ----------
    measure : array_like
        The measure(s) to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted measure(s)

    Raises
    ------
    TypeError
        If ``measure`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> unit_to_microunit(1) == 1. * 1000000
    True
    """

    return measure * 1000000.


def unit_to_nanounit(measure):
    """
    Convert measures in whole units to billionths of units.

    Parameters
    ----------
    measure : array_like
        The measure(s) to be converted

    Returns
    -------
    out : float or :py:class:`numpy.ndarray`
        The converted measure(s)

    Raises
    ------
    TypeError
        If ``measure`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> unit_to_nanounit(1) == 1. * 1000000000
    True
    """

    return measure * 1000000000.


def contiguous_subsequences(sequence):
    """
    Extract a list of the contiguous subsequences in ``sequence``.

    Parameters
    ----------
    sequence : list of int
        A list of montotonically increasing integers

    Returns
    -------
    list of list of int
        A list of lists of contiguous subsequences in ``sequence``

    Examples
    --------
    >>> contiguous_subsequences([])
    []

    >>> contiguous_subsequences([1])
    [[1]]

    >>> contiguous_subsequences([1,2,3])
    [[1, 2, 3]]

    >>> contiguous_subsequences([-4,2,3,4,5,10,11,12,13,14])
    [[-4], [2, 3, 4, 5], [10, 11, 12, 13, 14]]
    """

    subsequences = []

    if len(sequence) == 0:
        return []

    current_subsequence = [sequence[0]]
    for i in range(1, len(sequence)):
        if sequence[i] == current_subsequence[-1] + 1:
            current_subsequence.append(sequence[i])
        else:
            subsequences.append(current_subsequence)
            current_subsequence = [sequence[i]]

    subsequences.append(current_subsequence)

    return subsequences


def detect_artifacts(data, fs, up=0.2, down=0.1, signal_min=0., signal_max=1., window_size=0., mode='interpolate'):
    """
    Using the method described in [1], detect and remove artifacts
    in an electrodermal activity signal. In summary, this method considers any
    increase in EDA greater than ``up`` or any decrease in EDA greater than
    ``down`` within a second to be an artifact. Artifacts can either be
    replaced with :py:class:`numpy.nan`, or the values in ``data`` before and
    after the artifact can be used to interpolate across the artifact. A
    window size can be set that will exclude data before and after each
    artifact.

    Parameters
    ----------
    data : array_like
        The original data
    fs : int or float
        The sample rate of the original data
    up : float, optional
        The maximum absolute rise in amplitude that is allowable in one
        second expressed as a fraction of the entire signal range (the
        default is ``0.2``)
    down : float, optional
        The maximum absolute fall in amplitude that is allowable in one
        second expressed as a fraction of the entire signal range (the
        default is ``0.1``)
    signal_min : int, optional
        The minimum allowable value in ``data`` (the default is ``0.``) Values
        below ``signal_min`` will be set to ``signal_min``.
    signal_max : float, optional
        The maximum allowable value in ``data`` (the default is ``1.``) Values
        above ``signal_max`` will be set to ``signal_max``.
    window_size : float, optional
        If a window size is set (default is ``0.``), this value is taken as a
        window of ``window_size`` seconds that is centered over each detected
        artifact. All samples within this window are also considered artifacts.
    mode : str, optional
        If ``'interpolate'`` (the default), ``data`` will be interpolated
        across artifacts. If ``'nan'``, artifacts will be replaced with
        :py:class:`numpy.nan`

    Returns
    -------
    clean_data : :py:class:`numpy.ndarray`
        The data with artifacts removed
    quality : float
        The percentage of the original signal that did not contain artifacts

    Raises
    ------
    TypeError
        If ``arr`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> data = [0.1, 0.1, 0.1, 0.3, 0.1, 0.1]
    >>> clean, q = detect_artifacts(data, 2, signal_min=0, signal_max=0.3)
    >>> clean
    array([ 0.1,  0.1,  0.1,  0.1,  0.1,  0.1])
    >>> np.testing.assert_almost_equal(q, 2./3.)

    >>> data = [0.1, 0.1, 0.1, 0.101, 0.1, 0.1]
    >>> clean, q = detect_artifacts(data, 2, signal_min=0, signal_max=0.3)
    >>> clean
    array([ 0.1  ,  0.1  ,  0.1  ,  0.101,  0.1  ,  0.1  ])
    >>> q
    1.0

    >>> data = [0.1, 0.1, 0.1, 0.3, 0.1, 0.1]
    >>> detect_artifacts(data, 2, signal_min=0, signal_max=0.3, mode='nan')[0]
    array([ 0.1,  0.1,  0.1,  nan,  nan,  0.1])

    >>> data = [0.5, 0.55, 0.5, 0.55, 0.1, 0.2, 0.55, 0.9]
    >>> detect_artifacts(data, 3, mode='nan')[0]
    array([ 0.5 ,  0.55,  0.5 ,  0.55,   nan,   nan,   nan,   nan])

    >>> data = [0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0]
    >>> detect_artifacts(data, 2, signal_min=0., signal_max=1., window_size=1., mode='nan')[0]
    array([ 0.5,  0.5,  0.5,  nan,  nan,  nan,  1. ,  1. ,  1. ])

    >>> data = [0., 0., 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0]
    >>> detect_artifacts(data, 2, signal_min=0., signal_max=1., window_size=1., mode='nan')[0]
    array([  0.,  nan,  nan,  nan,  nan,  nan,   1.,   1.,   1.])

    >>> data = [0., 0., 0., 0., 1., 1., 1., 1., 1.]
    >>> detect_artifacts(data, 2, signal_min=0., signal_max=1., window_size=2., mode='nan')[0]
    array([  0.,   0.,  nan,  nan,  nan,  nan,  nan,   1.,   1.])

    >>> data = [0., 0., 0., 0., 1., 1., 1., 1., 1.]
    >>> detect_artifacts(data, 2, signal_min=0., signal_max=1., window_size=3., mode='nan')[0]
    array([  0.,  nan,  nan,  nan,  nan,  nan,  nan,  nan,   1.])

    >>> data = [0., 0., 0., 0., 0., 0., 0., 0., 1.]
    >>> detect_artifacts(data, 2, signal_min=0., signal_max=1., window_size=3., mode='nan')[0]
    array([  0.,   0.,   0.,   0.,   0.,  nan,  nan,  nan,  nan])

    >>> data = [0., 0., 1., 1., 1., 1., 1., 1., 1.]
    >>> detect_artifacts(data, 2, signal_min=0., signal_max=1., window_size=2., mode='nan')[0]
    array([  0.,  nan,  nan,  nan,  nan,   1.,   1.,   1.,   1.])

    >>> data = [0.5, 0.5, 0.5, 0.5, 0.4999, 0.5, 0.5, 0.5, 0.5]
    >>> detect_artifacts(data, 2, signal_min=0.5, signal_max=1., mode='nan')[0]
    array([ 0.5,  0.5,  0.5,  0.5,  nan,  0.5,  0.5,  0.5,  0.5])

    >>> data = [0.5, 0.5, 0.5, 0.5, 0.5001, 0.5, 0.5, 0.5, 0.5]
    >>> detect_artifacts(data, 2, signal_min=0., signal_max=0.5, mode='nan')[0]
    array([ 0.5,  0.5,  0.5,  0.5,  nan,  0.5,  0.5,  0.5,  0.5])

    .. [1] R. Kocielnik, N. Sidorova, F. M. Maggi, M. Ouwerkerk, and J.
        H. D. M. Westerink, “Smart Technologies for Long-Term Stress
        Monitoring at Work,” in Proceedings of the 2013 IEEE 26th
        International Symposium on Computer-Based Medical Systems (CBMS 2013),
        University of Porto, Porto, Portugal, 2013, pp. 53–58.
    """
    data = np.array(data)

    artifact_count = 0

    # Rises and falls should be positive percentages
    up = np.abs(up)
    down = np.abs(down)

    # Clip values outside of [signal_min, signal_max]
    # TODO: This should have an option to mark clipped values as artifacts
    min_clip_indices = data < signal_min
    max_clip_indices = data > signal_max
    normalized_data = np.clip(data, signal_min, signal_max)
    # print('data:', data)
    # print('normalized_data:', normalized_data)

    # Create a shifted copy of normalized data
    shifted_normalized_data = np.roll(normalized_data, 1)
    # print('shifted_normalized_data:', shifted_normalized_data)
    # shifted_normalized_data = np.roll(normalized_data, fs)

    # Calculate maximum allowable changes
    signal_range = np.abs(signal_max - signal_min)
    max_rise = up * signal_range
    max_fall = -down * signal_range

    # Convert max_rise and max_fall to sample-wise allowable rises/falls
    max_rise = max_rise / fs
    # print('max_rise:', max_rise)
    max_fall = max_fall / fs
    # print('max_fall:', max_fall)

    # Find differences
    differences = normalized_data - shifted_normalized_data
    # print('differences:', differences)

    # Find indices that are greater than max_rise or max_fall
    rise_artifact_indices = differences > max_rise
    # print('rise_artifact_indices:', rise_artifact_indices)
    fall_artifact_indices = differences < max_fall
    # print('fall_artifact_indices:', fall_artifact_indices)

    # Combine artifact index arrays
    artifact_indices = \
        rise_artifact_indices + \
        fall_artifact_indices + \
        min_clip_indices + \
        max_clip_indices
    # print('combined artifact_indices:', artifact_indices)

    # TODO: We could compare these to preceding values instead of losing them
    # Mark first fs indices as not artifacts
    artifact_indices[0:fs] = False
    # print('corrected artifact_indices:', artifact_indices)

    # Convert boolean indices to integer indices
    artifact_indices = np.nonzero(artifact_indices)[0]
    # print('integer artifact_indices:', artifact_indices)

    # window_size in samples
    window_n = 1
    if window_size > 0. and len(artifact_indices) > 0:
        window_n = np.int(np.ceil(window_size * fs))

        # Force odd window length
        if window_n % 2 == 0:
            window_n = window_n + 1

        # For each artifact index, create a artifact 'window'
        artifact_window_indices = []
        for artifact_index in artifact_indices:
            half_window_n = window_n // 2
            this_window_indices = np.arange(
                    artifact_index - half_window_n,
                    artifact_index + half_window_n + 1
            )
            artifact_window_indices.append(this_window_indices)

        from functools import reduce
        artifact_indices = reduce(np.union1d, artifact_window_indices)

    # print('integer artifact_indices:', artifact_indices)

    # Chop spurious indices from beginning and end
    artifact_indices = artifact_indices[artifact_indices < len(data)]
    artifact_indices = artifact_indices[artifact_indices > 0]

    # print('integer artifact_indices:', artifact_indices)

    # Get contiguous subsequences
    artifact_indices = contiguous_subsequences(artifact_indices)

    # TODO: Remove indices greater than length of data

    # If last subsequence of artifacts is the end of data, extend last good
    # value in data and remove this subsequence from artifacts
    if len(artifact_indices) != 0:
        last_artifact_index = artifact_indices[-1][-1]
        if last_artifact_index == len(normalized_data) - 1:

            artifact_start = artifact_indices[-1][0]
            artifact_end = artifact_indices[-1][-1] + 1

            artifact_count = artifact_count + artifact_end - artifact_start

            if mode == 'interpolate':
                normalized_data[artifact_start:artifact_end] = \
                    normalized_data[artifact_indices[-1][0] - 1]
            else:
                normalized_data[artifact_start:artifact_end] = np.nan

            artifact_indices.pop()

    for r in artifact_indices:

        artifact_count = artifact_count + len(r)

        if mode == 'interpolate':

            # TODO: We should use more than one index preceding and following artifact for interpolation
            # Add the previous and following indices onto r

            actual_artifact_indices = r.copy()
            non_artifact_indices = np.array([], dtype=np.dtype(np.int64))

            to_prepend = np.arange(r[0] - 5, r[0])
            to_append = np.arange(r[-1] + 1, r[-1] + 6)

            # r = np.insert(r, 0, r[0] - 1)
            # r = np.append(r, r[-1] + 1)

            non_artifact_indices = np.insert(non_artifact_indices, 0, to_prepend)
            non_artifact_indices = np.append(non_artifact_indices, to_append)

            too_low = non_artifact_indices < 0
            too_high = non_artifact_indices > len(data) - 1
            non_artifact_indices = non_artifact_indices[~(too_low + too_high)]

            interpolated_artifact = scipy.interpolate.pchip_interpolate(
                non_artifact_indices, data[non_artifact_indices], actual_artifact_indices
            )

            normalized_data[r] = interpolated_artifact

        else:
            normalized_data[r] = np.nan

    quality = 1. - (artifact_count / len(data))

    return normalized_data, quality


def windows(data, length, stride=None, pad=None, equal_lengths=False):
    """
    Separate an array into windows with an optional stride distance.

    Parameters
    ----------
    data : array_like
        The array to be 'windowed'
    length : int
        The length of each window
    stride : int, optional
        The distance between window start indices. If ``None``, ``length`` is
        used as ``stride``.
    pad : int or float, optional
        If ``pad`` is specified (default is ``None``), ``data`` will be
        extended with the value of ``pad`` such that all windows are of length
        ``length``.
    equal_lengths : bool, optional
        If ``True`` (default is ``False``), only equal length windows will be
        returned. In the event that the values for ``length`` and ``stride``
        would generate windows of uneven length at the end of data, these
        shorter windows are not returned. If ``False``, all windows are
        returned. In the event that the values for ``length`` and ``stride``
        would generate windows of uneven length at the end of data, these
        shorter windows are returned.

    Returns
    -------
    out : list of :py:class:`numpy.ndarray`
        A list of each of the windows of ``data`` in order

    Raises
    ------
    TypeError
        If ``data`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> windows([0, 1, 2, 3, 4, 5], length=3)
    [array([0, 1, 2]), array([3, 4, 5])]

    >>> windows([0, 1, 2, 3, 4, 5], length=3, stride=1)
    [array([0, 1, 2]), array([1, 2, 3]), array([2, 3, 4]), array([3, 4, 5]), array([4, 5]), array([5])]

    >>> windows([0, 1, 2, 3, 4, 5], 3, 1, equal_lengths=True)
    [array([0, 1, 2]), array([1, 2, 3]), array([2, 3, 4]), array([3, 4, 5])]

    >>> windows([0, 1, 2, 3, 4, 5], 3, 1, pad=-1)
    [array([0, 1, 2]), array([1, 2, 3]), array([2, 3, 4]), array([3, 4, 5]), array([ 4,  5, -1]), array([ 5, -1, -1])]

    >>> windows([0, 1, 2, 3, 4, 5], 12, equal_lengths=True)
    []

    >>> windows([0, 1, 2, 3, 4, 5], 12, equal_lengths=False)
    [array([0, 1, 2, 3, 4, 5])]

    >>> windows([0, 1, 2], length=1)
    [array([0]), array([1]), array([2])]

    >>> windows([0, 1, 2, 3, 4, 5], length=3, stride=4)
    [array([0, 1, 2]), array([4, 5])]
    """

    # Local copy of data for padding
    local_data = np.array(data)

    # Check value of stride
    if stride is None:
        stride = length

    # Generate start indices
    starts = np.arange(0, len(local_data), stride)

    # Container for windows
    out = list()

    # Iterate over start indices
    for i in starts:
        window = local_data[i:i+length]

        if len(window) < length:
            if pad is not None:
                difference = length - len(window)
                tail = np.repeat(pad, difference)
                window = np.concatenate([window, tail])
                out.append(window)
            elif equal_lengths is False:
                out.append(window)
        else:
            out.append(window)

    return out


def pad_array(arr, length, pad=0):
    """
    Pad an array to a specific ``length`` with a certain value. If ``length``
    is less than the length of ``arr``, ``arr`` is returned unchanged.

    Parameters
    ----------
    arr : array_like
        The array to be padded
    length : int
        The length of the array after padding
    pad : int or float, optional
        The value with which to extend **arr**

    Returns
    -------
    out : :py:class:`numpy.ndarray`
        The padded array

    Raises
    ------
    TypeError
        If ``arr`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> a = np.array([1,2,3])
    >>> padded = pad_array(a, 5)
    >>> np.testing.assert_equal(padded, np.array([1,2,3,0,0]))

    >>> padded = pad_array(a, 6, pad=-1)
    >>> np.testing.assert_equal(padded, np.array([1,2,3,-1,-1,-1]))

    >>> padded = pad_array(a, 2, pad=-1)
    >>> np.testing.assert_equal(padded, np.array([1, 2, 3]))

    >>> np.testing.assert_equal(a, np.array([1,2,3]))
    """
    arr = np.array(arr)
    tail_length = length - len(arr)
    if tail_length > 0:
        tail = np.repeat(pad, tail_length)
        return np.concatenate([arr, tail])
    else:
        return arr


def normalize_array(arr, range_min=0., range_max=1., clip=None):
    """
    Scale the values in an array to the range ``[min, max]``, optionally
    clipping the values in ``arr``.

    Parameters
    ----------
    arr : array_like
        The array to be normalized
    range_min : float, optional
        The minimum value in ``out`` (default is ``0.``). The minimum value in
        ``arr`` will be scaled to this value.
    range_max : float, optional
        The maximum value in ``out`` (default is ``1.``). The maximum value in
        ``arr`` will be scaled to this value.
    clip : tuple, optional
        If ``clip`` is specified (default is ``None``), it should be a tuple
        of length 2: ``(min, max)``. Values in ``arr`` that are less than this
        ``min`` will be set to ``min`` before normalization. Similarly, values
        in ``arr`` that are greater than this ``max`` will be set to ``max``
        before normalization.

    Returns
    -------
    out : :py:class:`numpy.ndarray`
        A normalized copy of ``arr``

    Raises
    ------
    TypeError
        If ``arr`` cannot be converted to a :py:class:`numpy.ndarray`

    Examples
    --------
    >>> normalize_array([-2, 0, 2])
    array([ 0. ,  0.5,  1. ])

    >>> normalize_array([-2, 0, 2], range_min=0.5, range_max=1.5)
    array([ 0.5,  1. ,  1.5])

    >>> normalize_array([1, 2, 3, 4, 5], clip=(2, 4))
    array([ 0. ,  0. ,  0.5,  1. ,  1. ])

    >>> normalize_array([-2, 0, 2], range_min=1., range_max=0.)
    array([ 1. ,  0.5,  0. ])
    """
    arr = np.array(arr)

    if clip is not None:
        arr = np.clip(arr, clip[0], clip[1])

    old_range = np.max(arr) - np.min(arr)
    new_range = range_max - range_min

    return (((arr - np.min(arr)) * new_range) / old_range) + range_min

