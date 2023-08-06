# coding=utf-8
# Filename: hdf5.py
# pylint: disable=C0103,R0903
"""
Pumps for the EVT simulation dataformat.

"""
from __future__ import division, absolute_import, print_function

from collections import defaultdict
import os.path

try:
    import pandas as pd
except ImportError:
    print("The HDF5 pump needs pandas: pip install pandas")

try:
    import numpy as np
except ImportError:
    print("The HDF5 Bucket needs numpy: pip install numpy")

try:
    import h5py
except ImportError:
    print("The HDF5 Sink and Bucket need h5py: pip install h5py")


from km3pipe import Pump, Module
from km3pipe.dataclasses import HitSeries
from km3pipe.logger import logging

log = logging.getLogger(__name__)  # pylint: disable=C0103

__author__ = 'tamasgal'


class HDF5Pump(Pump):
    """Provides a pump for KM3NeT HDF5 files"""
    def __init__(self, **context):
        super(self.__class__, self).__init__(**context)
        self.filename = self.get('filename')
        if os.path.isfile(self.filename):
            self._h5file = h5py.File(self.filename)
            try:
                self._n_events = len(self._h5file['/event'])
            except KeyError:
                raise KeyError("No events found.")
        else:
            raise IOError("No such file or directory: '{0}'"
                          .format(self.filename))
        self.index = None
        self._reset_index()

    def process(self, blob):
        try:
            blob = self.get_blob(self.index)
        except KeyError:
            self._reset_index()
            raise StopIteration
        self.index += 1
        return blob

    def get_blob(self, index):
        blob = {}
        n_event = index + 1
        raw_hits = self._h5file.get('/event/{0}/hits'.format(n_event))
        blob['Hits'] = HitSeries.from_hdf5(raw_hits)
        blob['EventInfo'] = self._h5file.get('/event/{0}/info'.format(n_event))
        return blob

    def finish(self):
        """Clean everything up"""
        self._h5file.close()

    def _reset_index(self):
        """Reset index to default value"""
        self.index = 0

    def __len__(self):
        return self._n_events

    def __iter__(self):
        return self

    def next(self):
        """Python 2/3 compatibility for iterators"""
        return self.__next__()

    def __next__(self):
        if self.index >= self._n_events:
            self._reset_index()
            raise StopIteration
        blob = self.get_blob(self.index)
        self.index += 1
        return blob

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.get_blob(index)
        elif isinstance(index, slice):
            return self._slice_generator(index)
        else:
            raise TypeError("index must be int or slice")

    def _slice_generator(self, index):
        """A simple slice generator for iterations"""
        start, stop, step = index.indices(len(self))
        for i in range(start, stop, step):
            yield self.get_blob(i)


class HDF5Sink(Module):
    def __init__(self, **context):
        """A Module to convert (KM3NeT) ROOT files to HDF5."""
        super(self.__class__, self).__init__(**context)
        self.filename = self.get('filename') or 'dump.h5'
        self.hits = {}
        self.mc_hits = {}
        self.mc_tracks = {}
        self.event_info = {}
        self.index = 0
        print("Processing {0}...".format(self.filename))

    def process(self, blob):
        try:
            self._add_hits(blob['Hits'], self.hits)
        except KeyError:
            print("No hits found. Skipping...")

        try:
            self._add_hits(blob['MCHits'], self.mc_hits)
        except KeyError:
            print("No MC hits found. Skipping...")

        try:
            self._add_mc_tracks(blob['MCTracks'])
        except KeyError:
            print("No MC tracks found. Skipping...")

        self._add_event_info(blob)

        self.index += 1
        return blob

    def _add_hits(self, hits, target):
        for hit in hits:
            target.setdefault('event_id', []).append(self.index)
            target.setdefault('id', []).append(hit.id)
            target.setdefault('pmt_id', []).append(hit.pmt_id)
            target.setdefault('time', []).append(hit.time)
            target.setdefault('tot', []).append(hit.tot)
            target.setdefault('triggered', []).append(hit.triggered)
            target.setdefault('dom_id', []).append(hit.dom_id)
            target.setdefault('channel_id', []).append(hit.channel_id)

    def _add_mc_tracks(self, mc_tracks):
        for mc_track in mc_tracks:
            self.mc_tracks.setdefault('event_id', []).append(self.index)
            self.mc_tracks.setdefault('id', []).append(mc_track.id)
            self.mc_tracks.setdefault('x', []).append(mc_track.pos.x)
            self.mc_tracks.setdefault('y', []).append(mc_track.pos.y)
            self.mc_tracks.setdefault('z', []).append(mc_track.pos.z)
            self.mc_tracks.setdefault('dx', []).append(mc_track.dir.x)
            self.mc_tracks.setdefault('dy', []).append(mc_track.dir.y)
            self.mc_tracks.setdefault('dz', []).append(mc_track.dir.z)
            self.mc_tracks.setdefault('time', []).append(mc_track.t)
            self.mc_tracks.setdefault('energy', []).append(mc_track.E)
            self.mc_tracks.setdefault('type', []).append(mc_track.type)

    def _add_event_info(self, blob):
        evt = blob['Evt']

        timestamp = evt.t.AsDouble()
        det_id = evt.det_id
        mc_id = evt.mc_id
        mc_t = evt.mc_t
        run = evt.run_id
        overlays = evt.overlays
        trigger_counter = evt.trigger_counter
        trigger_mask = evt.trigger_mask
        frame_index = evt.frame_index

        info = self.event_info

        info.setdefault('event_id', []).append(self.index)
        info.setdefault('timestamp', []).append(timestamp)
        info.setdefault('det_id', []).append(det_id)
        info.setdefault('mc_id', []).append(mc_id)
        info.setdefault('mc_t', []).append(mc_t)
        info.setdefault('run', []).append(run)
        info.setdefault('overlays', []).append(overlays)
        info.setdefault('trigger_counter', []).append(trigger_counter)
        info.setdefault('trigger_mask', []).append(trigger_mask)
        info.setdefault('frame_index', []).append(frame_index)

    def finish(self):
        h5_file = h5py.File(self.filename, 'w')
        if self.hits:
            df = pd.DataFrame(self.hits)
            rec = df.to_records(index=False)
            h5_file.create_dataset('/hits', data=rec)
            print("Finished writing hits in {0}".format(self.filename))
        if self.mc_hits:
            df = pd.DataFrame(self.mc_hits)
            rec = df.to_records(index=False)
            h5_file.create_dataset('/mc_hits', data=rec)
            print("Finished writing MC hits in {0}".format(self.filename))
        if self.mc_tracks:
            df = pd.DataFrame(self.mc_tracks)
            rec = df.to_records(index=False)
            h5_file.create_dataset('/mc_tracks', data=rec)
            print("Finished writing MC tracks in {0}".format(self.filename))
        if self.event_info:
            df = pd.DataFrame(self.event_info)
            rec = df.to_records(index=False)
            h5_file.create_dataset('/event_info', data=rec)
            print("Finished writing event info in {0}".format(self.filename))

        h5_file.close()


