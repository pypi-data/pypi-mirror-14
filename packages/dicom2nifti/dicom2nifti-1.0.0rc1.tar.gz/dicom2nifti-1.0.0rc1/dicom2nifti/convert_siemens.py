# -*- coding: utf-8 -*-
"""
dicom2nifti

@author: abrys
"""

from __future__ import print_function
import os
import re
import gc
import numpy
import nibabel
import dicom
import traceback
from dicom.tag import Tag
import dicom2nifti.convert_generic as convert_generic
from dicom2nifti.exceptions import ConversionValidationError, ConversionError
import dicom2nifti.common as common


# Disable this warning as there is not reason for an init class in an enum
# pylint: disable=w0232, r0903, E1101


class MosaicType(object):
    """
    Enum for the possible types of mosaic data
    """
    ASCENDING = 1
    DESCENDING = 2


# pylint: enable=w0232, r0903


def is_siemens(dicom_directory):
    """
    Use this function to detect if a dicom series is a siemens dataset
    :param dicom_directory: directory with dicom files for 1 scan
    """
    # read dicom header
    header = common.read_first_header(dicom_directory)

    # check if manufacturer is Siemens
    if 'Manufacturer' not in header or 'Modality' not in header:
        return False  # we try generic conversion in these cases

    if 'SIEMENS' not in header.Manufacturer.upper():
        return False

    # check if Modality is mr
    if header.Modality.upper() != 'MR':
        return False

    return True


def dicom_to_nifti(dicom_directory, output_file):
    """
    This is the main dicom to nifti conversion function for ge images.
    As input ge images are required. It will then determine the type of images and do the correct conversion
    :param output_file: filepath to the output nifti
    :param dicom_directory: directory with dicom files for 1 scan
    """

    assert is_siemens(dicom_directory)

    if _is_dti(dicom_directory):
        print('Found sequence type: MOSAIC DTI')
        return _mosaic_dti_to_nifti(dicom_directory, output_file)

    if _is_frmi(dicom_directory):
        print('Found sequence type: MOSAIC FMRI')
        return _mosaic_fmri_to_nifti(dicom_directory, output_file)

    grouped_dicoms = _classic_get_grouped_dicoms(dicom_directory)
    if _is_classic_dti(grouped_dicoms):
        print('Found sequence type: CLASSIC DTI')
        return _classic_dti_to_nifti(grouped_dicoms, output_file)

    if _is_classic_frmi(grouped_dicoms):
        print('Found sequence type: CLASSIC FMRI')
        return _classic_fmri_to_nifti(grouped_dicoms, output_file)

    print('Assuming anatomical data')
    return convert_generic.dicom_to_nifti(dicom_directory, output_file)


def _is_mosaic(input_data):
    """
    Use this function to detect if a dicom series is a siemens fmri dataset
    NOTE: Only the first slice will be checked so you can only provide an already sorted dicom directory
    (containing one series)
    """
    # take both dicom_directory and grouped dicoms list as input
    if type(input_data) is list:
        header = input_data[0][0]
    else:
        # read dicom header
        header = common.read_first_header(input_data)

    # check if image type contains m and mosaic
    if 'MOSAIC' not in header.ImageType:
        return False

    if 'AcquisitionMatrix' not in header or header.AcquisitionMatrix is None:
        return False

    return True


def _is_frmi(dicom_directory):
    """
    Use this function to detect if a dicom series is a siemens fmri dataset
    NOTE: Only the first slice will be checked so you can only provide an already sorted dicom directory
    (containing one series)
    """
    if not _is_mosaic(dicom_directory):
        return False

    # read dicom header
    header = common.read_first_header(dicom_directory)

    # bval and bvec should be absent
    if Tag(0x0019, 0x100c) in header:
        return False

    return True


