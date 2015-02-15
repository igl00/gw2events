import psutil
from PySide.QtGui import *
from PySide.QtCore import *

from events import GW2Events
from flowLayout import FlowLayout
import style
from ui import mainGui
from ui import aboutGui
from ui import settingsGui


class MainWindow(QMainWindow, mainGui.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        # Restore settings from previous session
        self.settings = QSettings("GW2Events", "igl00")
        self.read_window_settings()

        # Update the Gw2 Instance IP address
        self.iip_updater = IIPThread("Gw2.exe", self.serverAddress)
        self.iip_timer = QTimer(self)
        self.iip_timer.timeout.connect(lambda: self.iip_updater.start())

        # Build and update the event times
        self.gw2events = GW2Events()
        self.event_data = self.gw2events.events

        update_timer = QTimer(self)
        update_timer.timeout.connect(lambda: self.update_events(self.gw2events))
        update_timer.start(1000)

        # Load custom font
        QFontDatabase.addApplicationFont(':/assets/fonts/Legacy Sans Bold.ttf')

        # Set the applications style
        self.set_style_sheet()

        # Create the flow layout for the main canvas
        self.mainCanvas_layout = FlowLayout(margin=0, spacing=0)
        self.mainCanvas_widget.setLayout(self.mainCanvas_layout)

        # Add the details widget as the first flow item
        self.details = self.build_details_panel()
        self.details.hide()

        # Build the panels
        self.build_panels(self.gw2events)

        # Menu items
        # self.actionAlway_On_Top.triggered.connect(self.toggle_stay_on_top)  # Need to recreate window for it to work.
        self.actionAbout.triggered.connect(self.about_window)
        self.actionSettings.triggered.connect(self.settings_window)
        self.actionExit.triggered.connect(self.close)

        self.read_settings()

    def build_panels(self, gw2events):
        '''
        Build the boss panels
        :param gw2events:
        :return:
        '''
        events = gw2events.build_events()

        for event in events:
            boss, time, active = event
            average_time = gw2events.events[boss]["average_time"]

            # Generate the panel name from the boss name
            lower_name = boss.replace(" ", "").lower()
            name = "%s_widget" % lower_name
            panel_root_dir = ":/assets/panels/%s"
            panel_dir = panel_root_dir % lower_name + ".png"
            overlay_dir = panel_root_dir % "overlay.png"
            active_overlay_dir = panel_root_dir % "active_overlay.png"

            # Build a widget
            widget = BossPanel(name, panel_dir, overlay_dir, active_overlay_dir, boss, time, average_time, active)
            widget.setMinimumSize(QSize(350, 150))
            widget.setMaximumSize(QSize(350, 150))
            widget.setContentsMargins(0, 0, 0, 0)

            self.connect(widget, SIGNAL("clicked(QString)"), self.toggle_details_panel)

            # Set layouts
            self.mainCanvas_layout.addWidget(widget)

    def rebuild_panels(self, gw2events):
        '''
        Delete then recreate the boss panels
        :param gw2events:
        :return:
        '''
        for widget in self.mainCanvas_widget.findChildren(QWidget):
            widget.deleteLater()

        self.build_panels(gw2events)

    def build_details_panel(self, widget_name=None):
        '''
        Create the details panel
        :param widget_name:
        :return:
        '''
        detail_widget = QWidget()
        detail_widget.setMinimumSize(QSize(350, 450))
        detail_widget.setMaximumSize(QSize(350, 450))
        detail_widget.setContentsMargins(0, 0, 0, 0)
        detail_widget.setObjectName("details_widget")
        detail_widget.spawned_by = widget_name

        # Add to the font of the flow layout
        self.mainCanvas_layout.addWidget(detail_widget)

        return detail_widget

    def toggle_details_panel(self, widget):
        '''
        Show or hide the details panel depending on its current state.
        :param widget:
        :return:
        '''
        if self.details.isVisible():
            self.details.hide()
        else:
            self.details.show()

    def update_events(self, gw2events):
        '''
        Updates the times on the boss panels and calls a rebuild when the order needs to be changed.
        :param gw2events:
        :return:
        '''
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

    def start_iip_timer(self, run, frequency):
        '''
        Starts or stops the instace ip timer.
        :param run:
        :param frequency:
        :return:
        '''
        self.iip_timer.stop()
        if run == "true":
            self.iip_timer.start(frequency)
        else:
            self.serverAddress.setText("")

    def set_style_sheet(self):
        '''
        Apply the main css styles to the window.
        :return:
        '''
        style_sheet = QFile(":/assets/stylesheets/main.qss")
        style_sheet.open(QFile.ReadOnly)
        self.setStyleSheet(str(style_sheet.readAll()))

    def settings_window(self):
        '''
        Shows the settings window and runs the read_settings() method if the settings are accepted.
        :return:
        '''
        self.settings_window = SettingsWindow(self, self.settings)
        self.settings_window.show()
        self.settings_window.connect(self.settings_window, SIGNAL("accepted()"), self.read_settings)

    def read_window_settings(self):
        '''
        Reads the saved window state and applies it to the current window.
        :return:
        '''
        settings = self.settings
        settings.beginGroup("MainWindow")
        try:
            self.resize(settings.value("size"))
            self.move(settings.value("pos"))
        except TypeError:
            pass
        self.settings.endGroup()

    def write_window_settings(self):
        '''
        Saves the windows current state(size, position, ...)
        :return:
        '''
        settings = self.settings
        settings.beginGroup("MainWindow")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.endGroup()

    def read_settings(self):
        settings = self.settings
        settings.beginGroup("Settings")
        try:
            self.start_iip_timer(settings.value("iip"), settings.value("iip_frequency") * 1000)
        except TypeError as error:
            print(error)
            self.start_iip_timer(True, 5000)
        settings.endGroup()

    def about_window(self):
        '''
        Shows the about window.
        :return:
        '''
        self.about_window = AboutWindow(self)
        self.about_window.show()

    def closeEvent(self, event):
        '''
        Over-rides the default close event to enable the saving of the
        window position and size before it closes.
        :param event:
        :return:
        '''
        self.write_window_settings()
        event.accept()

class IIPThread(QThread):
    """
    A worker thread dedicated to getting the current Gw2 map instance IP address.
    """
    def __init__(self, process, label, parent=None):
        super().__init__(parent)
        self.process = process
        self.label = label

    def run(self):
        ip = self.get_remote_ip(self.process)
        self.update_iip(self.label, ip)

    def get_pid(self, process):
        """
        Returns the pid associated with the process name given.
        :param process:
        :return:
        """
        for proc in psutil.process_iter():
            try:
                if proc.name() == process:
                    return proc.pid
            except psutil.AccessDenied:
                pass

    def get_remote_ip(self, process):
        """
        Returns the most recent remote connection IP address for a given process.
        :return:
        """
        gw2 = psutil.Process(self.get_pid(process))
        # Get the most recent Gw2.exe remote connection
        connections = gw2.connections()

        if connections and len(connections) > 2:  # The number of connections varies. 3-4 seems normal in game.
                return gw2.connections()[-1].raddr[0]
        else:
            return None

    def update_iip(self, label, ip):
        if ip:
            label.setText("Instance: %s" % ip)
        else:
            label.setText("")


class BossPanel(QWidget):

    def __init__(self, name, background, overlay, active_overlay, boss, time, average_time, active, *args):
        super().__init__()
        self.setObjectName(name)

        self.background = background
        self.overlay = overlay
        self.active_overlay = active_overlay

        self.active = active

        self.update_active()

        self.title = self.create_title(boss)
        self.style_title()

        self.timer = self.create_timer(time, average_time)
        self.style_timer()

    def paintEvent(self, event):
        painter = QPainter()

        option = QStyleOption()
        option.initFrom(self)

        painter.begin(self)
        painter.drawPixmap(0, 0, QPixmap(self.background).scaled(self.size()))
        if self.active:
            painter.drawPixmap(0, 0, QPixmap(self.active_overlay).scaled(self.size()))
        else:
            painter.drawPixmap(0, 0, QPixmap(self.overlay).scaled(self.size()))

        s = self.style()
        s.drawPrimitive(QStyle.PE_Widget, option, painter, self)

        painter.end()

    def create_title(self, boss):
        boss_name_label = QLabel(self)
        boss_name_label.setText(boss)
        boss_name_label.setProperty("title", "true")

        return boss_name_label

    def style_title(self):
        title = self.title

        title.setFont(style.boss_name_font())

        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        if self.active:
            title.setFixedHeight(40)
            title.setFixedWidth(280)
            title.move(35, 46)
        else:
            title.setFixedHeight(28)
            title.setFixedWidth(140)
            title.move(5, 118)

    def create_timer(self, time, average_time):
        time_label = QLabel(self)
        time_label.setText(self.format_time(time, average_time))
        time_label.setProperty("timer", "true")

        return time_label

    def style_timer(self):
        self.timer.setFont(style.time_font())
        if self.active:
            self.timer.move(141, 78)
        else:
            self.timer.move(270, 7)

    def update_timer(self, time, average_time):
        # Set the timer text to the current event time
        self.timer.setText(self.format_time(time, average_time))

    def update_active(self):
        if self.active:
            self.setProperty("class", "active")
        else:
            self.setProperty("class", "inactive")

    def format_time(self, time, average_time):
        return GW2Events().format_seconds(time, average_time)

    def mouseReleaseEvent(self, event):
        self.emit(SIGNAL("clicked(QString)"), self.objectName())

    def __str__(self):
        return self.objectName()


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
        self.settings.beginGroup("Settings")
        try:
            if self.settings.value("iip") == "false":
                self.iipUdate_box.setChecked(False)
            self.iipUpdate_spinBox.setValue(int(self.settings.value("iip_frequency")))
        except TypeError as error:
            print(error)

    def write_settings(self):
        iip_update = self.iipUdate_box.isChecked()
        iip_update_every = self.iipUpdate_spinBox.value()

        self.settings.beginGroup("Settings")
        self.settings.setValue("iip", iip_update)
        self.settings.setValue("iip_frequency", iip_update_every)
        self.settings.endGroup()


def start_app():
    import sys

    # Create the app
    app = QApplication(sys.argv)
    # Set the style
    app.setStyle("plastique")
    # Create and show the main window
    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()