import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream
from ui.main_window import MainWindow

def load_stylesheet(file_path):
    style_file = QFile(file_path)
    if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        stream = QTextStream(style_file)
        return stream.readAll()
    return ""

def main():
    app = QApplication(sys.argv)
    
    # Load and set stylesheet
    stylesheet = load_stylesheet("resources/styles.qss")
    app.setStyleSheet(stylesheet)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()