def _is_classic_frmi(grouped_dicoms):
    """
    Use this function to detect if a dicom series is a siemens fmri dataset
    NOTE: Only the first slice will be checked so you can only provide an already sorted dicom directory
    (containing one series)
    """

    if _is_mosaic(grouped_dicoms):
        return False

    if len(grouped_dicoms) <= 1:
        return False

    # get dicom header
    header = grouped_dicoms[0][0]

    # bval and bvec should be absent
    if Tag(0x0019, 0x100c) in header:
        return False

    return True


def _is_dti(dicom_directory):
    """
    Use this function to detect if a dicom series is a siemens dti dataset
    NOTE: Only the first slice will be checked so you can only provide an already sorted dicom directory
    (containing one series)
    """
    if not _is_mosaic(dicom_directory):
        return False

    # read dicom header
    header = common.read_first_header(dicom_directory)

    # bval and bvec should be absent
    if Tag(0x0019, 0x100c) not in header:
        return False

    return True


def _is_classic_dti(grouped_dicoms):
    """
    Use this function to detect if a dicom series is a siemens dti dataset
    NOTE: Only the first slice will be checked so you can only provide an already sorted dicom directory
    (containing one series)
    """
    if _is_mosaic(grouped_dicoms):
        return False

    if len(grouped_dicoms) <= 1:
        return False

    # get dicom header
    header = grouped_dicoms[0][0]

    # bval and bvec should be absent
    if Tag(0x0019, 0x100c) not in header:
        return False

    return True


def _mosaic_fmri_to_nifti(dicom_directory, output_file):
    """
    This function will convert siemens fmri series to a nifti
    Some inspiration on which fields can be used was taken from
    http://slicer.org/doc/html/DICOMDiffusionVolumePlugin_8py_source.html
    """
    # Get the sorted mosaics
    print('Sorting dicom slices')
    sorted_mosaics = _get_sorted_mosaics(dicom_directory)
    common.validate_orientation(sorted_mosaics)

    # Create mosaic block
    print('Creating data block')
    full_block = _mosaic_get_full_block(sorted_mosaics)

    print('Creating affine')
    # Create the nifti header info
    affine = _create_affine_siemens_mosaic(dicom_directory)
    print('Creating nifti')
    # Convert to nifti
    img = nibabel.Nifti1Image(full_block, affine)
    common.set_tr_te(img, float(sorted_mosaics[0].RepetitionTime), float(sorted_mosaics[0].EchoTime))
    print('Saving nifti to disk')
    # Save to disk
    img.to_filename(output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file}


def _classic_fmri_to_nifti(grouped_dicoms, output_file):
    """
    This function will convert siemens fmri series to a nifti
    Some inspiration on which fields can be used was taken from
    http://slicer.org/doc/html/DICOMDiffusionVolumePlugin_8py_source.html
    """
    # Get the sorted mosaics
    all_dicoms = [i for sl in grouped_dicoms for i in sl]  # combine into 1 list for validating
    common.validate_orientation(all_dicoms)

    # Create mosaic block
    print('Creating data block')
    full_block = _classic_get_full_block(grouped_dicoms)

    print('Creating affine')
    # Create the nifti header info
    affine = common.create_affine(grouped_dicoms[0])

    print('Creating nifti')
    # Convert to nifti
    img = nibabel.Nifti1Image(full_block, affine)
    common.set_tr_te(img, float(grouped_dicoms[0][0].RepetitionTime), float(grouped_dicoms[0][0].EchoTime))
    print('Saving nifti to disk')
    # Save to disk
    img.to_filename(output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file}


def _classic_get_grouped_dicoms(dicom_directory, fast_read=False):
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
    grouped_dicoms = []

    # loop over all sorted dicoms
    stack_position_tag = Tag(0x0020, 0x0012)  # in this case it is the acquisition number
    for index in range(0, len(dicoms)):
        dicom_ = dicoms[index]
        stack_index = dicom_[stack_position_tag].value - 1
        while len(grouped_dicoms) <= stack_index:
            grouped_dicoms.append([])
        grouped_dicoms[stack_index].append(dicom_)

    return grouped_dicoms


