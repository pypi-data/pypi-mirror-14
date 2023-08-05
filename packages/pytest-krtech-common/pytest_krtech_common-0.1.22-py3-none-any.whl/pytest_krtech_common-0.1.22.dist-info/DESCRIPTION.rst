================================
Krtech common library for pytest
================================

Selenium web elements wrapper library based on allure report.
Contains base elements, pages and methods (steps).

------------
Installation
------------
You can install using pip:
::
    pip install pytest-krtech-common

-------------
Configuration
-------------
To configure ``conftest.py`` do:

code:: python
    import pytest
    from configuration import TestConfig, ConftestOptions

    class OverwrittenTestConfig(TestConfig):
        myprop = "myprop_value"
        mysqldb = "mydb"

    tc = OverwrittenTestConfig()
    c = ConftestOptions(tc)


    def pytest_addoption(parser):
        c.pytest_addoption(parser)


    @pytest.mark.tryfirst
    def pytest_runtest_makereport(item, call, __multicall__):
        return c.pytest_runtest_makereport(item, call, __multicall__)


    @pytest.yield_fixture(scope='session')
    def config(request):
        op = c.config(request)
        yield op
        op.driver.close()

-----
Usage
-----
Pages:

code:: python
    from selenium.webdriver.common.by import By
    from krtech.decorators import page
    from krtech.elements.base_element import BaseElement
    from krtech.pages.base_page import BasePage

    @page('Profile Page', By.ID, 'profilePageId')
    class ProfilePage(BasePage):
        HEADER = BaseElement("Profile page header", By.XPATH, ".//h6")

Tests:

code:: python
    from youproject.pages.profile_page import ProfilePage
    from krtech.steps.user_steps import UserSteps

    @pytest.mark.usefixtures('config')
    @allure.feature('Profile Header')
    class TestProfile:

    def test_profile_header(self, config):
        user = UserSteps(config)
        profile_page = ProfilePage(config)

        user.opens('/profile')
        user.should_see_element_matched_to(profile_page.PROFILE, equal_to_ignoring_case(c.customers_data.name))
        user.should_see_attribute_value(profile_page.OTHER, 'disabled', True)


-------------
Wheel package
-------------
To build a wheel package do::
  cd pytest-krtech-common/
  python setup.py bdist_wheel

Package should be available at::
  dist/pytest_krtech_common-0.1-py3-none-any.whl

To install from wheel do::
    pip install pytest_krtech_common-0.1-py3-none-any.whl


