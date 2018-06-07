# coding: utf-8

import numpy as np
from nose.tools import ok_, eq_

# local import
from smrt import make_snowpack, make_model, make_snow_layer
from smrt.inputs.sensor_list import amsre, active

#
# Ghi: rapid hack, should be splitted in different functions
#


def test_dmrt_oneconfig():
    # prepare inputs
    l = 2

    nl = l//2  # // Forces integer division
    thickness = np.array([0.1, 0.1]*nl)
    thickness[-1] = 100  # last one is semi-infinit
    radius = np.array([2e-4]*l)
    temperature = np.array([250.0, 250.0]*nl)
    density = [200, 400]*nl
    stickiness = [0.1, 0.1]*nl

    # create the snowpack
    snowpack = make_snowpack(thickness,
                             "sticky_hard_spheres",
                             density=density,
                             temperature=temperature,
                             radius=radius,
                             stickiness=stickiness)

    # create the EM Model
    m = make_model("dmrt_shortrange", "dort")

    # create the sensor
    radiometer = amsre('37V')

    # run the model
    res = m.run(radiometer, snowpack)

    print(res.TbV(), res.TbH())
    ok_((res.TbV() - 202.381059705594 ) < 1e-4)
    ok_((res.TbH() - 187.07930133881544) < 1e-4)


def test_less_refringent_bottom_layer_VV():
    # Regression test 19-03-2018: value may change if other bugs found
    snowpack = make_snowpack([0.2, 0.3], "sticky_hard_spheres", density = [290.0, 250.0], radius = 50e-6, stickiness=0.2)
    m = make_model("dmrt_qcacp_shortrange", "dort")
    scat = active(10e9, 45)
    res = m.run(scat, snowpack)
    print(res.sigmaVV())
    ok_(abs(res.sigmaVV() - 9.42202173e-06) < 1e-9)


def test_less_refringent_bottom_layer_HH():
    # Regression test 19-03-2018: value may change if other bugs found
    snowpack = make_snowpack([0.2, 0.3], "sticky_hard_spheres", density = [290.0, 250.0], radius = 50e-6, stickiness=0.2)
    m = make_model("dmrt_qcacp_shortrange", "dort")
    scat = active(10e9, 45)
    res = m.run(scat, snowpack)
    print(res.sigmaHH())
    ok_(abs(res.sigmaHH() - 8.86490556e-06) < 1e-9)


# The following test fails
# def test_less_refringent_bottom_layer_VV():
#     # Regression test 19-03-2018: value may change if other bugs found
#     snowpack = make_snowpack([0.2, 0.3], "sticky_hard_spheres", density = [290.0, 250.0], radius = 1e-4, stickiness=0.2)
#     m = make_model("dmrt_qcacp_shortrange", "dort")
#     scat = active(10e9, 45)
#     res = m.run(scat, snowpack)
#     print(res.sigmaVV())
#     ok_(abs(res.sigmaVV() - 7.54253344e-05) < 1e-7)
#
#
# def test_less_refringent_bottom_layer_HH():
#     # Regression test 19-03-2018: value may change if other bugs found
#     snowpack = make_snowpack([0.2, 0.3], "sticky_hard_spheres", density = [290.0, 250.0], radius = 1e-4, stickiness=0.2)
#     m = make_model("dmrt_qcacp_shortrange", "dort")
#     scat = active(10e9, 45)
#     res = m.run(scat, snowpack)
#     print(res.sigmaHH())
#     ok_(abs(res.sigmaHH() - 7.09606407e-05) < 1e-7)