def _classic_get_full_block(grouped_dicoms):
    """
    Generate a full datablock containing all timepoints
    """
    # For each slice / mosaic create a data volume block
    data_blocks = []
    for index in range(0, len(grouped_dicoms)):
        print('Creating block %s of %s' % (index + 1, len(grouped_dicoms)))
        data_blocks.append(_classic_timepoint_to_block(grouped_dicoms[index]))

    # Add the data_blocks together to one 4d block
    size_x = numpy.shape(data_blocks[0])[0]
    size_y = numpy.shape(data_blocks[0])[1]
    size_z = numpy.shape(data_blocks[0])[2]
    size_t = len(data_blocks)
    full_block = numpy.zeros((size_x, size_y, size_z, size_t), dtype=data_blocks[0].dtype)
    for index in range(0, size_t):
        full_block[:, :, :, index] = data_blocks[index]

    return full_block


def _classic_timepoint_to_block(timepoint_dicoms):
    """
    Convert slices to a block of data by reading the headers and appending
    """
    # similar way of getting the block to anatomical however here we are creating the dicom series our selves
    return common.get_volume_pixeldata(timepoint_dicoms)


def _mosaic_dti_to_nifti(dicom_directory, output_file):
    """
    This function will convert a siemens mosaic dti series to a nifti
    Some inspiration on which fields can be used was taken from
    http://slicer.org/doc/html/DICOMDiffusionVolumePlugin_8py_source.html
    """
    # Get the sorted mosaics
    print('Sorting dicom slices')
    sorted_mosaics = _get_sorted_mosaics(dicom_directory)
    common.validate_orientation(sorted_mosaics)

    # Validate if the software version is high enough and scanned HFS
    print('Validating DTI dataset')
    if sorted_mosaics[0].PatientPosition.upper() != 'HFS':
        raise ConversionValidationError('SIEMENS_DTI_NOT_HFS')

    print('Creating data block')
    full_block = _mosaic_get_full_block(sorted_mosaics)

    # Create the nifti header info
    print('Creating affine')
    affine = _create_affine_siemens_mosaic(dicom_directory)

    # Convert to nifti
    print('Creating nifti')
    print('Saving nifti to disk %s' % output_file)
    img = nibabel.Nifti1Image(full_block, affine)
    common.set_tr_te(img, float(sorted_mosaics[0].RepetitionTime), float(sorted_mosaics[0].EchoTime))
    # Create the bval en bvec files
    print('Creating bval en bvec files')
    base_path = os.path.dirname(output_file)
    base_name = os.path.splitext(os.path.splitext(os.path.basename(output_file))[0])[0]
    print('Creating bval en bvec files')
    bval_file = '%s/%s.bval' % (base_path, base_name)
    bvec_file = '%s/%s.bvec' % (base_path, base_name)
    _create_bvals(sorted_mosaics, bval_file)
    _create_bvecs(sorted_mosaics, bvec_file)

    # Save to disk
    print('Saving nifti to disk %s' % output_file)
    img.to_filename(output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file,
            'BVAL_FILE': bval_file,
            'BVEC_FILE': bvec_file}


def _classic_dti_to_nifti(grouped_dicoms, output_file):
    """
    This function will convert siemens fmri series to a nifti
    Some inspiration on which fields can be used was taken from
    http://slicer.org/doc/html/DICOMDiffusionVolumePlugin_8py_source.html
    """
    # Get the sorted mosaics
    all_dicoms = [i for sl in grouped_dicoms for i in sl]  # combine into 1 list for validating
    common.validate_orientation(all_dicoms)

    # Validate if the software version is high enough and scanned HFS
    print('Validating DTI dataset')
    if grouped_dicoms[0][0].PatientPosition.upper() != 'HFS':
        raise ConversionValidationError('SIEMENS_DTI_NOT_HFS')

    # Create mosaic block
    print('Creating data block')
    full_block = _classic_get_full_block(grouped_dicoms)
    # Create the bval en bvec files
    print('Creating bval en bvec files')
    base_path = os.path.dirname(output_file)
    base_name = os.path.splitext(os.path.splitext(os.path.basename(output_file))[0])[0]
    print('Creating bval en bvec files')
    bval_file = '%s/%s.bval' % (base_path, base_name)
    bvec_file = '%s/%s.bvec' % (base_path, base_name)
    _create_bvals(grouped_dicoms, bval_file)
    _create_bvecs(grouped_dicoms, bvec_file)

    print('Creating affine')
    # Create the nifti header info
    affine = common.create_affine(grouped_dicoms[0])
    print('Creating nifti')

    # Convert to nifti
    img = nibabel.Nifti1Image(full_block, affine)
    common.set_tr_te(img, float(grouped_dicoms[0][0].RepetitionTime), float(grouped_dicoms[0][0].EchoTime))
    print('Saving nifti to disk')
    # Save to disk
    img.to_filename(output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file,
            'BVAL_FILE': bval_file,
            'BVEC_FILE': bvec_file}


