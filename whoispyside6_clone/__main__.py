import sys
import asyncio
import functools
from PySide6.QtWidgets import QMainWindow
import qasync
from qasync import QApplication

from whoispyside6_clone.view import MainPage
from whoispyside6_clone.model.host_converter import HostConverter, create_hostConverter


def move_center(window: QMainWindow):
    """move window to center of screen

    Args:
        window (QMainWindow): main window
    """
    frame = window.frameGeometry()
    center_position = window.screen().availableGeometry().center()

    frame.moveCenter(center_position)
    window.move(frame.topLeft())


async def async_main():
    """
    async main for app
    """

    def close_future(future: asyncio.Future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            functools.partial(close_future, future, loop)
        )

    main_window = QMainWindow(None)
    main_window.setWindowTitle("Whoisclone")
    main_page = MainPage()

    main_window.setCentralWidget(main_page)

    main_window.show()
    move_center(main_window)

    await future
    return True


def main():
    """main for app"""
    if sys.version_info.major == 3 and sys.version_info.minor == 11:
        # this code run on 3.11
        # pylint: disable=protected-access
        with qasync._set_event_loop_policy(qasync.DefaultQEventLoopPolicy()):
            # pylint: disable=no-member
            runner = asyncio.runners.Runner()
            try:
                runner.run(async_main())
            except asyncio.exceptions.CancelledError:
                sys.exit(0)
            finally:
                runner.close()
    else:
        try:
            qasync.run(async_main())
        except asyncio.exceptions.CancelledError:
            sys.exit(0)


if __name__ == "__main__":
    main()
