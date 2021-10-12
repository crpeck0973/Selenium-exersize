from selenium import webdriver
import chromedriver_autoinstaller
import time
import ssl
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
ssl._create_default_https_context = ssl._create_unverified_context


chromedriver_autoinstaller.install()

driver = webdriver.Chrome()


def navigate_to_url(url):
    driver.get(url)

def validate_toc_correctness():
    toc_elements = driver.find_elements_by_css_selector('.toctext')
    toc_elements_text = [0, 1, 2, 3, 4, 5, 6, 7]
    for i in range(len(toc_elements)):
        toc_elements_text[i] = toc_elements[i].text
    header_elements = driver.find_elements_by_css_selector('.mw-headline')
    header_elements_text = [0,1,2,3,4,5,6,7]
    for x in range(len(header_elements)):
        header_elements_text[x] = header_elements[x].text
    assert header_elements_text == toc_elements_text
    return toc_elements

def check_toc_href():
    toc_elements = driver.find_elements_by_css_selector('li.toclevel-1 > a')
    for i in range(len(toc_elements)):
        assert toc_elements[i].get_attribute('href')
    
def check_nike_popup():
    element = driver.find_element_by_link_text('Nike')
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    action = ActionChains(driver)
    action.move_to_element(element)
    action.perform()
    wait = WebDriverWait(driver, 10)
    popup = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.mwe-popups-extract > p')))
    assert popup.text == "In ancient Greek civilization, Nike was a goddess who personified victory. Her Roman equivalent was Victoria."
    return element

def confirm_family_tree():
    assert driver.find_element_by_css_selector('table.toccolours > caption > b > a').get_attribute('innerHTML')


if __name__ == '__main__':
    navigate_to_url('https://en.wikipedia.org/wiki/Metis_(mythology)')
    validate_toc_correctness()
    check_toc_href()
    element = check_nike_popup()
    element.click()
    confirm_family_tree()