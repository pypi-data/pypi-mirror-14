# Copyright 2016 Joshua Taillon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import time
from datetime import datetime

from libtiff import TIFFfile, TIFFimage
import matplotlib
import numpy as np
import skfmm
from matplotlib import pyplot as plt

# from memory_profiler import profile
import gc

__version__ = '0.2.1'


def run_full_analysis_lsm_ysz(electrolyte_file,
                              electrolyte_and_pore_file,
                              electrolyte_and_lsm_file,
                              electrolyte_and_ysz_file,
                              date,
                              phase,
                              direction,
                              npzfile=None,
                              units='nm',
                              delay=0,
                              calculate_all=False,
                              load_from_prev_run=True,
                              create_hspy_sigs=True,
                              save_avizo_tiff=True,
                              tort_profile=True,
                              save_tort_prof=True,
                              in_ipython=True,
                              send_text=False,
                              text_email=None,
                              text_number=None,
                              text_carrier=None):
    """
    Run full tortuosity analysis for LSM/YSZ, calling other functions as
    necessary.

    Parameters
    ----------
    electrolyte_file: str
        Name of bulk electrolyte LabelField
    electrolyte_and_pore_file: str
        Name of LabelField containing bulk electrolyte and pore
    electrolyte_and_lsm_file: str
        Name of LabelField containing bulk electrolyte and LSM
    electrolyte_and_ysz_file: str
        Name of LabelField containing bulk electrolyte and YSZ
    date: str
        date string to be used in output filenames
    phase: str
        phase label to be used in output filenames
    direction: str
        direction of analysis ('x', 'y', or 'z')
    npzfile: str or None
        filename of previously saved data to use (if loading from disk)
    units: str
        units for labeling purpose
    delay: int
        delay to wait before running analysis (useful if running more than
        one at a time)
    calculate_all: bool
        flag to indicate that geodesic distance etc. should be calculated
        from scratch (takes a while)
    load_from_prev_run: bool
        flag to indicate that data should be loaded from disk, using the
        file specified in ``npzfile``
    create_hspy_sigs: bool
        flag to indicate if hyperspy signals should be created (to help
        visualize the results)
    save_avizo_tiff: bool

    tort_profile: bool

    save_tort_prof: bool

    in_ipython: bool
        flag to control if notifications from ipython will be shown.
        Requires the "Notifyme!" `extension <https://gist.github.com/jat255/bde
        d66839b424e20eb8bd1dc2336f841>`_
    send_text: bool
        flag to control if text should be sent (requires |texting|_ and
        |keyring|_ packages)
    text_email: string
        email address to send text from (see |textingTextServer|_)
    text_number: string
        number to send text to (see |textingTextServer|_)
    text_carrier: string
        carrier of number to send to (see |textingTextServer|_)

    Returns
    -------
    results: dict
        results is a dictionary containing all the various parameters that
        were calculated during the analysis

    Notes
    -----
    To authenticate your email server and store the password in your local
    keyring, run the following before trying to send texts:

    >>> import keyring
    ... keyring.set_password('python_TextServer', emailaddress, password)

    Examples
    --------

    >>> res = run_full_analysis_lsm_ysz(electrolyte_file="bulkYSZ.tif",
    ...                                 electrolyte_and_pore_file="bulkYSZandPRE.tif",
    ...                                 electrolyte_and_lsm_file="bulkYSZandLSM.tif",
    ...                                 electrolyte_and_ysz_file="bulkYSZandYSZ.tif",
    ...                                 date='2015-05-06',
    ...                                 phase='Pore',
    ...                                 direction='x',
    ...                                 npzfile=None,
    ...                                 units='nm',
    ...                                 delay=0,
    ...                                 calculate_all=True,
    ...                                 load_from_prev_run=False,
    ...                                 create_hspy_sigs=True,
    ...                                 save_avizo_tiff=True,
    ...                                 tort_profile=True,
    ...                                 save_tort_prof=True,
    ...                                 in_ipython=False,
    ...                                 send_text=True,
    ...                                 text_email="email@server.com",
    ...                                 text_number="8008675309",
    ...                                 text_carrier="verizon")

    .. |texting| replace:: ``texting``
    .. _texting: https://bitbucket.org/jat255/jat255-python-modules/src/09e8acf65230dd3f84df8b25f84000d2eec02755/texting/?at=master
    .. |keyring| replace:: ``keyring``
    .. _keyring: https://pypi.python.org/pypi/keyring
    .. |textingTextServer| replace:: ``texting.TextServer``
    .. _textingTextServer: https://bitbucket.org/jat255/jat255-python-modules/src/09e8acf65230dd3f84df8b25f84000d2eec02755/texting/texting/texting.py?at=master&fileviewer=file-view-default#texting.py-7

    """
    # Dictionary for phase -> filename mapping:
    filedict = {'Pore':electrolyte_and_pore_file,
                'LSM':electrolyte_and_lsm_file,
                'YSZ':electrolyte_and_ysz_file}

    # Check to make sure that both calculate and load options are specified
    if calculate_all:
        if load_from_prev_run:
            print("Both loading and calculating were specified. Calculating "
                  "is given preference, so data will not be loaded from disk.")
            sys.stdout.flush()
        load_from_prev_run = False

    # Dictionary to hold all the results
    results = {}

    # Imports
    if in_ipython:
        from IPython import get_ipython
        ipython = get_ipython()

        ipython.magic('load_ext notifyme')
        ipython.magic('notifysound default')

    if send_text:
        try:
            # noinspection PyUnresolvedReferences
            from texting.texting import TextServer
            txt_srv = TextServer(text_email, text_number, text_carrier)
        except ImportError as e:
            print('Could not import texting library. Is it installed?')
            send_text = False

    def get_time():
        return time.time()

    def done_text_send(text_start_time, text_end_time, process):
        """
        Send a text message with descriptive information about calculation
        times using the ``TextServer`` class

        Parameters
        ----------
        text_start_time: datetime.time object
            Starting time of interval
        text_end_time: datetime.time object
            Ending time of interval
        process: str
            Descriptive string to include in the message (usually what the
            name of the process was)
        """
        time_used = text_end_time - text_start_time
        hours_hold = int(time_used / 3600)
        minutes_hold = int(time_used / 60 - int(hours_hold * 60))
        seconds_hold = int(time_used - int(minutes_hold * 60))
        formatted_time = str(hours_hold).zfill(2) + ':' + str(
            minutes_hold).zfill(2) + ':' + str(seconds_hold).zfill(2)
        #
        msg = ('\nDONE\nProcess: ' + str(process) + '\nTime required: ' +
               str(formatted_time))

        # The actual mail send
        txt_srv.send_message(msg)

    # Delay (if requested):
    import time
    if delay > 0:
        print("Waiting %i seconds before running..." % delay)
        time.sleep(delay)

    # Calculating geodesic, euclidean, and tortuosity
    if calculate_all:
        fn_string = 'tortuosity_from_labels_' + direction
        fn = globals()[fn_string]
        print("Cathode data file is " + filedict[phase])
        sys.stdout.flush()

        start_time = get_time()
        g, e, t, d = fn(electrolyte_file,
                        filedict[phase],
                        phase,
                        units=units,
                        save_output=False,
                        print_output=True)
        results['g'] = g
        results['e'] = e
        results['t'] = t
        results['d'] = d
        print("Data stored in keys \'g\', \'e\', \'t\', and \'d\'")
        print("")
        if in_ipython:
            ipython.magic('notifyme $phase - $direction completed')
        if send_text:
            done_text_send(start_time,
                           get_time(),
                           phase + '-' + direction + ' done')

    # Saving results:
    if calculate_all:
        print("Saving results to disk...")
        sys.stdout.flush()
        start_time = get_time()
        save_results(fname=None,
                     geo_d=g,
                     euc_d=e,
                     tort=t,
                     desc=d,
                     phase=phase,
                     direction=direction)
        if in_ipython:
            ipython.magic('notifyme $phase - $direction saved')
        if send_text:
            done_text_send(start_time,
                           get_time(),
                           phase + '-' + direction + ' saved')

    # Loading data (after, instead of calculating from scratch):
    if load_from_prev_run:
        if npzfile is None:
            print("No .npz file was supplied for loading...")
            raise ValueError('npzfile not defined')
        print("Loading data from previous run...")
        sys.stdout.flush()
        g, e, t, d = load_results(npzfile)
        print("Old data loaded from " + npzfile)
        results['g'] = g
        results['e'] = e
        results['t'] = t
        results['d'] = d
        print("Stored in keys \'g\', \'e\', \'t\', and \'d\'")
        print("")
        sys.stdout.flush()

    # Visualizing results (requires hyperspy):
    if create_hspy_sigs:
        import hyperspy.signals as signals

        g_s = signals.Image(g)
        g_s.metadata.General.title = phase + "_" + direction + " Geodesic"

        e_s = signals.Image(e)
        e_s.metadata.General.title = phase + "_" + direction + " Euclidean"

        t_s = signals.Image(t)
        t_s.metadata.General.title = phase + "_" + direction + " Tortuosity"

        # for i in [g_s, e_s, t_s]:
        #   i.plot()

        results['g_s'] = g_s
        results['e_s'] = e_s
        results['t_s'] = t_s
        print("Hyperspy signals are in values \'g_s\', \'e_s\', and \'t_s\'")
        print("")
        sys.stdout.flush()

    # Saving as tiff for Avizo:
    if save_avizo_tiff:
        save_as_tiff(date + "_" + phase + "_" + direction + "-tort.tif",
                     t,
                     'float32',
                     d)
        print("")
        sys.stdout.flush()

    # Average tortuosity profile:
    if tort_profile:
        print("Calculating average tortuosity profile")
        sys.stdout.flush()

        t_avg, e_avg = tortuosity_profile(t,
                                          e,
                                          axis=direction)
        f = plot_tort_prof(t_avg,
                           e_avg,
                           direction,
                           sns_fontscale=2,
                           sns_color_num=1)
        plt.tight_layout()
        matplotlib.rc('image', cmap='gray')

        results['f'] = f
        results['t_avg'] = t_avg
        results['e_avg'] = e_avg
        print("Average tortuosity plot is in variable \'f\', profiles are "
              "in \'t_avg\' and \'e_avg\'")
        print("")
        sys.stdout.flush()

    # Save profile to disk:
    if save_tort_prof:
        save_profile_to_csv(date + '_' +
                            phase + '_' +
                            direction + '-tort-profile.csv',
                            e_avg / 1000,  # divide by 1000 to get microns
                            t_avg,
                            direction,
                            phase)

    return results


