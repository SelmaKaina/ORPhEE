from mypackage import form
from PySide6.QtWidgets import (QApplication)

try:
    app = QApplication([])
    window = form.MainWindow()
    window.show()
    app.exec()

except Exception as e:
    print("error : ",e)
    input("Appuyez sur Entrée pour fermer l'application.")
    QApplication.instance().quit()  # Quitter l'application PyQt
