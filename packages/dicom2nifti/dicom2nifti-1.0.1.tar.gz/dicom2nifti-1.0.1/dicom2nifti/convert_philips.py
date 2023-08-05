# -*- coding: utf-8 -*-
"""
dicom2nifti

@author: abrys
"""

from __future__ import print_function
import os
import gc
import numpy
import nibabel
import dicom
import dicom2nifti.common as common
from dicom.tag import Tag
import dicom2nifti.convert_generic as convert_generic
from dicom2nifti.exceptions import ConversionError
dicom.config.enforce_valid_values = False


def is_philips(dicom_directory):
    """
    Use this function to detect if a dicom series is a philips dataset
    :param dicom_directory: directory with dicom files for 1 scan
    """
    # read dicom header
    header = common.read_first_header(dicom_directory)

    if 'Manufacturer' not in header or 'Modality' not in header:
        return False  # we try generic conversion in these cases

    # check if manufacturer is Philips
    if 'PHILIPS' not in header.Manufacturer.upper():
        return False

    # check if Modality is mr
    if header.Modality.upper() != 'MR':
        return False

    return True


def dicom_to_nifti(dicom_directory, output_file):
    """
    This is the main dicom to nifti conversion fuction for philips images.
    As input philips images are required. It will then determine the type of images and do the correct conversion

    Examples: See unit test
    :param output_file: file path to the output nifti
    :param dicom_directory: directory with dicom files for 1 scan
    """

    assert is_philips(dicom_directory)

    if is_multiframe_dicom(dicom_directory):
        _assert_explicit_vr(dicom_directory)
        print('Found multiframe dicom')
        if _is_multiframe_dti(dicom_directory):
            print('Found sequence type: MULTIFRAME DTI')
            return _multiframe_dti_to_nifti(dicom_directory, output_file)

        if _is_multiframe_fmri(dicom_directory):
            print('Found sequence type: MULTIFRAME FMRI')
            return _multiframe_to_nifti(dicom_directory, output_file)

        if _is_multiframe_anatomical(dicom_directory):
            print('Found sequence type: MULTIFRAME ANATOMICAL')
            return _multiframe_to_nifti(dicom_directory, output_file)
    else:
        print('Found singleframe dicom')
        grouped_dicoms = _get_grouped_dicoms(dicom_directory)
        if _is_singleframe_fmri(dicom_directory):
            print('Found sequence type: SINGLEFRAME FMRI')
            return _singleframe_to_nifti(grouped_dicoms, output_file)

        if _is_singleframe_dti(dicom_directory):
            print('Found sequence type: SINGLEFRAME DTI')
            return _singleframe_dti_to_nifti(grouped_dicoms, output_file)

    print('Assuming anatomical data')
    return convert_generic.dicom_to_nifti(dicom_directory, output_file)


def _assert_explicit_vr(dicom_directory):
    """
    Assert that explicit vr is used
    """
    header = common.read_first_header(dicom_directory)
    if header.file_meta[0x0002, 0x0010].value == '1.2.840.10008.1.2':
        raise ConversionError('IMPLICIT_VR_ENHANCED_DICOM')


def is_multiframe_dicom(dicom_directory):
    """
    Use this function to detect if a dicom series is a siemens fmri dataset
    NOTE: Only the first slice will be checked so you can only provide an already sorted dicom directory
    (containing one series)
    :param dicom_directory: directory with dicom files for 1 scan
    """
    # read dicom header
    header = common.read_first_header(dicom_directory)
    if header.file_meta[0x0002, 0x0002].value == '1.2.840.10008.5.1.4.1.1.4.1':
        return True
    return False


