import psutil
from PySide.QtGui import *
from PySide.QtCore import *
from time import sleep

from events import GW2EVENTS
from flowLayout import FlowLayout
from build_utils import resource_path
import mainGui


class MainWindow(QMainWindow, mainGui.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        # Update the Gw2 Instance IP address
        self.iipThread = IIPThread()

        self.connect(self.iipThread, SIGNAL("instanceIP(QString)"), self.update_iip, Qt.DirectConnection)
        self.iipThread.start()

        # Build and update the event times
        self.gw2events = GW2EVENTS()
        self.event_data = self.gw2events.events

        timers = QTimer(self)
        timers.timeout.connect(lambda: self.update_events(self.gw2events))
        timers.start(1000)

        # Load custom font
        QFontDatabase.addApplicationFont(':/assets/fonts/Legacy Sans Bold.ttf')

        # Create the flow layout for the main canvas
        self.mainCanvas_layout = FlowLayout(margin=0, spacing=0)
        self.mainCanvas_widget.setLayout(self.mainCanvas_layout)

        # Add the details widget as the first flow item
        self.details = self.build_details_panel()
        self.details.hide()

        # Build the panels
        self.build_panels(self.gw2events)

        # Misc
        self.actionCompact.activated.connect(self.toggle_details_panel)

    def build_panels(self, gw2events):
        events = gw2events.build_events()

        for event in events:
            boss, time, active = event
            average_time = gw2events.events[boss]["average_time"]

            # Generate the panel name from the boss name
            name = boss.replace(" ", "").lower()
            panelRootDir = ":/assets/panels/%s"
            panelDir = panelRootDir % name + ".png"
            overlayDir = panelRootDir % "overlay.png"

            # Build a widget
            widget = TileWidget(panelDir, overlayDir)
            widget.setMinimumSize(QSize(350, 150))
            widget.setMaximumSize(QSize(350, 150))
            widget.setContentsMargins(0, 0, 0, 0)
            widget.setObjectName("%s_widget" % name)
            widget.active = active

            # Build the name label
            boss_label = QLabel(widget)
            boss_label.setText(boss)
            boss_label.setFont(self.boss_font())
            boss_label.setObjectName("%s_name_label" % name)
            boss_label.move(30, 112)

            # Build the time label
            time_label = QLabel(widget)
            time_label.setText(self.format_time(time, average_time))
            time_label.setObjectName("%s_time_label" % name)
            time_label.setFont(self.time_font())
            time_label.setStyleSheet(self.color_time(active))
            time_label.move(270, 7)

            # Build the active label
            active_label = QLabel(widget)
            active_label.setText(self.set_active_label(active))
            active_label.setObjectName("%s_active_label" % name)
            active_label.setFont(self.active_font())
            active_label.setStyleSheet("color: rgb(177, 58, 58);")
            active_label.move(95, 50)

            # Set layouts
            self.mainCanvas_layout.addWidget(widget)


    def rebuild_panels(self, gw2events):
        for widget in self.mainCanvas_widget.findChildren(QWidget):
            widget.deleteLater()
        self.build_panels(gw2events)

    def build_details_panel(self, widget_name=None):
        #widget = self.findChild(QWidget, "%s_widget" % widget_name)
        detail_widget = QWidget()
        detail_widget.setMinimumSize(QSize(350, 450))
        detail_widget.setMaximumSize(QSize(350, 450))
        detail_widget.setContentsMargins(0, 0, 0, 0)
        detail_widget.setObjectName("details_widget")

        # Build the active label
        active_label = QLabel(detail_widget)
        active_label.setText("Bam!!")
        active_label.setObjectName("details_active_label")
        active_label.setFont(self.active_font())
        active_label.setStyleSheet("color: rgb(177, 58, 58);")
        active_label.move(95, 50)

        # Add to the font of the flow layout
        self.mainCanvas_layout.addWidget(detail_widget)

        return detail_widget

    def toggle_details_panel(self):
        details_widget = self.findChild(QWidget, "details_widget")
        if details_widget.isVisible():
            details_widget.hide()
        else:
            details_widget.show()

    def format_time(self, time, average_time):
        return self.gw2events.format_seconds(time, average_time)

    def color_time(self, active):
        if active:
            return "color: rgb(177, 58, 58);"
        else:
            return "color: rgb(162, 147, 130);"

    def time_font(self):
        font = QFont("ITCLegacySans LT Book")
        font.setStyleStrategy(QFont.PreferAntialias)
        font.setPixelSize(18)
        font.setBold(True)

        return font

    def boss_font(self):
        font = QFont("Arial")
        font.setStyleStrategy(QFont.PreferAntialias)
        font.setPixelSize(14)
        font.setBold(True)
        font.setCapitalization(QFont.Capitalization(True))

        return font

    def active_font(self):
        font = QFont("Arial")
        font.setStyleStrategy(QFont.PreferAntialias)
        font.setPixelSize(30)
        font.setBold(True)

        return font

    def set_active_label(self, active):
        if active:
            return "In Progress"
        else:
            return ""

    def update_events(self, gw2events):
        events = gw2events.build_events()
        for event in events:
            boss, time, active = event
            average_time = gw2events.events[boss]["average_time"]
            name = boss.replace(" ", "").lower()

            # Check to see if a rebuild is needed
            widget = self.findChild(QWidget, "%s_widget" % name)
            if widget:
                if widget.active and not active:
                    self.rebuild_panels(self.gw2events)
                    break

            # Update labels
            time_label = self.findChild(QLabel, "%s_time_label" % name)
            if time_label:
                time_label.setText(self.format_time(time, average_time))
                time_label.setStyleSheet(self.color_time(active))
                widget.active = active

            active_label = self.findChild(QLabel, "%s_active_label" % name)
            if active_label:
                active_label.setText(self.set_active_label(active))

    def update_iip(self, ip):
        if ip:
            self.serverAddress.setText("Instance: %s" % ip)
        else:
            self.serverAddress.setText("")


class IIPThread(QThread):
    """
    A worker thread dedicated to getting the current Gw2 map instance IP address.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        pass

        while True:
            self.emit(SIGNAL("instanceIP(QString)"), self.get_remote_ip('Gw2.exe'))
            sleep(5)

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
        if connections and len(connections) > 2:
                return gw2.connections()[-1].raddr[0]
        else:
            return None


class TileWidget(QWidget):

    def __init__(self, background=None, overlay=None, *args):
        self.background = background
        self.overlay = overlay
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(0, 0, QPixmap(self.background).scaled(self.size()))
        painter.drawPixmap(0, 0, QPixmap(self.overlay).scaled(self.size()))
        painter.end()


if __name__ == '__main__':

    import sys
    # Create the app
    app = QApplication(sys.argv)
    # Set the style
    app.setStyle("plastique")
    style = QFile(":/assets/stylesheets/main.qss")
    style.open(QFile.ReadOnly)
    app.setStyleSheet(str(style.readAll()))
    # Create and show the main window
    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())