def calculate_geodesic_distance(electrolyte_fname,
                                phase_fname,
                                units='nm',
                                print_output=True,
                                ):
    """
    Calculate the geodesic distance of an indexed tif file.

    .. note:: Deprecated. This function will work, but it is better to use
              :func:`tortuosity_from_labels_x`,
              :func:`tortuosity_from_labels_y`,
              and :func:`tortuosity_from_labels_z`.

    Parameters
    ----------
    electrolyte_fname: str
        Filename of a 3D tiff file that contains only the bulk electrolyte
        labelfield (as 1 values)
    phase_fname: str
        Filename of a 3D tiff file that contains the bulk electrolyte and the
        phase for which the geodesic distance is to be calculated
    units: str
        units of the given dimensions
    print_output: bool
        switch to control whether output is printed

    Returns
    -------
    d: np.array
        Numpy array with geodesic distance from supplied surface
    desc: str
        description string to be used when saving the file (for proper
        reading into Avizo)
    """

    # Load electrolyte data
    electrolyte_tif = TIFFfile(electrolyte_fname)
    electrolyte_array = electrolyte_tif.get_tiff_array()
    electrolyte_data = electrolyte_array[::].astype('int8')
    if print_output:
        print('Loaded electrolyte data.')

    # Load phase to be calculated data
    cathode_tif = TIFFfile(phase_fname)
    cathode_array = cathode_tif.get_tiff_array()
    cathode_data = cathode_array[::].astype('int8')
    if print_output:
        print('Loaded cathode data.')

    # Get information from Avizo-saved tiff file
    ifd = electrolyte_tif.get_first_ifd()
    size_x = ifd.get_value('ImageWidth')
    size_y = ifd.get_value('ImageLength')
    size_z = electrolyte_tif.get_depth()
    image_description = ifd.get_value('ImageDescription')
    if print_output:
        print('ImageDescription is: {}'.format(image_description))

    # Calculate some parameters from the image input
    bb_xmin, bb_xmax, bb_ymin, bb_ymax, bb_zmin, bb_zmax = \
        [eval(i) for i in image_description.split()[1:]]
    bound_x = bb_xmax - bb_xmin
    bound_y = bb_ymax - bb_ymin
    bound_z = bb_zmax - bb_zmin
    if print_output:
        print("Bounding box dimensions are: ({0:.2f}, {1:.2f}, "
              "{2:.2f})".format(bound_x, bound_y, bound_z) + " " + units)

    vox_x = (bb_xmax - bb_xmin) / float(size_x - 1)
    vox_y = (bb_ymax - bb_ymin) / float(size_y - 1)
    vox_z = (bb_zmax - bb_zmin) / float(size_z - 1)
    if print_output:
        print("Voxel dimensions are: ({0:.2f}, {1:.2f}, "
              "{2:.2f})".format(vox_x, vox_y, vox_z) + " " + units)

    # Switch electrolyte tag (1) to a negative value to create zero-contour
    cathode_data[electrolyte_data == 1] = -1

    # Mask the voxels where phase is not present:
    mask = cathode_data == 0
    cathode_data = np.ma.MaskedArray(cathode_data, mask)

    # Do geodesic distance calculation
    start_time = datetime.now()
    if print_output:
        print('Starting calculation at: {}'.format(start_time))
    # Calculate geodesic distance:
    d = skfmm.distance(cathode_data, dx=[vox_z, vox_y, vox_x])
    end_time = datetime.now()
    if print_output:
        print('Calculation took: {}'.format(end_time - start_time))

    # Set distances within the bulk electrolyte to zero:
    # d.data[electrolyte_data == 1] = 0

    return d.data, image_description


