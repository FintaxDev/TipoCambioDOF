from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

SCRIPT_FIND_URL = """
var url = ""
var phrase = "Tipo de cambio para solventar obligaciones denominadas en moneda extranjera pagaderas en la República Mexicana."
var elements = document.getElementsByTagName("a");
for(const e of elements){
    if(e.text.includes(phrase))
        url = e.href
}
url
"""

class PageOffline(QtWebEngineWidgets.QWebEnginePage):
    finished = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.date_url = QtCore.QUrl()
        self.loadFinished.connect(self.handle_loaded)
        self.pdfPrintingFinished.connect(self.handle_pdf)

    def search(self, date):
        self.date = date
        self.date_url = QtCore.QUrl("https://www.dof.gob.mx/index_111.php")
        query = QtCore.QUrlQuery()
        query.addQueryItem("year", self.date.toString("yyyy"))
        query.addQueryItem("month", self.date.toString("MM"))
        query.addQueryItem("day", self.date.toString("dd"))
        query.addQueryItem("edicion", "MAT")
        self.date_url.setQuery(query)
        self.load(self.date_url)

    def handle_loaded(self, ok):
        if ok:
            if self.url() == self.date_url:
                self.runJavaScript(SCRIPT_FIND_URL, self.handle_url)
            else:
                filename = "{}.pdf".format(self.date.toString("yyyy-MM-dd"))
                self.printToPdf(filename)
        else:
            self.finished.emit(False)

    def handle_url(self, url):
        if url:
            pdf_url = QtCore.QUrl.fromUserInput(url)
            self.load(pdf_url)
        else:
            self.finished.emit(False)

    def handle_pdf(self, path, ok):
        self.finished.emit(ok)

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.page = PageOffline()

        self.button = QtWidgets.QPushButton("Generar pdf")
        self.calendar = QtWidgets.QCalendarWidget()

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.calendar)
        lay.addWidget(self.button, alignment=QtCore.Qt.AlignCenter)

        self.button.clicked.connect(self.handle_clicked)
        self.page.finished.connect(self.handle_print_finished)

    def handle_clicked(self):
        date = self.calendar.selectedDate()
        self.page.search(date)
        self.button.setEnabled(False)

    def handle_print_finished(self, status):
        QtWidgets.QMessageBox.information(
            self,
            "Generación de PDF",
            "El PDF fue generado con éxito" if status else "La generación de PDF falló",
        )
        self.button.setEnabled(True)

def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.Spanish))
    w = Widget()
    w.resize(400, 400)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
