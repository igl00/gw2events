import psutil
import sys
import logging
import argparse
from PySide.QtGui import *
from PySide.QtCore import *

import build_utils
from events import GW2Events
from flowLayout import FlowLayout

from ui import mainGui, aboutGui, settingsGui, bossPanelGui, detailsPanelGui


class MainWindow(QMainWindow, mainGui.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the ui
        self.setupUi(self)

        # Restore settings from previous session
        self.settings = QSettings("GW2Events", "igl00")
        self.read_window_settings()

        # Set the asset root directory
        self.asset_root = ":/assets/"

        # Update the Gw2 Instance IP address
        self.ip_updater = IPThread("Gw2.exe")
        self.ip_timer = QTimer(self)
        self.ip_timer.timeout.connect(lambda: self.ip_updater.start())
        self.connect(self.ip_updater, SIGNAL("updateIP(QString)"), self.set_ip_label)

        # Build and update the event times
        self.gw2events = GW2Events()
        self.event_data = self.gw2events.events

        update_timer = QTimer(self)
        update_timer.timeout.connect(lambda: self.update_events(self.gw2events))
        update_timer.start(1000)

        # Load custom font
        self.add_font(self.asset_root + 'fonts/Legacy Sans Bold.ttf')
        self.add_font(self.asset_root + 'fonts/GWTwoFont1p1.ttf')

        # Set the applications style
        self.set_style_sheet()

        # Create the flow layout for the main canvas
        self.mainCanvas_layout = FlowLayout(margin=0, spacing=0)
        self.mainCanvas_widget.setLayout(self.mainCanvas_layout)

        # Add the details widget as the first flow item
        self.details = None
        logger.debug(self.gw2events.build_events()[0][0])
        self.build_details_panel(widget_name=self.gw2events.build_events()[0][0])
        self.details.hide()

        # Build the panels
        self.build_boss_panels(self.gw2events)

        # Create the extra windows
        self.settings_window = SettingsWindow(self, self.settings)
        self.about_window = AboutWindow(self)

        # Menu items
        # self.actionAlway_On_Top.triggered.connect(self.toggle_stay_on_top)  # Need to recreate window for it to work.
        self.actionAbout.triggered.connect(self.open_about_window)
        self.actionSettings.triggered.connect(self.open_settings_window)
        self.actionExit.triggered.connect(self.close)

        self.read_settings()

    def build_boss_panels(self, gw2events):
        """
        Build the boss panels
        """
        events = gw2events.build_events()

        for event in events:
            boss, time, active = event
            average_time = gw2events.events[boss]["average_time"]

            logger.debug("Building the boss panel for: %s" % boss)

            widget = BossPanel(self.asset_root, boss, time, average_time, active, parent=self.mainCanvas_widget)
            self.connect(widget, SIGNAL("clicked(QString)"), self.toggle_details_panel)

            self.mainCanvas_layout.addWidget(widget)

    def rebuild_panels(self, gw2events):
        """
        Delete then recreate the boss panels
        """
        details_hidden = self.details.isHidden()

        for widget in self.mainCanvas_widget.findChildren(QWidget):
            logger.debug("Scheduled for deletion: %s" % widget)
            widget.deleteLater()

        self.build_details_panel(widget_name=self.gw2events.build_events()[0][0])
        self.build_boss_panels(gw2events)

        if details_hidden:
            self.details.hide()

    def build_details_panel(self, widget_name):
        """
        Create the details panel
        """
        logger.debug("Building the details panel. Spawned by: %s" % widget_name)

        detail_widget = DetailsPanel(self.asset_root, self.event_data, widget_name, parent=self.mainCanvas_widget)

        # Add to the font of the flow layout
        self.mainCanvas_layout.addWidget(detail_widget)

        self.details = detail_widget

    def toggle_details_panel(self, widget):
        """
        Show or hide the details panel depending on its current state.
        """
        if self.details:
            self.details.show(widget)

    def update_events(self, gw2events):
        """
        Updates the times on the boss panels and calls a rebuild when the order needs to be changed.
        """
        events = gw2events.build_events()
        for event in events:
            boss, time, active = event
            average_time = gw2events.events[boss]["average_time"]
            name = boss.replace(" ", "").lower()

            # Get the widget for the current event
            widget = self.findChild(QWidget, "%s_widget" % name)
            if widget:
                # If the widget is active but the event is not rebuild all the panels
                if widget.active and not active:
                    self.rebuild_panels(self.gw2events)
                    break
                elif active and not widget.active:
                    self.rebuild_panels(self.gw2events)
                    break

                # Set the active state of the widget based on the events active state
                widget.active = active
                widget.update_active()
                # Update the current time
                widget.update_timer(time, average_time)

    def start_ip_timer(self, run, frequency):
        """
        Starts or stops the instace ip timer.
        """
        self.ip_timer.stop()
        if run == "true":
            self.ip_timer.start(frequency)
        else:
            self.serverAddress.setText("")

    def set_style_sheet(self):
        """
        Apply the main css styles to the window.
        """
        style_sheet = QFile(":/assets/stylesheets/main.qss")
        style_sheet.open(QFile.ReadOnly)
        self.setStyleSheet(str(style_sheet.readAll()))

    def open_settings_window(self):
        """
        Shows the settings window and runs the read_settings() method if the settings are accepted.
        """
        self.settings_window.show()
        self.settings_window.connect(self.settings_window, SIGNAL("accepted()"), self.read_settings)

    def read_window_settings(self):
        """
        Reads the saved window state and applies it to the current window.
        """
        settings = self.settings
        settings.beginGroup("MainWindow")
        try:
            self.resize(settings.value("size"))
            self.move(settings.value("pos"))
        except TypeError as error:
            logger.error(error)
        self.settings.endGroup()

    def write_window_settings(self):
        """
        Saves the windows current state(size, position, ...)
        """
        settings = self.settings
        settings.beginGroup("MainWindow")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.endGroup()

    def read_settings(self):
        settings = self.settings
        try:
            self.start_ip_timer(settings.value("update_ip"), settings.value("update_ip_frequency") * 1000)
        except TypeError as error:
            logger.error(error)
            self.start_ip_timer(True, 5000)

    def open_about_window(self):
        """
        Shows the about window.
        """
        self.about_window.show()

    def set_ip_label(self, text):
        logger.debug("Received updateIP signal with update: \"%s\"" % text)
        self.serverAddress.setText(text)

    @staticmethod
    def add_font(font):
        """
        Add an external font to the application.
        """
        QFontDatabase.addApplicationFont(font)

    def closeEvent(self, event):
        """
        Over-rides the default close event to enable the saving of the
        window position and size before it closes.
        """
        self.write_window_settings()
        event.accept()


class IPThread(QThread):
    """
    A worker thread dedicated to getting the current Gw2 map instance IP address.
    """
    def __init__(self, process, parent=None):
        super().__init__(parent)
        logger.debug("Started the ip thread.")
        self.process = process

    def run(self):
        ip = self.get_remote_ip(self.process)
        logger.debug("IPThread ip: %s" % ip)
        self.broadcast_ip(ip)

    def get_pid(self, process):
        """
        Returns the pid associated with the process name given.
        """
        for p in psutil.process_iter():
            try:
                if p.name() == process:
                    return p.pid
            except psutil.AccessDenied:
                pass

    def get_remote_ip(self, process):
        """

        Returns the most recent remote connection IP address for a given process.
        """
        gw2 = psutil.Process(self.get_pid(process))
        # Get the most recent Gw2.exe remote connection
        connections = gw2.connections()

        if connections and len(connections) > 2:  # The number of connections varies. 3-4 seems normal in game.
            return gw2.connections()[-1].raddr[0]
        else:
            return None

    def broadcast_ip(self, ip):
        if ip:
            broadcast = "Instance: %s" % ip
        else:
            broadcast = ""
        self.emit(SIGNAL("updateIP(QString)"), broadcast)


class BossPanel(QWidget, bossPanelGui.Ui_BossPanel):

    def __init__(self, asset_dir, boss, time, average_time, active, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.name = "%s_widget" % boss.replace(" ", "").lower()
        self.setObjectName(self.name)

        self.boss = boss
        self.time = self.format_time(time, average_time)
        self.active = active
        self.setProperty("class", "bossPanel")

        self.time_label.setText(self.time)
        self.active_time_label.setText(self.time)
        self.title_label.setText(boss)
        self.active_title_label.setText(boss)

        self.asset_root_dir = asset_dir
        self.asset_dir = asset_dir + "panels/boss/"

        self.update_active()

    def paintEvent(self, event):
        painter = QPainter()

        option = QStyleOption()
        option.initFrom(self)

        painter.begin(self)
        painter.drawPixmap(0, 0, QPixmap(self.asset_dir + self.name.split("_")[0] + ".png").scaled(self.size()))
        if self.active:
            painter.drawPixmap(0, 0, QPixmap(self.asset_dir + "active_overlay.png").scaled(self.size()))
        else:
            painter.drawPixmap(0, 0, QPixmap(self.asset_dir + "overlay.png").scaled(self.size()))

        s = self.style()
        s.drawPrimitive(QStyle.PE_Widget, option, painter, self)

        painter.end()

    def update_active(self):
        self.title_label.setVisible(not self.active)
        self.active_title_label.setVisible(self.active)
        self.time_label.setVisible(not self.active)
        self.active_time_label.setVisible(self.active)

    def update_timer(self, time, average_time):
        # Set the timer text to the current event time
        current_time = self.format_time(time, average_time)
        self.time_label.setText(current_time)
        self.active_time_label.setText(current_time)

    def mouseReleaseEvent(self, event):
        self.emit(SIGNAL("clicked(QString)"), self.boss)

    @staticmethod
    def format_time(time, average_time):
        return GW2Events().format_seconds(time, average_time)

    def __str__(self):
        return self.objectName()


class DetailsPanel(QWidget, detailsPanelGui.Ui_DetailsPanel):
    def __init__(self, asset_dir, event_data, spawned_by, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.event_data = event_data
        self.spawned_by = spawned_by

        self.asset_root_dir = asset_dir
        self.asset_dir = asset_dir + "panels/details/"

        self.setProperty("class", "detailsPanel")

        self.connect(self.waypoint_copy_button, SIGNAL("clicked()"), self.send_waypoint_to_clipboard)

        self.redraw()

    def set_labels(self):
        # Name label
        self.boss_name_label.setText(self.spawned_by)
        self.resize_boss_name_label()

        # Level label
        self.level_label.setText(self.event_data[self.spawned_by]["level"])

        # Waypoint label
        self.waypoint_name_label.setText(self.event_data[self.spawned_by]["waypoint"]["name"] + ": ")
        self.waypoint_link_label.setText(self.event_data[self.spawned_by]["waypoint"]["link"])

    def resize_boss_name_label(self):
        name_length = len(self.spawned_by)
        font = QFont("GWTwoFont Version 1.1")
        font.setPixelSize(self.translate_range(name_length))  # Return range between 25 - 40 base on name_length
        self.boss_name_label.setFont(font)

    def redraw(self):
        self.set_labels()
        self.draw_loot()
        self.repaint()

    def draw_loot(self):
        for i in reversed(range(self.loot_items_layout.count())):
            self.loot_items_layout.itemAt(i).widget().deleteLater()

        self.loot_items_layout.setAlignment(Qt.AlignCenter)

        for item in self.event_data[self.spawned_by]["loot"]:
            for k, v in item.items():
                logger.debug("%s - %s" % (k, v))
                self.loot_items_layout.addWidget(LootWidget(name=k, quantity=v))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.drawPixmap(0, 0, QPixmap(self.asset_dir + "details_panel.png").scaled(self.size()))
        spawned_by_lower = self.spawned_by.replace(" ", "").lower()
        painter.drawPixmap(0, 0, QPixmap(self.asset_dir + "map_%s.png" % spawned_by_lower).scaled(self.size()))

        painter.end()

    def send_waypoint_to_clipboard(self):
        waypoint = self.waypoint_link_label.text()
        clipboard = QClipboard()
        clipboard.setText(waypoint)

    def show(self, widget):
        self.spawned_by = widget
        self.redraw()
        super().show()

    @staticmethod
    def translate_range(value, left_min=7, left_max=19, right_min=30, right_max=40):
        """
        Original: http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
        Takes a value with a given range and scales it to its correct value in another given range
        """
        #TODO: replace with a QLabel that scales the contained text to fit.

        # Figure out how 'wide' each range is
        left_span = left_max - left_min
        right_span = right_max - right_min
        # Convert the left range into a 0-1 range (float)
        value_scaled = float(value - left_min) / float(left_span)
        # Convert the 0-1 range into a value in the right range.
        return int(right_max - (value_scaled * right_span))

    def __str__(self):
        return self.objectName()


class LootWidget(QWidget):
    def __init__(self, parent=None, name=None, quantity=None):
        super().__init__(parent)

        self.root_dir = ":/assets/panels/details/"
        self.setObjectName(name)

        self.setFixedSize(40, 60)

        self.loot_name = name
        self.setMouseTracking(True)
        self.setToolTip(name)

        self.quantity = QLabel(self)
        self.quantity.setText(quantity)
        self.quantity.setFixedWidth(40)
        self.quantity.move(0, 43)
        self.quantity.setAlignment(Qt.AlignCenter)

        font = QFont("Arial")
        font.setPixelSize(12)
        font.setBold(True)

        self.quantity.setFont(font)

        if name == "Dragonite Ore":
            self.quantity.setStyleSheet("QLabel {color: rgb(207, 100, 201);}")
        else:
            self.quantity.setStyleSheet("QLabel {color: rgb(233, 222, 39);}")

        self.name = "_".join(self.objectName().lower().split(" "))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(0, 0, QPixmap(self.root_dir + "icon_%s.png" % self.name).scaled(40, 40))
        painter.end()


class AboutWindow(QDialog, aboutGui.Ui_About):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class SettingsWindow(QDialog, settingsGui.Ui_Settings):
    def __init__(self, parent, settings):
        super().__init__(parent)

        self.setupUi(self)
        self.connect(self, SIGNAL("accepted()"), self.write_settings)

        self.settings = settings
        self.read_settings()

    def read_settings(self):
        logger.debug(self.settings.allKeys())
        try:
            logger.debug(self.settings.value("update_ip"))
            logger.debug(self.settings.value("update_ip_frequency"))
            if self.settings.value("update_ip") == "false":
                self.update_ip_box.setChecked(False)
            self.update_ip_spinBox.setValue(int(self.settings.value("update_ip_frequency")))
        except TypeError as error:
            logger.error(error)

    def write_settings(self):
        update_ip = self.update_ip_box.isChecked()
        update_ip_frequency = self.update_ip_spinBox.value()

        logger.debug("Writing the settings: update_ip=%s, update_ip_frequency=%s" % (update_ip, update_ip_frequency))

        self.settings.setValue("update_ip", update_ip)
        self.settings.setValue("update_ip_frequency", update_ip_frequency)


def set_logger(level):
    # Create the logger and set the log level
    if level:
        logger.setLevel(level)
    else:
        logger.disabled = True

    # Setup logging to the console
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] - %(name)s:%(levelname)s(%(lineno)s): %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def process_args(args):
    # Set the log level
    levels = {
        'debug': logging.DEBUG,
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO
    }
    level = levels.get(args.log, None)
    set_logger(level)

    assets_dirty = False

    # Rebuild assets
    if args.rb_qrc:
        build_utils.compile_assets()
        assets_dirty = True

    # Rebuild ui
    if args.rb_ui:
        build_utils.compile_ui()
        assets_dirty = True

    # Reload ui modules if the assets have been rebuilt
    if assets_dirty:
        import importlib
        importlib.reload(mainGui)
        importlib.reload(aboutGui)
        importlib.reload(settingsGui)
        importlib.reload(bossPanelGui)
        importlib.reload(detailsPanelGui)


def start_app():
    # Get and process command line arguments
    parser = argparse.ArgumentParser(description="Creates a UI to display upcoming GW2 boss events.")
    parser.add_argument("--log",
                        help="Run the logger at given level. Options are: DEBUG, CRITICAL, ERROR, WARNING or INFO")
    parser.add_argument("--rb_qrc",
                        action="store_true",
                        help="Updates the assets by rebuilding the qrc file")
    parser.add_argument("--rb_ui",
                        action="store_true",
                        help="Converts the latest .ui files to python versions")

    args = parser.parse_args()
    process_args(args)

    # Create the app
    app = QApplication(sys.argv)
    # Set the style
    app.setStyle("plastique")

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    logger = logging.getLogger("GW2Events")
    start_app()