# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import logging


# Start the browser and login with standard_user
def login (user, password) -> WebDriver:
    logger.info('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    # setup 10 seconds to wait for element is loaded
    driver.implicitly_wait(5)

    logger.info('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    driver.find_element(by=By.ID, value="user-name").send_keys(user)
    driver.find_element(by=By.ID, value="password").send_keys(password)
    login_button = driver.find_element(by=By.ID, value="login-button")

    if login_button.is_displayed():
        login_button.submit()
        logger.info(f"User: {user} login successfully")

    header = driver.find_element(by=By.CSS_SELECTOR, value="#header_container .app_logo").text
    is_toggle_displayed = driver.find_element(by=By.ID, value="menu_button_container").is_displayed()

    assert "Swag Labs" == header, "Failed to verify header"
    assert True == is_toggle_displayed, "Toggle is not displayed"
    logger.info("Verify user navigate to home page successfully")
    return driver

def add_items_to_cart():
    items = driver.find_elements(by=By.CSS_SELECTOR, value="#inventory_container .inventory_list .inventory_item")

    for item in items:
        item.find_element(by=By.CSS_SELECTOR, value="button").click()
        item_text = item.find_element(by=By.CLASS_NAME, value="inventory_item_name").text
        logger.info(f"Add {item_text} to cart successfully")

    cart_items = driver.find_element(by=By.CSS_SELECTOR, value="#shopping_cart_container .shopping_cart_badge").text
    assert len(items) == int(cart_items), "Failed to add all item to cart"
    logger.info("Add all item into cart successfully")

def remove_items_from_cart():
    items = driver.find_elements(by=By.CSS_SELECTOR, value="#inventory_container .inventory_list .inventory_item")
    for item in items:
        item.find_element(by=By.CSS_SELECTOR, value="button").click()
        item_text = item.find_element(by=By.CLASS_NAME, value="inventory_item_name").text
        logger.info(f"Remove {item_text} from cart successfully")

    try:
        is_existing_element = driver.find_element(by=By.CSS_SELECTOR, value="#shopping_cart_container .shopping_cart_badge").is_displayed()
    except NoSuchElementException:
        logger.info("DOM Element is removed from UI")
        is_existing_element = False

    assert False == is_existing_element
    logger.info("Remove all item from cart successfully")

def full_e2e_test():
    add_items_to_cart()

    driver.find_element(by=By.CSS_SELECTOR, value="#shopping_cart_container .shopping_cart_badge").click()
    logger.info("Navigate to cart page successfully")

    driver.find_element(by=By.ID, value="checkout").click()
    logger.info("Navigate to checkout page successfully")

    driver.find_element(by=By.ID, value="first-name").send_keys("tung")
    logger.info("Fill firstname successfuly")
    driver.find_element(by=By.ID, value="last-name").send_keys("tt44")
    logger.info("Fill lastname successfuly")
    driver.find_element(by=By.ID, value="postal-code").send_keys("1234567")
    logger.info("Fill postal-code successfuly")
    driver.find_element(by=By.ID, value="continue").click()
    logger.info("Navigate to final checkout page successfully")

    is_summary_displayed = driver.find_element(by=By.CSS_SELECTOR, value="#checkout_summary_container .summary_info").is_displayed()
    assert True == is_summary_displayed, "Summary Info is not displayed"

    driver.find_element(by=By.ID, value="finish").click()
    logger.info("Finish checkout successfully, Navigate to Complete page successfully")

    is_checkout = driver.find_element(by=By.CLASS_NAME, value="pony_express").is_displayed()
    assert True == is_checkout, "Icon checkout is not displayed"
    is_completed = driver.find_element(by=By.CSS_SELECTOR, value="#header_container .header_secondary_container").text
    assert "Checkout: Complete!" == is_completed

    driver.find_element(by=By.ID, value="back-to-products").click()

    header = driver.find_element(by=By.CSS_SELECTOR, value="#header_container .app_logo").text
    is_toggle_displayed = driver.find_element(by=By.ID, value="menu_button_container").is_displayed()
    assert "Swag Labs" == header, "Failed to verify header"
    assert True == is_toggle_displayed, "Toggle is not displayed"
    logger.info("Go back to home page successfully")

if __name__ == "__main__":
    logging.basicConfig(
        filename="automation-test.log",
        filemode="w",
        encoding="utf-8",
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting automation test with selenium...")
    driver = login('standard_user', 'secret_sauce')
    add_items_to_cart()
    remove_items_from_cart()
    full_e2e_test()
    logger.info("End automation test with selenium...")
    driver.quit()
