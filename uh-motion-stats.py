#!/usr/bin/python

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

try:
    email = os.environ["UH_MOTION_EMAIL"]
    password = os.environ["UH_MOTION_PW"]
except KeyError:
    print "ERROR: Please set UH_MOTION_EMAIL and UH_MOTION_PW env variables"
    sys.exit(-1)

path_to_chromedriver = '/Users/jrlorence/PycharmProjects/UHMotionStats/chromedriver'
browser = webdriver.Chrome(path_to_chromedriver)

url = 'https://www.unitedhealthcaremotion.com/'

# reveal and fill in log-in form
browser.get(url)
browser.find_element_by_link_text('LOG IN').click()
email_field = browser.find_element_by_xpath('//div[2]/div/div/form/div/div[2]/input')
email_field.click()
email_field.send_keys(email)
password_field = browser.find_element_by_xpath('//div[2]/div/div/form/div/div[3]/input')
password_field.send_keys(password)
password_field.send_keys(Keys.ENTER)

# Log-in redirect and browse to rankins page
browser.implicitly_wait(10)
browser.find_element_by_link_text('Rankings').click()
browser.implicitly_wait(5)

# Parse and store rankings results
table_id = browser.find_element_by_id('rankTable')
table_body = browser.find_element_by_tag_name('tbody')
rows = table_body.find_elements_by_tag_name("tr")

# parse ranking table, and safe off people for later printing
rankings = []
for row in rows:
    # Get the columns (all the column 2)
    cols = row.find_elements_by_tag_name("td")
    person = {}
    person['rank'] = cols[0].text
    person['name'] = cols[1].text
    person['steps_monthly_current'] = cols[2].text
    person['steps_monthly_average'] = cols[3].text
    person['steps_lifetime'] = cols[4].text
    rankings.append(person)

# log out (playing nice) and clean up browser
browser.find_element_by_link_text('LOG OUT').click()
browser.implicitly_wait(5)
browser.quit()

# Pretty printing out to user
print ""
print "{0:3} {1:16} {2:6}  {3:8} {4:8}".format(
    '#', 'Name', 'M-avg', 'M-cur', 'Lifetime'
)
print "{0:3} {1:16} {2:6}  {3:8} {4:8}".format(
    '---', '----------------',
    '------', '--------', '--------'
)
for person in rankings:
    print "{0:3} {1:16} {2:6}  {3:8} {4:8}".format(
        person['rank'],
        person['name'],
        person['steps_monthly_average'],
        person['steps_monthly_current'],
        person['steps_lifetime']
    )
print ""

