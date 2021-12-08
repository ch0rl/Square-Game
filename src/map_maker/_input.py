import threading


class Keyboard_Handler:
    """Class for handling the keyboard in the background

    *** Stolen shamelessly from my NEA ***
    """

    def __init__(self):
        self.buffer = ""
        self.newline = False
        self.kill_ = False

    def __watch_keyboard(self):
        while True:
            if self.kill_:
                break

            text = input()

            self.buffer += text
            self.newline = True

    def start_thread(self) -> None:
        """Starts the background thread for watching the keyboard"""
        self.thread = threading.Thread(target=self.__watch_keyboard)
        self.thread.start()

    def access_text(self, delete: bool = True) -> str:
        """Return the text saved in the buffer
        
        :param delete: Whether to clear the buffer or not
        :return: The text saved in the buffer
        """

        string = self.buffer
        self.newline = False

        if delete:
            self.buffer = ""

        return string

    def kill(self) -> None:
        self.kill_ = True
