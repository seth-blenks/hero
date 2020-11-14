import unittest
from database import db,Comments,Statistics,User
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from app import create_app
from config import config
from threading import Thread
import os,sys
import time

class SeleniumTestCase(unittest.TestCase):
    client = None
    BASE = "http://localhost:5000"

    @classmethod
    def setUpClass(cls):
        opt = Options()
        opt.headless = True

        cls.app = create_app("Test")
        cls.context = cls.app.app_context()
        cls.context.push()

        

        cls.server_thread = Thread(target=cls.app.run)
        cls.server_thread.start()

        cls.client = Firefox(options=opt)

        
    def test_homepage()

    

        

    @classmethod
    def tearDownClass(cls):
        cls.client.get("http://localhost:5000/shutdown")
        cls.client.close()
        cls.client.quit()
        cls.server_thread.join()
        cls.context.pop()

if __name__ == "__main__":
    unittest.main()