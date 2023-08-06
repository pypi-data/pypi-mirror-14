# Copyright (c) 2013,Vienna University of Technology,
# Department of Geodesy and Geoinformation
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Vienna University of Technology,
#      Department of Geodesy and Geoinformation nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

Created on Tue Nov 25 11:51:59 2014

@author: Christoph.Paulik@geo.tuwien.ac.at
'''

import netCDF4
import numpy as np
import pytest
import os
import stat
import tempfile
from shutil import rmtree


def set_writeable(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


@pytest.yield_fixture()
def tempdir():
    old_path = os.getcwd()
    new_path = tempfile.mkdtemp()
    os.chdir(new_path)
    yield
    os.chdir(old_path)
    rmtree(new_path, onerror=set_writeable)


def test_float32_big_endian_masking(tempdir):

    nc = netCDF4.Dataset("temp.nc", "w")
    nc.createDimension('obs', 10)
    var_big_endian = nc.createVariable(
        'obs_big_endian', '>f8', ('obs', ), endian='big')
    print var_big_endian[:]
    var_native_endian = nc.createVariable(
        'obs_native_endian', '<f8', ('obs', ), endian='native')
    print var_native_endian[:]
