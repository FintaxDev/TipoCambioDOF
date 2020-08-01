import datetime
import requests
import re
import sys
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from tkinter import *
from tkinter import messagebox
from tkcalendar import *

def descarga_pdf():
    
    fecha = datetime.datetime.strptime(cal.get_date(), "%d-%m-%Y").strftime("%Y-%m-%d")
    day = datetime.datetime.strptime(cal.get_date(), "%d-%m-%Y").strftime("%d")
    month = datetime.datetime.strptime(cal.get_date(), "%d-%m-%Y").strftime("%m")
    year = datetime.datetime.strptime(cal.get_date(), "%d-%m-%Y").strftime("%Y")
    strURL = "https://www.dof.gob.mx/index_111.php?year=" + year + "&month=" + month + "&day=" + day + "&edicion=MAT"
    req = requests.get(strURL)
    soup = BeautifulSoup(req.text, "lxml")

    for sub_heading in soup.find_all("a", href=True):

        if re.sub("[^\w .]", "", sub_heading.text) == "Tipo de cambio para solventar obligaciones denominadas en moneda extranjera pagaderas en la República Mexicana.":

            DOF_URL = "https://www.dof.gob.mx" + sub_heading.get("href")

            app = QtWidgets.QApplication(sys.argv)
            loader = QtWebEngineWidgets.QWebEngineView()
            loader.page().pdfPrintingFinished.connect(loader.close)
            loader.load(QtCore.QUrl(DOF_URL))

            def emit_pdf(finished):
                loader.page().printToPdf(fecha + ".pdf")
                messagebox.showinfo("Descarga", "Descarga exitosa.")

            loader.loadFinished.connect(emit_pdf)
            loader.loadFinished.connect(app.exit)
            app.exec()

root = Tk()
root.title("Seleccionar fecha")
root.iconbitmap("icono.ico")
root.geometry("400x400")

fecha_hoy = datetime.datetime.now()
dia_hoy = int(fecha_hoy.strftime("%d"))
mes_hoy = int(fecha_hoy.strftime("%m"))
año_hoy = int(fecha_hoy.strftime("%Y"))

cal = Calendar(root, selectmode="day", year=año_hoy, month=mes_hoy, day=dia_hoy, date_pattern="dd-mm-yyyy")
cal.pack(pady=20, fill="both", expand=True)

my_button = Button(cal, text="Descargar PDF", command=descarga_pdf)
my_button.pack(pady=20)

root.mainloop()
