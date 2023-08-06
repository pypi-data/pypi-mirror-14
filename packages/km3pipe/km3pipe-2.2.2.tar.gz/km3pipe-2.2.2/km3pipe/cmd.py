# coding=utf-8
# Filename: cmd.py
"""
KM3Pipe command line utility.

Usage:
    km3pipe test
    km3pipe tohdf5 [-s] -i FILE -o FILE
    km3pipe (-h | --help)
    km3pipe --version

Options:
    -h --help  Show this screen.
    -i FILE    Input file.
    -o FILE    Output file.
    -s         Write each event in a separate dataset.

"""
from __future__ import division, absolute_import, print_function

from km3pipe import version


def tohdf5(input_file, output_file, separate_events=False):
    """Convert ROOT file to HDF5 file"""
    from km3pipe import Pipeline  # noqa
    from km3pipe.pumps import AanetPump, HDF5Sink, HDF5Sink2  # noqa

    sink = HDF5Sink2 if separate_events else HDF5Sink

    pipe = Pipeline()
    pipe.attach(AanetPump, filename=input_file)
    pipe.attach(sink,
                filename=output_file,
                separate_events=separate_events)
    pipe.drain()


def main():
    from docopt import docopt
    arguments = docopt(__doc__, version=version)

    if arguments['tohdf5']:
        tohdf5(arguments['-i'], arguments['-o'], arguments['-s'])
