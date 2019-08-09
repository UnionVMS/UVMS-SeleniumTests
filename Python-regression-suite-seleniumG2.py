import unittest
import time
import timeout_decorator
import os
import datetime
import random
import sys
from unittest.case import _AssertRaisesContext
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import subprocess
import os
import psycopg2
import requests
import urllib.request
from os.path import expanduser
import os.path
import csv
import codecs
import xmlrunner
import distutils.dir_util
from io import BytesIO
from zipfile import ZipFile
import urllib.request
import platform
import collections
from pathlib import Path
import copy
import zeep

# Import parameters from parameter file
from UnionVMSparametersG2 import *


def startup_browser_and_login_to_unionVMS(self):
    # Print Selenium version
    print("Selenium version")
    print(selenium.__version__)
    # Start Chrome browser
    self.driver = webdriver.Chrome()
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Print Chrome version
    print("Driver capabilities")
    print (self.driver.capabilities)
    # Maximize browser window
    self.driver.maximize_window()
    self.driver.get(httpUnionVMSurlString)
    time.sleep(2)

    # if Hav och vatten proxy page is presented, then autologin
    try:
        if self.driver.find_element_by_xpath("/html/head/title"):
            self.driver.switch_to.frame("content")
            self.driver.find_element_by_css_selector("img[alt=\"Automatisk inloggning\"]").click()
            time.sleep(2)
    except:
        pass

    # if Pop-up windows exists then click cancel
    try:
        if self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/form"):
            self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/form/div[3]/button[2]").click()
            time.sleep(2)
    except:
        pass

    wait_for_element_by_id_to_exist(wait, "userId", "userId checked 0")
    time.sleep(1)
    self.driver.find_element_by_id("userId").send_keys(defaultUserName)
    self.driver.find_element_by_id(defaultUserNamePassword).send_keys(defaultUserNamePassword)
    time.sleep(1)
    self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div/div[2]/div[3]/div[2]/form/div[3]/div/button").click()
    time.sleep(2)
    try:
        self.driver.find_element_by_partial_link_text(defaultContext).click()
    except:
        pass


def shutdown_browser(self):
    if (hasattr(self, 'driver') and self.driver is not None):
        self.driver.quit()
        self.driver = None


def generate_NAF_string(countryValue, ircsValue, cfrValue, externalMarkingValue, latValue, longValue, speedValue, courseValue, dateValue, timeValue, vesselNameValue):
    # Generate NAF string to send
    nafSource = '//SR//FR/'
    nafSource = nafSource + countryValue
    nafSource = nafSource + "//AD/UVM//TM/POS//RC/"
    nafSource = nafSource + ircsValue
    nafSource = nafSource + "//IR/"
    nafSource = nafSource + cfrValue
    nafSource = nafSource + "//XR/"
    nafSource = nafSource + externalMarkingValue
    nafSource = nafSource + "//LT/"
    nafSource = nafSource + latValue
    nafSource = nafSource + "//LG/"
    nafSource = nafSource + longValue
    nafSource = nafSource + "//SP/"
    nafSource = nafSource + str(speedValue * 10)
    nafSource = nafSource + "//CO/"
    nafSource = nafSource + str(courseValue)
    nafSource = nafSource + "//DA/"
    nafSource = nafSource + dateValue
    nafSource = nafSource + "//TI/"
    nafSource = nafSource + timeValue
    nafSource = nafSource + "//NA/"
    nafSource = nafSource + vesselNameValue
    nafSource = nafSource + "//FS/"
    nafSource = nafSource + countryValue
    nafSource = nafSource + "//ER//"
    return nafSource


def get_target_path():
    # Get correct download path
    if platform.system() == "Windows":
        # Check if environment variable MAVEN_PROJECTBASEDIR exists, if so set correct path otherwise default targetPathWindows
        if "MAVEN_PROJECTBASEDIR" in os.environ:
            localTargetPathWindows = os.environ["MAVEN_PROJECTBASEDIR"] + "\\target"
        else:
            localTargetPathWindows = targetPathWindows
        print("targetPathWindows is: " + localTargetPathWindows)
        return localTargetPathWindows
    else:
        targetPathLinux = os.path.abspath(os.path.dirname(__file__))
        return targetPathLinux


def save_elements_to_file(fileName, dataElementToSave, dateTimeState):
    print('----------------------------')
    # Save path to current dir
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Save current dir (cwd)")
    print(cwd)
    # Change to target folder
    targetPath = get_target_path()
    os.chdir(targetPath)
    print(os.path.abspath(os.path.dirname(__file__)))
    print('Current working dir: ' + targetPath)
    # Check if file exists. If so remove it
    if os.path.exists(fileName):
        os.remove(fileName)
    print('Open file: ' + fileName)
    print('----------------------------')
    # Open csv file and save all elements in list
    iofile = open(fileName, "w")
    with iofile as output:
        writer = csv.writer(output, lineterminator=';') #writer = csv.writer(output, lineterminator='\n')
        # Check if dateTimeState is True or False
        # If True then save the dataElementToSave in data and time format
        if dateTimeState:
            tmpdateTimeToString = datetime.datetime.strftime(dataElementToSave, '%Y')
            writer.writerow([tmpdateTimeToString])
            tmpdateTimeToString = datetime.datetime.strftime(dataElementToSave, '%m')
            writer.writerow([tmpdateTimeToString])
            tmpdateTimeToString = datetime.datetime.strftime(dataElementToSave, '%d')
            writer.writerow([tmpdateTimeToString])
            tmpdateTimeToString = datetime.datetime.strftime(dataElementToSave, '%H')
            writer.writerow([tmpdateTimeToString])
            tmpdateTimeToString = datetime.datetime.strftime(dataElementToSave, '%M')
            writer.writerow([tmpdateTimeToString])
            tmpdateTimeToString = datetime.datetime.strftime(dataElementToSave, '%S')
            writer.writerow([tmpdateTimeToString])
        else:
            for val in dataElementToSave:
                writer.writerow([val])
    iofile.close()
    # Change back the path to current dir
    os.chdir(cwd)
    print(cwd)


def reload_page_and_goto_default(self):
    # Reload page and goto default page
    self.driver.get(httpUnionVMSurlString)


def check_inmarsat_fully_synced(self):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Reload page and goto default page
    reload_page_and_goto_default(self)
    time.sleep(4)
    # Click on Mobile terminal tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(4)
    # Click on new terminal button
    wait_for_element_by_id_to_exist(wait, "mt-btn-create", "mt-btn-create checked")
    time.sleep(1)
    self.driver.find_element_by_id("mt-btn-create").click()
    time.sleep(3)
    # Select Transponder system
    self.driver.find_element_by_id("mt-0-typeAndPlugin").click()
    time.sleep(1)
    elementIsMissing = False
    while True:
        # Test if Inmarsat-C parameters fully synced
        try:
            self.driver.find_element_by_link_text("Inmarsat-C : Thrane&Thrane").click()
        except NoSuchElementException:
            elementIsMissing = True
        # IF elementIsMissing THEN wait and test again ELSE break
        if elementIsMissing:
            # Wait 15 seconds
            time.sleep(15)
            # Reload page
            reload_page_and_goto_default(self)
            time.sleep(5)
            # Click on Mobile terminal tab
            self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
            time.sleep(5)
            # Click on new terminal button
            self.driver.find_element_by_id("mt-btn-create").click()
            time.sleep(3)
            # Select Transponder system
            self.driver.find_element_by_id("mt-0-typeAndPlugin").click()
            time.sleep(1)
            elementIsMissing = False
        else:
            break
    time.sleep(5)


