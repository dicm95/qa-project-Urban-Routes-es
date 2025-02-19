import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_tariff = (By.ID, 'tariff-card-4')
    phone_field = (By.CLASS_NAME, 'np-button')
    add_phone_number = (By.ID, 'phone')
    payment_method = (By.CLASS_NAME, 'pp-button.filled')
    add_card = (By_CLASS_NAME, 'pp-row.disabled')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.ID, 'code')
    card_wrapper = (By.CLASS_NAME, 'card-wrapper')
    add_button = (By.XPATH, '//button[text()='Agregar']')
    comment_field = (By.ID, 'comment')
    toggle_switch = (By.CLASS_NAME, 'switch-input')
    ice_cream_counter_plus = (By.XPATH, '//div[contains(text(), 'Helado')]//following::div[contains(@class, 'counter-plus')]')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_comfort(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def click_phone_field(self):
        self.driver.find_element(*self.phone_field).click()

    def set_phone(self, phone_number):
        self.driver.find_element(*self.add_phone_number).send_keys(phone_number)

    def select_payment_method(self):
        self.driver.find_element(*self.payment_method).click()

    def add_payment_card(self):
        self.driver.find_element(*self.add_card).click()

    def add_card_number(self, card_number):
        self.driver.find_element(*self.card_number_field).send_keys(card_number)

    def add_cvv_code(self, card_code):
        self.driver.find_element(*self.cvv_code_field).send_keys(card_code)

    def activate_add_button(self):
        self.driver.find_element(*self.card_wrapper).click()

    def click_add_button(self):
        self.driver.find_element(*self.add_button).click()

    def add_message_for_driver(self, message_for_driver):
        self.driver.find_element(*self.comment_field).send_keys(message_for_driver)

    def add_blanket_and_scarves(self):
        self.driver.find_element(*self.toggle_switch).click()

    def add_ice_cream(self):
        self.driver.find_element(*self.ice_cream_counter_plus).click()



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_set_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_comfort()

    def test_set_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone_field()
        routes_page.set_phone(phone_number)
        retrieve_phone_code(driver)

    def test_add_payment_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_payment_method()
        routes_page.add_payment_card()
        routes_page.add_card_number(card_number)
        routes_page.add_cvv_code(card_code)
        routes_page.activate_add_button()
        routes_page.click_add_button()

    def test_add_driver_message(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        message_for_driver = data.message_for_driver
        routes_page.add_message_for_driver(message_for_driver)

    def test_add_blanket_and_scarves(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_toggle()

    def test_add_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_ice_cream()
        routes_page.add_ice_cream()

    def test_modal_appearance(self):
        self.driver.get(data.urban_routes_url)
        WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'smart-button'))

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