def _is_multiframe_dti(dicom_directory):
    """
    Use this function to detect if a dicom series is a philips multiframe dti dataset
    """
    # check if it is multi frame dicom
    if not is_multiframe_dicom(dicom_directory):
        return False

    header = common.read_first_header(dicom_directory)

    # check if there are multiple stacks
    number_of_stack_slices = common.get_ss_value(header[Tag(0x2001, 0x105f)][0][Tag(0x2001, 0x102d)])

    number_of_stacks = int(int(header.NumberOfFrames) / int(number_of_stack_slices))
    if number_of_stacks <= 1:
        return False

    # check if there is diffusion info in the frame
    found_diffusion = False
    diffusion_tag = Tag(0x0018, 0x9117)
    for frame in header.PerFrameFunctionalGroupsSequence:
        if diffusion_tag in frame:
            found_diffusion = True
            break
    if not found_diffusion:
        return False

    return True


def _is_multiframe_fmri(dicom_directory):
    """
    Use this function to detect if a dicom series is a philips multiframe fmri dataset
    """
    # check if it is multi frame dicom
    if not is_multiframe_dicom(dicom_directory):
        return False

    header = common.read_first_header(dicom_directory)

    # check if there are multiple stacks
    number_of_stack_slices = common.get_ss_value(header[Tag(0x2001, 0x105f)][0][Tag(0x2001, 0x102d)])
    number_of_stacks = int(int(header.NumberOfFrames) / number_of_stack_slices)
    if number_of_stacks <= 1:
        return False

    # check if there is NO diffusion info in the frame
    found_diffusion = False
    diffusion_tag = Tag(0x0018, 0x9117)
    for frame in header.PerFrameFunctionalGroupsSequence:
        if diffusion_tag in frame:
            found_diffusion = True
            break
    if found_diffusion:
        return False

    return True


def _is_multiframe_anatomical(dicom_directory):
    """
    Use this function to detect if a dicom series is a philips multiframe anatomical dataset
    NOTE: Only the first slice will be checked so you can only provide an already sorted dicom directory
    (containing one series)
    """
    # check if it is multi frame dicom
    if not is_multiframe_dicom(dicom_directory):
        return False

    header = common.read_first_header(dicom_directory)

    # check if there are multiple stacks
    number_of_stack_slices = common.get_ss_value(header[Tag(0x2001, 0x105f)][0][Tag(0x2001, 0x102d)])
    number_of_stacks = int(int(header.NumberOfFrames) / number_of_stack_slices)

    if number_of_stacks > 1:
        return False

    return True


def _is_singleframe_fmri(dicom_directory):
    """
    Use this function to detect if a dicom series is a philips singleframe fmri dataset
    """
    header = common.read_first_header(dicom_directory)

    # check if there are stack information
    slice_number_mr_tag = Tag(0x2001, 0x100a)
    if slice_number_mr_tag not in header:
        return False

    # check if there are multiple timepoints
    grouped_dicoms = _get_grouped_dicoms(dicom_directory, fast_read=False)
    if len(grouped_dicoms) <= 1:
        return False

    # check that there is bval information
    if _is_bval_type_a(grouped_dicoms) or _is_bval_type_b(grouped_dicoms):
        return False

    return True


