from PySide.QtGui import QFont


def time_font():
    font = QFont("ITCLegacySans LT Book")
    font.setStyleStrategy(QFont.PreferAntialias)
    # font.setPixelSize(18)
    # font.setBold(True)

    return font


def boss_name_font():
    font = QFont("Arial")
    font.setStyleStrategy(QFont.PreferAntialias)
    # font.setPixelSize(14)
    # font.setBold(True)
    # font.setCapitalization(QFont.Capitalization(True))

    return font


def active_font():
    font = QFont("Arial")
    font.setStyleStrategy(QFont.PreferAntialias)
    # font.setPixelSize(30)
    # font.setBold(True)

    return font