def tortuosity_from_labels_x(electrolyte_fname,
                             phase_fname,
                             phase,
                             units='nm',
                             print_output=True,
                             save_output=False):
    """
    Calculate the tortuosity (normal to electrolyte interface, x-direction)
    from supplied label fields

    Parameters
    ----------
    electrolyte_fname: str
        Filename of a 3D tiff file that contains only the bulk electrolyte
        labelfield (as 1 values)
    phase_fname: str
        Filename of a 3D tiff file that contains the bulk electrolyte and the
        phase for which the geodesic distance is to be calculated
    phase: str
        Phase that is being calculated. i.e. 'pore', 'LSM', 'YSZ', etc.
    units: str
        units of the given dimensions
    print_output: bool
        switch to control whether output is printed
    save_output: bool
        switch to control whether data is saved to .npy files for later recall

    Returns
    --------
    geo_d: np.array
        Numpy array with geodesic distance from supplied surface
    euc_d: np.array
        Numpy array with euclidean distance from electrolyte
    tort: np.array
        Numpy array with tortuosity at each point
    desc: str
        description string to be used when saving the file (for proper
        reading into Avizo)
    """

    if print_output:
        print('Starting calculation on ' + phase + ' in x direction.')
        sys.stdout.flush()

    global_start_time = datetime.now()

    # Load electrolyte data
    start_time = datetime.now()
    electrolyte_tif = TIFFfile(electrolyte_fname)
    electrolyte_array = electrolyte_tif.get_tiff_array()
    electrolyte_data = electrolyte_array[::].astype('int8')
    end_time = datetime.now()
    if print_output:
        print('Loaded electrolyte data in {} seconds.'.format(end_time -
                                                              start_time))
        sys.stdout.flush()

    # Load phase to be calculated data
    start_time = datetime.now()
    cathode_tif = TIFFfile(phase_fname)
    cathode_array = cathode_tif.get_tiff_array()
    cathode_data = cathode_array[::].astype('int8')
    end_time = datetime.now()
    if print_output:
        print('Loaded cathode data in {} seconds.'.format(end_time -
                                                          start_time))
        sys.stdout.flush()

    # Get information from Avizo-saved tiff file
    ifd = electrolyte_tif.get_first_ifd()
    size_x = ifd.get_value('ImageWidth')
    size_y = ifd.get_value('ImageLength')
    size_z = electrolyte_tif.get_depth()
    image_description = ifd.get_value('ImageDescription')
    if print_output:
        print('ImageDescription is: {}'.format(image_description))
        sys.stdout.flush()

    # Calculate some parameters from the image input
    bb_xmin, bb_xmax, bb_ymin, bb_ymax, bb_zmin, bb_zmax = \
        [eval(i) for i in image_description.split()[1:]]
    bound_x = bb_xmax - bb_xmin
    bound_y = bb_ymax - bb_ymin
    bound_z = bb_zmax - bb_zmin
    if print_output:
        print("Bounding box dimensions are: ({0:.2f}, {1:.2f}, "
              "{2:.2f})".format(bound_x, bound_y, bound_z) + " " + units)
        sys.stdout.flush()

    vox_x = (bb_xmax - bb_xmin) / float(size_x - 1)
    vox_y = (bb_ymax - bb_ymin) / float(size_y - 1)
    vox_z = (bb_zmax - bb_zmin) / float(size_z - 1)
    if print_output:
        print("Voxel dimensions are: ({0:.2f}, {1:.2f}, "
              "{2:.2f})".format(vox_x, vox_y, vox_z) + " " + units)
        sys.stdout.flush()

    # Switch electrolyte tag (1) to a negative value to create zero-contour
    cathode_data[electrolyte_data == 1] = -1

    # Mask the voxels where phase is not present:
    cathode_mask = cathode_data == 0

    cathode_ma = np.ma.MaskedArray(cathode_data, cathode_mask)
    del cathode_mask
    gc.collect()

    # Do geodesic distance calculation
    start_time = datetime.now()
    if print_output:
        print('Starting geodesic calculation at: {}'.format(start_time))
        sys.stdout.flush()
    geo_d = _geo_dist(cathode_ma, vox_x, vox_y, vox_z)
    end_time = datetime.now()
    if print_output:
        print('Geodesic calculation took: {}'.format(end_time -
                                                     start_time))
        sys.stdout.flush()

    # Calculating zero reference for each [x,y] point for euclidean distance
    start_time = datetime.now()
    x_interface = _calc_interface(electrolyte_data)
    end_time = datetime.now()
    if print_output:
        print("Calculating zero distance interface took: "
              "{}".format(end_time - start_time))
        sys.stdout.flush()

    # Calculate euclidean distance
    start_time = datetime.now()
    # noinspection PyTypeChecker
    euc_d = _calc_euc_x(x_interface, electrolyte_data, vox_x)
    end_time = datetime.now()
    if print_output:
        print("Calculating euclidean distance took: {}".format(end_time -
                                                               start_time))
        sys.stdout.flush()

    # Calculate tortuosity
    start_time = datetime.now()
    tort = _calc_tort(geo_d, euc_d, electrolyte_data)
    end_time = datetime.now()
    if print_output:
        print("Calculating tortuosity took: {}".format(end_time - start_time))
        sys.stdout.flush()

    start_time = datetime.now()
    if save_output:
        if print_output:
            print("Saving data...")
            sys.stdout.flush()
        save_results(fname=None,
                     direction='x',
                     phase=phase,
                     geo_d=geo_d.data,
                     euc_d=euc_d,
                     tort=tort.data,
                     desc=image_description)
        end_time = datetime.now()
        if print_output:
            print("Saving data took: {}".format(end_time - start_time))
            sys.stdout.flush()

    end_time = datetime.now()
    if print_output:
        print("Total execution time was: {}".format(end_time -
                                                    global_start_time))
        sys.stdout.flush()

    return geo_d.data, euc_d, tort.data, image_description


