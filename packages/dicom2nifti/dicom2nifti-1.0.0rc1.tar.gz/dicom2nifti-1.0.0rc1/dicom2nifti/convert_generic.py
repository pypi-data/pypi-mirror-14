# -*- coding: utf-8 -*-
"""
dicom2nifti

@author: abrys
"""

from __future__ import print_function
import gc
import os

import numpy
import nibabel
from dicom.tag import Tag
import dicom
import dicom2nifti.common as common


def dicom_to_nifti(dicom_directory, output_file):
    """
    This function will convert an anatomical dicom series to a nifti

    Examples: See unit test
    :param output_file: filepath to the output nifti
    :param dicom_directory: directory with the dicom files for a single scan
    """

    # make sure there are only dicom files in the directory
    _remove_non_dicoms(dicom_directory)
    # remove localizers based on image type
    _remove_localizers_by_imagetype(dicom_directory)
    # remove_localizers based on image orientation
    _remove_localizers_by_orientation(dicom_directory)

    all_dicoms = _get_all_dicoms(dicom_directory, False)
    # validate all the dicom files for correct orientations
    common.validate_slicecount(all_dicoms)
    # validate that all slices have the same orientation
    common.validate_orientation(all_dicoms)
    # validate that we have an orthogonal image (to detect gantry tilting etc)
    common.validate_orthogonal(all_dicoms)

    # Get data; originally z,y,x, transposed to x,y,z
    data = common.get_volume_pixeldata(all_dicoms)
    affine = common.create_affine(all_dicoms)

    # Convert to nifti
    img = nibabel.Nifti1Image(data, affine)

    # Set TR and TE if available
    if Tag(0x0018, 0x0081) in all_dicoms[0] and Tag(0x0018, 0x0081) in all_dicoms[0]:
        common.set_tr_te(img, float(all_dicoms[0].RepetitionTime), float(all_dicoms[0].EchoTime))

    # Save to disk
    print('Saving nifti to disk %s' % output_file)
    img.to_filename(output_file)
    gc.collect()  # force the collection for conversion of big datasets this is needed

    return {'NII_FILE': output_file}


def _remove_non_dicoms(dicom_directory):
    """
    Search dicoms for localizers and delete them
    """
    # Loop overall files and build dict
    for root, _, file_names in os.walk(dicom_directory):
        # go over all the files and try to read the dicom header
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if not common.is_dicom_file(file_path):
                os.remove(file_path)


def _remove_localizers_by_imagetype(dicom_directory):
    """
    Search dicoms for localizers and delete them
    """
    # Loop overall files and build dict
    for root, _, file_names in os.walk(dicom_directory):
        # go over all the files and try to read the dicom header
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if common.is_dicom_file(file_path):
                # Read each dicom file and put in dict
                read_dicom = dicom.read_file(file_path, stop_before_pixels=True)
                if 'ImageType' in read_dicom and 'LOCALIZER' in read_dicom.ImageType:
                    print('Removing localizer %s ' % file_path)
                    os.remove(file_path)
                    continue
                # 'Projection Image' are Localizers for CT only see MSMET-234
                if 'CT' in read_dicom.Modality and \
                        'ImageType' in read_dicom and 'PROJECTION IMAGE' in read_dicom.ImageType:
                    print('Removing projection image %s ' % file_path)
                    os.remove(file_path)
                    continue


def _remove_localizers_by_orientation(dicom_directory):
    """
    Removing localizers based on the orientation.
    This is needed as in some cases with ct data there are some localizer/projection type images that cannot
    be distiguished by the dicom headers. This is why we kick out all orientations that do not have more than 4 files
    4 is the limit anyway for converting to nifti on our case
    """
    orientations = []
    sorted_dicoms = {}
    # Loop overall files and build dict
    for root, _, file_names in os.walk(dicom_directory):
        for file_name in file_names:
            dicom_file = os.path.join(root, file_name)
            dicom_header = dicom.read_file(dicom_file, stop_before_pixels=True)
            # Create affine matrix (http://nipy.sourceforge.net/nibabel/dicom/dicom_orientation.html#dicom-slice-affine)
            image_orient1 = numpy.array(dicom_header.ImageOrientationPatient)[0:3]
            image_orient2 = numpy.array(dicom_header.ImageOrientationPatient)[3:6]
            image_orient_combined = (image_orient1.tolist(), image_orient2.tolist())
            found_orientation = False
            for orientation in orientations:
                if numpy.allclose(image_orient_combined[0], numpy.array(orientation[0]), rtol=0.001, atol=0.001) \
                        and numpy.allclose(image_orient_combined[1], numpy.array(orientation[1]), rtol=0.001,
                                           atol=0.001):
                    sorted_dicoms[str(orientation)].append(dicom_file)
                    found_orientation = True
                    break
            if not found_orientation:
                orientations.append(image_orient_combined)
                sorted_dicoms[str(image_orient_combined)] = [dicom_file]

    # if there are multiple possible orientations delete orientations where there are less than 4 files
    # we don't convert anything less that that anyway
    if len(sorted_dicoms.keys()) > 1:
        for dicom_files in sorted_dicoms.values():
            if len(dicom_files) <= 4:
                for dicom_file in dicom_files:
                    print('Removing badly oriented dicom %s ' % dicom_file)
                    os.remove(dicom_file)


def _get_all_dicoms(dicom_directory, fast_read=True):
    """
    Search all mosaics in the dicom directory, sort and validate them
    """
    # Loop overall files and build dict
    dicoms = []
    for root, _, file_names in os.walk(dicom_directory):
        # go over all the files and try to read the dicom header
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if common.is_dicom_file(file_path):
                # Read each dicom file and put in dict
                read_dicom = dicom.read_file(file_path, stop_before_pixels=fast_read)
                dicoms.append(read_dicom)

    dicoms = sorted(dicoms, key=lambda k: k.InstanceNumber)
    return dicoms
