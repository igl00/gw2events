import psutil
from PySide.QtGui import *
from PySide.QtCore import *

from events import GW2Events
from flowLayout import FlowLayout
import style
import mainGui


class MainWindow(QMainWindow, mainGui.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        # Update the Gw2 Instance IP address
        iip_updater = IIPThread("Gw2.exe", self.serverAddress)
        iip_timer = QTimer(self)
        iip_timer.timeout.connect(lambda: iip_updater.start())
        iip_timer.start(5000)

        # Build and update the event times
        self.gw2events = GW2Events()
        self.event_data = self.gw2events.events

        update_timer = QTimer(self)
        update_timer.timeout.connect(lambda: self.update_events(self.gw2events))
        update_timer.start(1000)

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
            activeOverlayDir = panelRootDir % "active_overlay.png"

            # Build a widget
            widget = TileWidget(panelDir, overlayDir, activeOverlayDir)
            widget.setMinimumSize(QSize(350, 150))
            widget.setMaximumSize(QSize(350, 150))
            widget.setContentsMargins(0, 0, 0, 0)
            widget.setObjectName("%s_widget" % name)
            widget.active = active

            # Build the name label
            boss_label = QLabel(widget)
            boss_label.setText(boss)
            boss_label.setFont(style.boss_font())
            boss_label.setObjectName("%s_name_label" % name)
            boss_label.move(30, 112)

            # Build the time label
            time_label = QLabel(widget)
            time_label.setText(self.format_time(time, average_time))
            time_label.setObjectName("%s_time_label" % name)
            time_label.setFont(style.time_font())
            time_label.setStyleSheet(style.color_time(active))
            time_label.move(270, 7)

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
                elif active:
                    widget.active = True
                else:
                    widget.active = False

            # Update labels
            time_label = self.findChild(QLabel, "%s_time_label" % name)
            if time_label:
                time_label.setText(self.format_time(time, average_time))
                time_label.setStyleSheet(style.color_time(active))
                widget.active = active


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


class TileWidget(QWidget):

    def __init__(self, background=None, overlay=None, active_overlay=None, *args):
        self.background = background
        self.overlay = overlay
        self.active_overlay = active_overlay
        self.active = False
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(0, 0, QPixmap(self.background).scaled(self.size()))
        painter.drawPixmap(0, 0, QPixmap(self.overlay).scaled(self.size()))
        if self.active:
            painter.drawPixmap(0, 0, QPixmap(self.active_overlay).scaled(self.size()))
        painter.end()



if __name__ == '__main__':

    import sys
    # Create the app
    app = QApplication(sys.argv)
    # Set the style
    app.setStyle("plastique")
    styleSheet = QFile(":/assets/stylesheets/main.qss")
    styleSheet.open(QFile.ReadOnly)
    app.setStyleSheet(str(styleSheet.readAll()))
    # Create and show the main window
    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())