class HDF5Sink2(Module):
    def __init__(self, **context):
        """A Module to convert (KM3NeT) ROOT files to HDF5."""
        super(self.__class__, self).__init__(**context)
        self.filename = self.get('filename') or 'dump.h5'
        self.hits = {}
        self.mc_hits = {}
        self.mc_tracks = {}
        self.event_info = {}
        self.h5_file = h5py.File(self.filename, 'w')
        self.index = 1
        print("Processing {0}...".format(self.filename))

    def process(self, blob):
        target = '/event/{0}/'.format(self.index)
        self.h5_file.create_group(target)

        self._add_event_info(blob, target=target+'info')

        if 'Hits' in blob:
            self._add_hits(blob['Hits'], target=target+'hits')

        if 'MCHits' in blob:
            self._add_hits(blob['MCHits'], target=target+'mc_hits')

        if 'MCTracks' in blob:
            self._add_tracks(blob['MCTracks'], target=target+'mc_tracks')

        self.index += 1
        return blob

    def _add_event_info(self, blob, target):
        evt = blob['Evt']

        timestamp = evt.t.AsDouble()
        det_id = evt.det_id
        mc_id = evt.mc_id
        mc_t = evt.mc_t
        run = evt.run_id
        overlays = evt.overlays
        trigger_counter = evt.trigger_counter
        trigger_mask = evt.trigger_mask
        frame_index = evt.frame_index

        info = defaultdict(list)

        info['event_id'].append(self.index)
        info['timestamp'].append(timestamp)
        info['det_id'].append(det_id)
        info['mc_id'].append(mc_id)
        info['mc_t'].append(mc_t)
        info['run'].append(run)
        info['overlays'].append(overlays)
        info['trigger_counter'].append(trigger_counter)
        info['trigger_mask'].append(trigger_mask)
        info['frame_index'].append(frame_index)

        self._dump_dict(info, target)

    def _add_hits(self, hits, target):
        hits_dict = defaultdict(list)
        for hit in hits:
            hits_dict['id'].append(hit.id)
            hits_dict['pmt_id'].append(hit.pmt_id)
            hits_dict['time'].append(hit.time)
            hits_dict['tot'].append(hit.tot)
            hits_dict['triggered'].append(hit.triggered)
            hits_dict['dom_id'].append(hit.dom_id)
            hits_dict['channel_id'].append(hit.channel_id)
        self._dump_dict(hits_dict, target)

    def _add_tracks(self, tracks, target):
        tracks_dict = defaultdict(list)
        for track in tracks:
            tracks_dict['id'].append(track.id)
            tracks_dict['x'].append(track.pos.x)
            tracks_dict['y'].append(track.pos.y)
            tracks_dict['z'].append(track.pos.z)
            tracks_dict['dx'].append(track.dir.x)
            tracks_dict['dy'].append(track.dir.y)
            tracks_dict['dz'].append(track.dir.z)
            tracks_dict['time'].append(track.t)
            tracks_dict['energy'].append(track.E)
            tracks_dict['type'].append(track.type)
        self._dump_dict(tracks_dict, target)

    def _dump_dict(self, data, target):
        if not data:
            return
        df = pd.DataFrame(data)
        rec = df.to_records(index=False)
        self.h5_file.create_dataset(target, data=rec)

    def finish(self):
        self.h5_file.close()


class HDF5Bucket(Module):
    def __init__(self, **context):
        super(self.__class__, self).__init__(**context)
        self.filename = self.get("filename")
        self.prefix = self.get("prefix")
        self.store = defaultdict(list)

    def process(self, blob):
        for key, val in blob[self.prefix].items():
            self.store[key].append(val)

    def finish(self):
        h5 = h5py.File(self.filename, mode='w')
        loc = '/' + self.prefix + '/'
        h5.create_group(loc)
        for key, data in self.store.items():
            h5.create_dataset(loc, key, np.array(data))
        h5.close()
