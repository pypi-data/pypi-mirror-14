# -*- coding: utf-8 -*-
"""
this module houses all the code to just convert a directory of random dicom files

@author: abrys
"""
from __future__ import print_function

import dicom
import os
import dicom2nifti.common as common
import dicom2nifti.convert_dicom as convert_dicom
from six import iteritems, u
import tempfile
import shutil
import string
import unicodedata
import six
from builtins import bytes


def convert_directory(dicom_directory, output_folder, compression=True, reorient=True):
    """
    This function will order all dicom files by series and order them one by one
    :param compression: enable or disable gzip compression
    :param reorient: reorient the dicoms according to LAS orientation
    :param output_folder: folder to write the nifti files to
    :param dicom_directory: directory with dicom files
    """
    # sort dicom files by series uid
    dicom_series = {}
    for root, _, files in os.walk(dicom_directory):
        for dicom_file in files:
            file_path = os.path.join(root, dicom_file)
            if common.is_dicom_file(file_path):
                # read the dicom as fast as possible
                # (max length for SeriesInstanceUID is 64 so defer_size 100 should be ok)
                dicom_headers = dicom.read_file(file_path, defer_size=100, stop_before_pixels=True)
                if dicom_headers.SeriesInstanceUID not in dicom_series:
                    dicom_series[dicom_headers.SeriesInstanceUID] = []
                dicom_series[dicom_headers.SeriesInstanceUID].append((file_path, dicom_headers))

    # start converting one by one
    for series_id, dicom_info in iteritems(dicom_series):
        work_dir = tempfile.mkdtemp()
        try:
            # construct the filename for the nifti
            base_filename = _remove_accents_('%s_%s' % (dicom_info[0][1].SeriesNumber, dicom_info[0][1].SequenceName))
            print('--------------------------------------------')
            print('Start converting ', base_filename)
            if compression:
                nifti_file = os.path.join(output_folder, base_filename + '.nii.gz')
            else:
                nifti_file = os.path.join(output_folder, base_filename + '.nii')
            # copy all dicom files to the working directory
            for dicom_file in dicom_info:
                shutil.copy2(dicom_file[0], work_dir)
            convert_dicom.dicom_series_to_nifti(work_dir, nifti_file, reorient)
        finally:
            shutil.rmtree(work_dir)


def _remove_accents_(filename):
    """
    Function that will try to remove accents from a unicode string to be used in a filename.
    input filename should be either an ascii or unicode string
    """
    if type(filename) is type(six.u('')):
        unicode_filename = filename
    else:
        unicode_filename = six.u(filename)
    valid_characters = bytes(b'-_.() 1234567890abcdefghijklmnopqrstuvwxyz')
    cleaned_filename = unicodedata.normalize('NFKD', unicode_filename).encode('ASCII', 'ignore')

    new_filename = six.u('')

    for char_int in bytes(cleaned_filename):
        char_byte = bytes([char_int])
        if char_byte in valid_characters:
            new_filename += char_byte.decode()

    return new_filename
