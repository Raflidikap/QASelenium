import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from amazoncaptcha import AmazonCaptcha

class TestAmazon:
    driver = ''
    search_words = ('iphone 13', 'converse', 'gundam')

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(20)
        self.driver.get('https://www.amazon.com/')

    
    @pytest.mark.parametrize('search_query', search_words)
    def test_amazon_search(self, search_query):

        #CAPTCHA HANDLER
        captchaImage = self.driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute('src')

        captcha = AmazonCaptcha.fromlink(captchaImage)
        captcha_value = AmazonCaptcha.solve(captcha)

        self.driver.find_element(By.ID, 'captchacharacters').send_keys(captcha_value)
        button = self.driver.find_element(By.CLASS_NAME, 'a-button-text')
        button.click()

        #SEARCH
        search = self.driver.find_element(By.ID, 'twotabsearchtextbox')
        search.send_keys(search_query, Keys.ENTER)

        expected_text = f'\"{search_query}"'
        actual_text = self.driver.find_element(By.XPATH,"//span[@class='a-color-state a-text-bold']").text

        assert expected_text == actual_text, f'Error. Expected text: {expected_text}, but found: {actual_text}'

        
    def teardown_method(self):
        self.driver.quit()