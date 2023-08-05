#!/usr/bin/env python
import unittest
import wintx

import matplotlib
# Matplotlib is to use PNG visual output rather than screen display
matplotlib.use('Agg')
import pygrib

from datetime import datetime
from wintx import Fastener
from wintx.errors import WintxImportError
from wintx.importers import Grib

class WintxGribImporterTestCase(unittest.TestCase):

  WINTX_CONF_FILE = './wintx.conf'
  GRIB_FILE = './rap_130_20131122_1800_001.grb2'

  def setUp(self):
    self.wintx_instance = Fastener(self.WINTX_CONF_FILE)

  def tearDown(self):
    if( self.wintx_instance is not None ):
      self.wintx_instance.__startTransaction__()
      self.wintx_instance.cursor.execute("DELETE FROM Data")
      self.wintx_instance.cursor.execute("DELETE FROM Location")
      self.wintx_instance.cursor.execute("DELETE FROM Variable")
      self.wintx_instance.cursor.execute("DELETE FROM Level")
      self.wintx_instance.__endTransaction__(commit=True)

  def test_import_file(self):
    base_import_filter = {
        'latitude': {'>=': 40.0, '<=': 45.0},
        'longitude': {'>=': -88.0, '<=': -84.0},
    }

    import_filter = base_import_filter.copy()
    import_filter['varname'] = 'Pressure'
    import_instance = Grib.Importer('test', import_filter, self.WINTX_CONF_FILE)
    self.assertRaises(WintxImportError, import_instance.importFile, self.GRIB_FILE)

    import_filter = base_import_filter.copy()
    import_filter['varname'] = 'Geopotential Height'
    import_filter['level'] = 1000
    import_instance = Grib.Importer('test', import_filter, self.WINTX_CONF_FILE)
    result = import_instance.importFile(self.GRIB_FILE, ignore_unknowns=True)
    self.assertEqual(result['insertedRecords'], 1100)
    self.assertEqual(len(result['duplicateRecords']), 0)

    import_instance = Grib.Importer('test', import_filter, self.WINTX_CONF_FILE)
    result = import_instance.importFile(self.GRIB_FILE, ignore_unknowns=True)
    self.assertEqual(result['insertedRecords'], 0)
    self.assertEqual(len(result['duplicateRecords']), 1100)

    import_instance = Grib.Importer('test2', import_filter, self.WINTX_CONF_FILE)
    result = import_instance.importFile(self.GRIB_FILE, ignore_unknowns=True)
    self.assertEqual(result['insertedRecords'], 1100)
    self.assertEqual(len(result['duplicateRecords']), 0)

    import_filter['level'] = {'>=': 900, '<=': 975}
    import_instance = Grib.Importer('test', import_filter, self.WINTX_CONF_FILE)
    result = import_instance.importFile(self.GRIB_FILE, ignore_unknowns=True)
    self.assertEqual(result['insertedRecords'], 4400)
    self.assertEqual(len(result['duplicateRecords']), 0)

    import_filter['varname'] = 'Temperature'
    import_filter['level'] = 600
    import_instance = Grib.Importer('test', import_filter, self.WINTX_CONF_FILE)
    result = import_instance.importFile(self.GRIB_FILE, ignore_unknowns=True)
    self.assertEqual(result['insertedRecords'], 1100)
    self.assertEqual(len(result['duplicateRecords']), 0)

    import_filter['time'] = datetime.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    import_instance = Grib.Importer('test', import_filter, self.WINTX_CONF_FILE)
    result = import_instance.importFile(self.GRIB_FILE, ignore_unknowns=True)
    self.assertEqual(result['insertedRecords'], 0)
    self.assertEqual(len(result['duplicateRecords']), 0)

    import_filter = base_import_filter.copy()
    import_filter['varname'] = ['Geopotential Height', 'Temperature']
    import_filter['level'] = {'>=': 300, '<=': 400}
    import_instance = Grib.Importer('test', import_filter, self.WINTX_CONF_FILE)
    result = import_instance.importFile(self.GRIB_FILE, ignore_unknowns=True)
    self.assertEqual(result['insertedRecords'], 11000)
    self.assertEqual(len(result['duplicateRecords']), 0)

    import_filter['varname'].append('Pressure')
    import_filter['level'] = 0
    import_filter['leveltype'] = 'maxWind'
    import_instance = Grib.Importer('test', import_filter, self.WINTX_CONF_FILE)
    result = import_instance.importFile(self.GRIB_FILE, ignore_unknowns=True)
    self.assertEqual(result['insertedRecords'], 1100)
    self.assertEqual(len(result['duplicateRecords']), 0)

if( __name__=='__main__' ):
  unittest.main()
