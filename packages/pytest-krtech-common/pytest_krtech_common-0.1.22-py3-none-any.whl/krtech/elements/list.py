# coding=utf-8
import time

from selenium.webdriver.support.wait import WebDriverWait

from krtech.elements.base_element import BaseElement


class List(BaseElement):
    def __init__(self, name, by, locator):
        super(List, self).__init__(name, by, locator)
        self.element = None
        self.__elements = []

    def get_element_contains_text(self, text):
        for e in self.elements:
            if text.lower() in e.text.lower():
                self.element = e
                return self

    def get_element_by_text(self, text):
        for e in self.elements:
            if text.strip() == e.text.strip():
                self.element = e
                return self

    def get_element_by_attribute(self, attr, value):
        for e in self.elements:
            if e.get_attribute(attr) == value:
                self.element = e
                return self

    def get_element_by_index(self, index):
        if index < len(self.elements):
            self.element = self.elements[index]
            return self

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, value):
        self.__elements = value

    def __getitem__(self):
        return self

    def __str__(self):
        return self.name

    def __get__(self, obj, owner):
        driver = obj.config.driver
        timeout = int(obj.config.element_wait)
        time.sleep(float(obj.config.element_init_timeout))

        WebDriverWait(driver, timeout).until(
            lambda s: len(driver.find_elements(self.by, self.locator)) > 0)

        self.__elements = driver.find_elements(self.by, self.locator)
        return self
