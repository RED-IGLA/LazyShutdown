import sys

from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QMessageBox, \
    QComboBox, QLabel
from PySide6.QtCore import Qt
import subprocess

from core.version import get_version

time_type_enum = {
    0: 1,
    1: 60,
    2: 3600,
    3: 86400
}

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"LazyShutdown {get_version(short=True)}")
        self.setMinimumSize(480, 0)
        self.setFixedHeight(130)

        # Input value
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter a time to shut down (ex. 1800, 1.5 for hours)")

        # Time type combo box
        self.time_type_cb = QComboBox()
        self.time_type_cb.addItems(["Seconds", "Minutes", "Hours", "Days"])

        # Set timer button
        self.set_timer_button = QPushButton("Set timer")
        self.set_timer_button.pressed.connect(self.on_set_timer_button)

        # Clear timer button
        self.clear_timer_button = QPushButton("Clear timer")
        self.clear_timer_button.pressed.connect(self.on_clear_timer_button)

        self.author_label = QLabel()
        self.author_label.setText(f"Powered by\n"
                                  "RED IGLA\n"
                                  + str(get_version()))
        self.author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Line input layout (horizontal)
        text_input_layout = QHBoxLayout()
        text_input_layout.addWidget(self.input_field)
        text_input_layout.addWidget(self.time_type_cb)
        text_input_layout.addWidget(self.set_timer_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Main layout (vertical)
        main_layout = QVBoxLayout()
        main_layout.addLayout(text_input_layout)
        main_layout.addWidget(self.clear_timer_button)
        main_layout.addWidget(self.author_label)
        main_layout.addStretch()

        # Main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    """
    Set timer function
    All this bullshit is needed for float value type, ex. 1.5 hours.
    Yeah we can use QSpinBox, but he did not support so necessary to us float.
    """
    def on_set_timer_button(self):
        raw_value = self.input_field.text()
        time_type = self.time_type_cb.currentIndex()

        print(f"Trying set timer to: [{raw_value}]")
        print("Trying get type...")
        try:
            input_value = int(raw_value)
        except ValueError:
            try:
                input_value = float(raw_value)
            except ValueError:
                QMessageBox.warning(self, "Invalid time type",
                                    "Please enter a valid time\n"
                                    "* Integer or Float")
                print("Error: Invalid time type")
                return

        # Insurance :)
        if not input_value or input_value <= 0:
            QMessageBox.warning(self, "Invalid time type", "Unable to determine the type of value")
            print("Error: Invalid time type")
            return

        print(f"Found value type is: {type(input_value)}")
        print(f"Current time type is: {time_type}")

        total_seconds = int(input_value * time_type_enum[time_type])
        print(f"Total seconds: {total_seconds}")

        result = subprocess.run(["shutdown", "/s", "/t", str(total_seconds)], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        result_return_code = result.returncode
        match result_return_code:
            case 0:
                # QMessageBox.information(self, "Timer is set", "Timer successfully set!\n"
                #                         f"Total seconds: {total_seconds}")
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Timer set")
                msg.setText("Timer successfully set!")

                msg.addButton("Ok", QMessageBox.ButtonRole.AcceptRole)
                btn_exit = msg.addButton("Exit", QMessageBox.ButtonRole.RejectRole)
                btn_clear = msg.addButton("Clear", QMessageBox.ButtonRole.ActionRole)

                btn_exit.clicked.connect(lambda: sys.exit())
                btn_clear.clicked.connect(self.on_clear_timer_button)

                msg.exec()

                print(f"Timer successfully set for: {total_seconds}")
                return
            case 1116:
                QMessageBox.critical(self, f"Error: {result_return_code}", "Error while set the timer\n"
                                                                      "Maybe wrong time value (type)")
                print(f"Error while set the timer: {result_return_code}")
                return
            case 1190:
                QMessageBox.critical(self, f"Error: {result_return_code}", "Timer is already set\n"
                                                    "Clear current timer to set a new one")
                print(f"Error while set the timer: {result_return_code}")
                return
            case _:
                QMessageBox.critical(self, f"Error: {result_return_code}", f"Not expected error: {result_return_code}")
                print(f"Not expected error: {result_return_code}")

    """
    Clear timer function
    Emm, i think i have nothing to say. Just clear.
    """
    def on_clear_timer_button(self):
        result = subprocess.run(["shutdown", "/a"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        result_return_code = result.returncode
        match result_return_code:
            case 0:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Timer cleared")
                msg.setText("Timer successfully cleared!")

                msg.addButton("Ok", QMessageBox.ButtonRole.AcceptRole)
                btn_exit = msg.addButton("Exit", QMessageBox.ButtonRole.RejectRole)

                btn_exit.clicked.connect(lambda: sys.exit())

                msg.exec()
                print("Timer successfully cleared")
                return
            case 1116:
                QMessageBox.critical(self, f"Error: {result_return_code}", "The timer is not registered\n"
                                     "Nothing to clear")
                print(f"Error while clear the timer: {result_return_code}")
                return
            case _:
                QMessageBox.critical(self, f"Error: {result_return_code}", f"Not expected error: {result_return_code}")
                print(f"Not expected error: {result_return_code}")