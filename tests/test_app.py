import argparse
from unittest.mock import patch

import pytest

from src import App


@pytest.fixture
def app():
    return App()


def test_run_index_files_mode(app):
    with patch.object(app, 'load_files') as mock_load_files:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(mode='index-files', question=None)):
            app.run()
            mock_load_files.assert_called_once()


def test_run_ask_question_mode(app):
    with patch.object(app, 'ask_question') as mock_ask_question:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(mode='ask-question', question='test question')):
            app.run()
            mock_ask_question.assert_called_once_with('test question')


def test_run_search_mode(app):
    with patch.object(app, 'search') as mock_search:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(mode='search', question='test query')):
            app.run()
            mock_search.assert_called_once_with('test query')


def test_run_get_markdown_mode(app):
    with patch.object(app, 'get_markdown') as mock_get_markdown:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(mode='get-markdown', question=None)):
            app.run()
            mock_get_markdown.assert_called_once()