# @profile
def tortuosity_from_labels_y(electrolyte_fname,
                             phase_fname,
                             phase,
                             units='nm',
                             print_output=True,
                             save_output=False):
    """
    Calculate the tortuosity (parallel to electrolyte interface, y-direction)
    from supplied label fields

    Parameters
    ----------
    electrolyte_fname: str
        Filename of a 3D tiff file that contains only the bulk electrolyte
        labelfield (as 1 values)
    phase_fname: str
        Filename of a 3D tiff file that contains the bulk electrolyte and the
        phase for which the geodesic distance is to be calculated
    phase: str
        Phase that is being calculated. i.e. 'pore', 'LSM', 'YSZ', etc.
    units: str
        units of the given dimensions
    print_output: bool
        switch to control whether output is printed
    save_output: bool
        switch to control whether data is saved to .npy files for later recall

    Returns
    --------
    geo_d: np.array
        Numpy array with geodesic distance from supplied surface
    euc_d: np.array
        Numpy array with euclidean distance from electrolyte
    tort: np.array
        Numpy array with tortuosity at each point
    desc: str
        description string to be used when saving the file (for proper
        reading into Avizo)
    """

    global_start_time = datetime.now()

    if print_output:
        print('Starting calculation on ' + phase + ' in y direction.')
        sys.stdout.flush()

    # Load electrolyte data
    start_time = datetime.now()
    electrolyte_tif = TIFFfile(electrolyte_fname)
    electrolyte_array = electrolyte_tif.get_tiff_array()
    electrolyte_data = electrolyte_array[::].astype('int8')
    end_time = datetime.now()
    if print_output:
        print('Loaded electrolyte data in {} seconds.'.format(end_time -
                                                              start_time))
        sys.stdout.flush()

    # Load phase to be calculated data
    start_time = datetime.now()
    cathode_tif = TIFFfile(phase_fname)
    cathode_array = cathode_tif.get_tiff_array()
    cathode_data = cathode_array[::].astype('int8')
    end_time = datetime.now()
    if print_output:
        print('Loaded cathode data in {} seconds.'.format(end_time -
                                                          start_time))
        sys.stdout.flush()

    # Get information from Avizo-saved tiff file
    ifd = electrolyte_tif.get_first_ifd()
    size_x = ifd.get_value('ImageWidth')
    size_y = ifd.get_value('ImageLength')
    size_z = electrolyte_tif.get_depth()
    image_description = ifd.get_value('ImageDescription')
    if print_output:
        print('ImageDescription is: ' + image_description)
        sys.stdout.flush()

    # Calculate some parameters from the image input
    bb_xmin, bb_xmax, bb_ymin, bb_ymax, bb_zmin, bb_zmax = \
        [eval(i) for i in image_description.split()[1:]]
    bound_x = bb_xmax - bb_xmin
    bound_y = bb_ymax - bb_ymin
    bound_z = bb_zmax - bb_zmin
    if print_output:
        print("Bounding box dimensions are: ({0:.2f}, {1:.2f}, "
              "{2:.2f})".format(bound_x, bound_y, bound_z) + " " + units)
        sys.stdout.flush()

    vox_x = (bb_xmax - bb_xmin) / float(size_x - 1)
    vox_y = (bb_ymax - bb_ymin) / float(size_y - 1)
    vox_z = (bb_zmax - bb_zmin) / float(size_z - 1)
    if print_output:
        print("Voxel dimensions are: ({0:.2f}, {1:.2f}, "
              "{2:.2f})".format(vox_x, vox_y, vox_z) + " " + units)
        sys.stdout.flush()

    # Set electrolyte area to zero in cathode data
    cathode_data[cathode_data == 1] = 0

    # Mask the voxels where phase is not present:
    cathode_mask = cathode_data == 0

    # Switch XZ zero-plane to a negative value to create zero-contour
    cathode_data[:,0,:] = -1

    cathode_ma = np.ma.MaskedArray(cathode_data, cathode_mask)
    del cathode_mask
    gc.collect()

    # Do geodesic distance calculation
    start_time = datetime.now()
    if print_output:
        print('Starting geodesic calculation at: {}'.format(start_time))
        sys.stdout.flush()
    geo_d = _geo_dist(cathode_ma, vox_x, vox_y, vox_z)
    end_time = datetime.now()
    if print_output:
        print('Geodesic calculation took: {}'.format(end_time -
                                                     start_time))
        sys.stdout.flush()

    # Do not need to calculating zero reference for the y-direction (use
    # just plane)
    # start_time = datetime.now()
    # x_interface = _calc_interface(electrolyte_data)
    # end_time = datetime.now()
    # if print_output:
    #     print("Calculating zero distance interface took: "
    #           "{}".format(end_time - start_time))

    # Calculate euclidean distance
    start_time = datetime.now()

    y_interface = np.zeros_like(electrolyte_data[:,0,:], dtype=np.float32)
    euc_d = np.zeros_like(electrolyte_data, dtype=np.float32)

    for (z,x), value in np.ndenumerate(y_interface):
        # set the value at each [x,z] point to a numpy array that ranges the
        # z dimension times the vox_y size
        # so this value can be compared with that calculated geodesically
        euc_d[z,:,x] = np.arange(len(euc_d[z,:,x])) * vox_y

    euc_d[euc_d < 0] = 0    # set all negative values to zero,
    #                         since they are on the other side of the
    #                         electrolyte (probably don't need this for y-dir)
    end_time = datetime.now()
    if print_output:
        print("Calculating euclidean distance took: {}".format(end_time -
                                                               start_time))
        sys.stdout.flush()

    # Calculate tortuosity
    start_time = datetime.now()
    tort = _calc_tort(geo_d, euc_d, electrolyte_data)
    end_time = datetime.now()
    if print_output:
        print("Calculating tortuosity took: {}".format(end_time - start_time))
        sys.stdout.flush()

    start_time = datetime.now()
    if save_output:
        if print_output:
            print("Saving data...")
            sys.stdout.flush()
        save_results(fname=None,
                     direction='y',
                     phase=phase,
                     geo_d=geo_d.data,
                     euc_d=euc_d,
                     tort=tort.data,
                     desc=image_description)
        end_time = datetime.now()
        if print_output:
            print("Saving data took: {}".format(end_time - start_time))
            sys.stdout.flush()

    end_time = datetime.now()
    if print_output:
        print("Total execution time was: {}".format(end_time -
                                                    global_start_time))
        sys.stdout.flush()

    return geo_d.data, euc_d, tort.data, image_description


