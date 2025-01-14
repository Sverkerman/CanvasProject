import customtkinter
from customtkinter import CTkImage
import sys
import os
import logging
import atexit

software_name = "CanvasProject"
version = "1.00"

# Get the AppData path and create the Logs directory inside it
# Define log directory in a cross-platform way
if os.name == 'nt':  # Windows
    log_dir = os.path.join(os.getenv('LOCALAPPDATA'), software_name, "Logs")
    is_windows = True
else:  # macOS/Linux
    log_dir = os.path.join(os.path.expanduser("~"), software_name, "Logs")

    is_windows = False

# Create the Logs folder if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Configure logging to save logs in the logs folder
log_file = os.path.join(log_dir, f"{software_name}.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Handle unhandled exceptions
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

# Custom Logger class
class Logger:
    def __init__(self, filename, terminal):
        self.terminal = terminal  # Reference to the original terminal (stdout or stderr)
        self.log = open(filename, "a", encoding="utf-8")

    def write(self, message):
        if self.terminal:
            self.terminal.write(message)
        if self.log:
            self.log.write(message)

    def flush(self):
        if self.terminal:
            self.terminal.flush()
        if self.log:
            self.log.flush()

    def close(self):
        if self.log:
            self.log.close()

# Initialize custom loggers for stdout and stderr
sys.stdout = Logger(log_file, sys.__stdout__)  # Redirect stdout
sys.stderr = Logger(log_file, sys.__stderr__)  # Redirect stderr

# Ensure log files are closed on program exit
atexit.register(lambda: sys.stdout.close())
atexit.register(lambda: sys.stderr.close())

def start_program():
    # Initialize main window
    root = customtkinter.CTk()
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    root.title("Sverker")
    root.geometry("700x400")

    return root

if __name__ == "__main__":
    root = start_program()
    root.mainloop()
