# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RIVM_PluginConfigManager
                                 A QGIS plugin
 Plugin to manage the different dev/acc/prd configuration profiles of different RIVM plugins
                             -------------------
        begin                : 2017-08-21
        copyright            : (C) 2017 by RIVM
        email                : marnix.de.ridder@rivm.nl
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load RIVM_PluginConfigManager class from file RIVM_PluginConfigManager.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .rivm_plugin_config_manager import RIVM_PluginConfigManager
    return RIVM_PluginConfigManager(iface)
