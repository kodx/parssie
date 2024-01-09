import sys
from qtpy.QtCore import QMetaObject
from qtpy.QtUiTools import QUiLoader
from qtpy.QtCore import QFile, QIODevice


class UiLoader(QUiLoader):
    _baseinstance = None

    def createWidget(self, classname, parent=None, name=""):
        if parent is None and self._baseinstance is not None:
            widget = self._baseinstance
        else:
            widget = super().createWidget(classname, parent, name)
            if self._baseinstance is not None:
                setattr(self._baseinstance, name, widget)
        return widget

    def loadUi(self, ui_file, baseinstance=None):
        self._baseinstance = baseinstance
        ui_file = QFile(ui_file)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file.fileName()}: {ui_file.errorString()}")
            sys.exit(-1)
        widget = self.load(ui_file)
        ui_file.close()
        if not widget:
            print(self.errorString())
            sys.exit(-1)
        QMetaObject.connectSlotsByName(baseinstance)
        return widget
