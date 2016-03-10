# -*- coding: utf-8 -*-
"""
dicom2nifti

@author: abrys
"""

import unittest
import tempfile
import shutil
import os

import tests.test_data as test_data
import dicom2nifti.convert_ge as convert_ge
from tests.test_tools import compare_nifti, compare_bval, compare_bvec, ground_thruth_filenames


class TestConversionGE(unittest.TestCase):
    def test_dti(self):
        tmp_output_dir = tempfile.mkdtemp()
        try:
            results = convert_ge.dicom_to_nifti(test_data.GE_DTI,
                                                os.path.join(tmp_output_dir, 'test.nii.gz'))
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GE_DTI)[0]) == True
            assert compare_bval(results['BVAL_FILE'],
                                ground_thruth_filenames(test_data.GE_DTI)[2]) == True
            assert compare_bvec(results['BVEC_FILE'],
                                ground_thruth_filenames(test_data.GE_DTI)[3]) == True

            convert_ge.dicom_to_nifti(test_data.GE_DTI_IMPLICIT,
                                      os.path.join(tmp_output_dir, 'test.nii.gz'))
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GE_DTI_IMPLICIT)[0]) == True
            assert compare_bval(results['BVAL_FILE'],
                                ground_thruth_filenames(test_data.GE_DTI_IMPLICIT)[2]) == True
            assert compare_bvec(results['BVEC_FILE'],
                                ground_thruth_filenames(test_data.GE_DTI_IMPLICIT)[3]) == True
        finally:
            shutil.rmtree(tmp_output_dir)

    def test_fmri(self):
        tmp_output_dir = tempfile.mkdtemp()
        try:
            results = convert_ge.dicom_to_nifti(test_data.GE_FMRI,
                                      os.path.join(tmp_output_dir, 'test.nii.gz'))
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GE_FMRI)[0]) == True
            results = convert_ge.dicom_to_nifti(test_data.GE_FMRI_IMPLICIT,
                                      os.path.join(tmp_output_dir, 'test.nii.gz'))
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GE_FMRI_IMPLICIT)[0]) == True
        finally:
            shutil.rmtree(tmp_output_dir)

    def test_anatomical(self):
        tmp_output_dir = tempfile.mkdtemp()
        try:
            results = convert_ge.dicom_to_nifti(test_data.GE_ANATOMICAL,
                                      os.path.join(tmp_output_dir, 'test.nii.gz'))
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GE_ANATOMICAL)[0]) == True
            results = convert_ge.dicom_to_nifti(test_data.GE_ANATOMICAL_IMPLICIT,
                                      os.path.join(tmp_output_dir, 'test.nii.gz'))
            assert compare_nifti(results['NII_FILE'],
                                 ground_thruth_filenames(test_data.GE_ANATOMICAL_IMPLICIT)[0]) == True
        finally:
            shutil.rmtree(tmp_output_dir)

    def test_is_ge(self):
        assert not convert_ge.is_ge(test_data.SIEMENS_ANATOMICAL)
        assert convert_ge.is_ge(test_data.GE_ANATOMICAL)
        assert not convert_ge.is_ge(test_data.PHILIPS_ANATOMICAL)

    def test_is_frmi(self):
        dti_group = convert_ge._get_grouped_dicoms(test_data.GE_DTI)
        fmri_group = convert_ge._get_grouped_dicoms(test_data.GE_FMRI)
        anatomical_group = convert_ge._get_grouped_dicoms(test_data.GE_ANATOMICAL)
        assert not convert_ge._is_frmi(dti_group)
        assert convert_ge._is_frmi(fmri_group)
        assert not convert_ge._is_frmi(anatomical_group)

    def test_is_dti(self):
        dti_group = convert_ge._get_grouped_dicoms(test_data.GE_DTI)
        fmri_group = convert_ge._get_grouped_dicoms(test_data.GE_FMRI)
        anatomical_group = convert_ge._get_grouped_dicoms(test_data.GE_ANATOMICAL)
        assert convert_ge._is_dti(dti_group)
        assert not convert_ge._is_dti(fmri_group)
        assert not convert_ge._is_dti(anatomical_group)


if __name__ == '__main__':
    unittest.main()
