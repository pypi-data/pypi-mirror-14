# coding=utf-8
import logging
import re

from krtech.elements.base_element import BaseElement
from selenium.webdriver.common.by import By


class List(BaseElement):

    def __init__(self, name, by, locator):
        super().__init__(name, by, locator)
        if by != By.XPATH:
            logger = logging.getLogger("element_list_logger")
            logger.warning(u"xpath selector only is allowed for ElementsList")

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
        l = list()
        i = 1
        for e in self.element.find_elements(self.by, self.locator):
            l.append(BaseElement("Элемент списка #" + str(i), self.by,
                                 "/descendant::" + re.sub('^%s' % '//', '', self.locator) + "[" + str(i) + "]")
                     .__get__(self))
            i += 1

        return l
