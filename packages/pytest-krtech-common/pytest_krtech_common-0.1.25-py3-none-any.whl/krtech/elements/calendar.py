# coding=utf-8
from krtech.elements.list import List
from selenium.webdriver.common.by import By

from krtech.elements.base_element import BaseElement


class Calendar(BaseElement):

    buttons = ".//button[@class='xdsoft_%s']"

    @property
    def previous(self):
        return BaseElement(u"Назад", By.XPATH, self.buttons % 'prev')

    @property
    def next(self):
        return BaseElement(u"Вперед", By.XPATH, self.buttons % 'next').__get__(self)

    @property
    def today(self):
        return BaseElement(u"Сегодня", By.XPATH, self.buttons % 'today_button').__get__(self)

    @property
    def year(self):
        return BaseElement(u"Год", By.XPATH, ".//div[@class='xdsoft_label xdsoft_year']/span").__get__(self)

    @property
    def year_list(self):
        return List(u"Список 'Год'", By.XPATH, "//div[contains(@class,'yearselect')]/div[1]/div").__get__(self)

    def get_year(self, year):
        """
        Выбирает год из открытого списка в календаре
        :param year: числовое представление года, например 2001
        :return: BaseElement год
        """
        for e in self.year_list:
            if year.__class__.__name__ == 'str':
                year = int(year)
            if year == int(e.get_attribute('data-value')):
                return e
        raise Exception(u"Год '" + str(year) + "' не найден в календаре")

    @property
    def month(self):
        return BaseElement(u"Месяц", By.XPATH, ".//div[@class='xdsoft_label xdsoft_month']/span").__get__(self)

    @property
    def month_list(self):
        return List(u"Список 'Месяц'", By.XPATH, "//div[contains(@class,'monthselect')]/div[1]/div").__get__(self)

    def get_month(self, month):
        """
        Выбирает месяц из открытого списка в календаре
        :param month: числовое или строковое наименование месяца, например 7 или "июль"
        :return: BaseElement месяц
        """
        for e in self.month_list:
            if month.__class__.__name__ == 'int':
                if int(month) == (int(e.get_attribute('data-value')) + 1):
                    return e
            else:
                if month.lower() == e.text.lower():
                    return e
        raise Exception(u"Месяц '" + str(month) + "' не найден в календаре")

    @property
    def current_day(self):
        return BaseElement(u"Текущий день", By.XPATH,
                           ".//td[contains(@class,'day') and contains(@class,'current')]").__get__(self)

    @property
    def day_list(self):
        return List(u"Список дней", By.XPATH,
                    "//td[contains(@class,'day') and not(contains(@class,'other'))]").__get__(self)

    def get_day(self, day):
        """
        Выбирает день из открытого списка в календаре
        :param day: числовое или строковое представление дня, например 24 или "24"
        :return: WebElement день
        """
        for e in self.day_list.elements:
            if int(day) == (int(e.text)):
                return e
        raise Exception(u"День '" + str(day) + "' не найден в календаре")

    def is_day_disabled(self, day):
        return 'disabled' in self.get_day(day).get_attribute('class')

    @property
    def top(self):
        return BaseElement(u"", By.XPATH, ".//div[@class='xdsoft_timepicker active']/button[1]").__get__(self)

    @property
    def bottom(self):
        return BaseElement(u"", By.XPATH, ".//div[@class='xdsoft_timepicker active']/button[2]").__get__(self)

    @property
    def time_list(self):
        return self.element.find_elements(By.XPATH, ".//div[contains(@class,'time_v')]/div")

    def get_time(self, time):
        for e in self.time_list:
            if time == e.text:
                return e
        raise Exception(u"Время '" + time + "' не найдено в календаре")
