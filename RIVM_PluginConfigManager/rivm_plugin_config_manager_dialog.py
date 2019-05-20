# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RIVM_PluginConfigManagerDialog
                                 A QGIS plugin
 Plugin to manage the different dev/acc/prd configuration profiles of different RIVM plugins
                             -------------------
        begin                : 2017-08-21
        git sha              : $Format:%H$
        copyright            : (C) 2017 by RIVM
        email                : marnix.de.ridder@rivm.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt import uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'rivm_plugin_config_manager_dialog_base.ui'))


class RIVM_PluginConfigManagerDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(RIVM_PluginConfigManagerDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
