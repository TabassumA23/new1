from api.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginSeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    @classmethod

    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.user = cls.User.objects.create_user(

            username="testuser",
            password="password123",
            email="testuser@example.com"
        )
        # Hardcoded for debugging or use reverse()
        cls.login_url = "/login/"  
        print(f"Set up test data: Login URL = {cls.login_url}")  

    def test_signup(self):
        """Test that a new user can sign up."""
        self.driver.get(f"{self.live_server_url}/signup/")

        # Fill out the signup form
        firstname_field = self.driver.find_element(By.NAME, "first_name")
        lastname_field = self.driver.find_element(By.NAME, "last_name")
        username_field = self.driver.find_element(By.NAME, "username")
        email_field = self.driver.find_element(By.NAME, "email")
        date_of_birth_field = self.driver.find_element(By.NAME, "date_of_birth")
        password_field = self.driver.find_element(By.NAME, "password")
        
        signup_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        firstname_field.send_keys("userfirstname")
        lastname_field.send_keys("userlastname")
        username_field.send_keys("newuser")
        email_field.send_keys("newuser@example.com")
        password_field.send_keys("password123")
        date_of_birth_field.send_keys("1990-01-01")
        signup_button.click()

        # Verify successful signup
        # Wait for the redirection to complete
        self.driver.implicitly_wait(10)

        # Verify the current URL matches the expected dashboard URL
        expected_url = "http://localhost:5173/?u=1"
        self.assertEqual(self.driver.current_url, expected_url)

    def test_signup_2(self):
        """Test that a new user can sign up."""
        self.driver.get(f"{self.live_server_url}/signup/")

        # Fill out the signup form
        firstname_field = self.driver.find_element(By.NAME, "first_name")
        lastname_field = self.driver.find_element(By.NAME, "last_name")
        username_field = self.driver.find_element(By.NAME, "username")
        email_field = self.driver.find_element(By.NAME, "email")
        date_of_birth_field = self.driver.find_element(By.NAME, "date_of_birth")
        password_field = self.driver.find_element(By.NAME, "password")
        
        signup_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        firstname_field.send_keys("userSecondfirstname")
        lastname_field.send_keys("userSecondlastname")
        username_field.send_keys("newSeconduser")
        email_field.send_keys("newuserSecond@example.com")
        password_field.send_keys("password123")
        date_of_birth_field.send_keys("1990-01-01")
        signup_button.click()
        # Verify successful signup
        # Wait for the redirection to complete
        self.driver.implicitly_wait(10)

        # Verify the current URL matches the expected dashboard URL
        expected_url = "http://localhost:5173/?u=2"
        self.assertEqual(self.driver.current_url, expected_url)

    


    def test_successful_login(self):
        """Test that a valid user can log in and is redirected to the dashboard."""
        self.driver.get(f"{self.live_server_url}/login/")

        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys("testuser")
        password_field.send_keys("password123")
        login_button.click()

        # Wait for the redirection or page content
        self.driver.implicitly_wait(10)

        # Debugging outputs
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page Source: {self.driver.page_source}")

        # Verify the redirect and page content
        expected_url = f"{self.live_server_url}/login/"
        self.assertEqual(self.driver.current_url, expected_url)
        
    def test_successful_login_2(self):
        """Test that a valid user can log in and is redirected to the dashboard."""
        self.driver.get(f"{self.live_server_url}/login/")

        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys("userSeconduser")
        password_field.send_keys("password123")
        login_button.click()

        # Wait for the redirection or page content
        self.driver.implicitly_wait(10)

        # Debugging outputs
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page Source: {self.driver.page_source}")

        # Verify the redirect and page content
        expected_url = f"{self.live_server_url}/login/"
        self.assertEqual(self.driver.current_url, expected_url)

    def test_filter_users_by_age(self):
        """Test that users can be filtered by age."""
        

        self.driver.get("http://localhost:5173/FindFriends/")

        # Locate filter field and butto

        # Locate the "Min Age" input field and enter a value
        min_age_input = self.driver.find_element(By.ID, "minAge")
        min_age_input.clear()  # Clear any existing value
        min_age_input.send_keys("18")  # Enter the minimum age

        # Locate the "Max Age" input field and enter a value
        max_age_input = self.driver.find_element(By.ID, "maxAge")
        max_age_input.clear()  # Clear any existing value
        max_age_input.send_keys("25")  # Enter the maximum age

        # Verify filtered results
        self.assertIn("Filtered users", self.driver.page_source)  # Adjust to match your page content

    def test_send_friend_request(self):
        """Test that a user can send a friend request."""
       
        # Log in first
        self.test_successful_login()

        self.driver.get(f"{self.live_server_url}/FindFriends/")  # Replace with the correct users page URL

        # Locate the friend request button
        send_request_button = self.driver.find_element(By.XPATH, "//button[@data-user-id='2']")  # Update the selector
        send_request_button.click()

        # Verify friend request sent
        self.assertIn("Friend request sent", self.driver.page_source)

    def test_accept_friend_request(self):
        """Test that a user can accept a friend request."""
        # Log in as another user
        self.driver.get(f"{self.live_server_url}/login/")

        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys("otheruser")
        password_field.send_keys("password456")
        login_button.click()

        # Navigate to friend requests page
        self.driver.get(f"{self.live_server_url}/?u=2/")

        # Locate and accept the friend request
        accept_button = self.driver.find_element(By.XPATH, "//button[@data-request-id='1']")  # Update selector
        accept_button.click()

        # Verify friend request accepted
        self.assertIn("Friend request accepted", self.driver.page_source)