def create_one_new_asset_from_gui(self, vesselNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(5)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Click on new Asset button
    wait_for_element_by_id_to_exist(wait, "asset-btn-create", "uvms-header-menu-item-assets checked 2")
    time.sleep(5)
    self.driver.find_element_by_id("asset-btn-create").click()
    # Select F.S value
    wait_for_element_by_id_to_exist(wait, "asset-input-flagStateCode", "asset-input-flagStateCode checked 3")
    time.sleep(3)
    self.driver.find_element_by_id("asset-input-flagStateCode").click()
    wait_for_element_by_id_to_exist(wait, "asset-input-flagStateCode-item-2", "asset-input-flagStateCode-item-2 checked 4")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-flagStateCode-item-2").click()
    # Enter IRCS value
    wait_for_element_by_id_to_exist(wait, "asset-input-ircs", "asset-input-ircs checked 5")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-ircs").send_keys(ircsValue[vesselNumber])
    # Enter Name value
    self.driver.find_element_by_id("asset-input-name").send_keys(vesselName[vesselNumber])
    # Enter External Marking Value
    self.driver.find_element_by_id("asset-input-externalMarking").send_keys(externalMarkingValue[vesselNumber])
    # Enter CFR Value
    self.driver.find_element_by_id("asset-input-cfr").send_keys(cfrValue[vesselNumber])
    # Enter IMO Value
    self.driver.find_element_by_id("asset-input-imo").send_keys(imoValue[vesselNumber])
    # Enter HomePort Value
    self.driver.find_element_by_id("asset-input-homeport").send_keys(homeportValue[vesselNumber])
    # Select Gear Type value
    wait_for_element_by_id_to_exist(wait, "asset-input-gearType", "asset-input-gearType checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-gearType").click()
    wait_for_element_by_id_to_exist(wait, "asset-input-gearType-item-0", "asset-input-gearType-item-0 checked 7")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-gearType-item-0").click()
    # Enter MMSI Value
    self.driver.find_element_by_id("asset-input-mmsi").send_keys(mmsiValue[vesselNumber])
    # Select License Type value
    self.driver.find_element_by_id("asset-input-licenseType").click()
    wait_for_element_by_id_to_exist(wait, "asset-input-licenseType-item-0", "asset-input-licenseType-item-0 checked 8")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-licenseType-item-0").click()
    # Length Value
    self.driver.find_element_by_id("asset-input-lengthValue").send_keys(lengthValue[vesselNumber])
    # Gross Tonnage Value
    self.driver.find_element_by_id("asset-input-grossTonnage").send_keys(grossTonnageValue[vesselNumber])
    # Main Power Value
    self.driver.find_element_by_id("asset-input-power").send_keys(powerValue[vesselNumber])
    # Main Producer Name Value
    self.driver.find_element_by_id("asset-input-producername").send_keys(producernameValue)
    # Main Producer Code Value
    self.driver.find_element_by_id("asset-input-producercode").send_keys(producercodeValue)
    # Click on the Contacts tab
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    # Click on "Add contact" link
    wait_for_element_by_id_to_exist(wait, "asset-btn-add-contact", "asset-btn-add-contact checked 9")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-add-contact").click()
    # Main Contact Name Value
    wait_for_element_by_id_to_exist(wait, "asset-input-contact-name-0", "asset-input-contact-name-0 checked 10")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-contact-name-0").send_keys(contactNameValue[vesselNumber])
    print(contactNameValue[vesselNumber])
    # Main E-mail Value
    self.driver.find_element_by_id("asset-input-contact-email-0").send_keys(contactEmailValue[vesselNumber])
    # Main Contact Number Value
    self.driver.find_element_by_id("asset-input-contact-number-0").send_keys(contactPhoneNumberValue[vesselNumber])
    # Click on Save Asset button
    wait_for_element_by_id_to_exist(wait, "menu-bar-save", "menu-bar-save checked 11")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-save").click()
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 12")
    time.sleep(3)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def check_new_asset_exists(self, vesselNumber):
    # Set Webdriver wait
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Search for the new created asset in the asset list
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumber])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Check that the new asset exists in the list.
    wait_for_element_by_css_selector_to_exist(wait, "td[title=\"" + vesselName[vesselNumber] + "\"]", "asset-input-simple-search checked 4")
    time.sleep(1)
    self.assertEqual(vesselName[vesselNumber], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[vesselNumber] + "\"]").text)
    # Click on details button for new asset
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 5")
    time.sleep(3)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Check that the F.S value is correct.
    #self.assertEqual(countryValue[vesselNumber], self.driver.find_element_by_id("asset-input-countryCode").text)
    wait_for_element_by_id_to_exist(wait, "asset-input-flagStateCode", "asset-input-flagStateCode checked 6")
    time.sleep(3)
    self.assertEqual(countryValue[vesselNumber], self.driver.find_element_by_id("asset-input-flagStateCode").text)
    # Check that the IRCS value is correct
    self.assertEqual(ircsValue[vesselNumber], self.driver.find_element_by_id("asset-input-ircs").get_attribute("value"))
    # Check that the Name value is correct
    self.assertEqual(vesselName[vesselNumber], self.driver.find_element_by_id("asset-input-name").get_attribute("value"))
    # Check that External Marking Value is correct
    self.assertEqual(externalMarkingValue[vesselNumber], self.driver.find_element_by_id("asset-input-externalMarking").get_attribute("value"))
    # Check that the CFR value is correct
    self.assertEqual(cfrValue[vesselNumber], self.driver.find_element_by_id("asset-input-cfr").get_attribute("value"))
    # Check that the IMO value is correct
    self.assertEqual(imoValue[vesselNumber], self.driver.find_element_by_id("asset-input-imo").get_attribute("value"))
    # Check that the HomePort value is correct
    self.assertEqual(homeportValue[vesselNumber], self.driver.find_element_by_id("asset-input-homeport").get_attribute("value"))
    # Check that the Gear Type value is correct.
    self.assertEqual(gearTypeValue[vesselNumber], self.driver.find_element_by_id("asset-input-gearType").text)
    # Check that the MMSI value is correct
    self.assertEqual(mmsiValue[vesselNumber], self.driver.find_element_by_id("asset-input-mmsi").get_attribute("value"))
    # Check that the License Type value is correct.
    self.assertEqual(licenseTypeValue, self.driver.find_element_by_id("asset-input-licenseType").text)
    # Check that the Length Type value is correct.
    self.assertEqual(lengthValue[vesselNumber], self.driver.find_element_by_id("asset-input-lengthValue").get_attribute("value"))
    # Check that the Gross Tonnage value is correct.
    self.assertEqual(grossTonnageValue[vesselNumber], self.driver.find_element_by_id("asset-input-grossTonnage").get_attribute("value"))
    # Check that the Power value is correct.
    self.assertEqual(powerValue[vesselNumber], self.driver.find_element_by_id("asset-input-power").get_attribute("value"))
    # Check that the Producer Name value is correct.
    #
    # Needs to be updated according to asset database
    #
    #
    # self.assertEqual("Mikael", self.driver.find_element_by_id("asset-input-producername").get_attribute("value"))
    # Check that the Producer Code value is correct.
    self.assertEqual(producercodeValue, self.driver.find_element_by_id("asset-input-producercode").get_attribute("value"))
    # Click on the Contacts tab
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    # Check that the Contact Name value is correct.
    wait_for_element_by_id_to_exist(wait, "asset-input-contact-name-0", "asset-input-contact-name-0 checked 7")
    time.sleep(1)
    self.assertEqual(contactNameValue[vesselNumber], self.driver.find_element_by_id("asset-input-contact-name-0").get_attribute("value"))
    # Check that the E-mail value is correct.
    self.assertEqual(contactEmailValue[vesselNumber], self.driver.find_element_by_id("asset-input-contact-email-0").get_attribute("value"))
    # Check that the E-mail value is correct.
    self.assertEqual(contactPhoneNumberValue[vesselNumber], self.driver.find_element_by_id("asset-input-contact-number-0").get_attribute("value"))
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 8")
    time.sleep(3)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def create_one_new_mobile_terminal_from_gui(self, mobileTerminalNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on mobile terminal tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    # Click on new terminal button
    wait_for_element_by_id_to_exist(wait, "mt-btn-create", "mt-btn-create checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("mt-btn-create").click()
    # Select Transponder system
    wait_for_element_by_id_to_exist(wait, "mt-0-typeAndPlugin", "mt-btn-create checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("mt-0-typeAndPlugin").click()
    # self.driver.find_element_by_link_text("Inmarsat-C : twostage").click()
    wait_for_element_by_link_text_to_exist(wait, "Inmarsat-C : Thrane&Thrane", "Inmarsat-C : Thrane&Thrane checked 4")
    time.sleep(1)
    self.driver.find_element_by_link_text("Inmarsat-C : Thrane&Thrane").click()
    # Enter serial number
    wait_for_element_by_id_to_exist(wait, "mt-0-serialNumber", "mt-0-serialNumber checked 5")
    time.sleep(1)
    self.driver.find_element_by_id("mt-0-serialNumber").send_keys(serialNoValue[mobileTerminalNumber])
    # Enter Transceiver type
    self.driver.find_element_by_id("mt-0-tranciverType").send_keys(transceiverType[mobileTerminalNumber])
    # Enter Software Version
    self.driver.find_element_by_id("mt-0-softwareVersion").send_keys(softwareVersion)
    # Enter Antenna
    self.driver.find_element_by_id("mt-0-antenna").send_keys(antennaVersion)
    # Enter Satellite Number
    self.driver.find_element_by_id("mt-0-satelliteNumber").send_keys(satelliteNumber[mobileTerminalNumber])
    # Enter DNID Number
    self.driver.find_element_by_name("dnid").send_keys(dnidNumber[mobileTerminalNumber])
    # Enter Member Number
    self.driver.find_element_by_name("memberId").send_keys(memberIdnumber[mobileTerminalNumber])
    # Enter Installed by
    self.driver.find_element_by_id("mt-0-channel-0-installedBy").send_keys(installedByName)
    # Expected frequency
    self.driver.find_element_by_id("mt-0-channel-0-frequencyExpected").clear()
    self.driver.find_element_by_id("mt-0-channel-0-frequencyExpected").send_keys(expectedFrequencyHours)
    # Grace period
    self.driver.find_element_by_id("mt-0-channel-0-frequencyGrace").clear()
    self.driver.find_element_by_id("mt-0-channel-0-frequencyGrace").send_keys(gracePeriodFrequencyHours)
    # In port
    self.driver.find_element_by_id("mt-0-channel-0-frequencyPort").clear()
    self.driver.find_element_by_id("mt-0-channel-0-frequencyPort").send_keys(inPortFrequencyHours)
    # Activate Mobile Terminal button
    self.driver.find_element_by_id("mt-0-activation").click()
    # Click on save button
    wait_for_element_by_id_to_exist(wait, "menu-bar-save", "menu-bar-save checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-save").click()
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-save checked 7")
    time.sleep(3)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def check_new_mobile_terminal_exists(self, mobileTerminalNumber):
    # Set Webdriver wait
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Select Mobile Terminal tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    # Enter Serial Number in
    wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[7]", "XPATH checked 2")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(serialNoValue[mobileTerminalNumber])
    # Click in search button
    wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 3")
    time.sleep(1)
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    # Check Serial Number in the list
    wait_for_element_by_xpath_to_exist(wait, "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[3]", "XPATH checked 4")
    time.sleep(1)
    self.assertEqual(serialNoValue[mobileTerminalNumber], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[3]").text)
    # Check Member Number in the list
    self.assertEqual(memberIdnumber[mobileTerminalNumber], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
    # Check DNID Number in the list
    self.assertEqual(dnidNumber[mobileTerminalNumber], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)
    # Click on details button
    wait_for_element_by_xpath_to_exist(wait, "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button", "XPATH checked 5")
    time.sleep(3)
    self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
    # Check Serial Number
    wait_for_element_by_id_to_exist(wait, "mt-0-serialNumber", "mt-0-serialNumber checked 6")
    time.sleep(1)
    self.assertEqual(serialNoValue[mobileTerminalNumber], self.driver.find_element_by_id("mt-0-serialNumber").get_attribute("value"))
    # Check Transceiver Type
    self.assertEqual(transceiverType[mobileTerminalNumber], self.driver.find_element_by_id("mt-0-tranciverType").get_attribute("value"))
    # Check Software Version
    self.assertEqual(softwareVersion, self.driver.find_element_by_id("mt-0-softwareVersion").get_attribute("value"))
    # Check Satellite Number
    self.assertEqual(satelliteNumber[mobileTerminalNumber], self.driver.find_element_by_id("mt-0-satelliteNumber").get_attribute("value"))
    # Check Antenna Version
    self.assertEqual(antennaVersion, self.driver.find_element_by_id("mt-0-antenna").get_attribute("value"))
    # Check DNID Number
    self.assertEqual(dnidNumber[mobileTerminalNumber], self.driver.find_element_by_name("dnid").get_attribute("value"))
    # Check Member Number
    self.assertEqual(memberIdnumber[mobileTerminalNumber], self.driver.find_element_by_name("memberId").get_attribute("value"))
    # Check Installed by Name
    self.assertEqual(installedByName, self.driver.find_element_by_id("mt-0-channel-0-installedBy").get_attribute("value"))
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 7")
    time.sleep(3)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)



def link_asset_and_mobile_terminal(self, mobileTerminalNumber):
    # Set Webdriver wait
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Select Mobile Terminal tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    # Enter Serial Number in field
    wait_for_element_by_id_to_exist(wait, "mt-input-search-serialNumber", "mt-input-search-serialNumber checked 2")
    self.driver.find_element_by_id("mt-input-search-serialNumber").clear()
    self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(serialNoValue[mobileTerminalNumber])
    # Click in search button
    wait_for_element_by_id_to_exist(wait, "mt-btn-advanced-search", "mt-btn-advanced-search checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("mt-btn-advanced-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "mt-toggle-form", "mt-toggle-form checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("mt-toggle-form").click()
    # Click on Link Asset
    wait_for_element_by_id_to_exist(wait, "mt-btn-assign-asset", "mt-toggle-form checked 4")
    time.sleep(1)
    self.driver.find_element_by_id("mt-btn-assign-asset").click()
    # Enter Asset Name and clicks on the search button
    wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[23]", "XPATH checked 5")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//input[@type='text'])[23]").send_keys(ircsValue[mobileTerminalNumber])
    wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 6")
    time.sleep(1)
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    # Click on connect button
    wait_for_element_by_css_selector_to_exist(wait, "td.textAlignRight > button.btn.btn-primary", "td.textAlignRight > button.btn.btn-primary checked 7")
    time.sleep(3)
    self.driver.find_element_by_css_selector("td.textAlignRight > button.btn.btn-primary").click()
    # Click on Link button
    wait_for_element_by_css_selector_to_exist(wait, "div.col-md-6.textAlignRight > button.btn.btn-primary", "div.col-md-6.textAlignRight > button.btn.btn-primary checked 8")
    time.sleep(1)
    self.driver.find_element_by_css_selector("div.col-md-6.textAlignRight > button.btn.btn-primary").click()
    # Enter Reason comment
    wait_for_element_by_name_to_exist(wait, "comment", "NAME comment checked 9")
    time.sleep(1)
    self.driver.find_element_by_name("comment").send_keys("Need to connect this mobile terminal with this asset.")
    # Click on Link button 2
    wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary", "div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary checked 10")
    time.sleep(1)
    self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
    # Close page
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 11")
    time.sleep(3)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)



def generate_NAF_and_verify_position(self,speedValue,courseValue):
    # Set Webdriver wait
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Get Current Date and time in UTC
    currentUTCValue = datetime.datetime.utcnow()
    earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
    earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
    earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
    earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')
    # Generate NAF string to send
    nafSource = '//SR//FR/'
    nafSource = nafSource + countryValue[0]
    nafSource = nafSource + "//AD/UVM//TM/POS//RC/"
    nafSource = nafSource + ircsValue[0]
    nafSource = nafSource + "//IR/"
    nafSource = nafSource + cfrValue[0]
    nafSource = nafSource + "//XR/"
    nafSource = nafSource + externalMarkingValue[0]
    nafSource = nafSource + "//LT/"
    nafSource = nafSource + lolaPositionValues[0][0][0]
    nafSource = nafSource + "//LG/"
    nafSource = nafSource + lolaPositionValues[0][0][1]
    nafSource = nafSource + "//SP/"
    nafSource = nafSource + str(speedValue * 10)
    nafSource = nafSource + "//CO/"
    nafSource = nafSource + str(courseValue)
    nafSource = nafSource + "//DA/"
    nafSource = nafSource + earlierPositionDateValueString
    nafSource = nafSource + "//TI/"
    nafSource = nafSource + earlierPositionTimeValueString
    nafSource = nafSource + "//NA/"
    nafSource = nafSource + vesselName[0]
    nafSource = nafSource + "//FS/"
    nafSource = nafSource + countryValue[0]
    nafSource = nafSource + "//ER//"
    nafSourceURLcoded = urllib.parse.quote_plus(nafSource)
    totalNAFrequest = httpNAFRequestString + nafSourceURLcoded
    print(nafSource)
    # Generate request
    r = requests.get(totalNAFrequest)
    # Check if request is OK (200)
    if r.ok:
        print("200 OK")
    else:
        print("Request NOT OK!")
    # Save current UTC date and time to file (Used in Audit test cases)
    # Set referenceDateTime to current UTC time
    referenceDateTime = datetime.datetime.utcnow()
    # Save referenceDateTime1 to file
    save_elements_to_file(referenceDateTimeFileName[0], referenceDateTime, True)
    # Wait 3 seconds
    time.sleep(3)
    # Select Positions tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-movement", "uvms-header-menu-item-movement checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-movement").click()
    # Enter IRCS for newly created position
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[2]", "XPATH checked 2")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
    wait_for_element_by_link_text_to_exist(wait, linkTextValue, "Link text checked 3")
    time.sleep(1)
    self.driver.find_element_by_link_text(linkTextValue).click()
    wait_for_element_by_xpath_to_exist(wait, "//input[@type='text']", "XPATH checked 4")
    time.sleep(1)
    self.driver.find_element_by_xpath("//input[@type='text']").clear()
    self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
    # Click on search button
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[2]", "XPATH checked 5")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
    # Enter Vessel to verify position data
    wait_for_element_by_css_selector_to_exist(wait, "td[title=\"" + countryValue[0] + "\"]", "CSS selector checked 5")
    time.sleep(1)
    self.assertEqual(countryValue[0], self.driver.find_element_by_css_selector("td[title=\"" + countryValue[0] + "\"]").text)
    self.assertEqual(externalMarkingValue[0], self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue[0] + "\"]").text)
    self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
    self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
    self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[6]").text)
    self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][0] + "\"]").text)
    self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][1] + "\"]").text)
    # Log speed Value Log
    print("td[title=\"" + "%.2f" % speedValue + " kts" + "\"]")
    self.assertEqual("%.2f" % speedValue + " kts", self.driver.find_element_by_css_selector("td[title=\"" + "%.2f" % speedValue + " kts" + "\"]").text)
    self.assertEqual(str(courseValue) + "°", self.driver.find_element_by_css_selector("td[title=\"" + str(courseValue) + "°" + "\"]").text)
    self.assertEqual(sourceValue[0], self.driver.find_element_by_css_selector("td[title=\"" + sourceValue[0] + "\"]").text)
    time.sleep(2)
    return earlierPositionDateTimeValueString