def _mosaic_get_full_block(sorted_mosaics):
    """
    Generate a full datablock containing all timepoints
    """
    # For each slice / mosaic create a data volume block
    data_blocks = []
    for index in range(0, len(sorted_mosaics)):
        data_blocks.append(_mosaic_to_block(sorted_mosaics[index]))

    # Add the data_blocks together to one 4d block
    size_x = numpy.shape(data_blocks[0])[0]
    size_y = numpy.shape(data_blocks[0])[1]
    size_z = numpy.shape(data_blocks[0])[2]
    size_t = len(data_blocks)
    full_block = numpy.zeros((size_x, size_y, size_z, size_t), dtype=data_blocks[0].dtype)
    for index in range(0, size_t):
        full_block[:, :, :, index] = data_blocks[index]

    # Apply the rescaling if needed
    if 'RescaleSlope' in sorted_mosaics[0] or 'RescaleIntercept' in sorted_mosaics[0]:
        rescale_slope = 1
        rescale_offset = 0
        if 'RescaleSlope' in sorted_mosaics[0]:
            rescale_slope = sorted_mosaics[0].RescaleSlope
        if 'RescaleIntercept' in sorted_mosaics[0]:
            rescale_offset = sorted_mosaics[0].RescaleIntercept
        common.apply_scaling(full_block, rescale_slope, rescale_offset)

    return full_block


def _get_sorted_mosaics(dicom_directory):
    """
    Search all mosaics in the dicom directory, sort and validate them
    """
    # Loop overall files and build dict
    mosaics = []
    for root, _, file_names in os.walk(dicom_directory):
        # go over all the files and try to read the dicom header
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if common.is_dicom_file(file_path):
                # Read each dicom file and put in dict
                mosaics.append(dicom.read_file(file_path, stop_before_pixels=False))

    # Order all dicom files by acquisition number
    sorted_mosaics = sorted(mosaics, key=lambda x: x.AcquisitionNumber)

    for index in range(0, len(sorted_mosaics) - 1):
        # Validate that there are no duplicate AcquisitionNumber
        if sorted_mosaics[index].AcquisitionNumber >= sorted_mosaics[index + 1].AcquisitionNumber:
            raise ConversionValidationError("INCONSISTENT_ACQUISITION_NUMBERS")

    return sorted_mosaics


def _get_asconv_headers(mosaic):
    """
    Getter for the asconv headers (asci header info stored in the dicom)
    """
    asconv_headers = re.findall(r'### ASCCONV BEGIN(.*)### ASCCONV END ###',
                                mosaic[Tag(0x0029, 0x1020)].value.decode(encoding='ISO-8859-1'),
                                re.DOTALL)[0]

    return asconv_headers


