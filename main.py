import sqlite3
import sys
from PyQt6 import QtWidgets, uic


conn = sqlite3.connect('coffee.sqlite')
cursor = conn.cursor()


class AddEditCoffeeForm(QtWidgets.QDialog):
    
    def __init__(self, coffee_id=None):
        super(AddEditCoffeeForm, self).__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)

        # Если передан ID, загружаем данные для редактирования
        self.coffee_id = coffee_id
        if coffee_id:
            cursor.execute("SELECT * FROM coffee WHERE id = ?", (coffee_id,))
            row = cursor.fetchone()
            self.lineEditName.setText(row[1])
            self.comboBoxRoastLevel.setCurrentText(row[2])
            self.comboBoxType.setCurrentText(row[3])
            self.lineEditTasteDescription.setText(row[4])
            self.doubleSpinBoxPrice.setValue(row[5])
            self.spinBoxPackageVolume.setValue(row[6])

        # Настройка кнопки Save
        self.pushButtonSave.clicked.connect(self.save_coffee)
        
    def save_coffee(self):
        name = self.lineEditName.text()
        roast_level = self.comboBoxRoastLevel.currentText()
        type_ = self.comboBoxType.currentText()
        taste_description = self.lineEditTasteDescription.text()
        price = self.doubleSpinBoxPrice.value()
        package_volume = self.spinBoxPackageVolume.value()

        if self.coffee_id:
            cursor.execute("""
                UPDATE coffee SET name=?, roast_level=?, type=?, taste_description=?, price=?, package_volume=?
                WHERE id=?
            """, (name, roast_level, type_, taste_description, price, package_volume, self.coffee_id))
        else:
            cursor.execute("""
                INSERT INTO coffee (name, roast_level, type, taste_description, price, package_volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, roast_level, type_, taste_description, price, package_volume))

        conn.commit()
        self.accept()
        

class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        uic.loadUi('main.ui', self)

        # Отключаем возможность редактирования ячеек
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.load_coffee_data()

        self.pushButtonAdd.clicked.connect(self.add_coffee)
        self.pushButtonEdit.clicked.connect(self.edit_coffee)


    def load_coffee_data(self):
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)  # ID, название, обжарка, тип, вкус, цена, объем

        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(col_data)))

    def add_coffee(self):
        dialog = AddEditCoffeeForm()
        if dialog.exec():
            self.load_coffee_data()

    def edit_coffee(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a coffee to edit.")
            return

        coffee_id = int(self.tableWidget.item(selected_row, 0).text())
        dialog = AddEditCoffeeForm(coffee_id)
        if dialog.exec():
            self.load_coffee_data()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())