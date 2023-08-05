# -*- coding: utf-8 -*-
"""
dicom2nifti

@author: abrys
"""
from __future__ import print_function

import os
import tempfile
import subprocess
import shutil

from dicom.tag import Tag

from dicom2nifti.exceptions import ConversionValidationError, ConversionError
import dicom2nifti.convert_generic as convert_generic
import dicom2nifti.convert_siemens as convert_siemens
import dicom2nifti.convert_ge as convert_ge
import dicom2nifti.convert_philips as convert_philips
import dicom2nifti.common as common
import dicom2nifti.image_reorientation as image_reorientation

# Disable this warning as there is not reason for an init class in an enum
# pylint: disable=w0232, r0903, C0103


class Vendor(object):
    """
    Enum with the vendor
    """
    GENERIC = 0
    SIEMENS = 1
    GE = 2
    PHILIPS = 3


# pylint: enable=w0232, r0903, C0103
def dicom_series_to_nifti(original_dicom_directory, output_file, reorient_nifti=True):
    """ Converts dicom single series (see pydicom) to nifty, mimicking SPM

    Examples: See unit test


    will return a dictionary containing
    - the NIFTI under key 'NIFTI'
    - the NIFTI file path under 'NII_FILE'
    - the BVAL file path under 'BVAL_FILE' (only for dti)
    - the BVEC file path under 'BVEC_FILE' (only for dti)

    IMPORTANT:
    If no specific sequence type can be found it will default to anatomical and try to convert.
    You should check that the data you are trying to convert is supported by this code

    Inspired by http://nipy.sourceforge.net/nibabel/dicom/spm_dicom.html
    Inspired by http://code.google.com/p/pydicom/source/browse/source/dicom/contrib/pydicom_series.py
    :param reorient_nifti: if True the nifti affine and data will be updated so the data is stored LAS oriented
    :param output_file: file path to write to
    :param original_dicom_directory: directory with the dicom files for a single series/scan
    """
    # copy files so we can can modify without altering the original
    temp_directory = tempfile.mkdtemp()
    try:
        dicom_directory = os.path.join(temp_directory, 'dicom')
        shutil.copytree(original_dicom_directory, dicom_directory)

        decompress_directory(dicom_directory)

        if not are_imaging_dicoms(dicom_directory):
            raise ConversionValidationError('NON_IMAGING_DICOM_FILES')

        vendor = _get_vendor(dicom_directory)
        if vendor == Vendor.GENERIC:
            results = convert_generic.dicom_to_nifti(dicom_directory, output_file)
        elif vendor == Vendor.SIEMENS:
            results = convert_siemens.dicom_to_nifti(dicom_directory, output_file)
        elif vendor == Vendor.GE:
            results = convert_ge.dicom_to_nifti(dicom_directory, output_file)
        elif vendor == Vendor.PHILIPS:
            results = convert_philips.dicom_to_nifti(dicom_directory, output_file)
        else:
            raise ConversionValidationError("UNSUPPORTED_DATA")

        # do image reorientation if needed
        if reorient_nifti:
            image_reorientation.reorient_image(results['NII_FILE'], results['NII_FILE'])
        return results
    finally:
        # remove the copied data
        shutil.rmtree(temp_directory)


def are_imaging_dicoms(dicom_directory):
    """
    This function will check the dicom headers to see which type of series it is
    Possibilities are fMRI, DTI, Anatomical (if no clear type is found anatomical is used)
    :param dicom_directory: directory with dicom files
    """

    # if it is philips and multiframe dicom then we assume it is ok
    if convert_philips.is_philips(dicom_directory):
        # in case of philips we need the actual uncompressed data for the check
        decompress_directory(dicom_directory)
        if convert_philips.is_multiframe_dicom(dicom_directory):
            return True

    # for all others if there is image position patient we assume it is ok
    header = common.read_first_header(dicom_directory)
    return Tag(0x0020, 0x0037) in header


def _get_vendor(dicom_directory):
    """
    This function will check the dicom headers to see which type of series it is
    Possibilities are fMRI, DTI, Anatomical (if no clear type is found anatomical is used)
    """
    # check if it is siemens frmi
    if convert_siemens.is_siemens(dicom_directory):
        print('Found manufacturer: SIEMENS')
        return Vendor.SIEMENS
    # check if it is ge frmi
    if convert_ge.is_ge(dicom_directory):
        print('Found manufacturer: GE')
        return Vendor.GE
    # check if it is ge frmi
    if convert_philips.is_philips(dicom_directory):
        print('Found manufacturer: PHILIPS')
        return Vendor.PHILIPS
    # check if it is siemens dti
    print('WARNING: Assuming generic vendor conversion (ANATOMICAL)')
    return Vendor.GENERIC


def decompress_dicom(input_file):
    """
    This function can be used to convert a jpeg compressed image to an uncompressed one for further conversion
    :param input_file: single dicom file to decompress
    """
    gdcmconv_executable = _which('gdcmconv')
    if gdcmconv_executable is None:
        gdcmconv_executable = _which('gdcmconv.exe')

    subprocess.check_output([gdcmconv_executable, '-w', input_file, input_file])


def decompress_directory(dicom_directory):
    """
    This function can be used to convert a folder of jpeg compressed images to an uncompressed ones
    :param dicom_directory: directory with dicom files to decompress
    """
    if not is_compressed(dicom_directory):
        return

    if _which('gdcmconv') is None and _which('gdcmconv.exe') is None:
        raise ConversionError('GDCMCONV_NOT_FOUND')

    print('Decompressing dicom files in %s' % dicom_directory)
    for root, _, files in os.walk(dicom_directory):
        for dicom_file in files:
            if common.is_dicom_file(os.path.join(root, dicom_file)):
                decompress_dicom(os.path.join(root, dicom_file))


def compress_dicom(input_file):
    """
    This function can be used to convert a jpeg compressed image to an uncompressed one for further conversion
    :param input_file: single dicom file to compress
    """
    gdcmconv_executable = _which('gdcmconv')
    if gdcmconv_executable is None:
        gdcmconv_executable = _which('gdcmconv.exe')

    subprocess.check_output([gdcmconv_executable, '-K', input_file, input_file])


def compress_directory(dicom_directory):
    """
    This function can be used to convert a folder of jpeg compressed images to an uncompressed ones
    :param dicom_directory: directory of dicom files to compress
    """
    if is_compressed(dicom_directory):
        return

    if _which('gdcmconv') is None and _which('gdcmconv.exe') is None:
        raise ConversionError('GDCMCONV_NOT_FOUND')

    print('Compressing dicom files in %s' % dicom_directory)
    for root, _, files in os.walk(dicom_directory):
        for dicom_file in files:
            if common.is_dicom_file(os.path.join(root, dicom_file)):
                compress_dicom(os.path.join(root, dicom_file))


def is_compressed(dicom_directory):
    """
    Check if dicoms are compressed or not
    :param dicom_directory: directory with dicom files for 1 scan
    """
    # read dicom header
    header = common.read_first_header(dicom_directory)
    uncompressed_types = ["1.2.840.10008.1.2",
                          "1.2.840.10008.1.2.1",
                          "1.2.840.10008.1.2.1.99",
                          "1.2.840.10008.1.2.2"]

    if 'TransferSyntaxUID' in header.file_meta and header.file_meta.TransferSyntaxUID in uncompressed_types:
        return False
    return True


def _which(program):
    import os

    def is_exe(executable_file):
        return os.path.isfile(executable_file) and os.access(executable_file, os.X_OK)

    file_path, file_name = os.path.split(program)
    if file_path:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