def generate_and_verify_manual_position(self,speedValue,courseValue):
    # Set Webdriver wait
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Select Positions tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-movement", "uvms-header-menu-item-movement checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-movement").click()
    # Click on New manual report
    wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 2")
    time.sleep(1)
    self. driver.find_element_by_xpath("//button[@type='submit']").click()
    # Enter IRCS value
    wait_for_element_by_name_to_exist(wait, "ircs", "NAME ircs checked 3")
    time.sleep(1)
    self.driver.find_element_by_name("ircs").send_keys(ircsValue[0])
    wait_for_element_by_css_selector_to_exist(wait, "strong", "CSS Selector strong checked 4")
    time.sleep(1)
    self.driver.find_element_by_css_selector("strong").click()
    # Get Current Date and time in UTC
    currentUTCValue = datetime.datetime.utcnow()
    earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
    earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:%S')
    self.driver.find_element_by_id("manual-movement-date-picker").clear()
    self.driver.find_element_by_id("manual-movement-date-picker").send_keys(earlierPositionDateTimeValueString)
    # Enter Position, Speed and Course
    self.driver.find_element_by_name("latitude").clear()
    self.driver.find_element_by_name("latitude").send_keys(lolaPositionValues[0][0][0])
    self.driver.find_element_by_name("longitude").clear()
    self.driver.find_element_by_name("longitude").send_keys(lolaPositionValues[0][0][1])
    self.driver.find_element_by_name("measuredSpeed").send_keys(str(speedValue))
    self.driver.find_element_by_name("course").send_keys(str(courseValue))
    # Click on Save Button
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[3]", "XPATH checked 5")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()

    # Save current UTC date and time to file (Used in Audit test cases)
    # Set referenceDateTime to current UTC time
    referenceDateTime = datetime.datetime.utcnow()
    # Save referenceDateTime1 to file
    save_elements_to_file(referenceDateTimeFileName[0], referenceDateTime, True)

    # Click on Confirm button
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[3]", "XPATH checked 6")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
    # Enter IRCS for newly created position
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[2]", "XPATH checked 7")
    time.sleep(5)
    self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
    wait_for_element_by_link_text_to_exist(wait, linkTextValue, "Link text Custom checked 8")
    time.sleep(1)
    self.driver.find_element_by_link_text(linkTextValue).click()
    self.driver.find_element_by_xpath("//input[@type='text']").clear()
    self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
    # Click on search button
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[2]", "XPATH checked 9")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
    # Verifies position data
    wait_for_element_by_css_selector_to_exist(wait, "td[title=\"" + countryValue[0] + "\"]", "CSS Selector checked 10")
    time.sleep(1)
    self.assertEqual(countryValue[0], self.driver.find_element_by_css_selector("td[title=\"" + countryValue[0] + "\"]").text)
    self.assertEqual(externalMarkingValue[0], self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue[0] + "\"]").text)
    self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
    self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
    self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[6]").text)
    self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][0] + "\"]").text)
    self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][1] + "\"]").text)
    # Log speed Value Log
    print("td[title=\"" + "%.2f" % speedValue + " kts" + "\"]")
    self.assertEqual("%.2f" % speedValue + " kts", self.driver.find_element_by_css_selector("td[title=\"" + "%.2f" % speedValue + " kts" + "\"]").text)
    self.assertEqual(str(courseValue) + "°", self.driver.find_element_by_css_selector("td[title=\"" + str(courseValue) + "°" + "\"]").text)
    self.assertEqual(sourceValue[1], self.driver.find_element_by_css_selector("td[title=\"" + sourceValue[1] + "\"]").text)
    time.sleep(2)
    return earlierPositionDateTimeValueString



