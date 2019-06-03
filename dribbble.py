#!/usr/bin/env python

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger,
                    level='INFO',
                    fmt='%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pdb import set_trace as bp ##for testing
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import re
import time
import csv
import os
import click
import sys
import csv

def check_exists_by_xpath(driver, xpath):
	try:
	    driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
	    return False
	return True

def get_name(url):
	x = url.split('/')
	logger.info("name of the user is: " + x[-1])
	return x[-1]

def modify(row, name):
	S = row[0:3] + name + row[6:]
	logger.info(S)
	return S

def go_login(driver):
	driver.find_element_by_xpath('//span[text() = "Sign in"]').click()
	time.sleep(2)
	element = driver.find_element_by_xpath('//input[@id="login"]')
	element.send_keys("faraday_anshul")
	time.sleep(1)
	element = driver.find_element_by_xpath('//input[@id="password"]')
	element.send_keys("Meghraj@123")
	time.sleep(1)
	driver.find_element_by_xpath('//input[@value="Sign In"]').click()
	time.sleep(1)

def add_new_line(actionChains):
	actionChains.key_down(Keys.ENTER)
	actionChains.key_down(Keys.ENTER)
	actionChains.key_up(Keys.ENTER)

def do_stuff(driver, url, template_reader):
	 # On the city page
	driver.get(url)

	time.sleep(5)

	go_login(driver)
	driver.find_element_by_xpath('//span[text()="Hire Me"]')
	if not check_exists_by_xpath(driver, '//span[text()="Hire Me"]'):
		return
	driver.find_element_by_xpath('//span[text()="Hire Me"]').click()
	time.sleep(4)

	element = driver.find_element_by_xpath('//input[@value="fulltime"]')
	logger.warn(element.get_attribute("id"))
	time.sleep(1)

	el=driver.find_element_by_xpath('//div[contains(@class,"type-of-work")]/label')
	el.click()
	time.sleep(1)

	textarea = driver.find_element_by_xpath('//textarea[@id="message_body"]')

	name = get_name(url)
	actionChains = ActionChains(driver)

	for row in template_reader:
		logger.info(row[0])
		S = row[0]
		if row[0] == "Hi (x),":
			S = modify(row[0], name)
		actionChains.send_keys_to_element(textarea, S)
		add_new_line(actionChains)

	actionChains.perform()
	time.sleep(1)

	# driver.find_element_by_xpath('//input[@value="Send Inquiry"]').click()
	time.sleep(20)


@click.command()
@click.option('--input', '-i', 'input_', required=True, type=click.Path(exists=True))
@click.option('--template',  '-t', 'template_', required=True, type=click.Path(exists=True))
@click.option('--driver', '-d', 'driver_', required=True, type=click.Path(exists=True))
def run(input_, template_, driver_):
	logger.info('Web Driver: %s.',os.path.expanduser(driver_))
	chrome_options = Options()
	driver = webdriver.Chrome(executable_path=os.path.realpath(driver_), chrome_options=chrome_options)
	
	template_file = open(template_, 'r')
	template_reader = csv.reader(template_file, delimiter = '|')

	with open(input_, 'r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			logger.warn(f'Processing {line_count + 1} line...')
			do_stuff(driver, row[0], template_reader)
			logger.info(f'Iteration successfully finished for {line_count + 1} line.')
			line_count += 1
		logger.info(f'Processed {line_count} lines.')
		sys.exit()

if __name__ == "__main__":
    run()