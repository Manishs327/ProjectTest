import pytest

from pages.launch_page import LaunchPage
from pages.search_results import SearchResults
from utilities.utils import Utils


@pytest.mark.usefixtures("setup")
class TestSearchAndVerify:

    def test_search_flight(self, ):
        lp=LaunchPage(self.driver)
        lp.departfrom("New Delhi")
        lp.goingto("Mumbai")
        lp.selectdate("28/12/2023")
        lp.clicksearch()
        lp.page_scroll()
        sr = SearchResults(self.driver)
        filtered_flights = sr.filter_flights()
        ut=Utils()
        ut.verify_search_results(filtered_flights)