def tortuosity_from_labels_z(electrolyte_fname,
                             phase_fname,
                             phase,
                             units='nm',
                             print_output=True,
                             save_output=False):
    """
    Calculate the tortuosity (parallel to electrolyte interface, z-direction)
    from supplied label fields

    Parameters
    ----------
    electrolyte_fname: str
        Filename of a 3D tiff file that contains only the bulk electrolyte
        labelfield (as 1 values)
    phase_fname: str
        Filename of a 3D tiff file that contains the bulk electrolyte and the
        phase for which the geodesic distance is to be calculated
    phase: str
        Phase that is being calculated. i.e. 'pore', 'LSM', 'YSZ', etc.
    units: str
        units of the given dimensions
    print_output: bool
        switch to control whether output is printed
    save_output: bool
        switch to control whether data is saved to .npy files for later recall

    Returns
    --------
    geo_d: np.array
        Numpy array with geodesic distance from supplied surface
    euc_d: np.array
        Numpy array with euclidean distance from electrolyte
    tort: np.array
        Numpy array with tortuosity at each point
    desc: str
        description string to be used when saving the file (for proper
        reading into Avizo)
    """

    global_start_time = datetime.now()

    if print_output:
        print('Starting calculation on ' + phase + ' in z direction.')
        sys.stdout.flush()

    # Load electrolyte data
    start_time = datetime.now()
    electrolyte_tif = TIFFfile(electrolyte_fname)
    electrolyte_array = electrolyte_tif.get_tiff_array()
    electrolyte_data = electrolyte_array[::].astype('int8')
    end_time = datetime.now()
    if print_output:
        print('Loaded electrolyte data in {} seconds.'.format(end_time -
                                                              start_time))
        sys.stdout.flush()

    # Load phase to be calculated data
    start_time = datetime.now()
    cathode_tif = TIFFfile(phase_fname)
    cathode_array = cathode_tif.get_tiff_array()
    cathode_data = cathode_array[::].astype('int8')
    end_time = datetime.now()
    if print_output:
        print('Loaded cathode data in {} seconds.'.format(end_time -
                                                          start_time))
        sys.stdout.flush()

    # Get information from Avizo-saved tiff file
    ifd = electrolyte_tif.get_first_ifd()
    size_x = ifd.get_value('ImageWidth')
    size_y = ifd.get_value('ImageLength')
    size_z = electrolyte_tif.get_depth()
    image_description = ifd.get_value('ImageDescription')
    if print_output:
        print('ImageDescription is: ' + image_description)
        sys.stdout.flush()

    # Calculate some parameters from the image input
    bb_xmin, bb_xmax, bb_ymin, bb_ymax, bb_zmin, bb_zmax = \
        [eval(i) for i in image_description.split()[1:]]
    bound_x = bb_xmax - bb_xmin
    bound_y = bb_ymax - bb_ymin
    bound_z = bb_zmax - bb_zmin
    if print_output:
        print("Bounding box dimensions are: ({0:.2f}, {1:.2f}, "
              "{2:.2f})".format(bound_x, bound_y, bound_z) + " " + units)
        sys.stdout.flush()

    vox_x = (bb_xmax - bb_xmin) / float(size_x - 1)
    vox_y = (bb_ymax - bb_ymin) / float(size_y - 1)
    vox_z = (bb_zmax - bb_zmin) / float(size_z - 1)
    if print_output:
        print("Voxel dimensions are: ({0:.2f}, {1:.2f}, "
              "{2:.2f})".format(vox_x, vox_y, vox_z) + " " + units)
        sys.stdout.flush()

    # Set electrolyte area to zero in cathode data
    cathode_data[cathode_data == 1] = 0

    # Mask the voxels where phase is not present:
    cathode_mask = cathode_data == 0

    # Switch XY zero-plane to a negative value to create zero-contour
    cathode_data[0,:,:] = -1

    cathode_ma = np.ma.MaskedArray(cathode_data, cathode_mask)
    del cathode_mask
    gc.collect()
    
    # Do geodesic distance calculation
    start_time = datetime.now()
    if print_output:
        print('Starting geodesic calculation at: {}'.format(start_time))
        sys.stdout.flush()
    geo_d = _geo_dist(cathode_ma, vox_x, vox_y, vox_z)
    end_time = datetime.now()
    if print_output:
        print('Geodesic calculation took: {}'.format(end_time -
                                                     start_time))
        sys.stdout.flush()

    # Do not need to calculating zero reference for the y-direction (use
    # just plane)
    # start_time = datetime.now()
    # x_interface = _calc_interface(electrolyte_data)
    # end_time = datetime.now()
    # if print_output:
    #     print("Calculating zero distance interface took: "
    #           "{}".format(end_time - start_time))

    # Calculate euclidean distance
    start_time = datetime.now()

    z_interface = np.zeros_like(electrolyte_data[0,:,:], dtype=np.float32)
    euc_d = np.zeros_like(electrolyte_data, dtype=np.float32)

    for (y,x), value in np.ndenumerate(z_interface):
        # set the value at each [x,z] point to a numpy array that ranges the
        # z dimension times the vox_z size
        # so this value can be compared with that calculated geodesically
        euc_d[:,y,x] = np.arange(len(euc_d[:,y,x])) * vox_z

    euc_d[euc_d < 0] = 0    # set all negative values to zero,
    #                         since they are on the other side of the
    #                         electrolyte (probably don't need this for y-dir)
    end_time = datetime.now()
    if print_output:
        print("Calculating euclidean distance took: {}".format(end_time -
                                                               start_time))
        sys.stdout.flush()

    # Calculate tortuosity
    start_time = datetime.now()
    tort = _calc_tort(geo_d, euc_d, electrolyte_data)
    end_time = datetime.now()
    if print_output:
        print("Calculating tortuosity took: {}".format(end_time - start_time))
        sys.stdout.flush()

    start_time = datetime.now()
    if save_output:
        if print_output:
            print("Saving data...")
            sys.stdout.flush()
        save_results(fname=None,
                     direction='z',
                     phase=phase,
                     geo_d=geo_d.data,
                     euc_d=euc_d,
                     tort=tort.data,
                     desc=image_description)
        end_time = datetime.now()
        if print_output:
            print("Saving data took: {}".format(end_time - start_time))
            sys.stdout.flush()

    end_time = datetime.now()
    if print_output:
        print("Total execution time was: {}".format(end_time -
                                                    global_start_time))
        sys.stdout.flush()

    return geo_d.data, euc_d, tort.data, image_description