def get_target_path():
    # Get correct download path
    if platform.system() == "Windows":
        # Check if environment variable MAVEN_PROJECTBASEDIR exists, if so set correct path otherwise default targetPathWindows
        if "MAVEN_PROJECTBASEDIR" in os.environ:
            localTargetPathWindows = os.environ["MAVEN_PROJECTBASEDIR"] + "\\target"
        else:
            localTargetPathWindows = targetPathWindows
        print("targetPathWindows is: " + localTargetPathWindows)
        return localTargetPathWindows
    else:
        targetPathLinux = os.path.abspath(os.path.dirname(__file__))
        return targetPathLinux



def get_test_report_path():
    # Get correct download path
    if platform.system() == "Windows":
        # Check if environment variable MAVEN_PROJECTBASEDIR exists, if so set correct path otherwise default testResultPathWindows
        if "MAVEN_PROJECTBASEDIR" in os.environ:
            localTestResultPathWindows = os.environ["MAVEN_PROJECTBASEDIR"] + "\\target\\failsafe-reports"
        else:
            localTestResultPathWindows = testResultPathWindows
        print("testResultPathWindows is:" + localTestResultPathWindows)
        return localTestResultPathWindows
    else:
        testResultPathLinux = os.path.abspath(os.path.dirname(__file__))
        return testResultPathLinux

if platform.system() == "Windows":
    # Set environment variable HOME to the value of USERPROFILE
    os.environ["HOME"] = os.environ["USERPROFILE"]
    print("Set HOME to: " + os.environ["HOME"])
    # We redefine timeout_decorator on windows
    class timeout_decorator:
        @staticmethod
        def timeout(*args, **kwargs):
            return lambda f: f # return a no-op decorator
else:
    import timeout_decorator


def get_elements_from_file(fileName):
    print('----------------------------')
    # Save path to current dir
    cwd = os.path.abspath(os.path.dirname(__file__))
    # Change to target folder
    targetPath = get_target_path()
    os.chdir(targetPath)
    print(os.path.abspath(os.path.dirname(__file__)))
    print('Current working dir: ' + targetPath)
    print('Open file: ' + fileName)
    print('----------------------------')
    # Open csv file and return all elements in list
    ifile = open(fileName, "rt", encoding="utf8")
    reader = csv.reader(ifile, delimiter=';')
    allRows = ['']
    for row in reader:
        allRows.append(row)
    ifile.close()
    # Deleting empty row
    del allRows[0]
    # Deleting header row
    del allRows[0]
    # Change back the path to current dir
    os.chdir(cwd)
    print(cwd)
    return allRows


def create_asset_from_file(self, assetFileName):
    # Create asset (assetFileName)
    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(assetFileName)
    # create_one_new_asset
    for x in range(0, len(assetAllrows)):
        create_one_new_asset_from_gui_with_parameters(self, assetAllrows[x])


def create_mobileterminal_from_file(self, assetFileName, mobileTerminalFileName):
    # Create Mobile Terminal for mentioned asset (assetFileName, mobileTerminalFileName)

    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(assetFileName)

    # Open saved csv file and read all mobile terminal elements
    mobileTerminalAllrows = get_elements_from_file(mobileTerminalFileName)

    # create_one new mobile terminal for mentioned asset
    for x in range(0, len(assetAllrows)):
        create_one_new_mobile_terminal_via_asset_tab_with_parameters(self, assetAllrows[x][1], mobileTerminalAllrows[x])



