import argparse
import logging

from src.operations.ask import LLMAsker
from src.operations.embed import EmbedService
from src.operations.extract import MarkdownExtractor
from src.operations.search import SearchEngine

logger = logging.getLogger('init')


class App:
    """ The main class of the application. """

    def __init__(self):
        self.doc_folder_path = "documents/"
        self.knowledge_base_filename = "raw_knowledge_base"
        self.knowledge_vector_filename = "knowledge_vector_database"

    def run(self):
        parser = argparse.ArgumentParser(
            description='Ask questions about the files of a case.')

        # Add optional "mode" argument (with values "load-files" and "ask-question" (default))
        parser.add_argument('--mode', choices=['index-files', 'ask-question', 'search',
                            'get-markdown'], default='ask-question', help='The mode of the application.')

        # Add question argument as required positional argument if mode is "ask-question"
        parser.add_argument('question', nargs='?', type=str,
                            help='The question to ask about the files of a case.')

        args = parser.parse_args()

        if args.mode == 'index-files':
            self.load_files()
        elif args.mode == 'ask-question':
            question = args.question
            if not question or question.isspace():
                parser.error(
                    'The question argument is required in "ask-question" mode.')
            self.ask_question(question)
        elif args.mode == 'search':
            question = args.question
            if not question or question.isspace():
                parser.error(
                    'The query argument is required in "search" mode.')
            self.search(question)
        elif args.mode == 'get-markdown':
            self.get_markdown()

    def load_files(self):
        embed_service = EmbedService(self.doc_folder_path,
                                     self.knowledge_base_filename)
        embed_service.embed()
        embed_service.save(self.knowledge_vector_filename)

    def search(self, query):
        # ToDo: Search the indexed files for results matching your query
        search_engine = SearchEngine(self.doc_folder_path,
                                     self.knowledge_vector_filename)
        response = search_engine.search(query)

        print(response)

    def get_markdown(self):
        markdown_extractor = MarkdownExtractor(self.doc_folder_path)
        markdown_extractor.process()
        markdown_extractor.save(self.knowledge_base_filename)

    def ask_question(self, question):
        logging.info('Asking question: %s', question)

        operator = LLMAsker(self.doc_folder_path,
                            self.knowledge_vector_filename)

        response = operator.ask(question)

        print(response)
