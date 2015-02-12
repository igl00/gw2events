# Compiles the qrc assets before starting the program
import build_utils
build_utils.compile_assets()
import main


# opt = QtGui.QStyleOption()
# opt.init(self)
# p = QtGui.QPainter(self)
# s = self.style()
# s.drawPrimitive(QtGui.QStyle.PE_Widget, opt, p, self)
#
#         s = self.style()
#         s.drawPrimitive(QStyle.PE_Widget, options, painter, self)
#
#         options = QStyleOption()
#         options.init(self)