def _is_float(value):
    """
    Check if float
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def _is_singleframe_dti(dicom_directory):
    """
    Use this function to detect if a dicom series is a philips singleframe dti dataset
    """
    header = common.read_first_header(dicom_directory)

    # check if there is stack information
    slice_number_mr_tag = Tag(0x2001, 0x100a)
    if slice_number_mr_tag not in header:
        return False

    # check if there are multiple timepoints
    grouped_dicoms = _get_grouped_dicoms(dicom_directory, fast_read=False)
    if len(grouped_dicoms) <= 1:
        return False

    # check that there is bval information
    if _is_bval_type_b(grouped_dicoms):
        return True
    if _is_bval_type_a(grouped_dicoms):
        return True

    return False


def _is_bval_type_a(grouped_dicoms):
    """
    Check if the bvals are stored in the first of 2 currently known ways for single frame dti
    """
    bval_tag = Tag(0x2001, 0x1003)
    bvec_x_tag = Tag(0x2005, 0x10b0)
    bvec_y_tag = Tag(0x2005, 0x10b1)
    bvec_z_tag = Tag(0x2005, 0x10b2)
    for group in grouped_dicoms:
        if bvec_x_tag in group[0] and _is_float(common.get_fl_value(group[0][bvec_x_tag])) and \
                        bvec_y_tag in group[0] and _is_float(common.get_fl_value(group[0][bvec_y_tag])) and \
                        bvec_z_tag in group[0] and _is_float(common.get_fl_value(group[0][bvec_z_tag])) and \
                        bval_tag in group[0] and _is_float(common.get_fl_value(group[0][bval_tag])) and \
                        common.get_fl_value(group[0][bval_tag]) != 0:
            return True
    return False


def _is_bval_type_b(grouped_dicoms):
    """
    Check if the bvals are stored in the second of 2 currently known ways for single frame dti
    """
    bval_tag = Tag(0x0018, 0x9087)
    bvec_tag = Tag(0x0018, 0x9089)
    for group in grouped_dicoms:
        if bvec_tag in group[0] and bval_tag in group[0]:
            bvec = common.get_fd_array_value(group[0][bvec_tag], 3)
            bval = common.get_fd_value(group[0][bval_tag])
            if _is_float(bvec[0]) and _is_float(bvec[1]) and _is_float(bvec[2]) and _is_float(bval) and bval != 0:
                return True
    return False


def _multiframe_dti_to_nifti(dicom_directory, output_file):
    """
    Convert a multiframe dti dicom file to a nifti with bval an bvec files
    """

    # Read the multiframe dicom file
    print('Read dicom file')
    multiframe_dicom = common.read_first_header(dicom_directory, fast_read=False)

    # Create mosaic block
    print('Creating data block')
    full_block = _multiframe_dti_to_block(multiframe_dicom)

    print('Creating affine')

    # Create the nifti header info
    affine = _create_affine_multiframe(multiframe_dicom)
    print('Creating nifti')

    # Convert to nifti
    img = nibabel.Nifti1Image(full_block, affine)
    timing_parameters = multiframe_dicom.SharedFunctionalGroupsSequence[0].MRTimingAndRelatedParametersSequence[0]
    first_frame = multiframe_dicom[Tag(0x5200, 0x9230)][0]
    common.set_tr_te(img, float(timing_parameters.RepetitionTime),
                     float(first_frame[0x2005, 0x140f][0].EchoTime))

    # Save to disk
    print('Saving nifti to disk %s' % output_file)
    img.to_filename(output_file)

    # Create the bval en bvec files
    base_path = os.path.dirname(output_file)
    base_name = os.path.splitext(os.path.splitext(os.path.basename(output_file))[0])[0]
    print('Creating bval en bvec files')
    bval_file = '%s/%s.bval' % (base_path, base_name)
    bvec_file = '%s/%s.bvec' % (base_path, base_name)
    _create_bvals_bvecs(multiframe_dicom, bval_file, bvec_file, img, output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file,
            'BVAL_FILE': bval_file,
            'BVEC_FILE': bvec_file}


def _multiframe_to_nifti(dicom_directory, output_file):
    """
    This function will convert philips fmri or anatomical multiframe series to a nifti
    """

    # Read the multiframe dicom file
    print('Read dicom file')
    multiframe_dicom = common.read_first_header(dicom_directory, fast_read=False)

    # Create mosaic block
    print('Creating data block')
    full_block = _multiframe_to_block(multiframe_dicom)

    print('Creating affine')

    # Create the nifti header info
    affine = _create_affine_multiframe(multiframe_dicom)
    print('Creating nifti')

    # Convert to nifti
    img = nibabel.Nifti1Image(full_block, affine)
    timing_parameters = multiframe_dicom.SharedFunctionalGroupsSequence[0].MRTimingAndRelatedParametersSequence[0]
    first_frame = multiframe_dicom[Tag(0x5200, 0x9230)][0]
    common.set_tr_te(img, float(timing_parameters.RepetitionTime),
                     float(first_frame[0x2005, 0x140f][0].EchoTime))

    print('Saving nifti to disk')
    # Save to disk
    print('Saving nifti to disk %s' % output_file)
    img.to_filename(output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file}


def _singleframe_to_nifti(grouped_dicoms, output_file):
    """
    This function will convert a philips singleframe series to a nifti
    """

    # Create mosaic block
    print('Creating data block')
    full_block = _singleframe_to_block(grouped_dicoms)

    print('Creating affine')
    # Create the nifti header info
    affine = common.create_affine(grouped_dicoms[0])

    print('Creating nifti')
    # Convert to nifti
    img = nibabel.Nifti1Image(full_block, affine)
    common.set_tr_te(img, float(grouped_dicoms[0][0].RepetitionTime), float(grouped_dicoms[0][0].EchoTime))

    print('Saving nifti to disk %s' % output_file)
    # Save to disk
    img.to_filename(output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file}


def _singleframe_dti_to_nifti(grouped_dicoms, output_file):
    """
    This function will convert a philips singleframe series to a nifti
    """

    # Create mosaic block
    print('Creating data block')
    full_block = _singleframe_to_block(grouped_dicoms)

    print('Creating affine')
    # Create the nifti header info
    affine = common.create_affine(grouped_dicoms[0])

    print('Creating nifti')
    # Convert to nifti
    img = nibabel.Nifti1Image(full_block, affine)
    common.set_tr_te(img, float(grouped_dicoms[0][0].RepetitionTime), float(grouped_dicoms[0][0].EchoTime))

    print('Saving nifti to disk %s' % output_file)
    # Save to disk
    img.to_filename(output_file)

    # Create the bval en bvec files
    base_name = os.path.splitext(output_file)[0]
    if base_name.endswith('.nii'):
        base_name = os.path.splitext(base_name)[0]

    print('Creating bval en bvec files')
    bval_file = '%s.bval' % base_name
    bvec_file = '%s.bvec' % base_name
    _create_singleframe_bvals_bvecs(grouped_dicoms, bval_file, bvec_file, img, output_file)

    gc.collect()  # force the collection for conversion of big datasets this is needed
    return {'NII_FILE': output_file,
            'BVAL_FILE': bval_file,
            'BVEC_FILE': bvec_file}


def _singleframe_to_block(grouped_dicoms):
    """
    Generate a full datablock containing all timepoints
    """
    # For each slice / mosaic create a data volume block
    data_blocks = []
    for index in range(0, len(grouped_dicoms)):
        print('Creating block %s of %s' % (index + 1, len(grouped_dicoms)))
        data_blocks.append(_stack_to_block(grouped_dicoms[index]))

    # Add the data_blocks together to one 4d block
    size_x = numpy.shape(data_blocks[0])[0]
    size_y = numpy.shape(data_blocks[0])[1]
    size_z = numpy.shape(data_blocks[0])[2]
    size_t = len(data_blocks)
    full_block = numpy.zeros((size_x, size_y, size_z, size_t), dtype=data_blocks[0].dtype)
    for index in range(0, size_t):
        full_block[:, :, :, index] = data_blocks[index]

    return full_block


def _stack_to_block(timepoint_dicoms):
    """
    Convert a mosaic slice to a block of data by reading the headers, splitting the mosaic and appending
    """
    return common.get_volume_pixeldata(timepoint_dicoms)


def _get_grouped_dicoms(dicom_directory, fast_read=False):
    """
    Search all dicoms in the dicom directory, sort and validate them

    fast_read = True will only read the headers not the data
    """
    # Loop overall files and build dict
    dicoms = []
    rows_tag = Tag(0x0028, 0x0010)
    columns_tag = Tag(0x0028, 0x0011)
    for root, _, file_names in os.walk(dicom_directory):
        # go over all the files and try to read the dicom header
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if common.is_dicom_file(file_path):
                # Read each dicom file and put in dict
                read_dicom = dicom.read_file(file_path, stop_before_pixels=fast_read)
                # skip files without data by checking rows anc columns.
                if rows_tag not in read_dicom or columns_tag not in read_dicom:
                    continue
                dicoms.append(read_dicom)

    # Order all dicom files by InstanceNumber
    dicoms = sorted(dicoms, key=lambda x: x.InstanceNumber)

    # now group per stack
    grouped_dicoms = [[]]  # list with first element a list
    timepoint_index = 0
    previous_stack_position = -1

    # loop over all sorted dicoms
    stack_position_tag = Tag(0x2001, 0x100a)  # put this there as this is a slow step and used a lot
    for index in range(0, len(dicoms)):
        dicom_ = dicoms[index]
        stack_position = 0
        if stack_position_tag in dicom_:
            stack_position = common.get_is_value(dicom_[stack_position_tag])
        if previous_stack_position == stack_position:
            # if the stack number is the same we move to the next timepoint
            timepoint_index += 1
            if len(grouped_dicoms) <= timepoint_index:
                grouped_dicoms.append([])
        else:
            # if it changes move back to the first timepoint
            timepoint_index = 0
        grouped_dicoms[timepoint_index].append(dicom_)
        previous_stack_position = stack_position

    return grouped_dicoms


def _create_affine_multiframe(multiframe_dicom):
    """
    Function to create the affine matrix for a siemens mosaic dataset
    This will work for siemens dti and fmri if in mosaic format
    """
    first_frame = multiframe_dicom[Tag(0x5200, 0x9230)][0]
    # Create affine matrix (http://nipy.sourceforge.net/nibabel/dicom/dicom_orientation.html#dicom-slice-affine)
    image_orient1 = numpy.array(first_frame.PlaneOrientationSequence[0].ImageOrientationPatient)[0:3].astype(float)
    image_orient2 = numpy.array(first_frame.PlaneOrientationSequence[0].ImageOrientationPatient)[3:6].astype(float)

    normal = numpy.cross(image_orient1, image_orient2)

    delta_r = float(first_frame[0x2005, 0x140f][0].PixelSpacing[0])
    delta_c = float(first_frame[0x2005, 0x140f][0].PixelSpacing[1])

    image_pos = numpy.array(first_frame.PlanePositionSequence[0].ImagePositionPatient).astype(float)

    delta_s = float(multiframe_dicom.SpacingBetweenSlices)
    return numpy.matrix(
        [[-image_orient1[0] * delta_r, -image_orient2[0] * delta_c, -delta_s * normal[0], -image_pos[0]],
         [-image_orient1[1] * delta_r, -image_orient2[1] * delta_c, -delta_s * normal[1], -image_pos[1]],
         [image_orient1[2] * delta_r, image_orient2[2] * delta_c, delta_s * normal[2], image_pos[2]],
         [0, 0, 0, 1]])


def _multiframe_to_block(multiframe_dicom):
    """
    Generate a full datablock containing all stacks
    """
    # Calculate the amount of stacks and slices in the stack
    number_of_stack_slices = int(common.get_ss_value(multiframe_dicom[Tag(0x2001, 0x105f)][0][Tag(0x2001, 0x102d)]))
    number_of_stacks = int(int(multiframe_dicom.NumberOfFrames) / number_of_stack_slices)

    # We create a numpy array
    size_x = multiframe_dicom.pixel_array.shape[2]
    size_y = multiframe_dicom.pixel_array.shape[1]
    size_z = number_of_stack_slices
    size_t = number_of_stacks
    # get the format
    format_string = common.get_numpy_type(multiframe_dicom)
    full_block = numpy.zeros((size_x, size_y, size_z, size_t), dtype=format_string)

    # get header info needed for ordering
    frame_info = multiframe_dicom[0x5200, 0x9230]

    data_4d = numpy.zeros((size_z, size_y, size_x, size_t), dtype=format_string)

    # loop over each slice and insert in datablock
    for slice_index in range(0, size_t * size_z):
        z_location = frame_info[slice_index].FrameContentSequence[0].InStackPositionNumber - 1
        t_location = frame_info[slice_index].FrameContentSequence[0].TemporalPositionIndex - 1

        data_4d[z_location, :, :, t_location] = multiframe_dicom.pixel_array[slice_index, :, :]

    # loop over each stack
    for t_index in range(0, size_t):
        # transpose the block so the directions are correct
        data_3d = numpy.transpose(data_4d[:, :, :, t_index], (2, 1, 0))
        # add the block the the full data
        full_block[:, :, :, t_index] = data_3d

    # Apply the rescaling if needed
    if 'RescaleSlope' in multiframe_dicom or 'RescaleIntercept' in multiframe_dicom:
        rescale_slope = 1
        rescale_offset = 0
        if 'RescaleSlope' in multiframe_dicom:
            rescale_slope = multiframe_dicom.RescaleSlope
        if 'RescaleIntercept' in multiframe_dicom:
            rescale_offset = multiframe_dicom.RescaleIntercept
        common.apply_scaling(full_block, rescale_slope, rescale_offset)

    return full_block


def _multiframe_dti_to_block(multiframe_dicom):
    """
    Generate a full datablock containing all stacks
    """
    # Calculate the amount of stacks and slices in the stack
    number_of_stack_slices = common.get_ss_value(multiframe_dicom[Tag(0x2001, 0x105f)][0][Tag(0x2001, 0x102d)])
    number_of_stacks = int(int(multiframe_dicom.NumberOfFrames) / number_of_stack_slices)

    # We create a numpy array
    size_x = multiframe_dicom.pixel_array.shape[2]
    size_y = multiframe_dicom.pixel_array.shape[1]
    size_z = number_of_stack_slices
    size_t = number_of_stacks

    # get the format
    format_string = common.get_numpy_type(multiframe_dicom)
    full_block = numpy.zeros((size_x, size_y, size_z, size_t), dtype=format_string)

    # get header info needed for ordering
    frame_info = multiframe_dicom[0x5200, 0x9230]
    data_4d = numpy.zeros((size_z, size_y, size_x, size_t), dtype=format_string)

    # loop over each slice and insert in datablock
    for index_z in range(0, size_z):
        for index_t in range(0, size_t):
            slice_index = int(size_t * index_z + index_t)
            z_location = frame_info[slice_index].FrameContentSequence[0].InStackPositionNumber - 1

            print('Importing slice on position %s %s %s' % (slice_index, z_location, index_t))
            data_4d[z_location, :, :, index_t] = multiframe_dicom.pixel_array[slice_index, :, :]

    # loop over each stack
    for t_index in range(0, size_t):
        # transpose the block so the directions are correct
        data_3d = numpy.transpose(data_4d[:, :, :, t_index], (2, 1, 0))
        # add the block the the full data
        full_block[:, :, :, t_index] = data_3d

    # Apply the rescaling if needed
    if 'RescaleSlope' in multiframe_dicom or 'RescaleIntercept' in multiframe_dicom:
        rescale_slope = 1
        rescale_offset = 0
        if 'RescaleSlope' in multiframe_dicom:
            rescale_slope = multiframe_dicom.RescaleSlope
        if 'RescaleIntercept' in multiframe_dicom:
            rescale_offset = multiframe_dicom.RescaleIntercept
        common.apply_scaling(full_block, rescale_slope, rescale_offset)

    return full_block


def _get_dicom_files(dicom_directory):
    """
    Search all dicoms in the dicom directory
    """
    dicoms = []
    for root, _, file_names in os.walk(dicom_directory):
        # go over all the files and try to read the dicom header
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if common.is_dicom_file(file_path):
                # Read each dicom file and put in dict
                dicoms.append(file_path)
    return dicoms


def _create_bvals_bvecs(multiframe_dicom, bval_file, bvec_file, nifti, nifti_file):
    """
    Write the bvals from the sorted dicom files to a bval file
    Inspired by https://github.com/IBIC/ibicUtils/blob/master/ibicBvalsBvecs.py
    """

    # create the empty arrays
    number_of_stack_slices = common.get_ss_value(multiframe_dicom[Tag(0x2001, 0x105f)][0][Tag(0x2001, 0x102d)])
    number_of_stacks = int(int(multiframe_dicom.NumberOfFrames) / number_of_stack_slices)

    bvals = numpy.zeros([number_of_stacks], dtype=numpy.int32)
    bvecs = numpy.zeros([number_of_stacks, 3])

    # loop over all timepoints and create a list with all bvals and bvecs
    for stack_index in range(0, number_of_stacks):
        stack = multiframe_dicom[Tag(0x5200, 0x9230)][stack_index]
        if str(stack[Tag(0x0018, 0x9117)][0][Tag(0x0018, 0x9075)].value) == 'DIRECTIONAL':
            bvals[stack_index] = common.get_fd_value(stack[Tag(0x0018, 0x9117)][0][Tag(0x0018, 0x9087)])
            bvecs[stack_index, :] = common.get_fd_array_value(stack[Tag(0x0018, 0x9117)][0]
                                                              [Tag(0x0018, 0x9076)][0][Tag(0x0018, 0x9089)], 3)

    # truncate nifti if needed
    nifti, bvals, bvecs = _fix_dti(bvals, bvecs, nifti, nifti_file)

    # save the found bvecs to the file
    common.write_bval_file(bvals, bval_file)
    common.write_bvec_file(bvecs, bvec_file)


def _fix_dti(bvals, bvecs, nifti, nifti_file):
    """
    This function will remove the last timepoint from the nifti, bvals and bvecs if the last vector is 0,0,0
    This is sometimes added at the end by philips
    """
    if not numpy.allclose(bvecs[-1], [0, 0, 0]):
        # nothing needs to be done here
        return nifti, bvals, bvecs
    # remove last elements from bvals and bvecs
    bvals = bvals[:-1]
    bvecs = bvecs[:-1]

    # remove last elements from the nifti
    new_nifti = nibabel.Nifti1Image(nifti.get_data()[:, :, :, :-1], nifti.get_affine())
    new_nifti.to_filename(nifti_file)

    return new_nifti, bvals, bvecs


def _create_singleframe_bvals_bvecs(grouped_dicoms, bval_file, bvec_file, nifti, nifti_file):
    """
    Write the bvals from the sorted dicom files to a bval file
    """

    # create the empty arrays
    bvals = numpy.zeros([len(grouped_dicoms)], dtype=numpy.int32)
    bvecs = numpy.zeros([len(grouped_dicoms), 3])

    # loop over all timepoints and create a list with all bvals and bvecs
    if _is_bval_type_a(grouped_dicoms):
        bval_tag = Tag(0x2001, 0x1003)
        bvec_x_tag = Tag(0x2005, 0x10b0)
        bvec_y_tag = Tag(0x2005, 0x10b1)
        bvec_z_tag = Tag(0x2005, 0x10b2)
        for stack_index in range(0, len(grouped_dicoms)):
            bvals[stack_index] = common.get_fl_value(grouped_dicoms[stack_index][0][bval_tag])
            bvecs[stack_index, :] = [common.get_fl_value(grouped_dicoms[stack_index][0][bvec_x_tag]),
                                     common.get_fl_value(grouped_dicoms[stack_index][0][bvec_y_tag]),
                                     common.get_fl_value(grouped_dicoms[stack_index][0][bvec_z_tag])]
    elif _is_bval_type_b(grouped_dicoms):
        bval_tag = Tag(0x0018, 0x9087)
        bvec_tag = Tag(0x0018, 0x9089)
        for stack_index in range(0, len(grouped_dicoms)):
            bvals[stack_index] = common.get_fd_value(grouped_dicoms[stack_index][0][bval_tag])
            bvecs[stack_index, :] = common.get_fd_array_value(grouped_dicoms[stack_index][0][bvec_tag], 3)

    # truncate nifti if needed
    nifti, bvals, bvecs = _fix_dti(bvals, bvecs, nifti, nifti_file)

    # save the found bvecs to the file
    common.write_bval_file(bvals, bval_file)
    common.write_bvec_file(bvecs, bvec_file)

