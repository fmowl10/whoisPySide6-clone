"""
    main page
"""


from typing import Optional
from qasync import asyncSlot
from PySide6.QtCore import QSize, Qt, Signal
import PySide6.QtCore
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QLineEdit,
    QDialog,
    QMessageBox,
)
from PySide6.QtWebEngineWidgets import QWebEngineView

from whoispyside6_clone.model.geolocation_getter import (
    GeolocationGetter,
    create_geolocationgetter,
)

from whoispyside6_clone.utils.country_emoji import get_flag

from aiodns.error import DNSError

from whoispyside6_clone.model.host_converter import HostConverter, create_hostConverter


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setWindowTitle("Whois-clone")
        self.setMinimumSize(QSize(300, 400))
        self.setContentsMargins(25, 25, 25, 25)

        vbox = QVBoxLayout(self)

        self.choosing_dropdown = QComboBox(self)

        self.choosing_dropdown.addItems(
            ["IP to name", "name to IP", "host to Location"]
        )
        vbox.addWidget(self.choosing_dropdown)

        self.host_text = QLineEdit(self)
        vbox.addWidget(self.host_text)

        self.convert_button = QPushButton(self)
        self.convert_button.setText("Convert")
        self.convert_button.clicked.connect(self.convert_button_clicked)
        vbox.addWidget(self.convert_button)
        self.output: QWidget = None

    @asyncSlot()
    async def convert_button_clicked(self):
        self.convert_button.setText("converting....")
        self.convert_button.setEnabled(False)
        if self.choosing_dropdown.currentText() == "host to Location":
            geo: GeolocationGetter = await create_geolocationgetter(
                self.host_text.text()
            )
            self.output = GeoDialog(geo)
            self.output.show()
            print(geo)
        elif self.choosing_dropdown.currentText() == "IP to name":
            try:
                host: HostConverter = await create_hostConverter(
                    "address", self.host_text.text()
                )
                print(host)
                self.output = AddressList(host.aliases)
                self.output.show()
            except DNSError as exc:
                msgbox = QMessageBox()
                msgbox.setText(exc.args[1])
                msgbox.show()
        elif self.choosing_dropdown.currentText() == "name to IP":
            host: HostConverter = await create_hostConverter(
                "name", self.host_text.text()
            )
            print(host)
            self.output = AddressList(host.addresses)
            self.output.show()

        self.convert_button.setEnabled(True)
        self.convert_button.setText("Convert")


class AddressList(QDialog):
    def __init__(self, addresses: list[str]):
        super().__init__()
        self.addresses = addresses
        self.setup()
        self.show()

    def setup(self) -> None:
        self.setMinimumSize(200, 200)
        vbox = QVBoxLayout()

        for address in self.addresses:
            vbox.addWidget(QLabel(address))

        self.setLayout(vbox)


class GeoDialog(QDialog):
    def __init__(self, data: GeolocationGetter):
        super().__init__()
        self.data = data
        self.setup()

    def setup(self) -> None:
        vbox = QVBoxLayout()

        labels = [
            QLabel(f"IP : {self.data.origin_query}"),
            QLabel(f"country : {self.data.country} {get_flag(self.data.country_code)}"),
            QLabel(f"timezone : {self.data.timezone}"),
            QLabel(f"isp : {self.data.isp}"),
            QLabel(f"org : {self.data.organization}"),
        ]

        for label in labels:
            vbox.addWidget(label)

        google_map = QWebEngineView()

        vbox.addWidget(google_map)

        google_map.load(
            f"https://www.google.com/maps?q={self.data.latitude},{self.data.longitude}"
        )

        self.setLayout(vbox)
