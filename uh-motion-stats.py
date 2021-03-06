#!/usr/bin/python

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

##################
# Settings
##################
uh_motion_homepage = 'https://www.unitedhealthcaremotion.com/'

###################
# GLOBAL VARIABLES
###################
email = 'UNSET'
password = 'UNSET'
chromedriver_location = 'UNSET'


def main():
    """Drive the script"""
    load_env_variables()
    rankings = get_leaderboard_stats()
    print_text_rankings(rankings)


def load_env_variables():
    """Load required settings/config from shell variables"""
    global email, password, chromedriver_location
    try:
        email = os.environ["UH_MOTION_EMAIL"]
        password = os.environ["UH_MOTION_PW"]
        chromedriver_location = os.environ["CHROMEDRIVER_LOCATION"]
    except KeyError:
        print (
                "ERROR: Please set the following environment variables:\n",
                "1) UH_MOTION_EMAIL = User's UHM email address\n",
                "2) UH_MOTION_PW = User's UHM password\n",
                "3) CHROMEDRIVER_LOCATION = Full path to chromedriver binary\n"
        )
        sys.exit(-1)


def get_leaderboard_stats():
    """Scrape UH Motion website and return leaderboard as sorted list of dicts"""

    # Load page and reveal log-in form
    browser = webdriver.Chrome(chromedriver_location)
    browser.get(uh_motion_homepage)
    browser.implicitly_wait(10)
    browser.find_element_by_link_text('LOG IN').click()

    # Fill in and submit log-in form
    email_field = browser.find_element_by_xpath('//div[2]/div/div/form/div/div[2]/input')
    email_field.click()
    email_field.send_keys(email)
    password_field = browser.find_element_by_xpath('//div[2]/div/div/form/div/div[3]/input')
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)

    # Log-in redirect and browse to rankings page
    browser.implicitly_wait(10)
    # TODO: Need to deal with occasional "Congratulations" new badges pop-up
    browser.find_element_by_link_text('Rankings').click()
    browser.implicitly_wait(5)

    # Parse and store rankings results
    table_id = browser.find_element_by_id('rankTable')
    table_body = table_id.find_element_by_tag_name('tbody')
    rows = table_body.find_elements_by_tag_name("tr")

    # parse ranking table, and safe off people for later printing
    rankings = []
    for row in rows:
        # Get the columns (all the column 2)
        cols = row.find_elements_by_tag_name("td")
        person = {
            'rank': cols[0].text,
            'name': cols[1].text,
            'steps_monthly_current': cols[2].text,
            'steps_monthly_average': cols[3].text,
            'steps_lifetime': cols[4].text
        }

        rankings.append(person)

    # log out (playing nice) and clean up browser
    browser.find_element_by_link_text('LOG OUT').click()
    browser.implicitly_wait(5)
    # TODO: Need to add some way to make sure we always quit driver
    browser.quit()

    # Returns list of dicts, sorted by ranking
    return rankings


def print_text_rankings(rankings):
    """Print rankings list to console in simple text format"""

    # Print head fields and diver
    print ""
    print "{0:3} {1:16} {2:6}  {3:8} {4:8}".format(
        '#', 'Name', 'M-avg', 'M-cur', 'Lifetime'
    )
    print "{0:3} {1:16} {2:6}  {3:8} {4:8}".format(
        '---', '----------------',
        '------', '--------', '--------'
    )

    # Print out each person's records, UHM determines rank by monthly_average
    for person in rankings:
        print "{0:3} {1:16} {2:6}  {3:8} {4:8}".format(
            person['rank'],
            person['name'],
            person['steps_monthly_average'],
            person['steps_monthly_current'],
            person['steps_lifetime']
        )
    print ""


# Default action is to call main() to drive script
if __name__ == "__main__":
    main()
