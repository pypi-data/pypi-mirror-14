# -*- coding: utf-8 -*-

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys


class DOM(object):
    """DOM element (don't instantiate this class yourself..)
    """
    def __init__(self, web_element):
        self.dom = web_element

    def __getattr__(self, attr):
        # defer to the web-element
        return getattr(self.dom, attr)

    def __getitem__(self, name):
        return self.dom.get_attribute(name)

    @property
    def visible(self):
        return self.dom.is_displayed()

    @property
    def enabled(self):
        return self.dom.is_enabled()

    @property
    def selected(self):
        return self.dom.is_selected()

    def type(self, keys):
        self.dom.send_keys(keys)
        return self

    def __iadd__(self, keys):
        self.dom.send_keys(keys)
        return self


class Browser(object):
    def __init__(self, browsername):
        self.driver = getattr(webdriver, browsername)()

    def __getattr__(self, attr):
        # defer to the webdriver
        return getattr(self.driver, attr)

    def __setitem__(self, query, keys):
        """type into a selector:

               b['#q'] = 'word'
        """
        item = self(query)
        item += keys
        return item

    def __call__(self, query):
        """jQuery-like convenience syntax.
        """
        return DOM(self.driver.find_element_by_css_selector(query))

    __getitem__ = __call__