def save_results(fname=None,
                 phase="",
                 direction="",
                 geo_d=None,
                 euc_d=None,
                 tort=None,
                 desc=None):
    """
    Saves all the results into a compressed numpy archive

    Parameters
    -----------
    geo_d: numpy array
        Geodesic distance array
    euc_d: numpy array
        Euclidean distance array
    tort: numpy array
        Tortuosity array
    desc: str
        Image description string
    """
    if fname is None:
        fname = time.strftime("%Y-%m-%d_%H.%M.%S_" + phase + '_' + direction +
                              '_all-results.npz')

    np.savez_compressed(fname,
                        geo_d=geo_d,
                        euc_d=euc_d,
                        tort=tort,
                        image_description=desc
                        )

    print("Saved results to " + fname)


def load_results(fname):
    """
    Loads the results that have been previously saved with :func:`save_results`

    Parameters
    -----------
    fname: str
        filename to load

    Returns
    --------
    geo_d: numpy array
        Geodesic distance array
    euc_d: numpy array
        Euclidean distance array
    tort: numpy array
        Tortuosity array
    desc: str
        Image description string
    """
    npzfile = np.load(fname)
    geo_d = npzfile['geo_d']
    euc_d = npzfile['euc_d']
    tort = npzfile['tort']
    desc = npzfile['image_description']

    # if description isn't None, cast it as string
    if desc.dtype != 'O':
        desc = str(desc)

    return geo_d, euc_d, tort, desc


