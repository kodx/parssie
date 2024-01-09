import sys
from urllib.request import Request, urlopen
from urllib.error import URLError
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import Slot
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from . import uiloader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = uiloader.UiLoader()
        loader.loadUi("src/ui/mainwindow.ui", self)

        # Настройка selenium для запуска без окна в фоновом режиме
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

        self.leRequestUrl.setText("https://jsonplaceholder.typicode.com/")
        self.leSelector.setText('//a[contains(@class, "no-underline")]')

        # Подключаем сигналы кнопок к слотам
        self.pbHTML.clicked.connect(self.start_html)
        self.pbLxml.clicked.connect(self.start_lxml)
        self.pbSelenium.clicked.connect(self.start_selenium)

    def __del__(self):
        self.driver.quit()

    def get_html(self) -> str:
        req = Request(self.leRequestUrl.text())
        data = ""
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, "reason"):
                print("We failed to reach a server.")
                print("Reason: ", e.reason)
            elif hasattr(e, "code"):
                print("The server couldn't fulfill the request.")
                print("Error code: ", e.code)
        else:
            data = response.read().decode("utf-8")
        return data

    @Slot()
    def start_html(self):
        data = self.get_html()

        self.pteResult.setPlainText(data)

    @Slot()
    def start_lxml(self):
        self.pteResult.clear()
        data = self.get_html()
        tree = html.fromstring(data)
        found_entries = tree.xpath(self.leSelector.text())
        self.pteResult.clear()
        for entry in found_entries:
            self.pteResult.appendPlainText(entry.text)

    @Slot()
    def start_selenium(self):
        self.pteResult.clear()
        url = self.leRequestUrl.text()
        self.driver.get(url)
        entries = self.driver.find_elements(By.XPATH, self.leSelector.text())
        for entry in entries:
            self.pteResult.appendPlainText(entry.text)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
