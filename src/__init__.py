import argparse
from os import environ

from rich.console import Console
from rich.markdown import Markdown

from src.operations.ask import LLMAsker
from src.operations.embed import EmbedService
from src.operations.extract import MarkdownExtractor
from src.operations.search import SearchEngine

console = Console()


class App:
    """ The main class of the application. """

    def __init__(self):
        self.doc_folder_path = environ.get("DOC_FOLDER_PATH", "documents/")
        self.knowledge_base_filename = environ.get(
            "KNOWLEDGE_BASE_FILENAME", "raw_knowledge_base")
        self.knowledge_vector_filename = environ.get(
            "KNOWLEDGE_VECTOR_FILENAME", "knowledge_vector_database")

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

        response = embed_service.save(self.knowledge_vector_filename)

        console.print(Markdown(response))

    def search(self, query):
        search_engine = SearchEngine(self.doc_folder_path,
                                     self.knowledge_vector_filename)
        response = search_engine.search(query)

        console.print(Markdown(response))

    def get_markdown(self):
        markdown_extractor = MarkdownExtractor(self.doc_folder_path)
        markdown_extractor.process()

        response = markdown_extractor.save(self.knowledge_base_filename)

        console.print(Markdown(response))

    def ask_question(self, question):
        operator = LLMAsker(self.doc_folder_path,
                            self.knowledge_vector_filename)
        response = operator.ask(question)

        console.print(Markdown(response))
