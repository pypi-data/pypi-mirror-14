# -*- coding: utf-8 -*-
"""
dicom2nifti

@author: abrys
"""

from __future__ import print_function
import dicom
import os
import numpy
import nibabel
from dicom.tag import Tag
import itertools
import gc
from six import string_types
from math import pow
import dicom2nifti.common as common
import dicom2nifti.convert_generic as convert_generic


def is_ge(dicom_directory):
    """
    Use this function to detect if a dicom series is a GE dataset
    :param dicom_directory: the directory containing the dicom files
    """
    # read dicom header
    header = common.read_first_header(dicom_directory)

    if 'Manufacturer' not in header or 'Modality' not in header:
        return False  # we try generic conversion in these cases

    # check if manufacturer is GE
    if 'GE MEDICAL SYSTEMS' not in header.Manufacturer.upper():
        return False

    # check if Modality is mr
    if header.Modality.upper() != 'MR':
        return False

    return True


def dicom_to_nifti(dicom_directory, output_file):
    """
    This is the main dicom to nifti conversion fuction for ge images.
    As input ge images are required. It will then determine the type of images and do the correct conversion

    Examples: See unit test
    :param output_file: the filepath to the output nifti file
    :param dicom_directory: the directory containing the dicom files (only 1 single scan)
    """
    assert is_ge(dicom_directory)

    print('Reading and sorting dicom files')
    grouped_dicoms = _get_grouped_dicoms(dicom_directory)

    if _is_dti(grouped_dicoms):
        print('Found sequence type: DTI')
        return _dti_to_nifti(grouped_dicoms, output_file)

    if _is_frmi(grouped_dicoms):
        print('Found sequence type: FMRI')
        return _fmri_to_nifti(grouped_dicoms, output_file)

    print('Assuming anatomical data')
    return convert_generic.dicom_to_nifti(dicom_directory, output_file)


def _is_frmi(grouped_dicoms):
    """
    Use this function to detect if a dicom series is a ge fmri dataset
    NOTE: Only the first slice will be checked so you can only provide an already sorted dicom directory
    (containing one series)
    """
    # read dicom header
    header = grouped_dicoms[0][0]

    # check if the dicom contains stack information
    if Tag(0x0020, 0x9056) not in header or Tag(0x0020, 0x9057) not in header:
        return False

    # check if contains multiple stacks
    if len(grouped_dicoms) <= 1:
        return False

    # check if contains no dti bval information
    bval_tag = Tag(0x0043, 0x1039)  # put this there as this is a slow step and used a lot
    found_bval = False
    for header in list(itertools.chain.from_iterable(grouped_dicoms)):
        if bval_tag in header and int(header[bval_tag].value[0]) != 0:
            found_bval = True
            break
    if found_bval:
        return False

    return True


def _is_dti(grouped_dicoms):
    """
    Use this function to detect if a dicom series is a ge dti dataset
    NOTE: Only the first slice will be checked so you can only provide an already sorted dicom directory
    (containing one series)
    """
    # read dicom header
    header = grouped_dicoms[0][0]

    # check if the dicom contains stack information
    if Tag(0x0020, 0x9056) not in header or Tag(0x0020, 0x9057) not in header:
        return False

    # check if contains multiple stacks
    if len(grouped_dicoms) <= 1:
        return False

    # check if contains dti bval information
    bval_tag = Tag(0x0043, 0x1039)  # put this there as this is a slow step and used a lot
    found_bval = False
    for header in list(itertools.chain.from_iterable(grouped_dicoms)):
        if bval_tag in header and int(header[bval_tag].value[0]) != 0:
            found_bval = True
            break
    if not found_bval:
        return False

    return True


def _fmri_to_nifti(grouped_dicoms, output_file):
    """
    This function will convert ge fmri series to a nifti
    """

    # Create mosaic block
    print('Creating data block')
    full_block = _get_full_block(grouped_dicoms)

    print('Creating affine')
    # Create the nifti header info
    affine = common.create_affine(grouped_dicoms[0])

    print('Creating nifti')
    # Convert to nifti
    img = nibabel.Nifti1Image(full_block, affine)
    common.set_tr_te(img, float(grouped_dicoms[0][0].RepetitionTime),
                     float(grouped_dicoms[0][0].EchoTime))
    print('Saving nifti to disk %s' % output_file)
    # Save to disk
    img.to_filename(output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file}


def _dti_to_nifti(grouped_dicoms, output_file):
    """
    This function will convert a ge dti series to a nifti
    """

    print('Creating data block')
    full_block = _get_full_block(grouped_dicoms)

    print('Creating affine')
    # Create the nifti header info
    affine = common.create_affine(grouped_dicoms[0])

    print('Creating nifti')
    # Convert to nifti
    img = nibabel.Nifti1Image(full_block, affine)
    common.set_tr_te(img, float(grouped_dicoms[0][0].RepetitionTime),
                     float(grouped_dicoms[0][0].EchoTime))
    # Create the bval en bevec files
    base_path = os.path.dirname(output_file)
    base_name = os.path.splitext(os.path.splitext(os.path.basename(output_file))[0])[0]
    print('Creating bval en bvec files')
    bval_file = '%s/%s.bval' % (base_path, base_name)
    bvec_file = '%s/%s.bvec' % (base_path, base_name)
    _create_bvals_bvecs(grouped_dicoms, bval_file, bvec_file)

    # Save to disk
    print('Saving nifti to disk %s' % output_file)
    img.to_filename(output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file,
            'BVAL_FILE': bval_file,
            'BVEC_FILE': bvec_file}


