import os
import backend.Watchdog

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

watchdog = backend.Watchdog.Watchdog()

watchdog.run()