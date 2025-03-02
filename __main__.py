import logging
import logging.config
import os
import warnings

import dotenv

warnings.filterwarnings("ignore")

dotenv.load_dotenv()

log_file_path = os.path.join(os.path.dirname(__file__), 'logging.conf')

logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger('root')


class LoggerFilter(logging.Filter):
    blocked_loggers = {'faiss', 'datasets', 'unstructured',
                       'timm', 'pikepdf', 'tzlocal', 'extract_msg', 'colbert'}

    def filter(self, record: logging.LogRecord) -> bool:
        return not any(blocked in record.name for blocked in self.blocked_loggers)


# Get the console handler and add the filter
for handler in logger.handlers:
    handler.addFilter(LoggerFilter())

if __name__ == '__main__':
    from src import App

    app = App()
    app.run()