def create_one_new_asset_from_gui_with_parameters(self, parameterList):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(4)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Click on new Asset button
    wait_for_element_by_id_to_exist(wait, "asset-btn-create", "asset-btn-create checked 2")
    time.sleep(4)
    self.driver.find_element_by_id("asset-btn-create").click()
    # Select F.S value
    wait_for_element_by_id_to_exist(wait, "asset-input-flagStateCode", "asset-input-flagStateCode checked 3")
    time.sleep(3)
    self.driver.find_element_by_id("asset-input-flagStateCode").click()
    wait_for_element_by_id_to_exist(wait, "asset-input-flagStateCode-item-"+parameterList[17], "asset-input-flagStateCode+parameterList checked 4")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-flagStateCode-item-"+parameterList[17]).click()

    # Enter IRCS value
    wait_for_element_by_id_to_exist(wait, "asset-input-ircs", "asset-input-ircs checked 5")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-ircs").send_keys(parameterList[0])
    # Enter Name value
    self.driver.find_element_by_id("asset-input-name").send_keys(parameterList[1])
    # Enter External Marking Value
    self.driver.find_element_by_id("asset-input-externalMarking").send_keys(parameterList[3])
    # Enter CFR Value
    self.driver.find_element_by_id("asset-input-cfr").send_keys(parameterList[2])
    # Enter IMO Value
    self.driver.find_element_by_id("asset-input-imo").send_keys(parameterList[4])
    # Enter HomePort Value
    self.driver.find_element_by_id("asset-input-homeport").send_keys(parameterList[7])
    # Select Gear Type value
    wait_for_element_by_id_to_exist(wait, "asset-input-gearType", "asset-input-gearType checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-gearType").click()
    wait_for_element_by_id_to_exist(wait, "asset-input-gearType-item-"+parameterList[8], "asset-input-gearType+parameterList checked 7")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-gearType-item-"+parameterList[8]).click()
    # Enter MMSI Value
    self.driver.find_element_by_id("asset-input-mmsi").send_keys(parameterList[5])
    # Select License Type value
    wait_for_element_by_id_to_exist(wait, "asset-input-licenseType", "asset-input-licenseType checked 8")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-licenseType").click()
    wait_for_element_by_id_to_exist(wait, "asset-input-licenseType-item-0", "asset-input-licenseType-item-0 checked 9")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-licenseType-item-0").click()
    # Length Value
    self.driver.find_element_by_id("asset-input-lengthValue").send_keys(parameterList[9])
    # Gross Tonnage Value
    self.driver.find_element_by_id("asset-input-grossTonnage").send_keys(parameterList[10])
    # Main Power Value
    self.driver.find_element_by_id("asset-input-power").send_keys(parameterList[11])
    # Main Producer Name Value
    self.driver.find_element_by_id("asset-input-producername").send_keys(parameterList[12])
    # Main Producer Code Value
    self.driver.find_element_by_id("asset-input-producercode").send_keys(parameterList[13])
    # Click on the Contacts tab
    wait_for_element_by_xpath_to_exist(wait, "//*[@id='CONTACTS']/span", "XPATH checked 11")
    time.sleep(1)
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    # Click on "Add contact" link
    wait_for_element_by_id_to_exist(wait, "asset-btn-add-contact", "asset-btn-add-contact checked 10")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-add-contact").click()
    # Main Contact Name Value
    wait_for_element_by_id_to_exist(wait, "asset-input-contact-name-0", "asset-input-contact-name-0 checked 11")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-contact-name-0").send_keys(parameterList[14])
    # Main E-mail Value
    self.driver.find_element_by_id("asset-input-contact-email-0").send_keys(parameterList[15])
    # Main Contact Number Value
    self.driver.find_element_by_id("asset-input-contact-number-0").send_keys(parameterList[16])
    # Main Street Value
    self.driver.find_element_by_id("asset-input-contact-streetname-0").send_keys(parameterList[18])
    # Main ZIP Value
    self.driver.find_element_by_id("asset-input-contact-zipcode-0").send_keys(parameterList[19])
    # Main City Value
    self.driver.find_element_by_id("asset-input-contact-cityname-0").send_keys(parameterList[20])
    # Main Country Value
    wait_for_element_by_id_to_exist(wait, "asset-input-contact-country-0", "asset-input-contact-country-0 checked 12")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-contact-country-0").click()
    wait_for_element_by_id_to_exist(wait, "asset-input-contact-country-0-item-"+parameterList[21], "asset-input-contact-country-0-item+parameterList checked 13")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-contact-country-0-item-"+parameterList[21]).click()
    # Click on Save Asset button
    wait_for_element_by_id_to_exist(wait, "menu-bar-save", "menu-bar-save checked 14")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-save").click()
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 15")
    time.sleep(5)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def create_one_new_mobile_terminal_via_asset_tab_with_parameters(self, vesselName, parameterRow):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Search for created asset
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName)
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 4")
    time.sleep(4)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Click on add new terminal button
    wait_for_element_by_id_to_exist(wait, "menu-bar-vessel-add-terminal", "menu-bar-vessel-add-terminal checked 5")
    time.sleep(3)
    self.driver.find_element_by_id("menu-bar-vessel-add-terminal").click()
    # Select Transponder system
    wait_for_element_by_id_to_exist(wait, "mt-0-typeAndPlugin", "mt-0-typeAndPlugin checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("mt-0-typeAndPlugin").click()
    wait_for_element_by_link_text_to_exist(wait, "Inmarsat-C : Thrane&Thrane", "Link text checked 7")
    time.sleep(1)
    self.driver.find_element_by_link_text("Inmarsat-C : Thrane&Thrane").click()
    # Enter serial number
    wait_for_element_by_id_to_exist(wait, "mt-0-serialNumber", "mt-0-serialNumber checked 8")
    time.sleep(1)
    self.driver.find_element_by_id("mt-0-serialNumber").send_keys(parameterRow[0])
    # Enter Transceiver type
    self.driver.find_element_by_id("mt-0-tranciverType").send_keys(parameterRow[1])
    # Enter Software Version
    self.driver.find_element_by_id("mt-0-softwareVersion").send_keys(parameterRow[2])
    # Enter Antenna
    self.driver.find_element_by_id("mt-0-antenna").send_keys(parameterRow[3])
    # Enter Satellite Number
    self.driver.find_element_by_id("mt-0-satelliteNumber").send_keys(parameterRow[4])
    # Enter DNID Number
    self.driver.find_element_by_name("dnid").send_keys(parameterRow[5])
    # Enter Member Number
    self.driver.find_element_by_name("memberId").send_keys(parameterRow[6])
    # Enter Installed by
    self.driver.find_element_by_id("mt-0-channel-0-installedBy").send_keys(parameterRow[7])
    # Expected frequency
    self.driver.find_element_by_id("mt-0-channel-0-frequencyExpected").clear()
    self.driver.find_element_by_id("mt-0-channel-0-frequencyExpected").send_keys(parameterRow[8])
    # Grace period
    self.driver.find_element_by_id("mt-0-channel-0-frequencyGrace").clear()
    self.driver.find_element_by_id("mt-0-channel-0-frequencyGrace").send_keys(parameterRow[10])
    # In port
    self.driver.find_element_by_id("mt-0-channel-0-frequencyPort").clear()
    self.driver.find_element_by_id("mt-0-channel-0-frequencyPort").send_keys(parameterRow[12])
    # Activate Mobile Terminal button if parameter is Active=1
    if parameterRow[14] == "1":
       self.driver.find_element_by_id("mt-0-activation").click()
    # Click on save button
    wait_for_element_by_xpath_to_exist(wait, "//*[@id='menu-bar-update']", "XPATH checked 9")
    time.sleep(1)
    self.driver.find_element_by_xpath("//*[@id='menu-bar-update']").click()
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 10")
    time.sleep(3)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def create_trip_from_file(deltaTimeValue, assetFileName, tripFileName):
    # Create Trip for mentioned asset and Mobile Terminal(assetFileName, tripFileName)

    # Set Current Date and time in UTC x hours back
    currentUTCValue = datetime.datetime.utcnow()
    currentPositionTimeValue = currentUTCValue - deltaTimeValue

    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(assetFileName)

    # Open saved csv file and read all trip elements for asset
    assetTripAllrows = get_elements_from_file(tripFileName)

    # create trip for mentioned asset and mobile terminal
    for x in range(0, len(assetAllrows)):
        # create number of position reports for the newly created asset/mobile terminal
        for y in range(0, len(assetTripAllrows)):
            # Create one position report via NAF
            currentPositionTimeValue = currentPositionTimeValue + datetime.timedelta(minutes=int(assetTripAllrows[y][5]))
            currentPositionDateValueString = datetime.datetime.strftime(currentPositionTimeValue, '%Y%m%d')
            currentPositionTimeValueString = datetime.datetime.strftime(currentPositionTimeValue, '%H%M')
            # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
            nafSource = generate_NAF_string(flagStateIndex[int(assetAllrows[x][17])], assetAllrows[x][0], assetAllrows[x][2], assetAllrows[x][3], str("%.3f" % float(assetTripAllrows[y][1])), str("%.3f" % float(assetTripAllrows[y][0])), float(assetTripAllrows[y][3]), assetTripAllrows[y][4], currentPositionDateValueString, currentPositionTimeValueString, assetAllrows[x][1])
            print(nafSource)
            nafSourceURLcoded = urllib.parse.quote_plus(nafSource)
            totalNAFrequest = httpNAFRequestString + nafSourceURLcoded
            # Generate request
            r = requests.get(totalNAFrequest)
            # Check if request is OK (200)
            if r.ok:
                print("200 OK")
            else:
                print("Request NOT OK!")
            # Delay 100ms
            time.sleep(0.1)


def create_report_and_check_trip_position_reports(self, assetFileName, tripFileName):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(assetFileName)
    # Open saved csv file and read all trip elements for asset
    assetTripAllrows = get_elements_from_file(tripFileName)
    # Create a new Report
    # Select Reporting tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-reporting", "uvms-header-menu-item-reporting checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-reporting").click()
    # Click on New Report button
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[18]", "XPATH checked 2")
    time.sleep(3)
    self.driver.find_element_by_xpath("(//button[@type='button'])[18]").click()
    # Enter reporting name (based on 1st ircs name from asset file)
    reportName = "Test (only " + assetAllrows[0][0] +")"
    wait_for_element_by_id_to_exist(wait, "reportName", "reportName checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("reportName").send_keys(reportName)
    # Enter Start and end Date Time
    currentUTCValue = datetime.datetime.utcnow()
    startTimeValue = currentUTCValue - datetime.timedelta(hours=336) # 2 weeks back
    endTimeValue = currentUTCValue + datetime.timedelta(hours=336) # 2 weeks ahead
    self.driver.find_element_by_id("report-start-date-picker").send_keys(startTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    self.driver.find_element_by_id("report-end-date-picker").send_keys(endTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    # Select asset view
    wait_for_element_by_link_text_to_exist(wait, "Select assets", "Link text checked 4")
    time.sleep(2)
    self.driver.find_element_by_link_text("Select assets").click()
    # Enter asset value
    wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[13]", "XPATH checked 5")
    time.sleep(3)
    self.driver.find_element_by_xpath("(//input[@type='text'])[13]").send_keys(assetAllrows[0][0])
    # Select Asset and save
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[27]", "XPATH checked 6")
    time.sleep(5)
    self.driver.find_element_by_xpath("(//button[@type='button'])[27]").click()
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[31]", "XPATH checked 7")
    time.sleep(5)
    self.driver.find_element_by_xpath("(//button[@type='button'])[31]").click()
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[35]", "XPATH checked 8")
    time.sleep(5)
    self.driver.find_element_by_xpath("(//button[@type='button'])[35]").click()
    # Run the new report
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[19]", "XPATH checked 9")
    time.sleep(5)
    self.driver.find_element_by_xpath("(//button[@type='button'])[19]").click()
    # Click on Tabular view icon
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[6]", "XPATH checked 10")
    time.sleep(5)
    self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
    # Click on Date column tab (To sort on Date)
    wait_for_element_by_xpath_to_exist(wait, "//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/thead/tr[3]/th[5]/div", "XPATH checked 11")
    time.sleep(4)
    self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/thead/tr[3]/th[5]/div").click()
    time.sleep(2)
    # Check the 5 first positions for mentioned asset
    for y in range(0, 5):
        self.assertEqual(str("%.3f" % float(assetTripAllrows[y][0])), self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y+1) + "]/td[6]/div").text)
        self.assertEqual(str("%.3f" % float(assetTripAllrows[y][1])), self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y+1) + "]/td[7]/div").text)
        # Special case if speed is zero (No decimals then)
        if float(assetTripAllrows[y][3]) == 0:
            self.assertEqual(assetTripAllrows[y][3] + " kts", self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y+1) + "]/td[9]/div").text)
        else:
            #self.assertEqual(str("%.5f" % float(assetTripAllrows[y][3])) + " kts", self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[9]/div").text)
            # Compare expected value with 5 decimals that only has 4 decimals resolution
            self.assertEqual(str("%.5f" % float(str("%.4f" % float(assetTripAllrows[y][3])))) + " kts", self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y+1) + "]/td[9]/div").text)
        self.assertEqual(assetTripAllrows[y][4] + "°", self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y+1) + "]/td[11]/div").text)
    time.sleep(2)



def wait_for_element_by_id_to_exist(wait, nameOfElement, finallyText):
    # Wait for element
    try:
        element = wait.until(EC.presence_of_element_located((By.ID, nameOfElement)))
    finally:
        print(finallyText)



def wait_for_element_by_link_text_to_exist(wait, nameOfElement, finallyText):
    # Wait for element
    try:
        element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, nameOfElement)))
    finally:
        print(finallyText)



def wait_for_element_by_css_selector_to_exist(wait, nameOfElement, finallyText):
    # Wait for element
    try:
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, nameOfElement)))
    finally:
        print(finallyText)

def wait_for_element_by_xpath_to_exist(wait, nameOfElement, finallyText):
    # Wait for element
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, nameOfElement)))
    finally:
        print(finallyText)



