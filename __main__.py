from src import App
import os
import logging.config
import logging
import dotenv

dotenv.load_dotenv()


log_file_path = os.path.join(os.path.dirname(__file__), 'logging.conf')

logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger()

if __name__ == '__main__':
    app = App()
    app.run()