def _get_mosaic_type(mosaic):
    """
    Check the extra ascconv headers for the mosaic type based on the slice position
    We always assume axial in this case
    the implementation resembles the last lines of documentation in
    https://www.icts.uiowa.edu/confluence/plugins/viewsource/viewpagesrc.action?pageId=54756326
    """

    ascconv_headers = _get_asconv_headers(mosaic)

    try:
        size = int(re.findall(r'sSliceArray\.lSize\s*=\s*(\d+)', ascconv_headers)[0])

        # get the locations of the slices
        slice_location = [None] * size
        for index in range(size):
            axial_result = re.findall(
                r'sSliceArray\.asSlice\[%s\]\.sPosition\.dTra\s*=\s*([-+]?[0-9]*\.?[0-9]*)' % index,
                ascconv_headers)
            if len(axial_result) > 0:
                axial = float(axial_result[0])
            else:
                axial = 0.0
            slice_location[index] = axial

        # should we invert (https://www.icts.uiowa.edu/confluence/plugins/viewsource/viewpagesrc.action?pageId=54756326)
        invert = False
        invert_result = re.findall(r'sSliceArray\.ucImageNumbTra\s*=\s*([-+]?0?x?[0-9]+)', ascconv_headers)
        if len(invert_result) > 0:
            invert_value = int(invert_result[0], 16)
            if invert_value >= 0:
                invert = True

        # return the correct slice types
        if slice_location[0] <= slice_location[1]:
            if not invert:
                return MosaicType.ASCENDING
            else:
                return MosaicType.DESCENDING
        else:
            if not invert:
                return MosaicType.DESCENDING
            else:
                return MosaicType.ASCENDING
    except:
        traceback.print_exc()
        raise ConversionError("MOSAIC_TYPE_NOT_SUPPORTED")


def _mosaic_to_block(mosaic):
    """
    Convert a mosaic slice to a block of data by reading the headers, splitting the mosaic and appending
    """
    # get the mosaic type
    mosaic_type = _get_mosaic_type(mosaic)

    # get the size of one tile format is 64p*64 or 80*80 or something similar
    matches = re.findall(r'(\d+)\D+(\d+)\D*', str(mosaic[Tag(0x0051, 0x100b)].value))[0]

    ascconv_headers = _get_asconv_headers(mosaic)
    size = [int(matches[0]),
            int(matches[1]),
            int(re.findall(r'sSliceArray\.lSize\s*=\s*(\d+)', ascconv_headers)[0])]

    # get the number of rows and columns
    number_x = int(mosaic.Rows / size[0])
    number_y = int(mosaic.Columns / size[1])

    # get the format
    format_string = common.get_numpy_type(mosaic)

    # reshape the 1d array to 3d
    data_1d = numpy.fromstring(mosaic.PixelData, dtype=format_string)
    # recreate 2d slice
    data_2d = numpy.reshape(data_1d, (size[1] * number_y, size[0] * number_x))
    # create 3d block
    data_3d = numpy.zeros((size[2], size[1], size[0]), dtype=format_string)
    # fill 3d block by taking the correct portions of the slice
    z_index = 0
    for y_index in range(0, number_y):
        if z_index >= size[2]:
            break
        for x_index in range(0, number_x):
            if mosaic_type == MosaicType.ASCENDING:
                data_3d[z_index, :, :] = data_2d[size[1] * y_index:size[1] * (y_index + 1),
                                                 size[0] * x_index:size[0] * (x_index + 1)]
            else:
                data_3d[size[2] - (z_index + 1), :, :] = data_2d[size[1] * y_index:size[1] * (y_index + 1),
                                                                 size[0] * x_index:size[0] * (x_index + 1)]
            z_index += 1
            if z_index >= size[2]:
                break
    # reorient the block of data
    data_3d = numpy.transpose(data_3d, (2, 1, 0))

    return data_3d