def wait_for_element_by_name_to_exist(wait, nameOfElement, finallyText):
    # Wait for element
    try:
        element = wait.until(EC.presence_of_element_located((By.NAME, nameOfElement)))
    finally:
        print(finallyText)




# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# T E S T    C A S E S
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------



class UnionVMSTestCase(unittest.TestCase):


    def setUp(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)


    def tearDown(self):
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=300)
    def test_0001b_change_default_configuration_parameters(self):
        # The test case changes Default home page to asset and Coordinates format to dd.mmm
        # if Reporting Query List is presented, then close it
        try:
            if self.driver.find_element_by_css_selector("h4.modal-title"):
                self.driver.find_element_by_xpath("//div[@id='map']/div[5]/div/div/div/div/div/i").click()
                time.sleep(2)
        except:
            pass
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Admin tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-audit-log", "uvms-header-menu-item-audit-log checked")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        wait_for_element_by_link_text_to_exist(wait, "CONFIGURATION", "CONFIGURATION checked")
        time.sleep(1)
        self.driver.find_element_by_link_text("CONFIGURATION").click()
        # Click on Global setting subtab under Configuration Tab
        wait_for_element_by_css_selector_to_exist(wait, "#globalSettings > span", "CSS Selector #globalSettings > span checked")
        time.sleep(1)
        self.driver.find_element_by_css_selector("#globalSettings > span").click()
        # Click to change Coordinates format to dd.mmm
        wait_for_element_by_xpath_to_exist(wait, "(//input[@name='coordinateFormat'])[2]", "XPATH checked")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//input[@name='coordinateFormat'])[2]").click()
        # Save current UTC date and time to file (Used in Audit test cases)
        # Set referenceDateTime to current UTC time
        referenceDateTime = datetime.datetime.utcnow()
        # Save referenceDateTime1 to file
        save_elements_to_file(referenceDateTimeFileName[0], referenceDateTime, True)
        # Click to change Default home page to Asset page
        wait_for_element_by_xpath_to_exist(wait, "//button[@id='']", "XPATH checked")
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@id='']").click()
        wait_for_element_by_id_to_exist(wait, "-item-4", "uvms-header-menu-item-audit-log checked")
        time.sleep(1)
        self.driver.find_element_by_id("-item-4").click()
        # Save current UTC date and time to file (Used in Audit test cases)
        # Set referenceDateTime to current UTC time
        referenceDateTime = datetime.datetime.utcnow()
        # Save referenceDateTime1 to file
        save_elements_to_file(referenceDateTimeFileName[1], referenceDateTime, True)
        # Check inmarsat plugin is fully synced
        check_inmarsat_fully_synced(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0002_create_one_new_asset(self):
        # Create new asset (first in the list)
        create_one_new_asset_from_gui(self, 0)


    @timeout_decorator.timeout(seconds=180)
    def test_0003_check_new_asset_exists(self):
        # Check new asset (first in the list)
        check_new_asset_exists(self, 0)


    @timeout_decorator.timeout(seconds=180)
    def test_0004_create_one_new_mobile_terminal(self):
        # Create new Mobile Terminal (first in the list)
        create_one_new_mobile_terminal_from_gui(self, 0)


    @timeout_decorator.timeout(seconds=180)
    def test_0005_check_new_mobile_terminal_exists(self):
        # Check new Mobile Terminal (first in the list)
        check_new_mobile_terminal_exists(self, 0)


    @timeout_decorator.timeout(seconds=180)
    def test_0006_link_asset_and_mobile_terminal(self):
        # Link asset 1 with mobile terminal 1 (first in the list)
        link_asset_and_mobile_terminal(self,0)


    @timeout_decorator.timeout(seconds=180)
    def test_0007_generate_NAF_and_verify_position(self):
        # Create a NAF position and verify the position
        generate_NAF_and_verify_position(self,reportedSpeedValue,reportedCourseValue)


    @timeout_decorator.timeout(seconds=180)
    def test_0008_generate_and_verify_manual_position(self):
        # Create a manual position and verify the position
        generate_and_verify_manual_position(self, reportedSpeedValue, reportedCourseValue)


    @timeout_decorator.timeout(seconds=300)
    def test_0052_create_assets_trip_1_2_3_part1(self):
        # Create assets, Mobile for Trip 1
        create_asset_from_file(self, 'asset1.csv')
        create_mobileterminal_from_file(self, 'asset1.csv', 'mobileterminal1.csv')
        # Create assets, Mobile for Trip 2
        create_asset_from_file(self, 'asset2.csv')
        create_mobileterminal_from_file(self, 'asset2.csv', 'mobileterminal2.csv')
        # Create assets, Mobile for Trip 3
        create_asset_from_file(self, 'asset3.csv')
        create_mobileterminal_from_file(self, 'asset3.csv', 'mobileterminal3.csv')


    @timeout_decorator.timeout(seconds=300)
    def test_0052_create_assets_trip_1_2_3_part2(self):
        # Create Trip 1-3
        create_trip_from_file(datetime.timedelta(hours=14), 'asset1.csv', 'trip1.csv')
        create_trip_from_file(datetime.timedelta(hours=14), 'asset2.csv', 'trip2.csv')
        create_trip_from_file(datetime.timedelta(hours=14), 'asset3.csv', 'trip3.csv')
        time.sleep(1)


    @timeout_decorator.timeout(seconds=300)
    def test_0052b_create_report_and_check_asset_in_reporting_view(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('asset1.csv')
        # Select Reporting tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-reporting", "uvms-header-menu-item-reporting checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-reporting").click()
        # Enter reporting name (based on 1st ircs name from asset file)
        reportName = "Test (only " + assetAllrows[0][0] +")"
        wait_for_element_by_id_to_exist(wait, "reportName", "reportName checked 2")
        time.sleep(5)
        self.driver.find_element_by_id("reportName").send_keys(reportName)
        # Enter Start and end Date Time
        currentUTCValue = datetime.datetime.utcnow()
        startTimeValue = currentUTCValue - datetime.timedelta(hours=336) # 2 weeks back
        endTimeValue = currentUTCValue + datetime.timedelta(hours=336) # 2 weeks ahead
        self.driver.find_element_by_id("report-start-date-picker").send_keys(startTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
        self.driver.find_element_by_id("report-end-date-picker").send_keys(endTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
        # Select asset view
        wait_for_element_by_link_text_to_exist(wait, "Select assets", "Link text checked 3")
        time.sleep(2)
        self.driver.find_element_by_link_text("Select assets").click()
        # Enter asset value
        wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[13]", "XPATH checked 4")
        time.sleep(3)
        self.driver.find_element_by_xpath("(//input[@type='text'])[13]").send_keys(assetAllrows[0][0])
        # Select Asset and save
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[26]", "XPATH checked 5")
        time.sleep(3)
        self.driver.find_element_by_xpath("(//button[@type='button'])[26]").click()
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[30]", "XPATH checked 6")
        time.sleep(3)
        self.driver.find_element_by_xpath("(//button[@type='button'])[30]").click()
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[33]", "XPATH checked 7")
        time.sleep(3)
        self.driver.find_element_by_xpath("(//button[@type='button'])[33]").click()
        # Click on run button to start running the report
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[19]", "XPATH checked 8")
        time.sleep(5)
        self.driver.find_element_by_xpath("(//button[@type='button'])[19]").click()
        # Click on Tabular view icon
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[6]", "XPATH checked 9")
        time.sleep(7)
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        # Click on Tracks tab
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='map']/div[6]/div/div/div/div/div/div[1]/ul/li[3]/a", "XPATH checked 10")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='map']/div[6]/div/div/div/div/div/div[1]/ul/li[3]/a").click()
        time.sleep(2)
        # Check that only one row exist with 1st ircs name from asset file
        # NOTE: Following check is disabled due to howto solved bug UV-379
        #self.assertEqual(assetAllrows[0][0], self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div[3]/div/table/tbody/tr/td[3]/div").text)
        #try:
        #    self.assertFalse(self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div[3]/div/table/tbody/tr[2]/td[3]/div").text)
        #except NoSuchElementException:
        #    pass
        #time.sleep(5)


    @timeout_decorator.timeout(seconds=300)
    def test_0055_create_assets_trip_4_part1(self):
        # Create assets, Mobile for Trip 4
        create_asset_from_file(self, 'asset4.csv')
        create_mobileterminal_from_file(self, 'asset4.csv', 'mobileterminal4.csv')

    @timeout_decorator.timeout(seconds=300)
    def test_0055_create_assets_trip_4_part2(self):
        # Create Trip 4
        create_trip_from_file(datetime.timedelta(hours=14), 'asset4.csv', 'trip4.csv')


    @timeout_decorator.timeout(seconds=300)
    def test_0055b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'asset4.csv', 'trip4.csv')


    @timeout_decorator.timeout(seconds=300)
    def test_0056_create_assets_trip_5_and_6_part1(self):
        # Create assets, Mobile for Trip 5
        create_asset_from_file(self, 'asset5.csv')
        create_mobileterminal_from_file(self, 'asset5.csv', 'mobileterminal5.csv')
        # Create assets, Mobile for Trip 6
        create_asset_from_file(self, 'asset6.csv')
        create_mobileterminal_from_file(self, 'asset6.csv', 'mobileterminal6.csv')

    @timeout_decorator.timeout(seconds=300)
    def test_0056_create_assets_trip_5_and_6_part2(self):
        # Create Trip 5-6
        create_trip_from_file(datetime.timedelta(hours=18), 'asset5.csv', 'trip5.csv')
        create_trip_from_file(datetime.timedelta(hours=7, minutes=40), 'asset6.csv', 'trip6.csv')


    @timeout_decorator.timeout(seconds=300)
    def test_0056b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'asset5.csv', 'trip5.csv')
        reload_page_and_goto_default(self)
        time.sleep(1)
        create_report_and_check_trip_position_reports(self, 'asset6.csv', 'trip6.csv')
        time.sleep(1)


    @timeout_decorator.timeout(seconds=300)
    def test_0057_create_assets_trip_7(self):
        # Create assets, Mobile for Trip 7
        create_asset_from_file(self, 'asset7.csv')
        create_mobileterminal_from_file(self, 'asset7.csv', 'mobileterminal7.csv')
        create_trip_from_file(datetime.timedelta(hours=14), 'asset7.csv', 'trip7.csv')


    @timeout_decorator.timeout(seconds=300)
    def test_0058_create_assets_trip_8(self):
        # Create assets, Mobile for Trip 8
        create_asset_from_file(self, 'asset8.csv')
        create_mobileterminal_from_file(self, 'asset8.csv', 'mobileterminal8.csv')
        create_trip_from_file(datetime.timedelta(hours=6), 'asset8.csv', 'trip8.csv')


    @timeout_decorator.timeout(seconds=300)
    def test_0059_create_assets_trip_9(self):
        # Create assets, Mobile for Trip 9
        create_asset_from_file(self, 'asset9.csv')
        create_mobileterminal_from_file(self, 'asset9.csv', 'mobileterminal9.csv')
        create_trip_from_file(datetime.timedelta(hours=30), 'asset9.csv', 'trip9.csv')