def _get_full_block(grouped_dicoms):
    """
    Generate a full datablock containing all timepoints
    """
    # For each slice / mosaic create a data volume block
    data_blocks = []
    for index in range(0, len(grouped_dicoms)):
        print('Creating block %s of %s' % (index + 1, len(grouped_dicoms)))
        data_blocks.append(_timepoint_to_block(grouped_dicoms[index]))

    # Add the data_blocks together to one 4d block
    size_x = numpy.shape(data_blocks[0])[0]
    size_y = numpy.shape(data_blocks[0])[1]
    size_z = numpy.shape(data_blocks[0])[2]
    size_t = len(data_blocks)
    full_block = numpy.zeros((size_x, size_y, size_z, size_t), dtype=data_blocks[0].dtype)
    for index in range(0, size_t):
        full_block[:, :, :, index] = data_blocks[index]

    return full_block


def _timepoint_to_block(timepoint_dicoms):
    """
    Convert slices to a block of data by reading the headers and appending
    """
    # similar way of getting the block to anatomical however here we are creating the dicom series our selves
    return common.get_volume_pixeldata(timepoint_dicoms)


def _get_grouped_dicoms(dicom_directory, fast_read=False):
    """
    Search all dicoms in the dicom directory, sort and validate them

    fast_read = True will only read the headers not the data
    """
    # Loop overall files and build dict
    dicoms = []
    for root, _, file_names in os.walk(dicom_directory):
        # go over all the files and try to read the dicom header
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if common.is_dicom_file(file_path):
                # Read each dicom file and put in dict
                dicoms.append(dicom.read_file(file_path, stop_before_pixels=fast_read))

    # Order all dicom files by InstanceNumber
    dicoms = sorted(dicoms, key=lambda x: x.InstanceNumber)

    # now group per stack
    grouped_dicoms = [[]]  # list with first element a list
    stack_index = 0
    previous_stack_position = -1

    # loop over all sorted dicoms
    stack_position_tag = Tag(0x0020, 0x9057)  # put this there as this is a slow step and used a lot
    for index in range(0, len(dicoms)):
        dicom_ = dicoms[index]
        # if the stack number decreases we moved to the next stack
        stack_position = 0
        if stack_position_tag in dicom_:
            stack_position = dicom_[stack_position_tag].value
        if previous_stack_position > stack_position:
            stack_index += 1
            grouped_dicoms.append([])
        grouped_dicoms[stack_index].append(dicom_)
        previous_stack_position = stack_position

    return grouped_dicoms


def get_bvals_bvecs(dicom_directory):
    """
    Function to only retrieve the bvals and bvecs from a dicom set
    :param dicom_directory: directory with dicom files for 1 single scan
    """
    grouped_dicoms = _get_grouped_dicoms(dicom_directory, fast_read=True)
    bvals, bvecs = _get_bvals_bvecs(grouped_dicoms)
    return bvals, bvecs


def _get_bvals_bvecs(grouped_dicoms):
    """
    Write the bvals from the sorted dicom files to a bval file
    """
    # loop over all timepoints and create a list with all bvals and bvecs
    bvals = numpy.zeros([len(grouped_dicoms)], dtype=numpy.int32)
    bvecs = numpy.zeros([len(grouped_dicoms), 3])

    for group_index in range(0, len(grouped_dicoms)):
        dicom_ = grouped_dicoms[group_index][0]
        # 0019:10bb: Diffusion X
        # 0019:10bc: Diffusion Y
        # 0019:10bd: Diffusion Z
        # 0043:1039: B-values (4 values, 1st value is actual B value)

        # bval can be stored both in string as number format in dicom so implement both
        # some workarounds needed for implicit transfer syntax to work
        if isinstance(dicom_[Tag(0x0043, 0x1039)].value, string_types):  # this works for python2.7
            original_bval = float(dicom_[Tag(0x0043, 0x1039)].value.split('\\')[0])
        elif isinstance(dicom_[Tag(0x0043, 0x1039)].value, bytes):  # this works for python3.o
            original_bval = float(dicom_[Tag(0x0043, 0x1039)].value.decode("utf-8").split('\\')[0])
        else:
            original_bval = dicom_[Tag(0x0043, 0x1039)][0]
        original_bvec = numpy.array([0, 0, 0], dtype=numpy.float)
        original_bvec[0] = -float(dicom_[Tag(0x0019, 0x10bb)].value)  # invert based upon mricron output
        original_bvec[1] = float(dicom_[Tag(0x0019, 0x10bc)].value)
        original_bvec[2] = float(dicom_[Tag(0x0019, 0x10bd)].value)

        # Add calculated B Value
        if original_bval != 0:  # only normalize if there is a value
            corrected_bval = original_bval * pow(numpy.linalg.norm(original_bvec), 2)
            if numpy.linalg.norm(original_bvec) != 0:
                normalized_bvec = original_bvec / numpy.linalg.norm(original_bvec)
            else:
                normalized_bvec = original_bvec
        else:
            corrected_bval = original_bval
            normalized_bvec = original_bvec

        bvals[group_index] = int(round(corrected_bval))  # we want the original numbers back as in the protocol
        bvecs[group_index, :] = normalized_bvec

    return bvals, bvecs


def _create_bvals_bvecs(grouped_dicoms, bval_file, bvec_file):
    """
    Write the bvals from the sorted dicom files to a bval file
    """

    # get the bvals and bvecs
    bvals, bvecs = _get_bvals_bvecs(grouped_dicoms)

    # save the found bvecs to the file
    common.write_bval_file(bvals, bval_file)
    common.write_bvec_file(bvecs, bvec_file)
