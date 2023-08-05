=============
 dicom2nifti
=============

Python library for converting dicom files to nifti

:Author: Arne Brys
:Organization: `icometrix <https://www.icometrix.com>`_
:Repository: https://github.com/icometrix/dicom2nifti

===============
 Documentation
===============
---------------
 Installation
---------------
.. code-block:: bash

   pip install dicom2nifti

---------------
 General usage
---------------
.. code-block:: python

   import dicom2nifti

   dicom2nifti.dummy_function(dummy_data)

----------------
 Supported data
----------------
Most anatomical data for CT and MR should be supported as long as they are in classical dicom files.

Try avoiding "Implicit VR Endian" if possible as this makes converting non anatomical (i.e. DTI, fMRI, ...) much more difficult.

There is some vendor specific support, more specifically for DTI and fMRI

GE MR
^^^^^^
Anatomical data should all be support.
Both DTI(and similar) and fMRI(and similar) are supported.

Siemens MR
^^^^^^^^^^^
Anatomical data should all be support.
Both DTI(and similar) and fMRI(and similar) are supported.

Philips MR
^^^^^^^^^^^
For classical dicom files dicom2nifti support anatomical, DTI(and similar) and fMRI(and similar).

For "Philips Enhanced Dicom" there is no support for "Implicit VR Endian" transfer syntax.
For the others we support anatomical, DTI(and similar) and fMRI(and similar).

------------------
 Unsupported data
------------------
If you encounter unsupported data you can help the development of dicom2nifti by providing a dataset. This dataset should be anonymised (but leave as much of the private fields as possible).
