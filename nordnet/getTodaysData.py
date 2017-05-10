from selenium import webdriver
from selenium.webdriver.common.keys import Keys # For enter-key
import getpass
import time, sys

def loginNordnet(filename, password_string):
    print "----------------------------------------------------"
    print "Booting virtual browser... and opening 'nordnet.no'"

    # Browser will run in a virtual display
    driver = webdriver.PhantomJS()
    # driver = webdriver.Firefox() # This will show up in a window (good for testing)

    # Open the URL
    driver.get('https://www.nordnet.no/mux/login/start.html')

    # Set timeout
    driver.set_script_timeout(30)
    time.sleep(2) # Wait two seconds to load

    sys.stdout.write("Logging in..."); sys.stdout.flush()

    username = driver.find_element_by_id("input1")
    # username = driver.find_element_by_id("username")
    username.send_keys("haakonvt")
    pw = driver.find_element_by_id("pContent")
    # pw = driver.find_element_by_id("password")
    pw.send_keys(password_string, Keys.ENTER)

    time.sleep(2) # Wait two seconds to load

    driver.get('https://www.nordnet.no/mux/web/depa/mindepa/depaoversikt.html')
    sys.stdout.write("\rLogging in... success!\n"); sys.stdout.flush()
    sys.stdout.write("\rSave to file, logging out and closing browser..."); sys.stdout.flush()

    # Get all info on page as text and save to file
    text = driver.find_element_by_tag_name("body").text
    with open(filename, 'w') as the_file:
        the_file.write(text.encode('utf8'))

    # Click the log out button!
    logout_link = driver.find_element_by_partial_link_text('Logg ut')
    logout_link.click()

    # Quit driver
    time.sleep(1)
    driver.quit()

    sys.stdout.write("\rSave to file, logging out and closing browser... success!\n"); sys.stdout.flush()


if __name__ == '__main__':
    password_string = getpass.getpass('Password: ')
    if not password_string:
        print "You have to type in your login password! Exiting!"
        sys.exit(0)
    loginNordnet("dagensData.txt", password_string)
