import pytest
from src.parser import URLParser


@pytest.fixture
def parser():
    return URLParser(lambda x: x, lambda x: x)


data = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Link Example</title>
    </head>
    <body>
        <h1>Links Example</h1>
    
        <p>This is an example of HTML links with both relative and absolute URLs:</p>
    
        <ul>
            <li><a href="https://www.example.com">Absolute Link to Example.com</a></li>
            <li><a href="/about.html">Relative Link to About Page</a></li>
            <li><a href="images/pic.jpg">Relative Link to an Image</a></li>
        </ul>
    
    </body>
    </html>
"""


class TestParser:
    def test_parse(self, parser: URLParser, mocker):
        spy_filter = mocker.spy(parser, "url_filter")
        spy_processor = mocker.spy(parser, "url_processor")

        parser.feed(data)

        # Make sure that we call as many filters as processors
        assert spy_filter.call_count == spy_processor.call_count
