import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QLineEdit, QComboBox, QPushButton, QToolBar, QStatusBar, QGridLayout, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import mysql.connector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 600)
        self.setWindowTitle("Student Management System")
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # This code is for the menu of the item

        add_student_action = QAction(QIcon("icons/add.png"), "Add the student", self)
        add_student_action.triggered.connect(self.insert)

        about_action = QAction("About", self)

        search_student_action = QAction(QIcon("icons/search.png"), "Search the student", self)
        search_student_action.triggered.connect(self.search)

        file_menu_item.addAction(add_student_action)
        help_menu_item.addAction(about_action)
        edit_menu_item.addAction(search_student_action)

        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # This code is for the table of creation

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.load_data()

        # Create Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Toolbar Action
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Status Bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Cell clicking detection
        self.table.cellClicked.connect(self.cell_clicked)

    # Method to load the data in th etable
    def load_data(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="love@2002",
            database="Python_Work"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select * from students");
        result = mycursor.fetchall()
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))
        mydb.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)

        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()



class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adding the student")
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        layout = QVBoxLayout()

        self.stud_name = QLineEdit()
        self.stud_name.setPlaceholderText("Name")
        layout.addWidget(self.stud_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mob_num = QLineEdit()
        self.mob_num.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mob_num)

        add_stud = QPushButton("Add the student")
        layout.addWidget(add_stud)

        add_stud.clicked.connect(self.add_student)

        self.setLayout(layout)

    def add_student(self):
        course = self.course_name.itemText(self.course_name.currentIndex())
        name = self.stud_name.text()
        mobile = self.mob_num.text()
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="love@2002",
            database="Python_Work"
        )
        cursor = mydb.cursor()
        sql = "INSERT INTO students (Name,Course,Mobile) VALUES (%s, %s, %s)"
        val = (name, course, mobile)
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()
        mydb.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search the student")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        layout = QVBoxLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Enter the student to search")
        layout.addWidget(self.search_name)

        srch_stud = QPushButton("Search Student")
        layout.addWidget(srch_stud)

        srch_stud.clicked.connect(self.search_student)
        self.setLayout(layout)

    def search_student(self):
        name = self.search_name.text()
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update the student")
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        layout = QVBoxLayout()

        index = main_window.table.currentRow()
        # Get data
        stud_name = main_window.table.item(index, 1).text()
        course_name = main_window.table.item(index, 2).text()
        self.id = main_window.table.item(index, 0).text()
        mob_no = main_window.table.item(index, 3).text()

        self.stud_name = QLineEdit(stud_name)
        self.stud_name.setPlaceholderText("Name")
        layout.addWidget(self.stud_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        self.mob_num = QLineEdit(mob_no)
        self.mob_num.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mob_num)

        add_stud = QPushButton("Update the student")
        layout.addWidget(add_stud)

        add_stud.clicked.connect(self.update_student)

        self.setLayout(layout)

    def update_student(self):
        course = self.course_name.itemText(self.course_name.currentIndex())
        name = self.stud_name.text()
        mobile = self.mob_num.text()
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="love@2002",
            database="Python_Work"
        )
        cursor = mydb.cursor()
        sql = "UPDATE students SET Name = %s , Course = %s , Mobile = %s Where Id = %s"
        val = (name, course, mobile, self.id)
        cursor.execute(sql, val)
        mydb.commit()
        cursor.close()
        mydb.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete ?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        yes.clicked.connect(self.delete_data)
        no.clicked.connect(self.save_data)
        self.setLayout(layout)
    def save_data(self):
        self.close()
    def delete_data(self):
        mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="love@2002",
                    database="Python_Work"
                )
        index = main_window.table.currentRow()
        id = main_window.table.item(index, 0).text()
        cursor = mydb.cursor()
        sql = "DELETE FROM students  Where Id = %s"
        val = (id,)
        cursor.execute(sql,val)
        mydb.commit()
        cursor.close()
        mydb.close()
        main_window.load_data()
        self.close()
        confirmation_widget=QMessageBox()
        confirmation_message="The Record is deleted Successfully"
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText(confirmation_message)
        confirmation_widget.exec()
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
