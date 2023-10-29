from src import utils
from hypothesis import given, strategies as st


class TestUtils:
    @given(st.text(min_size=5))
    def test_url_filter_returns(self, random_path: str) -> None:
        url = f"https://www.monzo.com/{random_path}"
        netloc = "www.monzo.com"
        expected = f"https://www.monzo.com/{random_path}"
        url_filter = utils.get_url_filter(netloc)
        assert url_filter(url) == expected

    @given(st.text(min_size=5))
    def test_url_filter_returns_relative(self, random_path: str) -> None:
        url = f"/{random_path}"
        netloc = "www.monzo.com"
        expected = f"/{random_path}"
        url_filter = utils.get_url_filter(netloc)
        assert url_filter(url) == expected

    @given(st.text(min_size=5))
    def test_url_filter_removes_invalid(self, random_path: str) -> None:
        url = f"https://www.another.com/{random_path}"
        netloc = "www.monzo.com"
        url_filter = utils.get_url_filter(netloc)
        assert url_filter(url) is None

    @given(st.text(min_size=5))
    def test_url_processor_returns(self, random_path: str) -> None:
        url = f"https://www.monzo.com/{random_path}"
        netloc = "www.monzo.com"
        expected = f"https://www.monzo.com/{random_path}"
        url_processor = utils.get_url_processor(netloc)
        assert url_processor(url) == expected

    @given(st.text(min_size=5))
    def test_url_processor_returns(self, random_path: str) -> None:
        url = f"/{random_path}"
        netloc = "www.monzo.com"
        expected = f"https://www.monzo.com/{random_path}"
        url_processor = utils.get_url_processor(netloc)
        assert url_processor(url) == expected

    @given(st.text(min_size=5))
    def test_url_is_relative_true(self, random_path: str) -> None:
        url = f"/{random_path}"
        assert utils.is_url_relative(url)

    @given(st.text(min_size=5))
    def test_url_is_relative_false(self, random_path: str) -> None:
        url = f"https://www.sth.com/{random_path}"
        assert not utils.is_url_relative(url)