class UnionVMSTestCaseRealTimeMap(unittest.TestCase):


    def setUp(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)


    def tearDown(self):
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0001b_change_default_configuration_parameters(self):
        # Startup browser and login
        UnionVMSTestCase.test_0001b_change_default_configuration_parameters(self)


    @timeout_decorator.timeout(seconds=300)
    def test_0052_0059_create_assets_trip_1_9_without_mobile_terminal(self):
        # Create assets, Mobile for Trip 1
        create_asset_from_file(self, assetFileNameList[0])
        # Create assets, Mobile for Trip 2
        create_asset_from_file(self, assetFileNameList[1])
        # Create assets, Mobile for Trip 3
        create_asset_from_file(self, assetFileNameList[2])
        # Create assets, Mobile for Trip 4
        #create_asset_from_file(self, 'asset4.csv')
        # Create assets, Mobile for Trip 5
        #create_asset_from_file(self, 'asset5.csv')
        # Create assets, Mobile for Trip 6
        #create_asset_from_file(self, 'asset6.csv')
        # Create assets, Mobile for Trip 7
        #create_asset_from_file(self, 'asset7.csv')
        # Create assets, Mobile for Trip 8
        #create_asset_from_file(self, 'asset8.csv')
        # Create assets, Mobile for Trip 9
        #create_asset_from_file(self, 'asset9.csv')
        time.sleep(1)


    @timeout_decorator.timeout(seconds=1000)
    def test_0200a_realtime_search_for_asset_and_click_asset_on_map(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)

        # Set Current Date and time in UTC x hours back
        deltaTimeValue = datetime.timedelta(hours=14)
        currentUTCValue = datetime.datetime.utcnow()
        currentPositionTimeValue = currentUTCValue - deltaTimeValue

        # Create Trip 1-9
        create_trip_from_file(datetime.timedelta(hours=14), assetFileNameList[0], tripFileNameList[0])
        create_trip_from_file(datetime.timedelta(hours=14), assetFileNameList[1], tripFileNameList[1])
        create_trip_from_file(datetime.timedelta(hours=14), assetFileNameList[2], tripFileNameList[2])
        #create_trip_from_file(datetime.timedelta(hours=72), 'asset4.csv', 'trip4.csv')
        #create_trip_from_file(datetime.timedelta(hours=72), 'asset5.csv', 'trip5.csv')
        #create_trip_from_file(datetime.timedelta(hours=61, minutes=40), 'asset6.csv', 'trip6.csv')
        #create_trip_from_file(datetime.timedelta(hours=72), 'asset7.csv', 'trip7.csv')
        #create_trip_from_file(datetime.timedelta(hours=24), 'asset8.csv', 'trip8.csv')
        #create_trip_from_file(datetime.timedelta(hours=48), 'asset9.csv', 'trip9.csv')


        # Wait to secure that the generated trip is finished.
        time.sleep(10)

        # Select Realtime view
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-realtime", "uvms-header-menu-item-realtime checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-realtime").click()
        wait_for_element_by_link_text_to_exist(wait, "Realtime map", "Link text checked 1")
        time.sleep(2)
        self.driver.find_element_by_link_text("Realtime map").click()


        # Activate view on Flags
        wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[3]", "XPATH checked 2")
        time.sleep(0.2)
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[3]").click()
        # Activate view on Names
        wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[5]", "XPATH checked 3")
        time.sleep(0.2)
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[5]").click()
        # Activate view on Speeds
        wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[6]", "XPATH checked 4")
        time.sleep(0.2)
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[6]").click()

        # Click on show control panel
        wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='i'])[1]/following::i[1]", "XPATH checked 5")
        time.sleep(0.2)
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='i'])[1]/following::i[1]").click()

        # Change Cap tracks (min) History value
        wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Cap tracks (min)'])[1]/following::input[1]", "XPATH checked 6")
        time.sleep(1)
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Cap tracks (min)'])[1]/following::input[1]").clear()
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Cap tracks (min)'])[1]/following::input[1]").send_keys(str(capTracksMinValue))
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Cap tracks (min)'])[1]/following::input[1]").send_keys(Keys.ENTER)


        for x in range(0, 3):

            # Print Asset Index Value
            print("Print Asset Index Value: " + str(x))

            # Open saved csv files and read all asset elements
            assetAllrows1 = get_elements_from_file(assetFileNameList[x])

            # Open saved csv files and read all trip elements
            assetTripAllrows1 = get_elements_from_file(tripFileNameList[x])

            print("-----assetAllrows1-----")
            print(assetAllrows1)
            print("-----assetTripAllrows1-----")
            print(assetTripAllrows1)

            # Enter the Asset name in search field
            wait_for_element_by_id_to_exist(wait, "mat-input-0", "mat-input-0 checked 7")
            time.sleep(5)
            self.driver.find_element_by_id("mat-input-0").clear()
            time.sleep(5)
            self.driver.find_element_by_id("mat-input-0").send_keys(assetAllrows1[0][1])

            # Click on the first item in the list to select asset
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::span[1]", "XPATH checked 7")
            time.sleep(2)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::span[1]").click()

            time.sleep(5)

            # Click in the middle of the Map
            print("Execute!")
            elem = self.driver.find_element_by_css_selector("#realtime-map canvas")
            ac = ActionChains(self.driver)
            ac.move_to_element_with_offset(self.driver.find_element_by_tag_name('body'), 0, 0)
            ac.move_to_element(elem).move_by_offset(0, 0).click().perform()
            print("Done!")

            # Check Asset Name
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::span[2]", "XPATH checked 8")
            time.sleep(1)
            self.assertEqual(assetAllrows1[0][1], self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::span[2]").text)

            # Check IRCS
            self.assertEqual(assetAllrows1[0][0], self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Ircs:'])[1]/following::div[1]").text)
            # Check MMSI
            self.assertEqual(assetAllrows1[0][5], self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Mmsi:'])[1]/following::div[1]").text)
            # Check Speed
            self.assertEqual(str("%.2f" % float(assetTripAllrows1[len(assetTripAllrows1)-1][3])), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Speed:'])[1]/following::div[1]").text)
            # Check Course
            self.assertEqual(str("%.2f" % float(assetTripAllrows1[len(assetTripAllrows1)-1][4])), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Heading:'])[1]/following::div[1]").text)
            # Check Flag state
            self.assertEqual(flagStateIndex[int(assetAllrows1[0][17])], self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Flagstate:'])[1]/following::div[1]").text)
            # Check Ext Marking
            self.assertEqual(assetAllrows1[0][3], self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='External marking:'])[1]/following::div[1]").text)
            # Check asset Length
            self.assertEqual(assetAllrows1[0][9], self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Length:'])[1]/following::div[1]").text)
            # Check licenseTypeValue
            self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='LicenceType:'])[1]/following::div[1]").text)
            # Check Producer Name
            self.assertEqual(assetAllrows1[0][12], self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Org. namn:'])[1]/following::div[1]").text)



            # Open Track and Forcast settings
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Mikael'])[1]/following::i[1]", "XPATH checked 9")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Mikael'])[1]/following::i[1]").click()
            time.sleep(2)

            # Activate tracks
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Track'])[1]/following::span[1]", "XPATH checked 10")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Track'])[1]/following::span[1]").click()
            time.sleep(5)

            # Enter the coordinates for the position report
            wait_for_element_by_id_to_exist(wait, "mat-input-0", "mat-input-0 checked 9")
            time.sleep(5)
            self.driver.find_element_by_id("mat-input-0").clear()
            self.driver.find_element_by_id("mat-input-0").send_keys("/c " + assetTripAllrows1[0][1] + " " + assetTripAllrows1[0][0])
            self.driver.find_element_by_id("mat-input-0").send_keys(Keys.ENTER)
            time.sleep(10)

            # Click in the middle of the Map
            print("Execute!")
            elem = self.driver.find_element_by_css_selector("#realtime-map canvas")
            ac = ActionChains(self.driver)
            ac.move_to_element_with_offset(self.driver.find_element_by_tag_name('body'), 0, 0)
            ac.move_to_element(elem).move_by_offset(0, 0).click().perform()
            print("Done!")

            time.sleep(5)

            # Click to expand the track list
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[2]", "XPATH checked 11")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[2]").click()

            # Check position data
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[2]", "XPATH checked 12")
            time.sleep(3)
            self.assertEqual(str("%.5f" % round(float(assetTripAllrows1[0][1]), 3)), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[2]").text)
            self.assertEqual(str("%.5f" % round(float(assetTripAllrows1[0][0]), 3)), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[3]").text)
            self.assertEqual(str("%.2f" % float(assetTripAllrows1[0][4])), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[4]").text)
            self.assertEqual(str("%.2f" % float(assetTripAllrows1[0][3])), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[5]").text)
            currentPositionDateTimeValueString = datetime.datetime.strftime(currentPositionTimeValue, '%Y-%m-%d %H:%M:00')
            self.assertEqual(currentPositionDateTimeValueString, self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[6]").text)
            time.sleep(3)

            # Delete the postion report in the list
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::i[1]", "XPATH checked 13")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::i[1]").click()

            time.sleep(3)

            # Collapse the track list
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[2]", "XPATH checked 14")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[2]").click()

            time.sleep(2)

            # Close Asset info list
            wait_for_element_by_xpath_to_exist(wait,  "(.//*[normalize-space(text()) and normalize-space(.)='" + assetAllrows1[0][1] +  "'])[1]/i[1]", "XPATH checked 15")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='" + assetAllrows1[0][1] +  "'])[1]/i[1]").click()

            time.sleep(5)

        # End pause
        time.sleep(1)



    @timeout_decorator.timeout(seconds=1000)
    def test_0200b_realtime_search_for_asset_and_click_asset_on_map(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)

        # Set Current Date and time in UTC x hours back
        deltaTimeValue = datetime.timedelta(hours=14)
        currentUTCValue = datetime.datetime.utcnow()
        currentPositionTimeValue = currentUTCValue - deltaTimeValue

        # Select Realtime view
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-realtime", "uvms-header-menu-item-realtime checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-realtime").click()
        wait_for_element_by_link_text_to_exist(wait, "Realtime map", "Link text checked 1")
        time.sleep(2)
        self.driver.find_element_by_link_text("Realtime map").click()


        # Activate view on Flags
        wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Flags'])[1]/following::span[1]", "XPATH checked 2")
        time.sleep(0.2)
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Flags'])[1]/following::span[1]").click()
        # Activate view on Names
        wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Names'])[1]/following::span[1]", "XPATH checked 3")
        time.sleep(0.2)
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Names'])[1]/following::span[1]").click()
        # Activate view on Speeds
        wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Speeds'])[1]/following::span[1]", "XPATH checked 4")
        time.sleep(0.2)
        self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Speeds'])[1]/following::span[1]").click()

        # Change Cap tracks (min) History value
        wait_for_element_by_css_selector_to_exist(wait, "input[type=\"number\"]", "CSS Selector checked 3")
        time.sleep(1)
        self.driver.find_element_by_css_selector("input[type=\"number\"]").clear()
        self.driver.find_element_by_css_selector("input[type=\"number\"]").send_keys(str(capTracksMinValue))
        self.driver.find_element_by_css_selector("input[type=\"number\"]").send_keys(Keys.ENTER)

        # Create Trip 1-9
        create_trip_from_file(datetime.timedelta(hours=14), assetFileNameList[0], tripFileNameList[0])
        create_trip_from_file(datetime.timedelta(hours=14), assetFileNameList[1], tripFileNameList[1])
        create_trip_from_file(datetime.timedelta(hours=14), assetFileNameList[2], tripFileNameList[2])
        #create_trip_from_file(datetime.timedelta(hours=72), 'asset4.csv', 'trip4.csv')
        #create_trip_from_file(datetime.timedelta(hours=72), 'asset5.csv', 'trip5.csv')
        #create_trip_from_file(datetime.timedelta(hours=61, minutes=40), 'asset6.csv', 'trip6.csv')
        #create_trip_from_file(datetime.timedelta(hours=72), 'asset7.csv', 'trip7.csv')
        #create_trip_from_file(datetime.timedelta(hours=24), 'asset8.csv', 'trip8.csv')
        #create_trip_from_file(datetime.timedelta(hours=48), 'asset9.csv', 'trip9.csv')

        # Wait to secure that the generated trip is finished.
        time.sleep(10)

        for x in range(0, 2):

            # Print Asset Index Value
            print("Print Asset Index Value: " + str(x))

            # Open saved csv files and read all asset elements
            assetAllrows1 = get_elements_from_file(assetFileNameList[x])

            # Open saved csv files and read all trip elements
            assetTripAllrows1 = get_elements_from_file(tripFileNameList[x])

            print("-----assetAllrows1-----")
            print(assetAllrows1)
            print("-----assetTripAllrows1-----")
            print(assetTripAllrows1)

            # Enter the Asset name in search field
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Search'])[2]/following::input[1]", "XPATH checked 6")
            time.sleep(5)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search'])[2]/following::input[1]").clear()
            time.sleep(5)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search'])[2]/following::input[1]").send_keys(assetAllrows1[0][1])

            # Click on the first item in the list to select asset
            # NOTE: Different xpath for different asset (Strange)
            if x == 0:
                wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Minimize'])[1]/following::span[1]", "XPATH checked 5(1)")
                time.sleep(2)
                self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Minimize'])[1]/following::span[1]").click()
            else:
                wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Minimize'])[1]/following::span[1]", "XPATH checked 5(1)")
                time.sleep(2)
                self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Minimize'])[2]/following::span[1]").click()

            time.sleep(5)

            # Click in the middle of the Map
            print("Execute!")
            elem = self.driver.find_element_by_css_selector("#realtime-map canvas")
            ac = ActionChains(self.driver)
            ac.move_to_element_with_offset(self.driver.find_element_by_tag_name('body'), 0, 0)
            ac.move_to_element(elem).move_by_offset(0, 0).click().perform()
            print("Done!")

            # Check Asset Name
            wait_for_element_by_css_selector_to_exist(wait, "fieldset > div", "CSS Selector checked 6")
            time.sleep(1)
            self.assertEqual(assetAllrows1[0][1], self.driver.find_element_by_css_selector("fieldset > div").text)
            # Check IRCS
            self.assertEqual(assetAllrows1[0][0], self.driver.find_element_by_xpath("//fieldset[2]/div").text)
            # Check MMSI
            self.assertEqual(assetAllrows1[0][5], self.driver.find_element_by_xpath("//fieldset[3]/div").text)
            # Check Speed
            self.assertEqual(str("%.2f" % float(assetTripAllrows1[len(assetTripAllrows1)-1][3])), self.driver.find_element_by_xpath("//fieldset[4]/div").text)
            # Check Course
            self.assertEqual(str("%.2f" % float(assetTripAllrows1[len(assetTripAllrows1)-1][4])), self.driver.find_element_by_xpath("//fieldset[5]/div").text)
            # Check Flag state
            self.assertEqual(flagStateIndex[int(assetAllrows1[0][17])], self.driver.find_element_by_xpath("//fieldset[6]/div").text)
            # Check Ext Marking
            self.assertEqual(assetAllrows1[0][3], self.driver.find_element_by_xpath("//fieldset[7]/div").text)
            # Check asset Length
            self.assertEqual(assetAllrows1[0][9], self.driver.find_element_by_xpath("//fieldset[8]/div").text)
            # Check licenseTypeValue
            self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//fieldset[9]/div").text)
            # Check Producer Name
            self.assertEqual(assetAllrows1[0][12], self.driver.find_element_by_xpath("//fieldset[10]/div").text)

            # Activate tracks
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Track'])[1]/following::span[1]", "XPATH checked 6")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Track'])[1]/following::span[1]").click()
            time.sleep(5)

            # Enter the coordinates for the position report
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Search'])[2]/following::input[1]", "XPATH checked 6")
            time.sleep(5)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search'])[2]/following::input[1]").clear()
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search'])[2]/following::input[1]").send_keys("/c " + assetTripAllrows1[0][1] + " " + assetTripAllrows1[0][0])
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search'])[2]/following::input[1]").send_keys(Keys.ENTER)
            time.sleep(5)

            # Click in the middle of the Map
            print("Execute!")
            elem = self.driver.find_element_by_css_selector("#realtime-map canvas")
            ac = ActionChains(self.driver)
            ac.move_to_element_with_offset(self.driver.find_element_by_tag_name('body'), 0, 0)
            ac.move_to_element(elem).move_by_offset(0, 0).click().perform()
            print("Done!")

            time.sleep(5)

            # Click to expand the track list
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[2]", "XPATH checked 7")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[2]").click()

            # Check position data
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[2]", "XPATH checked 8")
            time.sleep(3)
            self.assertEqual(str("%.5f" % round(float(assetTripAllrows1[0][1]), 3)), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[2]").text)
            self.assertEqual(str("%.5f" % round(float(assetTripAllrows1[0][0]), 3)), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[3]").text)
            self.assertEqual(str("%.2f" % float(assetTripAllrows1[0][4])), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[4]").text)
            self.assertEqual(str("%.2f" % float(assetTripAllrows1[0][3])), self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[5]").text)
            currentPositionDateTimeValueString = datetime.datetime.strftime(currentPositionTimeValue, '%Y-%m-%d %H:%M:00')
            self.assertEqual(currentPositionDateTimeValueString, self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::td[6]").text)
            time.sleep(3)

            # Delete the postion report in the list
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::i[1]", "XPATH checked 9")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Time'])[1]/following::i[1]").click()

            time.sleep(3)

            # Collapse the track list
            wait_for_element_by_xpath_to_exist(wait, "(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[2]", "XPATH checked 10")
            time.sleep(1)
            self.driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='alt + 9'])[1]/following::i[2]").click()

            time.sleep(5)

        # End pause
        time.sleep(1)



if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=get_test_report_path(), verbosity=2),failfast=False, buffer=False, catchbreak=False)
