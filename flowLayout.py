from PySide import QtCore, QtGui


class FlowLayout(QtGui.QLayout):
    def __init__(self, parent=None, panel_width=350, panel_height=150, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setMargin(margin)

        self.layoutMargin = margin

        self.panelWidth = panel_width
        self.panelHeight = panel_height

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def margin(self):
        return self.layoutMargin

    def setMargin(self, margin):
        self.layoutMargin = margin

    def addItem(self, item):
        self.itemList.append(item)

    def insertItem(self, pos, item):
        self.itemList.insert(pos, item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.margin(), 2 * self.margin())
        return size

    def doLayout(self, rect, testOnly):
        items = self.itemList
        resize_delay = self.panelWidth - 250  # Pixels allowed to be hidden before resizing
        border_right = rect.right() + resize_delay
        origin_x = rect.x()
        origin_y = rect.y()
        x = origin_x
        y = origin_y
        line_height = 0

        # Check for details widget
        if self.itemHeight(items[0]) > self.itemHeight(items[1]):
            panelToDetailRatio = int(self.itemHeight(items[0]) / self.panelHeight)
            details = True
        else:
            panelToDetailRatio = 0
            details = False

        # Layout the panels left>right, top>bottom.
        # It's going to need some more work to make it more flexible/faster
        for i, item in enumerate(items):
            width, height = item.sizeHint().toTuple()  # Set the current items width & height
            next_x = x + width

            if next_x > border_right and line_height > 0:
                # Deal with the panels to the right of the details
                if details and i <= int(panelToDetailRatio * (int(border_right/self.panelWidth)-1)):
                    x = origin_x + width
                    y += self.panelHeight
                # Else continue as normal
                else:
                    x = origin_x
                    y += line_height
                next_x = x + width
                line_height = 0

            # Position the item if not in test mode
            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, height)

        return y + line_height + origin_y

    def itemHeight(self, item):
        return item.sizeHint().height()