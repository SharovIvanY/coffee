import sqlite3
import sys
from PyQt6 import QtWidgets, uic


conn = sqlite3.connect('coffee.sqlite')
cursor = conn.cursor()


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        uic.loadUi('main.ui', self)

        # Отключаем возможность редактирования ячеек
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.load_coffee_data()

    def load_coffee_data(self):
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)  # ID, название, обжарка, тип, вкус, цена, объем

        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(col_data)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())