def _create_affine_siemens_mosaic(dicom_directory):
    """
    Function to create the affine matrix for a siemens mosaic dataset
    This will work for siemens dti and fmri if in mosaic format
    """
    # read dicom series with pds
    dicom_header = common.read_first_header(dicom_directory)

    # Create affine matrix (http://nipy.sourceforge.net/nibabel/dicom/dicom_orientation.html#dicom-slice-affine)
    image_orient1 = numpy.array(dicom_header.ImageOrientationPatient)[0:3]
    image_orient2 = numpy.array(dicom_header.ImageOrientationPatient)[3:6]

    normal = numpy.cross(image_orient1, image_orient2)

    delta_r = float(dicom_header.PixelSpacing[0])
    delta_c = float(dicom_header.PixelSpacing[1])

    image_pos = dicom_header.ImagePositionPatient

    delta_s = dicom_header.SpacingBetweenSlices
    return numpy.matrix(
        [[-image_orient1[0] * delta_r, -image_orient2[0] * delta_c, -delta_s * normal[0], -image_pos[0]],
         [-image_orient1[1] * delta_r, -image_orient2[1] * delta_c, -delta_s * normal[1], -image_pos[1]],
         [image_orient1[2] * delta_r, image_orient2[2] * delta_c, delta_s * normal[2], image_pos[2]],
         [0, 0, 0, 1]])


def _create_bvals(sorted_dicoms, bval_file):
    """
    Write the bvals from the sorted dicom files to a bval file
    """
    bvals = []
    for index in range(0, len(sorted_dicoms)):
        if type(sorted_dicoms[0]) is list:
            dicom_headers = sorted_dicoms[index][0]
        else:
            dicom_headers = sorted_dicoms[index]

        bvals.append(common.get_is_value(dicom_headers[Tag(0x0019, 0x100c)]))
    # save the found bvecs to the file
    common.write_bval_file(bvals, bval_file)


def _create_bvecs(sorted_dicoms, bvec_file):
    """
    Calculate the bvecs and write the to a bvec file
    # inspired by dicom2nii from mricron
    # see  http://users.fmrib.ox.ac.uk/~robson/internal/Dicom2Nifti111.m
    """
    if type(sorted_dicoms[0]) is list:
        dicom_headers = sorted_dicoms[0][0]
    else:
        dicom_headers = sorted_dicoms[0]

    # get the patient orientation
    image_orientation = dicom_headers.ImageOrientationPatient
    read_vector = numpy.array([float(image_orientation[0]), float(image_orientation[1]), float(image_orientation[2])])
    phase_vector = numpy.array([float(image_orientation[3]), float(image_orientation[4]), float(image_orientation[5])])
    mosaic_vector = numpy.cross(read_vector, phase_vector)

    # normalize the vectors
    read_vector /= numpy.linalg.norm(read_vector)
    phase_vector /= numpy.linalg.norm(phase_vector)
    mosaic_vector /= numpy.linalg.norm(mosaic_vector)
    # create an empty array for the new bvecs
    bvecs = numpy.zeros([len(sorted_dicoms), 3])
    # for each slice calculate the new bvec
    for index in range(0, len(sorted_dicoms)):
        if type(sorted_dicoms[0]) is list:
            dicom_headers = sorted_dicoms[index][0]
        else:
            dicom_headers = sorted_dicoms[index]

        # get the bval als this is needed in some checks
        bval = common.get_is_value(dicom_headers[Tag(0x0019, 0x100c)])
        # get the bvec if it exists in the headers
        bvec = numpy.array([0, 0, 0])
        if Tag(0x0019, 0x100e) in dicom_headers:
            # in case of implicit VR the private field cannot be split into an array, we do this here
            bvec = numpy.array(common.get_fd_array_value(dicom_headers[Tag(0x0019, 0x100e)], 3))
        # if bval is 0 or the vector is 0 no projection is needed and the vector is 0,0,0
        new_bvec = numpy.array([0, 0, 0])

        if bval > 0 and not (bvec == [0, 0, 0]).all():
            # project the bvec and invert the y direction
            new_bvec = numpy.array(
                [numpy.dot(bvec, read_vector), -numpy.dot(bvec, phase_vector), numpy.dot(bvec, mosaic_vector)])
            # normalize the bvec
            new_bvec /= numpy.linalg.norm(new_bvec)
        bvecs[index, :] = new_bvec
    # save the found bvecs to the file
    common.write_bvec_file(bvecs, bvec_file)
