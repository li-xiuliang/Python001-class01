from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    print(browser)

    browser.get('https://shimo.im/welcome')
    time.sleep(1)

    button = browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
    button.click()
    time.sleep(5)
    browser.find_element_by_xpath('//div[@class="input"]/input[@name = "mobileOrEmail"]').send_keys('123456@qq.com')
    time.sleep(5)
    browser.find_element_by_xpath('//div[@class="input"]/input[@name = "password"]').send_keys('password')
    time.sleep(5)
    login = browser.find_element_by_xpath('//button[@class = "sm-button submit sc-1n784rm-0 bcuuIb"]')
    login.click()
    print('finished')


except Exception as e:
    print(e)
finally:
    browser.close()
