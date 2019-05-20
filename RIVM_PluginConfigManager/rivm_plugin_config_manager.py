# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RIVM_PluginConfigManager
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
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolBar

# Initialize Qt resources from file resources.py
from . import resources
# Import the code for the dialog
from qgis.core import QgsMessageLog, Qgis

from .rivm_plugin_config_manager_dialog import RIVM_PluginConfigManagerDialog
from .networkaccessmanager import NetworkAccessManager, RequestsException
import os.path


class RIVM_PluginConfigManager:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'RIVM_PluginConfigManager_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.MSG_TITLE = self.tr('RIVM Plugin Config Manager')
        self.LAST_ENVIRONMENT_KEY = 'rivm_config/last_environment'
        self.PRD = 'prd'
        self.ACC = 'acc'
        self.DEV = 'dev'


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&RIVM_PluginConfigManager')

        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.get_rivm_toolbar()

        self.settings_url = 'http://repo.svc.cal-net.nl/repo/rivm/qgis/'
        self.nam = NetworkAccessManager()

    # TODO: move this to a commons class/module
    def get_rivm_toolbar(self):
        TOOLBAR_TITLE = 'RIVM Cal-Net Toolbar'  # TODO get this from commons and make translatable
        toolbars = self.iface.mainWindow().findChildren(QToolBar, TOOLBAR_TITLE)
        if len(toolbars) == 0:
            toolbar = self.iface.addToolBar(TOOLBAR_TITLE)
            toolbar.setObjectName(TOOLBAR_TITLE)
        else:
            toolbar = toolbars[0]
        return toolbar

    def get_rivm_iconpath(self, environment):
        icon_path = ':/plugins/RIVM_PluginConfigManager/images/icon.' + environment + '.svg'
        return icon_path

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RIVM_PluginConfigManager', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        # Create the dialog (after translation) and keep reference
        self.dlg = RIVM_PluginConfigManagerDialog(self.iface.mainWindow())
        # create the environments dropdown
        self.dlg.cb_environment.addItem(self.tr('Production'), self.PRD)
        self.dlg.cb_environment.addItem(self.tr('Acceptance'), self.ACC)
        self.dlg.cb_environment.addItem(self.tr('Development'), self.DEV)

        # set dialog environment dropdown to show the last selected environment as current
        environment = QSettings().value(self.LAST_ENVIRONMENT_KEY)
        index = self.dlg.cb_environment.findData(environment)
        if index < 0:
            index = 0
            environment = self.PRD
        self.dlg.cb_environment.setCurrentIndex(index)

        icon_path = self.get_rivm_iconpath(environment)
        self.action = self.add_action(
            icon_path,
            text=self.tr(u'Manage RIVM plugin configurations'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&RIVM_PluginConfigManager'),
                action)
            self.toolbar.removeAction(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # retrieve ini file
            try:
                index = self.dlg.cb_environment.currentIndex()
                environment = self.dlg.cb_environment.itemData(index)
                icon_path = self.get_rivm_iconpath(environment)
                self.action.setIcon(QIcon(icon_path))
                url = self.settings_url + environment + '.rivm.ini'
                (response, content) = self.nam.request(url)
                if response.status != 200:
                    # TODO: what? Take offline ini file?
                    self.info(self.tr("Error retrieving config, response: " + str(response.status)))
                    return
                self.info(response.content)
                # write ini file to settings.ini
                filename = os.path.join(os.path.dirname(__file__), "settings.ini")
                #self.info(filename)
                with open(filename, 'wb') as f:  # using 'with open', then file is explicitly closed
                    f.write(response.content)
                # create a QSettings object from it
                settings = QSettings(filename, QSettings.IniFormat)
                # merge that object into qgis user settings
                qgis_settings = QSettings()
                qgis_settings.setValue(self.LAST_ENVIRONMENT_KEY, environment)
                for key in settings.allKeys():
                    self.info('Setting: {} -> {}'.format(key, settings.value(key)))
                    qgis_settings.setValue(key, settings.value(key))

            except RequestsException as e:
                # "Handle" exception
                self.info("Exception in retrieving rivm.ini {}".format(e.message))

    def info(self, msg=""):
        QgsMessageLog.logMessage('{}'.format(msg), 'PDOK-services Plugin', Qgis.Info)
