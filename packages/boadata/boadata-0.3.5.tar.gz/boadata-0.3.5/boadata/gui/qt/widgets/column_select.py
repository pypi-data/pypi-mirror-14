from PyQt4 import QtCore, QtGui


class ColumnModel(QtCore.QAbstractListModel):
    def __init__(self, data_object, parent=None):
        """

        :type data_object: boadata.core.DataObject
        :return:
        """
        super(ColumnModel, self).__init__(parent)
        self.data_object = data_object

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        else:
            return len(self.data_object.columns)

    def data(self, index, role=None):
        """
        :type index: QtCore.QModelIndex
        :type role: int
        """
        if not index.isValid():
            return None
        # item = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return self.data_object.columns[index.row()]

    def get_index(self, name):
        return self.data_object.columns.index(name)


class ColumnSelect(QtGui.QListView):
    def __init__(self, data_object, parent=None):
        super(ColumnSelect, self).__init__(parent)
        self.setModel(ColumnModel(data_object, self))

    @property
    def selected_columns(self):
        return [self.model().data(index, QtCore.Qt.DisplayRole) for index in self.selectedIndexes()]

    def select_columns(self, columns):
        rows = [self.model().get_index(name) for name in columns]
        indexes = [self.model().index(i, 0, QtCore.QModelIndex()) for i in rows]
        ranges = [QtGui.QItemSelectionRange(index) for index in indexes]
        selection = QtGui.QItemSelection()
        for range in ranges:
            selection.append(range)
        self.selectionModel().select(selection, QtGui.QItemSelectionModel.ClearAndSelect)