def tortuosity_profile(tort, euc, axis='x'):
    """
    Calculate the average tortuosity along an axis

    Parameters
    ----------
    tort: Numpy array (output of :func:`tortuosity_from_labels_x`...)
        Contains the tortuosity data, with 0 values in the masked areas
    euc: Numpy array (output of :func:`tortuosity_from_labels_x`...)
        Contains the euclidean distance at each point
    axis: str
        Axis along which to calculate profile. Should be 'x', 'y', or 'z'

    Returns
    -------
    tort_prof: 1D Numpy array
        1D profile of average tortuosity at each point in the array
        (ignoring the masked areas)
    euc_prof: 1D Numpy array
        1D profile of the average euclidean distance at each point
    """

    # Set all 0 tortuosity values to nans so they are ignored when calculating
    # the average:
    tort[tort == 0] = np.nan

    axis_dict = {'x':2, 'y':1, 'z':0}

    # Figure out the correct axis:
    axes = [0, 1, 2]
    axes.remove(axis_dict[axis])
    axes = tuple(axes)

    # Calculate averages along relevant axes (ignoring nans):
    euc_prof = np.nanmean(euc, axis=axes)
    tort_prof = np.nanmean(tort, axis=axes)

    return tort_prof, euc_prof


def plot_tort_prof(tort_prof,
                   euc_prof,
                   direction,
                   units='nm',
                   figsize=None,
                   sns_style='white',
                   sns_context='paper',
                   sns_fontscale=1.5,
                   sns_cmap=None,
                   sns_color_num=0,
                   sns_kw=None,):
    """
    Plot a profile of the average tortuosity.

    Parameters
    ----------
    tort_prof: np.array
        tortuosity profile (output of :func:`tortuosity_profile`)
    euc_prof: np.array
        euclidean profile (output of :func:`tortuosity_profile`)
    direction: str
        direction for labeling
    units: str
        units of distance for labeling
    figsize : tuple of integers, optional, default: None
        width, height in inches. If not provided, defaults to rc
        figure.figsize.
    sns_style: str
        default style for seaborn ('white', 'dark', 'darkgrid', etc.)
    sns_context: str
        context for plotting with seaborn
    sns_fontscale: float
        font scale to pass to seaborn
    sns_cmap: list, str, tuple
        colormap for use with seaborn
        default is [light blue, dark teal, blue, red, green, orange]
        If str or tuple, then these parameters are passed to the
        seaborn.color_palette() function
    sns_color_num: int
        index of color (in ``sns_cmap``) to use
    sns_kw: dict
        additional arguments to be passed to seaborn.set_style
        (see http://goo.gl/WvLdc6 for details)

    Returns
    -------
    matplotlib figure, <matplotlib axes>
        Handle to figure that is plotted (and axes array if subplots)
    """
    # Import and setup seaborn styles
    if sns_kw is None:
        sns_kw = {}
    if sns_cmap is None:
        sns_cmap = ["#4C72B1", "#004040", "#023FA5", "#8E063B",
                    "#098C09", "#EF9708"]
    import seaborn as sns
    matplotlib.rcParams['mathtext.fontset'] = 'stixsans'
    sns.set(rc={'image.cmap': 'Greys_r'})
    sns.set_style(sns_style, sns_kw)
    sns.set_context(sns_context, font_scale=sns_fontscale)
    if type(sns_cmap) is tuple:
        palette = sns.color_palette(*sns_cmap)
    else:
        palette = sns.color_palette(sns_cmap)
    sns.color_palette(palette)

    if units is 'um':
        units = "${\mu}m$"

    fig = plt.figure(figsize=figsize)
    plt.plot(euc_prof, tort_prof, color=palette[sns_color_num])
    plt.xlabel('Euclidean distance (' + direction + " direction, " +
               units + ")")
    plt.ylabel("Average tortuosity")
    plt.tight_layout()

    return fig


def save_profile_to_csv(fname,
                        x,
                        y,
                        direction,
                        phase,
                        x_name='Euc_d',
                        y_name='tort',
                        fmt='%10.5f',
                        delimiter=',',
                        ):
    """
    Saves two profiles (x and y) into a text file.

    Parameters
    ----------
    fname: str
        filename to save to (no checks are done before overwriting)
    x: 1D np.array
        X-profile that will be used as first column
        should be a one dimensional numpy row vector
    y: np.array or list of np.arrays
        can be 1D np.array, or a list of them, with data in rows.
        Each row will be transformed to a column in the text files
    direction: str
        direction for labeling
    phase: str
        phase for labeling
    x_name: str
        Name of header in x-column
    y_name: str
        Name of header in y-column
    fmt: str
        Format for decimals to use
    delimiter: str
        Delimiter to use in the csv file
    """
    np.savetxt(fname, np.vstack((x,y)).transpose(),
               header=phase + " " + direction + "-direction \n" + x_name +
                      delimiter + '\t' + y_name,
               fmt=fmt,
               delimiter=delimiter)
    print('Saved', fname)


