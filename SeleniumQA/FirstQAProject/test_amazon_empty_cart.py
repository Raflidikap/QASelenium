from selenium import webdriver
from selenium.webdriver.common.by import By
from amazoncaptcha import AmazonCaptcha

class TestAmazonCart:   
    driver = ''

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.amazon.com/')
        self.driver.implicitly_wait(10)

    def test_amazon_empty_cart(self):
        captchaImage = self.driver.find_element(By.XPATH, "//div[@class = 'a-row a-text-center']//img").get_attribute('src')

        captcha = AmazonCaptcha.fromlink(captchaImage)
        captcha_value = AmazonCaptcha.solve(captcha)

        input_captcha = self.driver.find_element(By.ID, 'captchacharacters')
        input_captcha.send_keys(captcha_value)  

        button = self.driver.find_element(By.CLASS_NAME, 'a-button-text')
        button.click()

        cart = self.driver.find_element(By.ID, 'nav-cart')
        cart.click()

        actual_text = self.driver.find_element(By.XPATH, "//div[@id='sc-empty-cart']//h3").text
        expected_text = 'Your Amazon Cart is empty'

        assert actual_text == expected_text, f"Expected text: '{expected_text}', but found: '{actual_text}'"
        print(actual_text)


    def teardown_method(self):
        self.driver.quit()