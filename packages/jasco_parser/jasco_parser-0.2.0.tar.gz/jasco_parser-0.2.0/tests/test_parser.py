#!/usr/bin/env nosetests -v
# coding: utf-8
import os
from nose.tools import *
from jasco_parser import JASCOParser


filename = os.path.join(
    os.path.dirname(__file__),
    'test_fluorescence_spectrum.txt',
)


def test_parse():
    parser = JASCOParser()
    with open(filename, 'r') as fi:
        X = parser.parse(fi)
        eq_(X[0][0], 490.0)
        eq_(X[0][1], 1344.15)
        eq_(X[-1][0], 650.0)
        eq_(X[-1][1], 1.20398)


def test_load():
    parser = JASCOParser()
    X = parser.load(filename)
    eq_(X[0][0], 490.0)
    eq_(X[0][1], 1344.15)
    eq_(X[-1][0], 650.0)
    eq_(X[-1][1], 1.20398)