def load_profile_from_csv(fname,
                          delimiter=',',
                          skiprows=2):
    """
    Loads columns of a text file into 1D numpy arrays.

    Parameters
    ----------
    fname: str
        filename to load from
    delimiter: str
        character to use as delimiter
    skiprows: int
        number of header rows to skip at beginning of file

    Returns
    --------
    list of 1D np.array objects, 1 for each column in the data
    """
    data = np.loadtxt(fname,
                      delimiter=delimiter,
                      skiprows=skiprows).transpose()
    return [i[0] for i in np.vsplit(data, len(data))]


def save_as_tiff(fname, data, dtype, desc):
    """
    Save a numpy array as tiff (useful for transferring data back to Avizo)

    Parameters
    ----------
    fname: str
        Filename to save to
    data: np.array
        Data array to be written to image file
    dtype: str
        data type to save as. For some reason, euclidean distance works
        best as 'uint32', while the others are fine as 'float32'.
    desc: str
        Image description that includes bounding box info
    """
    tiff = TIFFimage(data.astype(dtype),
                     description=desc)
    tiff.write_file(fname, compression='lzw')


def _geo_dist(data, vox_x, vox_y, vox_z):
    """
    Internal helper method to call scikit-fmm distance method

    Parameters
    ----------
    data: masked data array to calculate on
    vox_x: x voxel size
    vox_y: y voxel size
    vox_z: z voxel size

    Returns
    -------
    d: distance transform as calculated by scikit-fmm
    """
    d = skfmm.distance(data, dx=[vox_z, vox_y, vox_x])

    # Convert dtype from float64 to float32 to save memory (almost half):
    d = np.ma.asarray(d, dtype='float32')

    # Set distances within the bulk electrolyte to zero:
    d.data[d.data < 0] = 0
    return d


def _calc_interface(electrolyte_data):
    """
    Calculates interface between bulk electrolyte and the cathode

    Parameters
    ----------
    electrolyte_data: label data for bulk electrolyte

    Returns
    -------
    x_interface: 2D numpy array
        x values of interface at each y and z locations
    """
    # create a single plane array with same x and y dimensions
    x_interface = np.zeros_like(electrolyte_data[:, :, 0], dtype=int)
    # visit each point on the array
    for (x, y), value in np.ndenumerate(x_interface):
        # set the value at each point to the first place where the electrolyte
        # value is 0 (which is the boundary between electrolyte and cathode)
        x_interface[x, y] = np.where(electrolyte_data[x, y, :] == 0)[0][0]

    return x_interface


def _calc_tort(geo_d, euc_d, electrolyte_data):
    """
    Calculates tortuosity from geodesic and euclidean distances

    Parameters
    ----------
    geo_d: Geodesic distance (Masked Array)
    euc_d: Euclidean distance (Numpy array)
    electrolyte_data: label data for bulk electrolyte

    Returns
    -------
    tort: tortuosity numpy array
    """

    old = np.seterr(divide='ignore')

    # Calculate tortuosity by dividing geo_d by euc_d
    tort = np.divide(geo_d, euc_d)
    # Clean up the data, removing values < 1 and any infinities
    tort[electrolyte_data == 1] = 0     # 0 so it will be ignored in bulk YSZ
    tort[np.logical_and(tort < 1, tort > 0)] = 1
    tort[np.isinf(tort)] = 1
    tort[np.isnan(tort)] = 1

    # tort should never be very large (greater than 2), so we can
    # safely represent it with a half precision float
    # 53.7MiB before, 44.0MiB after, so saving 18%
    # tort = np.ma.asarray(tort, dtype='float16')

    np.seterr(**old)

    return tort


def _calc_euc_x(x_interface, electrolyte_data, vox_x):
    """
    Calculates euclidean distance from electrolyte interface

    Parameters
    ----------
    x_interface: Numpy array containing x value of boundary for electrolyte
        for all y and z coordinates
    electrolyte_data: label data for bulk electrolyte
    vox_x: float
        voxel x-size

    Returns
    -------
    euc_d: euclidean distance numpy array
    """
    # create euclidean distance array of the same shape as the others
    euc_d = np.zeros_like(electrolyte_data, dtype=np.float32)
    # visit each [x,y] location in this array:
    for (x,y), value in np.ndenumerate(x_interface):
        # set the value at each [x,y] point to a numpy array that ranges the
        # x dimension minus the zero reference from before times the vox_x size
        # so this value can be compared with that calculated geodesically
        euc_d[x,y] = (np.arange(len(euc_d[x,y])) - x_interface[x,y]) * vox_x

    euc_d[euc_d < 0] = 0    # set all negative values to zero,
    #                         since they are on the other side of the
    #                         electrolyte

    return euc_d

    # How to create multiple processes for jobs:
    ############################################
    #
    # # Setup parallel stuff:
    # manager = multiprocessing.Manager()
    # return_dict = manager.dict()
    # jobs = []
    #
    # Calculate geodesic distance:
    # p = multiprocessing.Process(target=_geo_dist, args=('geo',
    #                                                     return_dict,
    #                                                     cathode_data,
    #                                                     vox_x,
    #                                                     vox_y,
    #                                                     vox_z))
    # jobs.append(p)
    # p.start()
    # if print_output:
    #     print('Started geo calc')
    #
    # Calculate euclidean distance:
    # p = multiprocessing.Process(target=_geo_dist, args=('euc',
    #                                                     return_dict,
    #                                                     all_data,
    #                                                     vox_x,
    #                                                     vox_y,
    #                                                     vox_z))
    # jobs.append(p)
    # p.start()
    # if print_output:
    #     print('Started euc calc')
    #
    # if print_output:
    #     print('Jobs list:' + repr(jobs))
    #
    # for proc in jobs:
    #     proc.join()
    #
    # geo_d = return_dict['geo']
    # euc_d = return_dict['euc']
