#!/usr/bin/env python2.7

# (c) Massachusetts Institute of Technology 2015-2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Created on Feb 11, 2015

@author: brian
"""

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

import matplotlib

# We want matplotlib to use our backend
matplotlib.use('module://matplotlib_backend')

import logging

from envisage.core_plugin import CorePlugin
from envisage.ui.tasks.tasks_plugin import TasksPlugin

from flow_task import FlowTaskPlugin
from cytoflow_application import CytoflowApplication
from op_plugins import ImportPlugin, ThresholdPlugin, HLogPlugin, RangePlugin, \
                       Range2DPlugin, PolygonPlugin, LogiclePlugin, \
                       BinningPlugin, LogPlugin
from view_plugins import HistogramPlugin, HexbinPlugin, ScatterplotPlugin, \
                         BarChartPlugin, Stats1DPlugin
                         
import sys

def run_gui():
    
    logging.basicConfig(level=logging.DEBUG)
    
    debug = ("--debug" in sys.argv)

    plugins = [CorePlugin(), TasksPlugin(), FlowTaskPlugin(debug = debug),
               ImportPlugin(), ThresholdPlugin(), HistogramPlugin(),
               HexbinPlugin(), ScatterplotPlugin(), RangePlugin(),
               Range2DPlugin(), PolygonPlugin(), BarChartPlugin(), 
               Stats1DPlugin(), BinningPlugin()]
    
    app = CytoflowApplication(id = 'edu.mit.synbio.cytoflow',
                              plugins = plugins)
    app.run()
    
    logging.shutdown()

if __name__ == '__main__':
    from pyface.qt import qt_api
    
    if qt_api == "pyside":
        print "Cytoflow uses PyQT; but it is trying to use PySide instead."
        print " - Make sure PyQT is installed."
        print " - If both are installed, and you don't need both, uninstall PySide."
        print " - If you must have both installed, select PyQT by setting the"
        print "   environment variable QT_API to \"pyqt\""
        print "   * eg, on Linux, type on the command line:"
        print "     QT_API=\"pyqt\" python run.py"
        print "   * on Windows, try: "
        print "     setx QT_API \"pyqt\""

        sys.exit(1)
    

    run_gui()
