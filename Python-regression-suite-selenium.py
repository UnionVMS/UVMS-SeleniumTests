import unittest
import time
import timeout_decorator
import os
import datetime
import random
import sys
from unittest.case import _AssertRaisesContext
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
from UnionVMSparameters import *


def externalError(process):
    print("Process '%s' returned code %s" % (process.args, process.returncode))
    # print("Run time: %s " % (time.time() - startTime))
    sys.exit(process.returncode)


def runSubProcess(command, shell, stdout=None):
    process = subprocess.Popen(command, shell=shell, stdout=stdout)
    process.wait()
    if process.returncode != 0:
        externalError(process)
    return process


def resetModuleDatabase():
    moduleDbVersionMap = {#'UVMS-AssetModule-APP': '4.0.8',
                          #'UVMS-ConfigModule-APP': '4.0.6',
                          #'UVMS-AuditModule-APP': '4.0.6',
                          #'UVMS-ExchangeModule-APP': '4.0.9',
                          #'UVMS-MovementModule-APP': '4.0.9',
                          #'UVMS-MobileTerminalModule-APP': '4.0.6',
                          #'UVMS-RulesModule-APP': '3.0.20',
                          #'UVMS-SpatialModule-DB': '1.0.5',
                          #'UVMS-ReportingModule-DB': '1.0.4',
                          #'UVMS-User-APP': '2.0.7',
                          #'UVMS-ActivityModule-APP': '1.0.6',
                          #'UVMS-MDRCacheModule-DB': '0.5.2'
                          }


    modulePrefixDownloadMap = {'UVMS-AssetModule-APP': 'asset-',
                              'UVMS-ConfigModule-APP': 'config-',
                              'UVMS-AuditModule-APP': 'audit-',
                              'UVMS-ExchangeModule-APP': 'exchange-',
                              'UVMS-MovementModule-APP': 'movement-',
                              'UVMS-MobileTerminalModule-APP': 'mobileterminal-',
                              'UVMS-RulesModule-APP': 'rules-',
                              'UVMS-SpatialModule-DB': 'spatial-db-',
                              'UVMS-ReportingModule-DB': 'reporting-db-',
                              'UVMS-User-APP': 'user-',
                              'UVMS-ActivityModule-APP': 'activity-',
                              'UVMS-MDRCacheModule-DB': 'mdr-db-'}
    
    print("Will checkout uvms modules to uvmsCheckoutPath:" + uvmsCheckoutPath )
    distutils.dir_util.mkpath(uvmsCheckoutPath)
    
    for m,v in moduleDbVersionMap.items():
        print( 'Checkout:' + m + " version:" + v)
        distutils.dir_util.mkpath(uvmsCheckoutPath+ "/" + m )
        moduleBasePath = uvmsCheckoutPath+ "/" + m + "/" +m + "-" + modulePrefixDownloadMap.get(m)  +  v 
        print("check dir already exist:" + moduleBasePath)
        if not os.path.isdir(moduleBasePath ):
            print(uvmsGitHubPath +m +  "/archive/"  + modulePrefixDownloadMap.get(m)  +  v  + ".zip")
            url = urllib.request.urlopen(uvmsGitHubPath +m +  "/archive/"  + modulePrefixDownloadMap.get(m)   + v  + ".zip")
            zipfile = ZipFile(BytesIO(url.read()))
            zipfile.extractall(uvmsCheckoutPath+ "/" + m + "/" )
            print("check dir already exist:" + moduleBasePath)
        if os.path.isdir(moduleBasePath ):
            print("execute liquidbase:" + m)
            if os.path.isdir(moduleBasePath + "/LIQUIBASE"):
                os.chdir(moduleBasePath + "/LIQUIBASE")
            if os.path.isdir(moduleBasePath + "/liquibase"):
                os.chdir(moduleBasePath + "/liquibase")         
            print(os.path.abspath(os.path.dirname(__file__)))
            runSubProcess(['mvn', 'liquibase:dropAll', 'liquibase:update', '-P', 'postgres,exec,testdata', dbURLjdbcString], True)
            time.sleep(1)

def populateIridiumImarsatCData():
    try:
        conn = psycopg2.connect(connectToDatabaseString)
        print("Yeeahh I am in!!!")
        cur = conn.cursor()

        # Add rows to mobterm.plugin table
        cur.execute("""SELECT * from mobterm.plugin""")
        rows = cur.fetchall()
        print("\nPrint out of Database " + dbServerName + " (Before):\n")
        for row in rows:
            print(row[0:])
        cur.execute("""INSERT INTO mobterm.plugin VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                    (1050, 'siriusone', 'eu.europa.ec.fisheries.uvms.plugins.iridium.siriusone', 'IRIDIUM', False,
                     'siriusone', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                    (1056, 'Thrane&Thrane', 'eu.europa.ec.fisheries.uvms.plugins.inmarsat', 'INMARSAT_C', False,
                     'Thrane&Thrane', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""SELECT * from mobterm.plugin""")
        rows = cur.fetchall()
        print("\nPrint out of Database " + dbServerName + " (After):\n")
        for row in rows:
            print(row[0:])
        conn.commit()

        # Add rows to mobterm.plugin_capability
        cur.execute("""SELECT * from mobterm.plugin_capability""")
        rows = cur.fetchall()
        print("\nPrint out of Database " + dbServerName + " (Before 2):\n")
        for row in rows:
            print(row[0:])
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1051, 1050, 'CONFIGURABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1052, 1050, 'SAMPLING', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1053, 1050, 'ONLY_SINGLE_OCEAN', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1054, 1050, 'MULTIPLE_OCEAN', 'FALSE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1055, 1050, 'POLLABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1057, 1056, 'ONLY_SINGLE_OCEAN', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1058, 1056, 'POLLABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1059, 1056, 'CONFIGURABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1060, 1056, 'SAMPLING', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1061, 1056, 'MULTIPLE_OCEAN', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""SELECT * from mobterm.plugin_capability""")
        rows = cur.fetchall()
        print("\nPrint out of Database " + dbServerName + " (After 2):\n")
        for row in rows:
            print(row[0:])
        conn.commit()

    except:
        print("I am unable to connect to the database")
    cur.close()
    conn.close()


def populateSanityRuleData():
    try:
        conn = psycopg2.connect(connectToDatabaseString)
        print("Yeeahh I am in!!!")
        cur = conn.cursor()
        cur.execute("""SELECT * from rules.sanityrule""")
        rows = cur.fetchall()
        print("\nPrint out of Database " + dbServerName + " (Before):\n")
        for row in rows:
            print(row[0:])

        cur.execute("""UPDATE rules.sanityrule SET sanityrule_expression = 'mobileTerminalConnectId == null && pluginType != "NAF"' WHERE sanityrule_expression = 'mobileTerminalConnectId == null';""")

        cur.execute("""SELECT * from rules.sanityrule""")
        print("\nPrint out of Database " + dbServerName + " (After):\n")
        rows = cur.fetchall()
        for row in rows:
            print(row[0:])
        conn.commit()


    except:
        print("I am unable to connect to the database")
    cur.close()
    conn.close()


def convertBooleanToZeroOneString(booleanValue):
    if booleanValue:
        return "1"
    else:
        return "0"



def startup_browser_and_login_to_unionVMS(self):
    # Start Chrome browser
    self.driver = webdriver.Chrome()
    # Maximize browser window
    self.driver.maximize_window()
    # Login to test user admin
    #self.driver.get("https://unionvmstest.havochvatten.se/unionvms/")
    #self.driver.implicitly_wait(5)
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


def create_one_new_asset_from_gui(self, vesselNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Click on new Asset button
    wait_for_element_by_id_to_exist(wait, "asset-btn-create", "uvms-header-menu-item-assets checked 2")
    time.sleep(3)
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
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def create_one_new_asset_from_gui_with_parameters(self, parameterList):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Click on new Asset button
    wait_for_element_by_id_to_exist(wait, "asset-btn-create", "asset-btn-create checked 2")
    time.sleep(3)
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
    time.sleep(2)
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
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def create_one_new_mobile_terminal_from_gui_with_parameters(self, parameterRow):
    # Click on mobile terminal tab
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(2)
    # Click on new terminal button
    self.driver.find_element_by_id("mt-btn-create").click()
    time.sleep(3)
    # Select Transponder system
    self.driver.find_element_by_id("mt-0-typeAndPlugin").click()
    time.sleep(1)
    self.driver.find_element_by_link_text("Inmarsat-C : Thrane&Thrane").click()
    time.sleep(1)
    # Enter serial number
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

    # Unmark Poll default setting
    self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/div[4]/div/div[2]/form/fieldset/div/div[3]/div[3]/div/div[2]/div[2]/label").click()

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
    time.sleep(2)
    # Activate Mobile Terminal button
    self.driver.find_element_by_id("mt-0-activation").click()
    time.sleep(5)
    # Click on save button
    self.driver.find_element_by_id("menu-bar-save").click()
    time.sleep(5)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)



def create_one_new_mobile_terminal_via_asset_tab(self, mobileTerminalNumber, vesselNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Search for created asset
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(ircsValue[vesselNumber])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 4")
    time.sleep(1)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Click on add new terminal button
    wait_for_element_by_id_to_exist(wait, "menu-bar-vessel-add-terminal", "menu-bar-vessel-add-terminal checked 5")
    time.sleep(1)
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
    wait_for_element_by_xpath_to_exist(wait, "//*[@id='menu-bar-update']", "XPATH checked 8")
    time.sleep(1)
    self.driver.find_element_by_xpath("//*[@id='menu-bar-update']").click()
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 8")
    time.sleep(2)
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
    time.sleep(1)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Click on add new terminal button
    wait_for_element_by_id_to_exist(wait, "menu-bar-vessel-add-terminal", "menu-bar-vessel-add-terminal checked 5")
    time.sleep(1)
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
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)



def create_one_new_channel_for_one_mobile_terminal(self, channelRow, referenceDateTimeValue):
    # Click on mobile terminal tab
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(2)
    # Search for mobile terminal via serial number
    self.driver.find_element_by_id("mt-input-search-serialNumber").clear()
    self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(channelRow[0])
    self.driver.find_element_by_id("mt-btn-advanced-search").click()
    time.sleep(5)
    # Click on detail button
    self.driver.find_element_by_id("mt-toggle-form").click()
    time.sleep(5)
    # Click on link "Add new channel"
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-addChannel").click()
    time.sleep(2)
    # Enter channel name
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-communicationChannel").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-communicationChannel").send_keys(channelRow[1])
    # Activate Poll if value is "true"
    if channelRow[2] == "1":
        self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-checkbox-polling").click()
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div/div[4]/div/div[2]/form/fieldset/div/div[3]/div[4]/div/div[2]/div[2]/label").click()
    # Activate Config if value is "true"
    if channelRow[3] == "1":
        self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-checkbox-config").click()
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div/div[4]/div/div[2]/form/fieldset/div/div[3]/div[4]/div/div[2]/div[3]/label").click()
    # Activate Default if value is "true"
    if channelRow[4] == "1":
        self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-checkbox-default").click()
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div/div[4]/div/div[2]/form/fieldset/div/div[3]/div[4]/div/div[2]/div[4]/label").click()
    # Enter DNID value
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-dnid").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-dnid").send_keys(channelRow[5])
    # Enter Member Number
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-memberId").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-memberId").send_keys(channelRow[6])
    # Enter Land station
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-lesDescription").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-lesDescription").send_keys(channelRow[7])
    # Enter Start Date/Time based on deltaHourValue from file
    tempTimeValue = referenceDateTimeValue + datetime.timedelta(hours=int(channelRow[8]))
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-started").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-started").send_keys(tempTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    # Enter Stop Date/Time based on deltaHourValue from file
    tempTimeValue = referenceDateTimeValue + datetime.timedelta(hours=int(channelRow[9]))
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-stopped").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-stopped").send_keys(tempTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    # Enter Installer from file
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-installedBy").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-installedBy").send_keys(channelRow[10])
    # Enter Installed Date/Time based on deltaHourValue from file
    tempTimeValue = referenceDateTimeValue + datetime.timedelta(hours=int(channelRow[11]))
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-installedOn").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-installedOn").send_keys(tempTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    # Enter Uninstalled Date/Time based on deltaHourValue from file
    tempTimeValue = referenceDateTimeValue + datetime.timedelta(hours=int(channelRow[12]))
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-uninstalled").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-uninstalled").send_keys(tempTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    # Enter Exp. frequency from file
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyExpected").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyExpected").send_keys(channelRow[13])
    # Enter Grace period from file
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyGrace").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyGrace").send_keys(channelRow[14])
    # Enter In port from file
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyPort").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyPort").send_keys(channelRow[15])

    # Click on Save button
    self.driver.find_element_by_id("menu-bar-update").click()
    time.sleep(2)
    # Enter Comment in comment field
    self.driver.find_element_by_name("comment").clear()
    self.driver.find_element_by_name("comment").send_keys(commentValue)
    time.sleep(1)
    # Click on Update button
    self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
    time.sleep(3)
    # Click on Cancel
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(3)



def create_one_new_channel_for_one_mobile_terminal_without_referenceDateTime(self, channelRow):
    # Click on mobile terminal tab
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(2)
    # Search for mobile terminal via serial number
    self.driver.find_element_by_id("mt-input-search-serialNumber").clear()
    self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(channelRow[0])
    self.driver.find_element_by_id("mt-btn-advanced-search").click()
    time.sleep(5)
    # Click on detail button
    self.driver.find_element_by_id("mt-toggle-form").click()
    time.sleep(5)
    # Click on link "Add new channel"
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-addChannel").click()
    time.sleep(2)
    # Enter channel name
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-communicationChannel").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-communicationChannel").send_keys(channelRow[1])
    # Activate Poll if value is "true"
    #if channelRow[2] == "1":
        #self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-checkbox-polling").click()
        #self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div/div[4]/div/div[2]/form/fieldset/div/div[3]/div[4]/div/div[2]/div[2]/label").click()
    # Activate Config if value is "true"
    #if channelRow[3] == "1":
        #self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-checkbox-config").click()
        #self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div/div[4]/div/div[2]/form/fieldset/div/div[3]/div[4]/div/div[2]/div[3]/label").click()
    # Activate Default if value is "true"
    #if channelRow[4] == "1":
        #self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-checkbox-default").click()
        #self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div/div[4]/div/div[2]/form/fieldset/div/div[3]/div[4]/div/div[2]/div[4]/label").click()
    # Enter DNID value
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-dnid").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-dnid").send_keys(channelRow[5])
    # Enter Member Number
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-memberId").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-memberId").send_keys(channelRow[6])
    # Enter Land station
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-lesDescription").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-lesDescription").send_keys(channelRow[7])
    # Enter Installer from file
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-installedBy").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-installedBy").send_keys(channelRow[10])
    # Enter Exp. frequency from file
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyExpected").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyExpected").send_keys(channelRow[13])
    # Enter Grace period from file
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyGrace").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyGrace").send_keys(channelRow[14])
    # Enter In port from file
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyPort").clear()
    self.driver.find_element_by_id("mt-" + channelRow[16] + "-channel-" + channelRow[17] + "-frequencyPort").send_keys(channelRow[15])

    # Click on Save button
    self.driver.find_element_by_id("menu-bar-update").click()
    time.sleep(2)
    # Enter Comment in comment field
    self.driver.find_element_by_name("comment").clear()
    self.driver.find_element_by_name("comment").send_keys(commentValue)
    time.sleep(1)
    # Click on Update button
    self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
    time.sleep(3)
    # Click on Cancel
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(3)





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
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def check_current_asset_pop_up_history_items(self, vesselNumber):
    # Check the values in the pop up window
    self.assertEqual(countryValue[vesselNumber], self.driver.find_element_by_css_selector("div.historyValues > div.col-md-6 > b").text)
    self.assertEqual(ircsValue[vesselNumber], self.driver.find_element_by_xpath("//div[3]/b").text)
    self.assertEqual(vesselName[vesselNumber], self.driver.find_element_by_xpath("//div[4]/b").text)
    self.assertEqual(imoValue[vesselNumber], self.driver.find_element_by_xpath("//div[7]/b").text)
    self.assertEqual(homeportValue[vesselNumber], self.driver.find_element_by_xpath("//div[8]/b").text)
    self.assertEqual(mmsiValue[vesselNumber], self.driver.find_element_by_xpath("//div[9]/b").text)
    self.assertEqual(licenseValue, self.driver.find_element_by_xpath("//div[10]/b").text)
    self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[11]/b").text)
    self.assertEqual(gearTypeValue[vesselNumber], self.driver.find_element_by_xpath("//div[17]/b").text)
    self.assertEqual(powerValue[vesselNumber] + " kW", self.driver.find_element_by_xpath("//div[19]/b").text)
    self.assertEqual(lengthValue[vesselNumber] + " m LOA", self.driver.find_element_by_xpath("//div[20]/b").text)
    time.sleep(1)


def check_first_contact_in_current_asset_pop_up_history_items(self, vesselNumber):
    # Check the 1st contact values in the pop up window
    self.assertEqual(contactNameValue[vesselNumber], self.driver.find_element_by_css_selector("div.col-md-12 > b").text)
    self.assertEqual(contactEmailValue[vesselNumber], self.driver.find_element_by_xpath("//li/div[2]/b").text)
    self.assertEqual(contactPhoneNumberValue[vesselNumber], self.driver.find_element_by_xpath("//li/div[3]/b").text)



def check_second_contact_in_current_asset_pop_up_history_items(self, vesselNumber):
    # Check the 2nd contact values in the pop up window
    self.assertEqual(contactNameValue[vesselNumber], self.driver.find_element_by_xpath("//li[2]/div/b").text)
    self.assertEqual(contactEmailValue[vesselNumber], self.driver.find_element_by_xpath("//li[2]/div[2]/b").text)
    self.assertEqual(contactPhoneNumberValue[vesselNumber], self.driver.find_element_by_xpath("//li[2]/div[3]/b").text)
    time.sleep(1)


def click_on_selected_asset_history_event(self, numberEvent):
    # Select if the numberEvent is zero (in other words, the 1st in the Asset History Event List
    if numberEvent == 0:
        self.driver.find_element_by_css_selector("td").click()
    else:
        self.driver.find_element_by_xpath("(//tr[@id='asset-btn-history-item']/td)[" + str((numberEvent*2)+1) + "]").click()



def check_asset_history_list(self, vesselNumberList, secondContactVesselNumberList):
    # Set Webdriver wait
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Go through the history for one asset and compare the values towards the asset values controled by the vesselNumberList
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Search for selected asset in the asset list
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumberList[0]])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 4")
    time.sleep(1)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Click on History tab
    wait_for_element_by_css_selector_to_exist(wait, "#HISTORY > span", "CSS Selector checked 5")
    time.sleep(1)
    self.driver.find_element_by_css_selector("#HISTORY > span").click()
    time.sleep(2)
    # Click on and check the items in the History list
    for y in range(len(vesselNumberList)):
        # Click on y-th item in the History list
        click_on_selected_asset_history_event(self, y)
        time.sleep(2)
        # Check the values in the pop up window
        check_current_asset_pop_up_history_items(self, vesselNumberList[y])
        # Check the 1st and 2nd contact info if available
        if secondContactVesselNumberList[y] != 0:
            # Check the second contact info if available
            check_first_contact_in_current_asset_pop_up_history_items(self, secondContactVesselNumberList[y])
            check_second_contact_in_current_asset_pop_up_history_items(self, vesselNumberList[y])
        else:
            check_first_contact_in_current_asset_pop_up_history_items(self, vesselNumberList[y])
        # Close History pop up window
        self.driver.find_element_by_css_selector("div.modal-footer > #asset-btn-close-history").click()
        time.sleep(2)
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)




def modify_one_new_asset_from_gui(self, oldVesselNumber, newVesselNumber):
    # Set Webdriver wait
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Search for selected asset in the asset list
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[oldVesselNumber])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 4")
    time.sleep(3)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Select F.S value
    wait_for_element_by_id_to_exist(wait, "asset-input-flagStateCode", "asset-input-flagStateCode checked 4")
    time.sleep(3)
    self.driver.find_element_by_id("asset-input-flagStateCode").click()
    wait_for_element_by_id_to_exist(wait, "asset-input-flagStateCode-item-1", "asset-input-flagStateCode-item-1 checked 5")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-flagStateCode-item-1").click()
    # Enter IRCS value
    wait_for_element_by_id_to_exist(wait, "asset-input-ircs", "asset-input-ircs checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-ircs").clear()
    self.driver.find_element_by_id("asset-input-ircs").send_keys(ircsValue[newVesselNumber])
    # Enter Name value
    self.driver.find_element_by_id("asset-input-name").clear()
    self.driver.find_element_by_id("asset-input-name").send_keys(vesselName[newVesselNumber])
    # Enter External Marking Value
    self.driver.find_element_by_id("asset-input-externalMarking").clear()
    self.driver.find_element_by_id("asset-input-externalMarking").send_keys(externalMarkingValue[newVesselNumber])
    # Enter CFR Value
    self.driver.find_element_by_id("asset-input-cfr").clear()
    self.driver.find_element_by_id("asset-input-cfr").send_keys(cfrValue[newVesselNumber])
    # Enter IMO Value
    self.driver.find_element_by_id("asset-input-imo").clear()
    self.driver.find_element_by_id("asset-input-imo").send_keys(imoValue[newVesselNumber])
    # Enter HomePort Value
    self.driver.find_element_by_id("asset-input-homeport").clear()
    self.driver.find_element_by_id("asset-input-homeport").send_keys(homeportValue[newVesselNumber])
    # Select Gear Type value
    self.driver.find_element_by_id("asset-input-gearType").click()
    wait_for_element_by_id_to_exist(wait, "asset-input-gearType-item-2", "asset-input-gearType-item-2 checked 4")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-gearType-item-2").click()
    # Enter MMSI Value
    self.driver.find_element_by_id("asset-input-mmsi").clear()
    self.driver.find_element_by_id("asset-input-mmsi").send_keys(mmsiValue[newVesselNumber])
    # Select License Type value
    # Not changed
    # Length Value
    self.driver.find_element_by_id("asset-input-lengthValue").clear()
    self.driver.find_element_by_id("asset-input-lengthValue").send_keys(lengthValue[newVesselNumber])
    # Gross Tonnage Value
    self.driver.find_element_by_id("asset-input-grossTonnage").clear()
    self.driver.find_element_by_id("asset-input-grossTonnage").send_keys(grossTonnageValue[newVesselNumber])
    # Main Power Value
    self.driver.find_element_by_id("asset-input-power").clear()
    self.driver.find_element_by_id("asset-input-power").send_keys(powerValue[newVesselNumber])
    # Main Producer Name Value
    #  self.driver.find_element_by_id("asset-input-producername").send_keys(producernameValue) Should be included when this works
    # Main Producer Code Value
    #  self.driver.find_element_by_id("asset-input-producercode").send_keys(producercodeValue) Should be included when this works
    # Click on the Contacts tab
    wait_for_element_by_xpath_to_exist(wait, "//*[@id='CONTACTS']/span", "XPATH checked 5")
    time.sleep(1)
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    time.sleep(1)
    # Main Contact Name Value
    wait_for_element_by_id_to_exist(wait, "asset-input-contact-name-0", "asset-input-contact-name-0 checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-contact-name-0").clear()
    self.driver.find_element_by_id("asset-input-contact-name-0").send_keys(contactNameValue[newVesselNumber])
    # Main E-mail Value
    self.driver.find_element_by_id("asset-input-contact-email-0").clear()
    self.driver.find_element_by_id("asset-input-contact-email-0").send_keys(contactEmailValue[newVesselNumber])
    # Main Contact Number Value
    self.driver.find_element_by_id("asset-input-contact-number-0").clear()
    self.driver.find_element_by_id("asset-input-contact-number-0").send_keys(contactPhoneNumberValue[newVesselNumber])
    # Click on Save Asset button
    wait_for_element_by_id_to_exist(wait, "menu-bar-update", "menu-bar-update checked 7")
    time.sleep(2)
    self.driver.find_element_by_id("menu-bar-update").click()
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 8")
    time.sleep(2)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def archive_one_asset_from_gui(self, vesselNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Search for selected asset in the asset list
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumber])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 4")
    time.sleep(2)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Click on delete button (Archive)
    wait_for_element_by_id_to_exist(wait, "menu-bar-archive", "menu-bar-archive checked 5")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-archive").click()
    # Add some comment to the asset that shall be archived
    wait_for_element_by_name_to_exist(wait, "comment", "Name checked 6")
    time.sleep(1)
    self.driver.find_element_by_name("comment").send_keys("Archive this asset!")
    # Click on Yes button
    wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 7")
    time.sleep(1)
    self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
    time.sleep(2)


def check_asset_archived(self, vesselNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Search for selected asset in the asset list
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumber])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(5)
    # Check that vessel name is greyed out
    # NOTE: Greyed out state has been removed, so therefore no check.
    #color_value = self.driver.find_element_by_css_selector("td[title=\"" + vesselName[35] + "\"]").value_of_css_property("color")
    #self.assertEqual(greyColorRGBA, color_value)
    #time.sleep(4)
    # Click on details button
    #self.driver.find_element_by_id("asset-toggle-form").click()
    #time.sleep(4)

    # Try to click on details button. Shall not exist.
    try:
        self.driver.find_element_by_id("asset-toggle-form").click()
    except NoSuchElementException:
        pass
    # Try to click on delete (archive) button. Shall not exist.
    #try:
    #    self.assertFalse(self.driver.find_element_by_id("menu-bar-archive").click())
    #except NoSuchElementException:
    #    pass
    time.sleep(2)


def archive_one_mobile_terminal_from_gui(self, mobileTerminalNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on mobile terminal tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    # Enter Serial Number in serial search field
    wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[7]", "XPATH checked 2")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//input[@type='text'])[7]").clear()
    self.driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(serialNoValue[mobileTerminalNumber])
    # Click in search button
    wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 3")
    time.sleep(1)
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "mt-toggle-form", "mt-toggle-form checked 4")
    time.sleep(1)
    self.driver.find_element_by_id("mt-toggle-form").click()
    # Click on archive button
    wait_for_element_by_id_to_exist(wait, "menu-bar-archive", "menu-bar-archive checked 5")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-archive").click()
    # Add some comment to the asset that shall be archived
    wait_for_element_by_name_to_exist(wait, "comment", "Name checked 6")
    time.sleep(1)
    self.driver.find_element_by_name("comment").send_keys("Archive this mobile terminal!")
    # Click on Archive button
    wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary", "CSS Selector checked 7")
    time.sleep(1)
    self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
    time.sleep(2)



def check_mobile_terminal_archived(self, mobileTerminalNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on mobile terminal tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    # Enter Serial Number in serial search field
    wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[7]", "XPATH checked 2")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//input[@type='text'])[7]").clear()
    self.driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(serialNoValue[mobileTerminalNumber])
    # Click in search button
    wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 3")
    time.sleep(1)
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(5)
    # Try to click on details button. Shall not exist.
    try:
        self.driver.find_element_by_id("mt-toggle-form").click()
    except NoSuchElementException:
        pass
    time.sleep(2)




def add_contact_to_existing_asset(self, currentVesselNumber, newVesselNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Search for selected asset in the asset list
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[currentVesselNumber])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 4")
    time.sleep(2)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Click on the Contacts tab
    wait_for_element_by_xpath_to_exist(wait, "//*[@id='CONTACTS']/span", "XPATH checked 5")
    time.sleep(2)
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    # Click on "Add contact" link
    wait_for_element_by_id_to_exist(wait, "asset-btn-add-contact", "asset-btn-add-contact checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-add-contact").click()
    # Add a second contact contactNameValue, contactEmailValue and contactPhoneNumberValue
    wait_for_element_by_id_to_exist(wait, "asset-input-contact-name-0", "asset-input-contact-name-0 checked 7")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-contact-name-0").click()
    self.driver.find_element_by_id("asset-input-contact-name-0").clear()
    self.driver.find_element_by_id("asset-input-contact-name-0").send_keys(contactNameValue[newVesselNumber])
    self.driver.find_element_by_id("asset-input-contact-email-0").clear()
    self.driver.find_element_by_id("asset-input-contact-email-0").send_keys(contactEmailValue[newVesselNumber])
    self.driver.find_element_by_id("asset-input-contact-number-0").clear()
    self.driver.find_element_by_id("asset-input-contact-number-0").send_keys(contactPhoneNumberValue[newVesselNumber])
    wait_for_element_by_id_to_exist(wait, "menu-bar-update", "menu-bar-update checked 8")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-update").click()
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 9")
    time.sleep(2)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def add_notes_to_existing_asset_and_check(self, currentVesselNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Search for selected asset in the asset list
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(2)
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[currentVesselNumber])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    time.sleep(2)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 4")
    time.sleep(1)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Click on the Notes tab
    wait_for_element_by_css_selector_to_exist(wait, "#NOTES > span", "#NOTES > span checked 5")
    time.sleep(2)
    self.driver.find_element_by_css_selector("#NOTES > span").click()
    # Enter note parameters
    # Enter date
    currentUTCValue = datetime.datetime.utcnow()
    startTimeValue = currentUTCValue - datetime.timedelta(hours=336)  # 2 weeks back
    wait_for_element_by_id_to_exist(wait, "asset-input-notesDate", "asset-input-notesDate checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-notesDate").click()
    self.driver.find_element_by_id("asset-input-notesDate").send_keys(startTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    # Select activity EL1
    wait_for_element_by_id_to_exist(wait, "asset-dropdown-notesActivity", "asset-dropdown-notesActivity checked 7")
    time.sleep(1)
    self.driver.find_element_by_id("asset-dropdown-notesActivity").click()
    wait_for_element_by_id_to_exist(wait, "asset-dropdown-notesActivity-item-22", "asset-dropdown-notesActivity-item-22 checked 8")
    time.sleep(1)
    self.driver.find_element_by_id("asset-dropdown-notesActivity-item-22").click()
    # Enter Note User
    wait_for_element_by_id_to_exist(wait, "asset-input-notesUser", "asset-input-notesUser checked 9")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-notesUser").click()
    self.driver.find_element_by_id("asset-input-notesUser").send_keys(noteUser[currentVesselNumber])
    # Enter Ready date
    currentUTCValue = datetime.datetime.utcnow()
    readyTimeValue = currentUTCValue + datetime.timedelta(hours=336)  # 2 weeks ahead
    wait_for_element_by_id_to_exist(wait, "asset-input-notesReadyDate", "asset-input-notesReadyDate checked 10")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-notesReadyDate").click()
    self.driver.find_element_by_id("asset-input-notesReadyDate").send_keys(readyTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    # Enter License Holder
    self.driver.find_element_by_id("asset-input-notesLicenseHolder").clear()
    self.driver.find_element_by_id("asset-input-notesLicenseHolder").send_keys(notesLicenseHolder[currentVesselNumber])
    # Enter Note Contact
    self.driver.find_element_by_id("asset-input-notesContact").clear()
    self.driver.find_element_by_id("asset-input-notesContact").send_keys(notesContact[currentVesselNumber])
    # Enter notes comment
    self.driver.find_element_by_id("asset-input-notesNotes").click()
    self.driver.find_element_by_id("asset-input-notesNotes").send_keys(commentValue)
    # Enter Sheet number
    self.driver.find_element_by_id("asset-input-notesSheetNumber").click()
    self.driver.find_element_by_id("asset-input-notesSheetNumber").send_keys(notesSheetNumber[currentVesselNumber])
    # Click on save button
    wait_for_element_by_id_to_exist(wait, "menu-bar-update", "menu-bar-update checked 11")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-update").click()
    # Leave new asset view
    wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 12")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    # Search for selected asset in the asset list
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 13")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[currentVesselNumber])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 14")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 15")
    time.sleep(1)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Click on the Notes tab
    wait_for_element_by_css_selector_to_exist(wait, "#NOTES > span", "CSS Selector checked 16")
    time.sleep(2)
    self.driver.find_element_by_css_selector("#NOTES > span").click()
    # Click on registered note
    wait_for_element_by_css_selector_to_exist(wait, "td", "CSS Selector checked 17")
    time.sleep(1)
    self.driver.find_element_by_css_selector("td").click()
    # Check parameter values
    wait_for_element_by_css_selector_to_exist(wait, "b", "CSS Selector checked 18")
    time.sleep(1)
    self.assertEqual(startTimeValue.strftime("%Y-%m-%d %H:%M:%S"), self.driver.find_element_by_css_selector("b").text)
    self.assertEqual("EL1", self.driver.find_element_by_xpath("//div[4]/b").text)
    self.assertEqual(noteUser[currentVesselNumber], self.driver.find_element_by_xpath("//div[5]/b").text)
    self.assertEqual(notesLicenseHolder[currentVesselNumber], self.driver.find_element_by_xpath("//div[6]/b").text)
    self.assertEqual(notesContact[currentVesselNumber], self.driver.find_element_by_xpath("//div[7]/b").text)
    self.assertEqual(commentValue, self.driver.find_element_by_css_selector("span > b").text)
    self.assertEqual(readyTimeValue.strftime("%Y-%m-%d %H:%M:%S"), self.driver.find_element_by_xpath("//div[10]/b").text)
    self.assertEqual(notesSheetNumber[currentVesselNumber], self.driver.find_element_by_xpath("//div[11]/b").text)
    time.sleep(1)
    # Click on close button to close popup window
    wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 16")
    time.sleep(1)
    self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
    time.sleep(2)


def check_contacts_to_existing_asset(self, currentVesselNumber, newVesselNumber):
    # Set Webdriver wait
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Click on asset tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(5)
    # Search for selected asset in the asset list
    wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[currentVesselNumber])
    wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    # Click on details button
    wait_for_element_by_id_to_exist(wait, "asset-toggle-form", "asset-toggle-form checked 4")
    time.sleep(1)
    self.driver.find_element_by_id("asset-toggle-form").click()
    # Click on the Contacts tab
    wait_for_element_by_xpath_to_exist(wait, "//*[@id='CONTACTS']/span", "XPATH checked 5")
    time.sleep(1)
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    # Check contacts info
    wait_for_element_by_id_to_exist(wait, "asset-input-contact-name-0", "asset-input-contact-name-0 checked 6")
    time.sleep(1)
    self.assertEqual(contactNameValue[newVesselNumber], self.driver.find_element_by_id("asset-input-contact-name-0").get_attribute("value"))
    self.assertEqual(contactEmailValue[newVesselNumber], self.driver.find_element_by_id("asset-input-contact-email-0").get_attribute("value"))
    self.assertEqual(contactPhoneNumberValue[newVesselNumber], self.driver.find_element_by_id("asset-input-contact-number-0").get_attribute("value"))
    self.assertEqual(contactNameValue[currentVesselNumber], self.driver.find_element_by_id("asset-input-contact-name-1").get_attribute("value"))
    self.assertEqual(contactEmailValue[currentVesselNumber], self.driver.find_element_by_id("asset-input-contact-email-1").get_attribute("value"))
    self.assertEqual(contactPhoneNumberValue[currentVesselNumber], self.driver.find_element_by_id("asset-input-contact-number-1").get_attribute("value"))
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
    time.sleep(1)
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
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)




def getAllColumnValuesforSelectedColumn(stringList, columnValue):
    tmpColumn = []
    for x in range(0, len(stringList)):
        tmpColumn.append(stringList[x][columnValue])
    return tmpColumn



def compareChannelLists(notedList, fileList):
    # Sort both lists
    notedList.sort(key=lambda x: x[0])
    fileList.sort(key=lambda x: x[0])

    # Get all Serial number (1st column) of fileList
    tmpColumn = getAllColumnValuesforSelectedColumn(fileList,0)
    # Remove duplicated values in tmpColumn
    tmpColumn = list(set(tmpColumn))
    # Sort tmpColumn
    tmpColumn.sort()
    # Loop through all Serial numbers in tmpColumn
    totalResultExists = []
    for x in range(0, len(tmpColumn)):
        # Loop through all rows in fileList
        fileListWithOneSerialNumber = []
        for y in range(0, len(fileList)):
            # If current serial number tmpColumn satisfies serial number fileList the add current fileList row to fileListWithOneSerialNumber
            if tmpColumn[x] == fileList[y][0]:
                fileListWithOneSerialNumber.append(fileList[y])
        # Loop through all rows in notedList
        notedListWithOneSerialNumber = []
        for y in range(0, len(notedList)):
            # If current serial number tmpColumn satisfies serial number notedList the add current notedList row to notedListWithOneSerialNumber
            if tmpColumn[x] == notedList[y][0]:
                notedListWithOneSerialNumber.append(notedList[y])
        # Compare the two list notedListWithOneSerialNumber and fileListWithOneSerialNumber. Return a result boolean list
        resultExists = check_sublist_in_other_list_if_it_exists(notedListWithOneSerialNumber, fileListWithOneSerialNumber)
        # Add boolean result to totalResultExists.
        totalResultExists.append(checkAllTrue(resultExists))
    print("compareChannelLists totalResultExists")
    print(totalResultExists)
    return checkAllTrue(totalResultExists)





def check_channel_and_mobile_terminal_data(self, channelAllrows, mobileTerminalAllrows, referenceDateTime):
    # The method check mobile terminal values and all additional channel values are correct presented on screen for all mobile terminals.
    #
    # Create new channel list that includes channel data from mobileTerminalAllrows plus channelAllrows
    channelListPartFromMobileTerminal = get_channel_part_for_one_mobile_terminal_list(mobileTerminalAllrows, pollConfigDefaultValue[0], pollConfigDefaultValue[1], pollConfigDefaultValue[2])
    channelTotalList = get_additional_list_result_from_from_two_channel_lists(channelAllrows, channelListPartFromMobileTerminal)
    # Sort the allrows list (1st Column)
    channelTotalList.sort(key=lambda x: x[0])

    # Click on Mobile Terminal tab
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(5)
    # Sort on linked asset column
    self.driver.find_element_by_id("mt-sort-serialNumber").click()
    time.sleep(1)

    # Read all Mobile Terminal data presented on Mobile Terminal List Tab.
    notedMobileTerminalList = []
    notedChannelsList = []
    for x in range(0, len(mobileTerminalAllrows)):
        # Search for mobile terminal via serial number
        self.driver.find_element_by_id("mt-input-search-serialNumber").clear()
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(mobileTerminalAllrows[x][0])
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(5)
        # Click on detail button
        self.driver.find_element_by_id("mt-toggle-form").click()
        time.sleep(5)
        # Add elements values to notedMobileTerminal list row
        notedMobileTerminal = []
        notedMobileTerminal.append(self.driver.find_element_by_id("mt-0-serialNumber").get_attribute("value"))
        notedMobileTerminal.append(self.driver.find_element_by_id("mt-0-tranciverType").get_attribute("value"))
        notedMobileTerminal.append(self.driver.find_element_by_id("mt-0-softwareVersion").get_attribute("value"))
        notedMobileTerminal.append(self.driver.find_element_by_id("mt-0-antenna").get_attribute("value"))
        notedMobileTerminal.append(self.driver.find_element_by_id("mt-0-satelliteNumber").get_attribute("value"))

        # Add append notedMobileTerminal row to notedMobileTerminalList
        notedMobileTerminalList.append(notedMobileTerminal)

        # Read all channels for current Mobile Terminal
        currentChannel = 0
        elementIsMissing = False
        while True:
            notedChannelRow = []
            # Test if current channel row exist
            try:
                testValue = self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-communicationChannel").get_attribute("value")
            except NoSuchElementException:
                elementIsMissing = True
            # Channel row exist then add channel row to notedChannelRow
            if elementIsMissing:
                break
            else:
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-serialNumber").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-communicationChannel").get_attribute("value"))

                # Get checkbox-polling Value and convert boolean value to zero or one in String type
                notedChannelRow.append(convertBooleanToZeroOneString(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-checkbox-polling").is_selected()))

                # Get checkbox-config Value and convert boolean value to zero or one in String type
                notedChannelRow.append(convertBooleanToZeroOneString(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-checkbox-config").is_selected()))

                # Get checkbox-default Value and convert boolean value to zero or one in String type
                notedChannelRow.append(convertBooleanToZeroOneString(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-checkbox-default").is_selected()))

                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-dnid").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-memberId").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-lesDescription").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-started").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-stopped").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-installedBy").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-installedOn").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-uninstalled").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-frequencyExpected").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-frequencyGrace").get_attribute("value"))
                notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-frequencyPort").get_attribute("value"))

            currentChannel = currentChannel + 1
            notedChannelsList.append(notedChannelRow)
        # Click on cancel button
        self.driver.find_element_by_id("menu-bar-cancel").click()
        time.sleep(2)

    # Sort the notedMobileTerminalList list (1st Column)
    notedMobileTerminalList.sort(key=lambda x: x[0])
    mobileTerminalAllrows.sort(key=lambda x: x[0])
    notedChannelsList.sort(key=lambda x: x[0])

    print("notedChannelsList")
    print(notedChannelsList)

    # Convert hour value in channelTotalList to correct Datetime format and save it in channelTotalListDateTimeFormat. This action makes it easier to compare later with the resultList
    channelTotalListDateTimeFormat = convertHoursValueInListToDateTimeFormat(channelTotalList, referenceDateTime)
    # Remove Mobile Terminal and Channel position data in channelTotalListDateTimeFormat. This action makes it easier to compare later with the resultList
    channelTotalListDateTimeFormatToCompare = removeLastNumberElementsInListRow(channelTotalListDateTimeFormat, 2)

    print("channelTotalListDateTimeFormatToCompare")
    print(channelTotalListDateTimeFormatToCompare)

    # Compare notedChannelsList read from GUI and read channelTotalListDateTimeFormatToCompare from file and return result.
    resultExists = compareChannelLists(notedChannelsList, channelTotalListDateTimeFormatToCompare)
    return resultExists


def add_second_channel_to_mobileterminal(self, mobileTerminalNumber, newMobileTerminalNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Select Mobile Terminal tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    # Enter Serial Number in serial search field
    wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[7]", "XPATH checked 2")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//input[@type='text'])[7]").clear()
    self.driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(serialNoValue[mobileTerminalNumber])
    # Click in search button
    wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 3")
    time.sleep(1)
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    # Click on details button
    wait_for_element_by_xpath_to_exist(wait, "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button", "XPATH checked 4")
    time.sleep(1)
    self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
    # Click on add Channel link
    wait_for_element_by_id_to_exist(wait, "mt-0-addChannel", "mt-0-addChannel checked 5")
    time.sleep(1)
    self.driver.find_element_by_id("mt-0-addChannel").click()
    # Enter 2:nd DNID Number
    wait_for_element_by_id_to_exist(wait, "mt-0-channel-1-dnid", "mt-0-channel-1-dnid checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("mt-0-channel-1-dnid").send_keys(dnidNumber[newMobileTerminalNumber])
    # Enter 2:nd Member Number
    self.driver.find_element_by_id("mt-0-channel-1-memberId").send_keys(memberIdnumber[mobileTerminalNumber])
    # Enter Installed by
    self.driver.find_element_by_id("mt-0-channel-1-installedBy").send_keys(installedByName)
    # Expected frequency
    self.driver.find_element_by_id("mt-0-channel-1-frequencyExpected").send_keys(expectedFrequencyHours)
    # Grace period
    self.driver.find_element_by_id("mt-0-channel-1-frequencyGrace").send_keys(gracePeriodFrequencyHours)
    # In port
    self.driver.find_element_by_id("mt-0-channel-1-frequencyPort").send_keys(inPortFrequencyHours)
    # Click on save button
    wait_for_element_by_id_to_exist(wait, "menu-bar-update", "menu-bar-update checked 7")
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-update").click()
    # Enter comment in the comment field
    wait_for_element_by_name_to_exist(wait, "comment", "Name checked 7")
    time.sleep(1)
    self.driver.find_element_by_name("comment").send_keys("comment")
    # Click on update button
    wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary", "CSS Selector checked 8")
    time.sleep(1)
    self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
    # Click on cancel button
    wait_for_element_by_id_to_exist(wait, "menu-bar-update", "menu-bar-cancel checked 9")
    time.sleep(1)
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
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def link_asset_and_mobile_terminal_with_parameters(self, mobileTerminalparameterRow, ircsOrCfrValue):
    # Select Mobile Terminal tab
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(2)
    # Enter Serial Number in field
    self.driver.find_element_by_id("mt-input-search-serialNumber").clear()
    self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(mobileTerminalparameterRow[0])
    # Click in search button
    self.driver.find_element_by_id("mt-btn-advanced-search").click()
    time.sleep(5)
    # Click on details button
    self.driver.find_element_by_id("mt-toggle-form").click()
    time.sleep(3)
    # Click on Link Asset
    self.driver.find_element_by_id("mt-btn-assign-asset").click()
    time.sleep(2)
    # Enter Asset Name and clicks on the search button
    self.driver.find_element_by_xpath("(//input[@type='text'])[23]").send_keys(ircsOrCfrValue)
    time.sleep(2)
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(3)
    # Click on connect button
    self.driver.find_element_by_css_selector("td.textAlignRight > button.btn.btn-primary").click()
    # Click on Link button
    time.sleep(2)
    self.driver.find_element_by_css_selector("div.col-md-6.textAlignRight > button.btn.btn-primary").click()
    # Enter Reason comment
    self.driver.find_element_by_name("comment").send_keys("Need to connect this mobile terminal with this asset.")
    time.sleep(2)
    # Click on Link button 2
    self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
    time.sleep(2)
    # Close page
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)



def change_and_check_speed_format(self,unitNumber):
    # Set wait time for web driver
    wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
    # Select Admin tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-audit-log", "uvms-header-menu-item-audit-log checked 1")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
    time.sleep(1)
    wait_for_element_by_link_text_to_exist(wait, "CONFIGURATION", "Link text checked 2")
    time.sleep(1)
    self.driver.find_element_by_link_text("CONFIGURATION").click()
    # Click on Global setting subtab under Configuration Tab
    wait_for_element_by_css_selector_to_exist(wait, "#globalSettings > span", "CSS Selector checked 3")
    time.sleep(3)
    self.driver.find_element_by_css_selector("#globalSettings > span").click()
    # Set Speed format to knots
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[4]", "XPATH checked 4")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
    wait_for_element_by_link_text_to_exist(wait, speedUnitTypesInText[unitNumber], "Link text checked 5")
    time.sleep(1)
    self.driver.find_element_by_link_text(speedUnitTypesInText[unitNumber]).click()
    # Click on Position Tab to check correct speed unit
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-movement", "uvms-header-menu-item-movement checked 6")
    time.sleep(1)
    self.driver.find_element_by_id("uvms-header-menu-item-movement").click()
    # Select Custom mode
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[2]", "XPATH checked 7")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
    wait_for_element_by_link_text_to_exist(wait, linkTextValue, "Link text checked 8")
    time.sleep(1)
    self.driver.find_element_by_link_text(linkTextValue).click()
    # Click on search button
    wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[2]", "XPATH checked 8")
    time.sleep(1)
    self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
    wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[11]", "XPATH checked 9")
    time.sleep(1)
    currentSpeedValue = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[11]").text
    print("Current: " +  currentSpeedValue + " Short Unit: " + speedUnitTypesShort[unitNumber])
    if currentSpeedValue.find(speedUnitTypesShort[unitNumber]) == -1:
        foundCorrectUnit = False
    else:
        foundCorrectUnit = True
    self.assertTrue(foundCorrectUnit)
    time.sleep(2)


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


def read_all_channels_for_selected_Mobile_Terminal(self):

    # Read all channels for selected Mobile Terminal
    notedChannelsList = []
    currentChannel = 0
    elementIsMissing = False
    while True:
        notedChannelRow = []
        # Test if current channel row exist
        try:
            testValue = self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-communicationChannel").get_attribute("value")
        except NoSuchElementException:
            elementIsMissing = True
        # Channel row exist then add channel row to notedChannelRow
        if elementIsMissing:
            break
        else:
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-serialNumber").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-communicationChannel").get_attribute("value"))

            # Get checkbox-polling Value and convert boolean value to zero or one in String type
            notedChannelRow.append(convertBooleanToZeroOneString(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-checkbox-polling").is_selected()))

            # Get checkbox-config Value and convert boolean value to zero or one in String type
            notedChannelRow.append(convertBooleanToZeroOneString(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-checkbox-config").is_selected()))

            # Get checkbox-default Value and convert boolean value to zero or one in String type
            notedChannelRow.append(convertBooleanToZeroOneString(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-checkbox-default").is_selected()))

            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-dnid").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-memberId").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-lesDescription").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-started").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-stopped").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-installedBy").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-installedOn").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-uninstalled").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-frequencyExpected").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-frequencyGrace").get_attribute("value"))
            notedChannelRow.append(self.driver.find_element_by_id("mt-0-channel-" + str(currentChannel) + "-frequencyPort").get_attribute("value"))
        currentChannel = currentChannel + 1
        notedChannelsList.append(notedChannelRow)
    return notedChannelsList


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

    # Select Positions tab
    wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-movement", "uvms-header-menu-item-movement checked 1")
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



def get_elements_from_file_without_deleting_paths_and_rows(fileName):
    # Open csv file and return all elements in list
    ifile = open(fileName, "rt", encoding="utf8")
    reader = csv.reader(ifile, delimiter=';')
    allRows = ['']
    for row in reader:
        allRows.append(row)
    ifile.close()
    # Deleting empty row
    del allRows[0]
    # Change back the path to current dir
    return allRows


def get_reference_date_time_from_file(referenceDateTimeFileName):
    # Open saved csv file and read saved referenceDateTime elements
    referenceDateTimeElementsFromFile = get_elements_from_file_without_deleting_paths_and_rows(referenceDateTimeFileName)

    print(referenceDateTimeElementsFromFile)

    yearValue = int(referenceDateTimeElementsFromFile[0][0])
    monthValue = int(referenceDateTimeElementsFromFile[0][1])
    dayValue = int(referenceDateTimeElementsFromFile[0][2])
    hourValue = int(referenceDateTimeElementsFromFile[0][3])
    minuteValue = int(referenceDateTimeElementsFromFile[0][4])
    secondValue = int(referenceDateTimeElementsFromFile[0][5])

    print("------------------------------------------------")
    print(yearValue)
    print("------------------------------------------------")
    print(monthValue)
    print("------------------------------------------------")
    print(dayValue)
    print("------------------------------------------------")
    print(hourValue)
    print("------------------------------------------------")
    print(minuteValue)
    print("------------------------------------------------")
    print(secondValue)

    # Set referenceDateTime to value based from referenceDateTimeElementsFromFile
    referenceDateTime = datetime.datetime(year=yearValue, month=monthValue, day=dayValue, hour=hourValue, minute=minuteValue, second=secondValue)

    return referenceDateTime




def adapt_asset_list_to_exported_CSV_file_standard(originAssetList):
    # Adapt originAssetList list to the "format" as for exported CSV files
    # The result is saved in newAssetListCSVformat
    newAssetListCSVformat = []
    for y in range(len(originAssetList)):
        # Building up one row in the list
        row = [flagStateIndex[int(originAssetList[y][17])], originAssetList[y][3], originAssetList[y][1], originAssetList[y][0], originAssetList[y][2], gearTypeIndex[int(originAssetList[y][8])], licenseTypeValue, '']
        newAssetListCSVformat.append(row)
    return newAssetListCSVformat


def adapt_mobile_terminal_list_to_exported_CSV_file_standard(originMobileTerminalList, originAssetList, linkAssetMobileTerminalList):
    # Adapt originMobileTerminalList list to the "format" as for exported CSV files
    # The result is saved in newMobileTerminalListCSVformat
    newMobileTerminalListCSVformat = []
    for y in range(len(originMobileTerminalList)):
        # Get CFR Value based on Link list between assets and mobile terminals
        tempCFRValue = get_asset_cfr_via_link_list(linkAssetMobileTerminalList, originMobileTerminalList[y][0])
        # Get asset name based on CFR value found in assetAllrows list
        tempAssetName = get_selected_asset_column_value_based_on_cfr(originAssetList, tempCFRValue, 1)
        # Get asset name based on CFR value found in assetAllrows list
        tempMMSIValue = get_selected_asset_column_value_based_on_cfr(originAssetList, tempCFRValue, 5)
        # Building up one row in the list
        row = [tempAssetName, originMobileTerminalList[y][0], originMobileTerminalList[y][6], originMobileTerminalList[y][5], transponderType[1], originMobileTerminalList[y][4], tempMMSIValue, statusValue[1]]
        newMobileTerminalListCSVformat.append(row)
    return newMobileTerminalListCSVformat



def check_sublist_in_other_list_if_it_exists(subAssetList, fullAssetList):
    # Check subAssetList in fullAssetList row by row
    # Returns a new list consists of booleans values
    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
    resultExists = []
    for y in range(0, len(subAssetList)):
        foundRow = False;
        for x in range(0, len(fullAssetList)):
            print("Compare list row " + str(y) + "---" + str(x))
            print(subAssetList[y])
            print(fullAssetList[x])
            if compare(fullAssetList[x], subAssetList[y]):
                print("Compared equal")
                foundRow = True;
        resultExists.append(foundRow)
    return resultExists


def checkAllTrue(booleanList):
    # Return True if All values in list are True, else False.
    for x in range(0, len(booleanList)):
        if not booleanList[x]:
            return False
    return True


def checkAnyTrue(booleanList):
    # Return True if Any values in list are True, else False.
    for x in range(0, len(booleanList)):
        if booleanList[x]:
            return True
    return False



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



def create_mobileterminal_from_file_based_on_link_file(self, assetFileName, mobileTerminalFileName, linkFileName):
    # Create Mobile Terminal based on linkFile, assetFile and mobileTerminalFile (assetFileName, mobileTerminalFileName)

    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(assetFileName)

    # Open saved csv file and read all mobile terminal elements
    mobileTerminalAllrows = get_elements_from_file(mobileTerminalFileName)

    # Open saved csv file and read all linked elements between assets and mobile terminals
    linkAssetMobileTerminalAllrows = get_elements_from_file(linkFileName)

    # create_one new mobile terminal for mentioned asset
    for x in range(0, len(linkAssetMobileTerminalAllrows)):
        assetVesselName = get_selected_asset_column_value_based_on_cfr(assetAllrows, linkAssetMobileTerminalAllrows[x][1], 1)
        mobileTerminalRowValue = get_selected_Mobile_terminal_row_based_on_serialNumber(mobileTerminalAllrows, linkAssetMobileTerminalAllrows[x][0])
        create_one_new_mobile_terminal_via_asset_tab_with_parameters(self, assetVesselName, mobileTerminalRowValue)




def create_mobileterminal_from_file_based_on_link_file_without_assetfilename(self, mobileTerminalFileName, linkFileName):
    # Create Mobile Terminal based on linkFile and mobileTerminalFile (mobileTerminalFileName, linkFileName)

    # Open saved csv file and read all mobile terminal elements
    mobileTerminalAllrows = get_elements_from_file(mobileTerminalFileName)

    # Open saved csv file and read all linked elements between assets and mobile terminals
    linkAssetMobileTerminalAllrows = get_elements_from_file(linkFileName)

    # create_one new mobile terminal for mentioned asset
    for x in range(0, len(linkAssetMobileTerminalAllrows)):
        print("-----------------------")
        print(x)
        print(linkAssetMobileTerminalAllrows[x][1])
        print("-----------------------")
        mobileTerminalRowValue = get_selected_Mobile_terminal_row_based_on_serialNumber(mobileTerminalAllrows, linkAssetMobileTerminalAllrows[x][0])
        create_one_new_mobile_terminal_from_gui_with_parameters(self, mobileTerminalRowValue)
        link_asset_and_mobile_terminal_with_parameters(self, mobileTerminalRowValue, linkAssetMobileTerminalAllrows[x][1])




def create_addtional_channels_for_mobileterminals_from_file(self, channelFileName, referenceDateTime):
    # Create addtional channels for Mobile Terminals from file based on channelFile

    # Open saved csv file and read all asset elements
    channelAllrows = get_elements_from_file(channelFileName)

    # create_one new channel for mentioned mobile terminal
    for x in range(0, len(channelAllrows)):
        create_one_new_channel_for_one_mobile_terminal(self, channelAllrows[x], referenceDateTime)



def create_addtional_channels_for_mobileterminals_without_referenceDateTime_from_file(self, channelFileName):
    # Create addtional channels for Mobile Terminals from file based on channelFile

    # Open saved csv file and read all asset elements
    channelAllrows = get_elements_from_file(channelFileName)

    # create_one new channel for mentioned mobile terminal
    for x in range(0, len(channelAllrows)):
        print("-----------------------")
        print(x)
        print(channelAllrows[x][0])
        print("-----------------------")
        create_one_new_channel_for_one_mobile_terminal_without_referenceDateTime(self, channelAllrows[x])





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
    time.sleep(1)
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


def get_selected_elements_in_list_from_mainList(assetAllrows, assetListIndexNumber, selectionValue):
    # Get a new asset List based on selected selection value
    assetList = []
    for x in range(0, len(assetAllrows)):
        if selectionValue in assetAllrows[x][assetListIndexNumber]:
            assetList.append(assetAllrows[x])
    return assetList


def get_selected_assets_from_assetList_interval(assetAllrows, assetListIndexNumber, intervalValueLow, intervalValueHigh):
    # Get a new asset List based on selected selection value
    assetList = []
    for x in range(0, len(assetAllrows)):
        if (float(assetAllrows[x][assetListIndexNumber]) >= intervalValueLow) and (float(assetAllrows[x][assetListIndexNumber]) < intervalValueHigh) :
                assetList.append(assetAllrows[x])
    return assetList


def get_remaining_elements_from_main_list(mainListAll, smallList):
    # Get a new remaining asset List based on asset list assetListAll and assetListSmall
    # Define compare rule
    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
    remainList = mainListAll.copy()
    for y in range(0, len(smallList)):
        for x in range(0, len(mainListAll)):
            if not compare(mainListAll[x], smallList[y]):
                try:
                    remainList.remove(smallList[y])
                except:
                    pass
    return remainList


def get_asset_info_from_asset_database(assetCFRValue):
    # Get detailed info about selected asset from asset database Fartyg 2
    client = zeep.Client(wsdl=httpNationalServiceEndpointString)
    answerValue = client.service.getVesselByCFR(assetCFRValue)
    return answerValue


def get_asset_cfr_via_link_list(linkList, serialNumber):
    # Returns corresponding cfr value based on selected SerialNumber and LinkList
    for x in range(0, len(linkList)):
        if serialNumber in linkList[x][0]:
            return linkList[x][1]
    return ""


def get_selected_asset_column_value_based_on_cfr(assetList, cfrValue, columnValue):
    # Returns asset column value where cfrValue satisfies the asset cfr column list
    for x in range(0, len(assetList)):
        if cfrValue in assetList[x][2]:
            return assetList[x][columnValue]
    return ""


def get_selected_Mobile_terminal_row_based_on_serialNumber(mobileTerminalList, serialNumberValue):
    # Returns mobile terminal row where serialNumber value satisfies the mobile terminal serialNumber column list
    for x in range(0, len(mobileTerminalList)):
        if serialNumberValue in mobileTerminalList[x][0]:
            return mobileTerminalList[x]
    return []


def get_channel_part_for_one_mobile_terminal_list(mobileTerminalList, pollValue, configValue, defaultValue):
    # Returns the channel values from the mobile terminal list
    channelListPart = []
    for x in range(0, len(mobileTerminalList)):
        # Create one channel row from the mobile terminal list
        tempChannelPartRow = [mobileTerminalList[x][0], channelDefaultName, pollValue, configValue, defaultValue, mobileTerminalList[x][5], mobileTerminalList[x][6], mobileTerminalList[x][15], mobileTerminalList[x][16], mobileTerminalList[x][17], mobileTerminalList[x][18], mobileTerminalList[x][19], mobileTerminalList[x][20], mobileTerminalList[x][8], mobileTerminalList[x][10], mobileTerminalList[x][12], mobileTerminalList[x][21], mobileTerminalList[x][22]]
        channelListPart.append(tempChannelPartRow)
    return channelListPart


def get_additional_list_result_from_from_two_channel_lists(list1, list2):
    # Return the total sum of list1 and list2
    channelTotalList = list1.copy()
    for x in range(0, len(list2)):
        channelTotalList.append(list2[x])
    return channelTotalList


def removeChar(stringValue, charValue):
    # Return new string where the charValue is removed from stringValue
    return stringValue.replace(charValue, "")


def convertHoursValueInListToDateTimeFormat(channelList, referenceDateTimeValue):
    # Convert the time coloumn fields with Hour values as is the base in the read CSV files.
    newChannelList = copy.deepcopy(channelList)
    for x in range(0, len(newChannelList)):
        if newChannelList[x][8] == "0":
            newChannelList[x][8] = ""
        else:
            tempTimeValue = referenceDateTimeValue + datetime.timedelta(hours=int(newChannelList[x][8]))
            newChannelList[x][8] = tempTimeValue.strftime("%Y-%m-%d %H:%M:%S")

        if newChannelList[x][9] == "0":
            newChannelList[x][9] = ""
        else:
            tempTimeValue = referenceDateTimeValue + datetime.timedelta(hours=int(newChannelList[x][9]))
            newChannelList[x][9] = tempTimeValue.strftime("%Y-%m-%d %H:%M:%S")

        if newChannelList[x][11] == "0":
            newChannelList[x][11] = ""
        else:
            tempTimeValue = referenceDateTimeValue + datetime.timedelta(hours=int(newChannelList[x][11]))
            newChannelList[x][11] = tempTimeValue.strftime("%Y-%m-%d %H:%M:%S")

        if newChannelList[x][12] == "0":
            newChannelList[x][12] = ""
        else:
            tempTimeValue = referenceDateTimeValue + datetime.timedelta(hours=int(newChannelList[x][12]))
            newChannelList[x][12] = tempTimeValue.strftime("%Y-%m-%d %H:%M:%S")
    return newChannelList


def removeLastNumberElementsInListRow(channelList,numberValue):
    # Delete numberValue of elements last in a list row.
    newChannelList = copy.deepcopy(channelList)
    for x in range(0, len(newChannelList)):
        # Create a temp row of current newChannelList row
        tmpRow = newChannelList[x]
        # Remove the last element in the temp row
        newChannelList[x] = tmpRow[:-numberValue]
    return newChannelList



def reload_page_and_goto_default(self):
    # Reload page and goto default page
    self.driver.get(httpUnionVMSurlString)


def check_inmarsat_fully_synced(self):
    # Reload page and goto default page
    reload_page_and_goto_default(self)
    time.sleep(4)
    # Click on Mobile terminal tab
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(4)
    # Click on new terminal button
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


def get_download_path():
    # Get correct download path
    if platform.system() == "Windows":
        home = expanduser("~")
        return home + downloadPathWindow
    else:
        return downloadPathLinux



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


class UnionVMSTestCaseInit(unittest.TestCase):

    @timeout_decorator.timeout(seconds=1000)
    def test_0001_reset_database_union_vms(self):
        # Create Browser
        #self.driver = webdriver.Chrome()
        # Save current default dir path
        default_current_dir = os.path.abspath(os.path.dirname(__file__))
        # Reset Module Database
        resetModuleDatabase()
        # Return to default current dir
        os.chdir(default_current_dir)
        # Populate Iridium Imarsat-C Data
        populateIridiumImarsatCData()
        # Populate Sanity Rule Data
        #populateSanityRuleData()
        time.sleep(15)



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
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        wait_for_element_by_link_text_to_exist(wait, "CONFIGURATION", "CONFIGURATION checked")
        self.driver.find_element_by_link_text("CONFIGURATION").click()
        # Click on Global setting subtab under Configuration Tab
        wait_for_element_by_css_selector_to_exist(wait, "#globalSettings > span", "CSS Selector #globalSettings > span checked")
        self.driver.find_element_by_css_selector("#globalSettings > span").click()
        # Click to change Coordinates format to dd.mmm
        wait_for_element_by_xpath_to_exist(wait, "(//input[@name='coordinateFormat'])[2]", "XPATH checked")
        self.driver.find_element_by_xpath("(//input[@name='coordinateFormat'])[2]").click()
        # Save current UTC date and time to file (Used in Audit test cases)
        # Set referenceDateTime to current UTC time
        referenceDateTime = datetime.datetime.utcnow()
        # Save referenceDateTime1 to file
        save_elements_to_file(referenceDateTimeFileName[0], referenceDateTime, True)
        # Click to change Default home page to Asset page
        wait_for_element_by_xpath_to_exist(wait, "//button[@id='']", "XPATH checked")
        self.driver.find_element_by_xpath("//button[@id='']").click()
        wait_for_element_by_id_to_exist(wait, "-item-4", "uvms-header-menu-item-audit-log checked")
        self.driver.find_element_by_id("-item-4").click()
        # Save current UTC date and time to file (Used in Audit test cases)
        # Set referenceDateTime to current UTC time
        referenceDateTime = datetime.datetime.utcnow()
        # Save referenceDateTime1 to file
        save_elements_to_file(referenceDateTimeFileName[1], referenceDateTime, True)
        # Check inmarsat plugin is fully synced
        check_inmarsat_fully_synced(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0001c_generate_NAF_position_for_unknown_asset_and_check_holding_table(self):
        # Generate NAF position report with unknown Asset

        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)

        # Set Current Date and time in UTC 4 hours into the future (This will make position report to be placed in Holding Table)
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue + datetime.timedelta(hours=deltaTimeValue)
        earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
        earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')

        # Set Long/Lat
        latStrValue = lolaPositionValues[6][0][0]
        longStrValue = lolaPositionValues[6][0][1]

        # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
        nafSource = generate_NAF_string(countryValue[37], ircsValue[37], cfrValue[37], externalMarkingValue[37], latStrValue, longStrValue, reportedSpeedValue, reportedCourseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[37])
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

        # Save current UTC date and time to file (Used in Audit test cases)
        # Set referenceDateTime to current UTC time
        referenceDateTime = datetime.datetime.utcnow()
        # Save referenceDateTime1 to file
        save_elements_to_file(referenceDateTimeFileName[0], referenceDateTime, True)

        # Select Alarms tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(3)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Click on search button
        wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 2")
        time.sleep(4)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        # Check Asset name
        wait_for_element_by_link_text_to_exist(wait, vesselName[37], "Link text checked 3")
        time.sleep(2)
        self.assertEqual(vesselName[37], self.driver.find_element_by_link_text(vesselName[37]).text)

        # Click on Details button
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[9]", "XPATH checked 4")
        time.sleep(3)
        self.driver.find_element_by_xpath("(//button[@type='button'])[9]").click()
        # Check Position report fields
        wait_for_element_by_xpath_to_exist(wait, "/html/body/div[7]/div/div/div[2]/div[3]/div[2]/div[1]/div", "XPATH checked 4")
        time.sleep(1)
        self.assertEqual(countryValue[37], self.driver.find_element_by_xpath("/html/body/div[7]/div/div/div[2]/div[3]/div[2]/div[1]/div").text)
        self.assertEqual(ircsValue[37], self.driver.find_element_by_xpath("//div[3]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[37], self.driver.find_element_by_xpath("//div[3]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue[37], self.driver.find_element_by_xpath("//div[3]/div[2]/div[4]/div").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath("//div[7]/div/div[2]/div").text)
        self.assertEqual(latStrValue, self.driver.find_element_by_xpath("//div[7]/div[2]/div/div").text)
        self.assertEqual(longStrValue, self.driver.find_element_by_xpath("//div[7]/div[2]/div[2]/div").text)
        self.assertEqual("%.0f" % reportedSpeedValue + " kts", self.driver.find_element_by_xpath("//div[7]/div[2]/div[3]/div").text)
        self.assertEqual(str(reportedCourseValue) + " °", self.driver.find_element_by_xpath("//div[7]/div[2]/div[4]/div").text)
        # Close Report Window
        wait_for_element_by_xpath_to_exist(wait, "//div[7]/div/div/div/div/i", "XPATH checked 5")
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(3)


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


    @timeout_decorator.timeout(seconds=180)
    def test_0009_create_second_new_asset(self):
        # Create new asset (second in the list)
        create_one_new_asset_from_gui(self, 1)

	
    @timeout_decorator.timeout(seconds=180)
    def test_0010_check_new_asset_exists(self):
        # Check new asset (second in the list)
        check_new_asset_exists(self, 1)


    @timeout_decorator.timeout(seconds=180)
    def test_0011_create_second_new_mobile_terminal(self):
        # Create new Mobile Terminal (second in the list)
        create_one_new_mobile_terminal_from_gui(self, 1)


    @timeout_decorator.timeout(seconds=180)
    def test_0012_check_second_new_mobile_terminal_exists(self):
        # Check new Mobile Terminal (second in the list)
        check_new_mobile_terminal_exists(self, 1)


    @timeout_decorator.timeout(seconds=180)
    def test_0013_unlink_asset_and_mobile_terminal(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Mobile Terminal tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        # Enter Serial Number in field
        wait_for_element_by_id_to_exist(wait, "mt-input-search-serialNumber", "mt-input-search-serialNumber checked 2")
        time.sleep(1)
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(serialNoValue[0])
        # Click in search button
        wait_for_element_by_id_to_exist(wait, "mt-btn-advanced-search", "mt-btn-advanced-search checked 3")
        time.sleep(1)
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        # Click on details button
        wait_for_element_by_id_to_exist(wait, "mt-toggle-form", "mt-toggle-form checked 4")
        time.sleep(1)
        self.driver.find_element_by_id("mt-toggle-form").click()
        # Click on unlinking button
        wait_for_element_by_id_to_exist(wait, "menu-bar-unlink", "menu-bar-unlink checked 5")
        time.sleep(1)
        self.driver.find_element_by_id("menu-bar-unlink").click()
        # Enter comment
        wait_for_element_by_name_to_exist(wait, "comment", "Element name comment checked 6")
        time.sleep(1)
        self.driver.find_element_by_name("comment").send_keys("Unlink Asset and MT.")
        # Click on unlinking button
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary", "CSS Selector checked 7")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
        time.sleep(2)



    @timeout_decorator.timeout(seconds=180)
    def test_0015_link_asset_to_another_mobile_terminal(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Mobile Terminal tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        # Enter Serial Number in field
        wait_for_element_by_id_to_exist(wait, "mt-input-search-serialNumber", "mt-input-search-serialNumber checked 2")
        time.sleep(1)
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(serialNoValue[1])
        # Click in search button
        wait_for_element_by_id_to_exist(wait, "mt-btn-advanced-search", "mt-btn-advanced-search checked 3")
        time.sleep(1)
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        # Click on details button
        wait_for_element_by_id_to_exist(wait, "mt-toggle-form", "mt-btn-advanced-search checked 4")
        time.sleep(1)
        self.driver.find_element_by_id("mt-toggle-form").click()
        # Click on Link Asset
        wait_for_element_by_id_to_exist(wait, "mt-btn-assign-asset", "mt-btn-assign-asset checked 5")
        self.driver.find_element_by_id("mt-btn-assign-asset").click()
        # Enter Asset Name and clicks on the search button
        wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[23]", "XPATH checked 6")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//input[@type='text'])[23]").send_keys(vesselName[0])
        wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 7")
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        # Click on connect button
        wait_for_element_by_css_selector_to_exist(wait, "td.textAlignRight > button.btn.btn-primary", "CSS Selector checked 8")
        time.sleep(3)
        self.driver.find_element_by_css_selector("td.textAlignRight > button.btn.btn-primary").click()
        # Click on Link button
        wait_for_element_by_css_selector_to_exist(wait, "div.col-md-6.textAlignRight > button.btn.btn-primary", "CSS Selector checked 9")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.col-md-6.textAlignRight > button.btn.btn-primary").click()
        # Enter Reason comment
        wait_for_element_by_name_to_exist(wait, "comment", "Element name checked 10")
        time.sleep(1)
        self.driver.find_element_by_name("comment").send_keys("Need to connect this mobile terminal with this asset.")
        # Click on Link button 2
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary", "CSS Selector checked 11")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
        # Close page
        wait_for_element_by_id_to_exist(wait, "menu-bar-cancel", "menu-bar-cancel checked 12")
        time.sleep(1)
        self.driver.find_element_by_id("menu-bar-cancel").click()
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0016_generate_and_verify_manual_position(self):
        # Startup browser and login
        UnionVMSTestCase.test_0008_generate_and_verify_manual_position(self)


    @timeout_decorator.timeout(seconds=300)
    def test_0017_create_assets_3_4_5_6(self):
        # Create assets 3-6 in the list
        for x in range(2, 6):
            create_one_new_asset_from_gui(self, x)
            time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0018_create_two_assets_to_group_and_check_group(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on asset tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        # Search for "ship"
        wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "uvms-header-menu-item-assets checked 2")
        time.sleep(1)
        self.driver.find_element_by_id("asset-input-simple-search").send_keys("ship")
        wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "uvms-header-menu-item-assets checked 3")
        time.sleep(1)
        self.driver.find_element_by_id("asset-btn-simple-search").click()
        time.sleep(5)
        # Get asset name values in the list
        assetList = []
        for x in range(6):
            tempAssetName = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) +"]/td[4]").text
            assetList.append(tempAssetName)
        # Check if asset list is not sorted
        if sorted(assetList) != assetList:
            # Sort on "Name" by click on "Name" once
            self.driver.find_element_by_id("asset-sort-name").click()
            time.sleep(1)
        # Select Fartyg1001 and Fartyg1002 by click
        self.driver.find_element_by_css_selector("td.checkboxContainer > input[type=\"checkbox\"]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        # Select Action "Save as Group"
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-actions", "asset-dropdown-actions checked 4")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        wait_for_element_by_link_text_to_exist(wait, "Save as Group", "Link text checked 5")
        time.sleep(1)
        self.driver.find_element_by_link_text("Save as Group").click()
        # Enter Group name and click on save button
        wait_for_element_by_css_selector_to_exist(wait, "form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]", "CSS Selector checked 8")
        time.sleep(1)
        self.driver.find_element_by_css_selector("form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]").send_keys(groupName[0])
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        # Check that Group 1 has been created
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-saved-search", "asset-dropdown-saved-search checked 9")
        time.sleep(5)
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        wait_for_element_by_link_text_to_exist(wait, groupName[0], "Link text checked 10")
        time.sleep(1)
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        self.driver.find_element_by_link_text(groupName[0]).click()
        # Check Assets in Group
        wait_for_element_by_css_selector_to_exist(wait, "td[title=\"" + countryValue[0] + "\"]", "CSS Selector checked 11")
        time.sleep(1)
        self.assertEqual(countryValue[0], self.driver.find_element_by_css_selector("td[title=\"" + countryValue[0] + "\"]").text)
        self.assertEqual(externalMarkingValue[0], self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue[0] + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual(gearTypeValue[0], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue[0] + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)
        self.assertEqual(countryValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[1], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[1] + "\"]").text)
        self.assertEqual(ircsValue[1], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[1] + "\"]").text)
        self.assertEqual(cfrValue[1], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[1] + "\"]").text)
        self.assertEqual(gearTypeValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)
        time.sleep(3)


    @timeout_decorator.timeout(seconds=180)
    def test_0019_add_two_assets_to_group_and_check_group(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on asset tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        # Search for "ship"
        wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "uvms-header-menu-item-assets checked 2")
        time.sleep(1)
        self.driver.find_element_by_id("asset-input-simple-search").send_keys("ship")
        wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
        time.sleep(1)
        self.driver.find_element_by_id("asset-btn-simple-search").click()
        time.sleep(5)
        # Get asset name values in the list
        assetList = []
        for x in range(6):
            tempAssetName = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) +"]/td[4]").text
            assetList.append(tempAssetName)
        # Check if asset list is not sorted
        if sorted(assetList) != assetList:
            # Sort on "Name" by click on "Name" once
            self.driver.find_element_by_id("asset-sort-name").click()
            time.sleep(1)
        # Select Fartyg1005 and Fartyg1006 by click
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[6]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[7]").click()
        # Select Action "Add to Group"
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        wait_for_element_by_link_text_to_exist(wait, "Add to Group", "Link text checked 7")
        time.sleep(1)
        self.driver.find_element_by_link_text("Add to Group").click()
        # Select "Group 1" and click on save button
        wait_for_element_by_id_to_exist(wait, "saveGroupDropdown", "saveGroupDropdown checked 8")
        time.sleep(1)
        self.driver.find_element_by_id("saveGroupDropdown").click()
        wait_for_element_by_xpath_to_exist(wait, "//a[contains(text(),'" + groupName[0] + "')]", "XPATH checked 8")
        time.sleep(1)
        self.driver.find_element_by_xpath("//a[contains(text(),'" + groupName[0] + "')]").click()
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 9")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        # Check that Group 1 has been created
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-saved-search", "asset-dropdown-saved-search checked 10")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        wait_for_element_by_link_text_to_exist(wait, groupName[0], "Link text checked 11")
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        # Click on Group 1
        self.driver.find_element_by_link_text(groupName[0]).click()
        # Check Assets in Group
        wait_for_element_by_css_selector_to_exist(wait, "td[title=\"" + countryValue[0] + "\"]", "CSS Selector checked 12")
        time.sleep(1)
        self.assertEqual(countryValue[0], self.driver.find_element_by_css_selector("td[title=\"" + countryValue[0] + "\"]").text)
        self.assertEqual(externalMarkingValue[0], self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue[0] + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual(gearTypeValue[0], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue[0] + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)

        wait_for_element_by_xpath_to_exist(wait, "//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]", "XPATH checked 14")
        self.assertEqual(countryValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[1], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[1] + "\"]").text)
        self.assertEqual(ircsValue[1], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[1] + "\"]").text)
        self.assertEqual(cfrValue[1], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[1] + "\"]").text)
        self.assertEqual(gearTypeValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)

        self.assertEqual(countryValue[4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[2]").text)
        self.assertEqual(externalMarkingValue[4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[3]").text)
        self.assertEqual(vesselName[4], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[4] + "\"]").text)
        self.assertEqual(ircsValue[4], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[4] + "\"]").text)
        self.assertEqual(cfrValue[4], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[4] + "\"]").text)
        self.assertEqual(gearTypeValue[4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[8]").text)

        self.assertEqual(countryValue[5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[2]").text)
        self.assertEqual(externalMarkingValue[5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[3]").text)
        self.assertEqual(vesselName[5], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[5] + "\"]").text)
        self.assertEqual(ircsValue[5], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[5] + "\"]").text)
        self.assertEqual(cfrValue[5], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[5] + "\"]").text)
        self.assertEqual(gearTypeValue[5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[8]").text)
        time.sleep(2)

	
    @timeout_decorator.timeout(seconds=180)
    def test_0020_remove_one_asset_group_and_check_group(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on asset tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        # Click on saved groups
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-saved-search", "uvms-header-menu-item-assets checked 2")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        wait_for_element_by_link_text_to_exist(wait, groupName[0], "Link text checked 3")
        time.sleep(1)
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        # Click on Group 1
        self.driver.find_element_by_link_text(groupName[0]).click()
        time.sleep(3)
        # Get asset name values in the group list
        assetList = []
        for x in range(4):
            tempAssetName = self.driver.find_element_by_xpath(
                "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) +"]/td[4]").text
            assetList.append(tempAssetName)
        # Check if asset list is not sorted
        if sorted(assetList) != assetList:
            # Sort on "Name" by click on "Name" once
            self.driver.find_element_by_id("asset-sort-name").click()
            time.sleep(1)
        # Select Fartyg1002 and Fartyg1005
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[4]").click()
        # Click on action button
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-actions", "asset-dropdown-actions checked 4")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        # Remove selected assets from Group 1
        wait_for_element_by_link_text_to_exist(wait, "Remove from Group", "Link text checked 5")
        time.sleep(1)
        self.driver.find_element_by_link_text("Remove from Group").click()
        time.sleep(1)
        # Reload page
        self.driver.refresh()
        # Click on saved groups
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-saved-search", "asset-dropdown-saved-search checked 6")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        wait_for_element_by_link_text_to_exist(wait, groupName[0], "Link text checked 7")
        time.sleep(1)
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        # Click on Group 1
        self.driver.find_element_by_link_text(groupName[0]).click()
        # Check Assets in Group
        wait_for_element_by_css_selector_to_exist(wait, "td[title=\"" + countryValue[0] + "\"]", "CSS Selector checked 8")
        time.sleep(1)
        self.assertEqual(countryValue[0], self.driver.find_element_by_css_selector("td[title=\"" + countryValue[0] + "\"]").text)
        self.assertEqual(externalMarkingValue[0], self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue[0] + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual(gearTypeValue[0], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue[0] + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)
        self.assertEqual(countryValue[5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue[5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[5], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[5] + "\"]").text)
        self.assertEqual(ircsValue[5], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[5] + "\"]").text)
        self.assertEqual(cfrValue[5], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[5] + "\"]").text)
        self.assertEqual(gearTypeValue[5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)
        time.sleep(3)


    @timeout_decorator.timeout(seconds=180)
    def test_0021_create_second_group_and_add_assets_to_group(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on asset tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        # Search for "ship"
        wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
        time.sleep(1)
        self.driver.find_element_by_id("asset-input-simple-search").send_keys("ship")
        wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
        time.sleep(1)
        self.driver.find_element_by_id("asset-btn-simple-search").click()
        time.sleep(5)
        # Get asset name values in the list
        assetList = []
        for x in range(6):
            tempAssetName = self.driver.find_element_by_xpath(
                "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) +"]/td[4]").text
            assetList.append(tempAssetName)
        # Check if asset list is not sorted
        if sorted(assetList) != assetList:
            # Sort on "Name" by click on "Name" once
            self.driver.find_element_by_id("asset-sort-name").click()
            time.sleep(1)
        # Select Fartyg1003 and Fartyg1005 by click
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[4]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[6]").click()
        # Select Action "Save as Group"
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-actions", "asset-dropdown-actions checked 4")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        wait_for_element_by_link_text_to_exist(wait, "Save as Group", "Link text checked 5")
        time.sleep(1)
        self.driver.find_element_by_link_text("Save as Group").click()
        # Enter Group name and click on save button
        wait_for_element_by_css_selector_to_exist(wait, "form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]", "CSS Selector checked 6")
        time.sleep(1)
        self.driver.find_element_by_css_selector("form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]").send_keys(groupName[1])
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 7")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        # Check that Group 2 has been created
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-actions", "asset-dropdown-actions checked 8")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-saved-search", "asset-dropdown-saved-search checked 9")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        wait_for_element_by_link_text_to_exist(wait, groupName[1], "Link text checked 10")
        time.sleep(1)
        self.assertEqual(groupName[1], self.driver.find_element_by_link_text(groupName[1]).text)
        # Click on Group 2
        self.driver.find_element_by_link_text(groupName[1]).click()
        # Check Assets in Group
        wait_for_element_by_css_selector_to_exist(wait, "td[title=\"" + countryValue[2] + "\"]", "CSS Selector checked 11")
        time.sleep(1)
        self.assertEqual(countryValue[2], self.driver.find_element_by_css_selector("td[title=\"" + countryValue[2] + "\"]").text)
        self.assertEqual(externalMarkingValue[2], self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue[2] + "\"]").text)
        self.assertEqual(vesselName[2], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[2] + "\"]").text)
        self.assertEqual(ircsValue[2], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[2] + "\"]").text)
        self.assertEqual(cfrValue[2], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[2] + "\"]").text)
        self.assertEqual(gearTypeValue[2], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue[2] + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)
        self.assertEqual(countryValue[4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue[4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[4], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[4] + "\"]").text)
        self.assertEqual(ircsValue[4], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[4] + "\"]").text)
        self.assertEqual(cfrValue[4], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[4] + "\"]").text)
        self.assertEqual(gearTypeValue[4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0022_delete_second_group_and_check(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on asset tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        # Click on "saved groups" drop box
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-saved-search", "asset-dropdown-saved-search checked 2")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        # Click on delete button for Group 2
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-saved-search-delete-item-1", "asset-dropdown-saved-search-delete-item-1 checked 3")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search-delete-item-1").click()
        # Click on confirmation button
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 4")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(1)
        # Reload page
        self.driver.refresh()
        # Check that Group 1 exists and Group 2 does not exist
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-saved-search", "asset-dropdown-saved-search checked 5")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        wait_for_element_by_link_text_to_exist(wait, groupName[0], "Link text checked 6")
        time.sleep(1)
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        try:
            self.assertFalse(self.driver.find_element_by_link_text(groupName[1]).text)
        except NoSuchElementException:
            pass
        time.sleep(3)


    @timeout_decorator.timeout(seconds=180)
    def test_0023_advanced_search_of_assets(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on asset tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        # Click on advanced search
        wait_for_element_by_css_selector_to_exist(wait, "#asset-toggle-search-view > span", "CSS Selector checked 2")
        time.sleep(1)
        self.driver.find_element_by_css_selector("#asset-toggle-search-view > span").click()
        # Search for all External Marking called "EXT3"(externalMarkingValue[0])
        wait_for_element_by_id_to_exist(wait, "asset-input-search-externalMarking", "asset-input-search-externalMarking checked 3")
        time.sleep(1)
        self.driver.find_element_by_id("asset-input-search-externalMarking").send_keys(externalMarkingValue[0])
        wait_for_element_by_id_to_exist(wait, "asset-btn-advanced-search", "asset-btn-advanced-search checked 4")
        time.sleep(1)
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(5)
        # Get asset name values in the list
        assetList = []
        for x in range(6):
            tempAssetName = self.driver.find_element_by_xpath(
                "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) +"]/td[4]").text
            assetList.append(tempAssetName)
        # Check if asset list is not sorted
        if sorted(assetList) != assetList:
            # Sort on "Name" by click on "Name" once
            self.driver.find_element_by_id("asset-sort-name").click()
            time.sleep(1)
        # Check Assets in List
        self.assertEqual(countryValue[0], self.driver.find_element_by_css_selector("td[title=\"" + countryValue[0] + "\"]").text)
        self.assertEqual(externalMarkingValue[0], self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue[0] + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual(gearTypeValue[0], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue[0] + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)
        for x in [1,2,3,4,5]:
            self.assertEqual(countryValue[x], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[2]").text)
            self.assertEqual(externalMarkingValue[x], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[3]").text)
            self.assertEqual(vesselName[x], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[x] + "\"]").text)
            self.assertEqual(ircsValue[x], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[x] + "\"]").text)
            self.assertEqual(cfrValue[x], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[x] + "\"]").text)
            self.assertEqual(gearTypeValue[x], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[7]").text)
            self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[8]").text)
        time.sleep(3)
        # Click on save group button
        self.driver.find_element_by_css_selector("#asset-btn-save-search > span").click()
        self.driver.find_element_by_css_selector("form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]").send_keys(groupName[2])
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(3)
        # Reload page
        self.driver.refresh()
        # Check that Group 3 exists in the list
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-saved-search", "uvms-header-menu-item-assets checked 5")
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        wait_for_element_by_link_text_to_exist(wait, groupName[2], "Link text checked 6")
        time.sleep(1)
        self.assertEqual(groupName[2], self.driver.find_element_by_link_text(groupName[2]).text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0024_export_assets_to_excel_file(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on asset tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-assets", "uvms-header-menu-item-assets checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        # Search for "ship"
        wait_for_element_by_id_to_exist(wait, "asset-input-simple-search", "asset-input-simple-search checked 2")
        time.sleep(3)
        self.driver.find_element_by_id("asset-input-simple-search").send_keys("ship")
        wait_for_element_by_id_to_exist(wait, "asset-btn-simple-search", "asset-btn-simple-search checked 3")
        time.sleep(1)
        self.driver.find_element_by_id("asset-btn-simple-search").click()
        time.sleep(5)
        # Get asset name values in the list
        assetList = []
        for x in range(6):
            tempAssetName = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) +"]/td[4]").text
            assetList.append(tempAssetName)
        # Check if asset list is not sorted
        if sorted(assetList) != assetList:
            # Sort on "Name" by click on "Name" once
            self.driver.find_element_by_id("asset-sort-name").click()
            time.sleep(1)
        # Select Fartyg1001 and Fartyg1002 by click
        self.driver.find_element_by_css_selector("td.checkboxContainer > input[type=\"checkbox\"]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        # Save path to current dir
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Change to Download folder for current user
        downloadPath = get_download_path()
        os.chdir(downloadPath)
        print(os.path.abspath(os.path.dirname(__file__)))
        # Check if file exists. If so remove it
        if os.path.exists(assetFileName):
            os.remove(assetFileName)
        # Select Action "Export selection"
        wait_for_element_by_id_to_exist(wait, "asset-dropdown-actions", "asset-dropdown-actions checked 4")
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        wait_for_element_by_link_text_to_exist(wait, "Export selection to CSV", "Link text checked 5")
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Open saved csv file and read all elements to "allrows"
        ifile  = open(assetFileName, "rt", encoding="utf8")
        reader = csv.reader(ifile, delimiter=';')
        allrows =['']
        for row in reader:
            print(row)
            allrows.append(row)
        ifile.close()
        del allrows[0]
        # Change back the path to current dir
        os.chdir(cwd)
        print(cwd)
        # Check that the elements in csv file is correct
        for y in range(len(allrows)):
            if y==0:
                # Check Headlines
                for x in range(len(assetHeadline)):
                    if not (x==0):
                        self.assertEquals(assetHeadline[x], allrows[y][x])
            else:
                # Check values in CSV file
                print("Test row: " + str(y))
                self.assertEqual(countryValue[y-1], allrows[y][0])
                self.assertEqual(externalMarkingValue[y-1], allrows[y][1])
                self.assertEqual(vesselName[y-1], allrows[y][2])
                self.assertEqual(ircsValue[y-1], allrows[y][3])
                self.assertEqual(cfrValue[y-1], allrows[y][4])
                self.assertEqual(gearTypeValue[y-1], allrows[y][5])
                self.assertEqual(licenseTypeValue, allrows[y][6])
        time.sleep(3)


    @timeout_decorator.timeout(seconds=300)
    def test_0025_create_new_mobile_terminal_3_6(self):
        # Create new Mobile Terminal (Number 3-6 in the list)
        for x in [2,3,4,5]:
            create_one_new_mobile_terminal_from_gui(self, x)


    @timeout_decorator.timeout(seconds=180)
    def test_0026_export_mobile_terminals_to_excel_file(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on mobile terminal tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-communication", "uvms-header-menu-item-communication checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        # Search on MemberID 100
        wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[9]", "XPATH checked 2")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//input[@type='text'])[9]").send_keys(memberIdnumber[0])
        wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 3")
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        # Sort on "Serial no"
        wait_for_element_by_id_to_exist(wait, "mt-sort-serialNumber", "mt-sort-serialNumber checked 4")
        time.sleep(1)
        self.driver.find_element_by_id("mt-sort-serialNumber").click()
        # Select Not linked row number 2-4 by click
        wait_for_element_by_xpath_to_exist(wait, "(//input[@type='checkbox'])[2]", "XPATH checked 5")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[4]").click()
        # Save row information for rows 2-4 in the list
        allrowsbackup = ['']
        currentrow = []
        # Check if first Element is empty (Probably not linked)
        tempElement = self.driver.find_element_by_xpath("//div[@id='content']//div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[1]/td[2]/span[1]/a").text
        if tempElement == '':
            tempElement = self.driver.find_element_by_xpath("//div[@id='content']//div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[1]/td[2]/span[3]").text
        currentrow.append(tempElement)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[6]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[7]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/span").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[9]/span").text)
        allrowsbackup.append(currentrow)
        currentrow = []
        # Check if first Element is empty (Probably not linked)
        tempElement = self.driver.find_element_by_xpath("//div[@id='content']//div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[2]/span[1]/a").text
        if tempElement == '':
            tempElement = self.driver.find_element_by_xpath("//div[@id='content']//div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[2]/span[3]").text
        currentrow.append(tempElement)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[5]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[6]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[8]/span").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[9]/span").text)
        allrowsbackup.append(currentrow)
        currentrow = []
        # Check if first Element is empty (Probably not linked)
        tempElement = self.driver.find_element_by_xpath("//div[@id='content']//div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[2]/span[1]/a").text
        if tempElement == '':
            tempElement = self.driver.find_element_by_xpath("//div[@id='content']//div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[2]/span[3]").text
        currentrow.append(tempElement)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[5]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[6]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[7]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[8]/span").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[9]/span").text)
        allrowsbackup.append(currentrow)
        del allrowsbackup[0]
        print("-------------------- SAVE START-----------------------")
        print(allrowsbackup)
        print("-------------------- SAVE END-----------------------")
        # Save path to current dir
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Change to Download folder for current user
        downloadPath = get_download_path()
        os.chdir(downloadPath)
        print(os.path.abspath(os.path.dirname(__file__)))
        # Check if file exists. If so remove it
        if os.path.exists(mobileTerminalFileName):
            os.remove(mobileTerminalFileName)
        # Select Action "Export selection"
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[4]", "XPATH checked 6")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        wait_for_element_by_link_text_to_exist(wait, "Export selection to CSV", "Link text checked 7")
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Open saved csv file and read all elements to "allrows"
        ifile  = open(mobileTerminalFileName, "rt", encoding="utf8")
        reader = csv.reader(ifile, delimiter=';')
        allrows =['']
        for row in reader:
            allrows.append(row)
        ifile.close()
        del allrows[0]
        # Change back the path to current dir
        os.chdir(cwd)
        print(cwd)
        # Check that the elements in csv file is correct
        for y in range(len(allrows)):
            if y==0:
                # Check Headlines
                for x in range(len(mobileTerminalHeadline)):
                    if not (x == 0):
                        self.assertEqual(mobileTerminalHeadline[x], allrows[y][x])
            else:
                print("Test row: " + str(y))
                for z in range(8):
                    self.assertEqual(allrowsbackup[y-1][z].lower(), allrows[y][z].lower())
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0027_view_audit_log(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on Audit tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-audit-log", "uvms-header-menu-item-audit-log checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        # Click on all sub tabs under Audit Log Tab
        wait_for_element_by_css_selector_to_exist(wait, "#EXCHANGE > span", "CSS Selector checked 2")
        time.sleep(1)
        self.driver.find_element_by_css_selector("#EXCHANGE > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#POSITION_REPORTS > span", "CSS Selector checked 3")
        self.driver.find_element_by_css_selector("#POSITION_REPORTS > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#ASSETS_AND_TERMINALS > span", "CSS Selector checked 4")
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#GIS > span", "CSS Selector checked 5")
        self.driver.find_element_by_css_selector("#GIS > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#ALARMS > span", "CSS Selector checked 6")
        self.driver.find_element_by_css_selector("#ALARMS > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#ACCESS_CONTROL > span", "CSS Selector checked 7")
        self.driver.find_element_by_css_selector("#ACCESS_CONTROL > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#ALL > span", "CSS Selector checked 8")
        self.driver.find_element_by_css_selector("#ALL > span").click()
        # Check sub tab names
        self.assertEqual("ALL", self.driver.find_element_by_css_selector("#ALL > span").text)
        self.assertEqual("EXCHANGE", self.driver.find_element_by_css_selector("#EXCHANGE > span").text)
        self.assertEqual("POSITION REPORTS", self.driver.find_element_by_css_selector("#POSITION_REPORTS > span").text)
        self.assertEqual("ASSETS AND TERMINALS", self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").text)
        self.assertEqual("GIS", self.driver.find_element_by_css_selector("#GIS > span").text)
        self.assertEqual("ALERTS", self.driver.find_element_by_css_selector("#ALARMS > span").text)
        self.assertEqual("ACCESS CONTROL", self.driver.find_element_by_css_selector("#ACCESS_CONTROL > span").text)
        time.sleep(3)


    @timeout_decorator.timeout(seconds=180)
    def test_0028_view_audit_and_export_log_to_file(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on Audit tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-audit-log", "uvms-header-menu-item-audit-log checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        # Enter User Name in the Username field
        wait_for_element_by_xpath_to_exist(wait, "//input[@type='text']", "XPATH checked 2")
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[@type='text']").clear()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(defaultUserName)
        # Filter on Create Operation
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[2]", "XPATH checked 3")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[3]/div/div[1]/div/div/form/div/div/div/div[1]/div[2]/div/div/ul/li[5]/a", "XPATH checked 4")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[3]/div/div[1]/div/div/form/div/div/div/div[1]/div[2]/div/div/ul/li[5]/a").click()
        # Click on search button
        wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 5")
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        # Check that the 4 first items in the Audit list are Mobile Terminals logs
        wait_for_element_by_xpath_to_exist(wait, "//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[1]/td[2]", "XPATH checked 6")
        time.sleep(1)
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[1]/td[2]").text)
        self.assertEqual("Create", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[1]/td[3]").text)
        self.assertEqual("Mobile Terminal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[1]/td[4]").text)
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual("Create", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual("Mobile Terminal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[4]").text)
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[3]/td[2]").text)
        self.assertEqual("Create", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[3]/td[3]").text)
        self.assertEqual("Mobile Terminal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[3]/td[4]").text)
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[4]/td[2]").text)
        self.assertEqual("Create", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[4]/td[3]").text)
        self.assertEqual("Mobile Terminal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[4]/td[4]").text)
        # Save row information for rows 1-4 in the list
        allrowsbackup = ['']
        currentrow = []
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[1]/td[2]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[1]/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[1]/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[1]/td[5]").text)
        allrowsbackup.append(currentrow)
        currentrow = []
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[5]").text)
        allrowsbackup.append(currentrow)
        currentrow = []
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[3]/td[2]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[3]/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[3]/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[3]/td[5]").text)
        allrowsbackup.append(currentrow)
        currentrow = []
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[4]/td[2]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[4]/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[4]/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[4]/td[5]").text)
        allrowsbackup.append(currentrow)
        del allrowsbackup[0]
        print("-------------------- SAVE START-----------------------")
        print(allrowsbackup)
        print("-------------------- SAVE END-----------------------")
        # Save path to current dir
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Change to Download folder for current user
        downloadPath = get_download_path()
        os.chdir(downloadPath)
        print(os.path.abspath(os.path.dirname(__file__)))
        # Check if file exists. If so remove it
        if os.path.exists(auditLogsFileName):
            os.remove(auditLogsFileName)
        # Select row number 1-4 by click
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[4]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[5]").click()
        # Select Action "Export selection"
        wait_for_element_by_id_to_exist(wait, "admin-dropdown-actions", "admin-dropdown-actions checked 7")
        self.driver.find_element_by_id("admin-dropdown-actions").click()
        wait_for_element_by_link_text_to_exist(wait, "Export selection to CSV", "Link text checked 8")
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Open saved csv file and read all elements to "allrows"
        ifile  = open(auditLogsFileName, "rt", encoding="utf8")
        reader = csv.reader(ifile, delimiter=';')
        allrows =['']
        for row in reader:
            allrows.append(row)
        ifile.close()
        del allrows[0]
        # Change back the path to current dir
        os.chdir(cwd)
        print(cwd)
        # Check that the elements in csv file is correct
        for y in range(len(allrows)):
            if y==0:
                # Check Headlines
                for x in range(len(auditLogsHeadline)):
                    if not (x == 0):
                        self.assertEqual(auditLogsHeadline[x], allrows[y][x])
            else:
                print("Test row: " + str(y))
                for z in range(4):
                    self.assertEqual(allrowsbackup[y-1][z].lower(), allrows[y][z].lower())
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0029_view_configuration_pages(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on Audit tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-audit-log", "uvms-header-menu-item-audit-log checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        wait_for_element_by_link_text_to_exist(wait, "CONFIGURATION", "Link text checked 2")
        time.sleep(1)
        self.driver.find_element_by_link_text("CONFIGURATION").click()
        # Click on all sub tabs under Configuration Tab
        wait_for_element_by_css_selector_to_exist(wait, "#globalSettings > span", "CSS Selector checked 3")
        time.sleep(1)
        self.driver.find_element_by_css_selector("#globalSettings > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#reporting > span", "CSS Selector checked 4")
        self.driver.find_element_by_css_selector("#reporting > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#asset > span", "CSS Selector checked 5")
        self.driver.find_element_by_css_selector("#asset > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#exchange > span", "CSS Selector checked 6")
        self.driver.find_element_by_css_selector("#exchange > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#movementrules > span", "CSS Selector checked 7")
        self.driver.find_element_by_css_selector("#movementrules > span").click()
        wait_for_element_by_css_selector_to_exist(wait, "#systemMonitor > span", "CSS Selector checked 8")
        self.driver.find_element_by_css_selector("#systemMonitor > span").click()
        # Check sub tab names
        self.assertEqual("SYSTEM MONITOR", self.driver.find_element_by_css_selector("#systemMonitor > span").text)
        self.assertEqual("GLOBAL SETTINGS", self.driver.find_element_by_css_selector("#globalSettings > span").text)
        self.assertEqual("REPORTING", self.driver.find_element_by_css_selector("#reporting > span").text)
        self.assertEqual("ASSETS", self.driver.find_element_by_css_selector("#asset > span").text)
        self.assertEqual("EXCHANGE", self.driver.find_element_by_css_selector("#exchange > span").text)
        self.assertEqual("MOVEMENT RULES", self.driver.find_element_by_css_selector("#movementrules > span").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0030_change_global_settings_change_date_format(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on Audit tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-audit-log", "uvms-header-menu-item-audit-log checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        wait_for_element_by_link_text_to_exist(wait, "CONFIGURATION", "Link text checked 2")
        time.sleep(1)
        self.driver.find_element_by_link_text("CONFIGURATION").click()
        # Click on Global setting subtab under Configuration Tab
        wait_for_element_by_css_selector_to_exist(wait, "#globalSettings > span", "CSS Selector checked 3")
        time.sleep(1)
        self.driver.find_element_by_css_selector("#globalSettings > span").click()
        time.sleep(1)
        # Check that Date format is correct
        try:
            radiobuttonDate1 = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/ng-include/div/div/div[1]/div[2]/div[1]/ul/li[1]/label/input").is_selected()
        except:
            print("Did NOT find selected radio button")
            radiobuttonDate1 = False
        try:
            radiobuttonDate2 = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/ng-include/div/div/div[1]/div[2]/div[1]/ul/li[2]/label/input").is_selected()
        except:
            print("Did NOT find selected radio button")
            radiobuttonDate2 = False
        currentDate = self.driver.find_element_by_css_selector("current-time.currentTime").text
        print(currentDate)
        if radiobuttonDate1:
            self.assertEqual("-", currentDate[4])
        if radiobuttonDate2:
            self.assertEqual("/", currentDate[2])
        time.sleep(1)
        # Change Date format and check that change is made
        if radiobuttonDate1:
            self.driver.find_element_by_xpath("(//input[@name='dateFormat'])[2]").click()
            time.sleep(2)
            currentDate = self.driver.find_element_by_css_selector("current-time.currentTime").text
            self.assertEqual("/", currentDate[2])
        if radiobuttonDate2:
            self.driver.find_element_by_name("dateFormat").click()
            time.sleep(2)
            currentDate = self.driver.find_element_by_css_selector("current-time.currentTime").text
            self.assertEqual("-", currentDate[4])
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0030b_change_global_settings_change_date_format(self):
        # Startup browser and login
        UnionVMSTestCase.test_0030_change_global_settings_change_date_format(self)



    @timeout_decorator.timeout(seconds=180)
    def test_0030c_generate_NAF_and_verify_position(self):
        # Startup browser and login
        UnionVMSTestCase.test_0007_generate_NAF_and_verify_position(self)



    @timeout_decorator.timeout(seconds=180)
    def test_0031_change_global_settings_change_speed_format(self):
        # Change and check speed unit type for Global Settings
        for x in [2,1,0]:
            print(x)
            change_and_check_speed_format(self,x)
            reload_page_and_goto_default(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0032_check_view_help_text(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on User Guide icon (Question mark icon)
        # Note: User Guide page is opened in a new tab
        wait_for_element_by_xpath_to_exist(wait, "//div[4]/a/i", "XPATH checked 1")
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[4]/a/i").click()
        # Switch tab focus for Selenium to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(5)
        # Check User guide page
        wait_for_element_by_id_to_exist(wait, "title-text", "title-text checked 2")
        time.sleep(5)
        self.assertEqual("Union VMS - User Manual", self.driver.find_element_by_id("title-text").text)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='main-content']/div[3]/ul/li[1]/span/a", "XPATH checked 3")
        time.sleep(2)
        self.assertEqual("Welcome to Union VMS!", self.driver.find_element_by_xpath("//*[@id='main-content']/div[3]/ul/li[1]/span/a").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0033_check_alerts_view(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Check List Headlines for Holding Table
        wait_for_element_by_css_selector_to_exist(wait, "th.st-sort.st-sort-descent", "CSS Selector checked 2")
        time.sleep(2)
        self.assertEqual("Date triggered (UTC)", self.driver.find_element_by_css_selector("th.st-sort.st-sort-descent").text)
        self.assertEqual("Object affected", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]").text)
        self.assertEqual("Rule", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[4]").text)
        # Select Alerts tab (Notifications)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[2]/a", "XPATH checked 3")
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[2]/a").click()
        # Check List Headlines for Notifications
        wait_for_element_by_css_selector_to_exist(wait, "th.st-sort.st-sort-descent", "CSS Selector checked 4")
        time.sleep(1)
        self.assertEqual("Date triggered (UTC)", self.driver.find_element_by_css_selector("th.st-sort.st-sort-descent").text)
        self.assertEqual("Object affected", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]").text)
        self.assertEqual("Rule", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[4]").text)
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 5")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        # Check List Headlines for Rules List
        wait_for_element_by_css_selector_to_exist(wait, "th.st-sort", "CSS Selector checked 6")
        time.sleep(1)
        self.assertEqual("Rule name", self.driver.find_element_by_css_selector("th.st-sort").text)
        self.assertEqual("Last triggered", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]").text)
        self.assertEqual("Date updated", self.driver.find_element_by_css_selector("th.st-sort.st-sort-descent").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0034_create_speed_rule_one(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 2")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        # Click on create button
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[2]", "XPATH checked 3")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        # Enter Rule name
        wait_for_element_by_name_to_exist(wait, "name", "Element name checked 3")
        time.sleep(1)
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys("Speed > " + str(reportedSpeedDefault[0]))
        # Enter Description
        self.driver.find_element_by_name("description").clear()
        self.driver.find_element_by_name("description").send_keys("Speed > " + str(reportedSpeedDefault[0]))
        # Enter Rule Speed > 8
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[3]", "XPATH checked 4")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[3]").click()
        wait_for_element_by_link_text_to_exist(wait, "(", "Link text checked 5")
        time.sleep(1)
        self.driver.find_element_by_link_text("(").click()
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[4]", "XPATH checked 6")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[4]").click()
        wait_for_element_by_link_text_to_exist(wait, "Position", "Link text checked 7")
        time.sleep(1)
        self.driver.find_element_by_link_text("Position").click()
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[5]", "XPATH checked 8")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[5]").click()
        wait_for_element_by_link_text_to_exist(wait, "Reported speed", "Link text checked 9")
        time.sleep(1)
        self.driver.find_element_by_link_text("Reported speed").click()
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[6]", "XPATH checked 10")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[6]").click()
        wait_for_element_by_link_text_to_exist(wait, ">", "Link text checked 11")
        time.sleep(1)
        self.driver.find_element_by_link_text(">").click()
        wait_for_element_by_name_to_exist(wait, "value", "Element name checked 12")
        time.sleep(1)
        self.driver.find_element_by_name("value").click()
        self.driver.find_element_by_name("value").clear()
        self.driver.find_element_by_name("value").send_keys(reportedSpeedDefault[0])
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[7]", "XPATH checked 14")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[7]").click()
        wait_for_element_by_link_text_to_exist(wait, ")", "Link text checked 15")
        time.sleep(1)
        self.driver.find_element_by_link_text(")").click()
        wait_for_element_by_css_selector_to_exist(wait, "span.link", "CSS Selector checked 15")
        time.sleep(1)
        self.driver.find_element_by_css_selector("span.link").click()
        # Check validation of Rule
        wait_for_element_by_css_selector_to_exist(wait, "span.success", "CSS Selector checked 16")
        time.sleep(1)
        self.assertEqual("Rule definition is valid.", self.driver.find_element_by_css_selector("span.success").text)
        # Submit the new Rule
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[3]", "XPATH checked 17")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 18")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        # Change "Notify by email" to Yes
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[2]", "XPATH checked 19")
        time.sleep(5)
        self.driver.find_element_by_xpath("(//button[@id=''])[2]").click()
        wait_for_element_by_link_text_to_exist(wait, "Yes", "Link text checked 20")
        time.sleep(1)
        self.driver.find_element_by_link_text("Yes").click()
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0035_verify_created_speed_rule_one(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 2")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        # Check Headline Names
        wait_for_element_by_css_selector_to_exist(wait, "th.st-sort", "CSS Selector checked 3")
        time.sleep(1)
        self.assertEqual(rulesHeadlineNames[0], self.driver.find_element_by_css_selector("th.st-sort").text)
        self.assertEqual(rulesHeadlineNames[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]").text)
        self.assertEqual(rulesHeadlineNames[2], self.driver.find_element_by_css_selector("th.st-sort.st-sort-descent").text)
        self.assertEqual(rulesHeadlineNames[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[5]").text)
        self.assertEqual(rulesHeadlineNames[4], self.driver.find_element_by_css_selector("th.notifyByTicket").text)
        self.assertEqual(rulesHeadlineNames[5], self.driver.find_element_by_css_selector("th.notifyByEmail").text)
        self.assertEqual(rulesHeadlineNames[6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[8]").text)
        self.assertEqual(rulesHeadlineNames[7], self.driver.find_element_by_css_selector("th.actions").text)
        # Check speed rule parameters
        self.assertEqual("Speed > " + str(reportedSpeedDefault[0]), self.driver.find_element_by_css_selector("td.statusColored.truncate-text").text)
        self.assertEqual("Yes", self.driver.find_element_by_xpath("(//button[@id=''])[1]").text)
        self.assertEqual("Yes", self.driver.find_element_by_xpath("(//button[@id=''])[2]").text)
        self.assertEqual("ACTIVE", self.driver.find_element_by_css_selector("span.label.label-success").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0036_create_NAF_position_with_speed_that_triggs_rule_one(self):
        # Create a NAF position and verify the position
        earlierPositionDateTimeValueString = generate_NAF_and_verify_position(self, reportedSpeedDefault[0] + 1, reportedCourseValue)
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on Alert tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(3)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Click on Notifications tab
        wait_for_element_by_link_text_to_exist(wait, "NOTIFICATIONS", "Link text checked 2")
        time.sleep(1)
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        # Check Asset and Rule names
        wait_for_element_by_link_text_to_exist(wait, vesselName[0], "Link text checked 3")
        time.sleep(1)
        self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
        self.assertEqual("Speed > " + str(reportedSpeedDefault[0]), self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + "\"]").text)
        # Click on details button
        wait_for_element_by_xpath_to_exist(wait, "//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button", "XPATH checked 3")
        time.sleep(3)
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        # Check Position parameters
        wait_for_element_by_css_selector_to_exist(wait, "div.value", "CSS Selector checked 4")
        time.sleep(1)
        self.assertEqual(countryValue[0], self.driver.find_element_by_css_selector("div.value").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[4]/div").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_xpath("//div[2]/div[5]/div").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedDefault[0] + 1) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        wait_for_element_by_xpath_to_exist(wait, "//div[7]/div/div/div/div/i", "XPATH checked 5")
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0037_create_manual_position_with_speed_that_triggs_rule_one(self):
        # Create a manual position and verify the position
        earlierPositionDateTimeValueString = generate_and_verify_manual_position(self, reportedSpeedDefault[0] + 1, reportedCourseValue)
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on Alert tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(3)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Click on Notifications tab
        wait_for_element_by_link_text_to_exist(wait, "NOTIFICATIONS", "Link text checked 2")
        time.sleep(1)
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        # Check Asset and Rule names
        wait_for_element_by_link_text_to_exist(wait, vesselName[0], "Link text checked 3")
        time.sleep(1)
        self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
        wait_for_element_by_css_selector_to_exist(wait, "td[title=\"Speed > " + str(reportedSpeedDefault[0]) + "\"]", "CSS Selector checked 3")
        time.sleep(2)
        self.assertEqual("Speed > " + str(reportedSpeedDefault[0]), self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + "\"]").text)
        # Click on details button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        # Check Position parameters
        wait_for_element_by_css_selector_to_exist(wait, "div.value", "CSS Selector checked 4")
        time.sleep(2)
        self.assertEqual(countryValue[0], self.driver.find_element_by_css_selector("div.value").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[4]/div").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_xpath("//div[2]/div[5]/div").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedDefault[0] + 1) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        wait_for_element_by_xpath_to_exist(wait, "//div[7]/div/div/div/div/i", "XPATH checked 5")
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0038_inactivate_speed_rule_one_and_check(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 2")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        # Click on edit rule icon
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[6]", "XPATH checked 3")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        # Click on selection drop down button
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[2]", "XPATH checked 4")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[2]").click()
        # Select "Inactive" state
        wait_for_element_by_link_text_to_exist(wait, "Inactive", "Link text checked 5")
        time.sleep(1)
        self.driver.find_element_by_link_text("Inactive").click()
        # Click on update button
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[2]", "XPATH checked 6")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        # Click on confirmation button
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 7")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        # Check that rule one is in inactive state
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/span", "XPATH checked 8")
        time.sleep(1)
        self.assertEqual("INACTIVE", self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/span").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0039_create_manual_position_with_speed_that_not_triggs_speed_rule_one(self):
        # Create a manual position and verify the position
        earlierPositionDateTimeValueString = generate_and_verify_manual_position(self, reportedSpeedDefault[0] + 1, reportedCourseValue)
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Click on Alert tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(3)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Click on Notifications tab
        wait_for_element_by_link_text_to_exist(wait, "NOTIFICATIONS", "Link text checked 2")
        time.sleep(1)
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        # Get Asset and Rule names
        wait_for_element_by_link_text_to_exist(wait, vesselName[0], "Link text checked 3")
        time.sleep(1)
        tempAsset = self.driver.find_element_by_link_text(vesselName[0]).text
        tempRuleName = self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + "\"]").text
        # Click on details button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        # Check that time is not correct
        wait_for_element_by_css_selector_to_exist(wait, "div.col-md-9 > div.value", "CSS Selector checked 4")
        time.sleep(1)
        self.assertNotEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        print(earlierPositionDateTimeValueString)
        print(self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0040_activate_speed_rule_one_and_check(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 2")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        # Click on edit rule icon
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[6]", "XPATH checked 3")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        # Click on selection drop down button
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[2]", "XPATH checked 4")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[2]").click()
        # Select "Active" state
        wait_for_element_by_link_text_to_exist(wait, "Active", "Link text checked 5")
        time.sleep(1)
        self.driver.find_element_by_link_text("Active").click()
        # Click on update button
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[2]", "XPATH checked 6")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        # Click on confirmation button
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 7")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        # Check that rule one is in active state
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/span", "XPATH checked 8")
        time.sleep(1)
        self.assertEqual("ACTIVE", self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/span").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0040b_create_NAF_position_with_speed_that_triggs_rule_one(self):
        # Startup browser and login
        UnionVMSTestCase.test_0036_create_NAF_position_with_speed_that_triggs_rule_one(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0041_remove_speed_rule_one(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 2")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Click on delete button icon
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[8]", "XPATH checked 3")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='button'])[8]").click()
        # Click on Yes button to comfirm
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 4")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0042_check_speed_rule_one_removed(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 2")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Try to find speed rule element)
        try:
            self.assertFalse(self.driver.find_element_by_css_selector("td.statusColored.truncate-text").text)
        except NoSuchElementException:
            pass
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0043_create_one_new_asset_and_mobile_terminal(self):
        # Create new asset (7th in the list)
        create_one_new_asset_from_gui(self, 6)
        create_one_new_mobile_terminal_via_asset_tab(self, 6, 6)


    @timeout_decorator.timeout(seconds=180)
    def test_0046_generate_manual_poll_and_check(self):
        # Set Webdriver wait
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Polling tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-polling-logs", "uvms-header-menu-item-polling-logs checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-polling-logs").click()
        # Click on new New poll button
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/div/ul/li[2]/a", "XPATH checked 2")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/div/ul/li[2]/a").click()
        # Search for IRCS
        wait_for_element_by_xpath_to_exist(wait, "(//input[@type='text'])[2]", "XPATH checked 3")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(ircsValue[6])
        wait_for_element_by_xpath_to_exist(wait, "//button[@type='submit']", "XPATH checked 4")
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        # Select IRCS in the list
        wait_for_element_by_xpath_to_exist(wait, "//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/span/div/table/tbody/tr/td[6]/button", "XPATH checked 5")
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/span/div/table/tbody/tr/td[6]/button").click()
        # Click on next button
        wait_for_element_by_css_selector_to_exist(wait, "div.col-md-12.textAlignRight > button.btn.btn-primary", "CSS Selector checked 6")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.col-md-12.textAlignRight > button.btn.btn-primary").click()
        # Enter comment in comment field
        wait_for_element_by_name_to_exist(wait, "comment", "Link name checked 6")
        time.sleep(1)
        self.driver.find_element_by_name("comment").send_keys("The best comment to IRCS " + ircsValue[6])
        # Submit poll
        wait_for_element_by_css_selector_to_exist(wait, "div.col-md-8.textAlignRight > button.btn.btn-primary", "CSS Selector checked 7")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.col-md-8.textAlignRight > button.btn.btn-primary").click()
        time.sleep(3)


    @timeout_decorator.timeout(seconds=180)
    def test_0047_create_modify_and_check_asset_history(self):
        # Create new asset (34th in the list)
        create_one_new_asset_from_gui(self, 34)
        # Check new asset (34th in the list)
        check_new_asset_exists(self, 34)
        # Add the used vesselNumbers to a vesselNumberList
        vesselNumberList =[34]
        # Add secondContactVesselNumberList (Not used here)
        secondContactVesselNumberList = [0]
        # Check asset start values
        check_asset_history_list(self, vesselNumberList, secondContactVesselNumberList)
        # Modify asset parameters
        modify_one_new_asset_from_gui(self, 34, 35)
        # Add the used vesselNumbers to a vesselNumberList
        vesselNumberList =[35, 34]
        # Add secondContactVesselNumberList (Not used here)
        secondContactVesselNumberList = [0, 0]
        # Check asset values in the history list and compare these values based on the values in the vesselNumberList
        check_asset_history_list(self, vesselNumberList, secondContactVesselNumberList)


    @timeout_decorator.timeout(seconds=180)
    def test_0048_add_contact_and_check_asset_history(self):
        # Add new contact for selected asset (35th in the list)
        add_contact_to_existing_asset(self, 35, 36)
        # Add the used vesselNumbers to a vesselNumberList
        vesselNumberList =[35, 35, 34]
        # Add secondContactVesselNumberList (Only first number used)
        secondContactVesselNumberList = [36, 0, 0]
        # Check all history items for asset against values in vesselNumberList
        check_asset_history_list(self, vesselNumberList, secondContactVesselNumberList)
        # Check contacts in the contacts tab
        check_contacts_to_existing_asset(self, 35, 36)


    @timeout_decorator.timeout(seconds=180)
    def test_0049_add_notes_and_check_asset_history(self):
        # Add new notes for selected asset (35th in the list)
        add_notes_to_existing_asset_and_check(self,35)


    @timeout_decorator.timeout(seconds=180)
    def test_0050_create_one_new_mobile_terminal(self):
        # Create new Mobile Terminal (first in the list)
        create_one_new_mobile_terminal_from_gui(self, 35)
        # Add channel to mobile terminal
        add_second_channel_to_mobileterminal(self, 35, 36)


    @timeout_decorator.timeout(seconds=180)
    def test_0050b_archive_and_check_mobile_terminal(self):
        # Archive mobile terminal
        archive_one_mobile_terminal_from_gui(self, 35)
        check_mobile_terminal_archived(self, 35)


    @timeout_decorator.timeout(seconds=180)
    def test_0051_archive_and_check_asset(self):
        # Archive asset
        archive_one_asset_from_gui(self, 35)
        check_asset_archived(self, 35)


    @timeout_decorator.timeout(seconds=300)
    def test_0052_create_assets_trip_1_2_3(self):
        # Create assets, Mobile for Trip 1
        create_asset_from_file(self, 'asset1.csv')
        create_mobileterminal_from_file(self, 'asset1.csv', 'mobileterminal1.csv')
        # Create assets, Mobile for Trip 2
        create_asset_from_file(self, 'asset2.csv')
        create_mobileterminal_from_file(self, 'asset2.csv', 'mobileterminal2.csv')
        # Create assets, Mobile for Trip 3
        create_asset_from_file(self, 'asset3.csv')
        create_mobileterminal_from_file(self, 'asset3.csv', 'mobileterminal3.csv')
        # Create Trip 1-3
        create_trip_from_file(datetime.timedelta(hours=72), 'asset1.csv', 'trip1.csv')
        create_trip_from_file(datetime.timedelta(hours=72), 'asset2.csv', 'trip2.csv')
        create_trip_from_file(datetime.timedelta(hours=72), 'asset3.csv', 'trip3.csv')
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
        time.sleep(3)
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
    def test_0056_create_assets_trip_5_and_6(self):
        # Create assets, Mobile for Trip 5
        create_asset_from_file(self, 'asset5.csv')
        create_mobileterminal_from_file(self, 'asset5.csv', 'mobileterminal5.csv')
        # Create assets, Mobile for Trip 6
        create_asset_from_file(self, 'asset6.csv')
        create_mobileterminal_from_file(self, 'asset6.csv', 'mobileterminal6.csv')
        # Create Trip 5-6
        create_trip_from_file(datetime.timedelta(hours=72), 'asset5.csv', 'trip5.csv')
        create_trip_from_file(datetime.timedelta(hours=61, minutes=40), 'asset6.csv', 'trip6.csv')


    @timeout_decorator.timeout(seconds=300)
    def test_0056b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'asset5.csv', 'trip5.csv')
        reload_page_and_goto_default(self)
        time.sleep(1)
        create_report_and_check_trip_position_reports(self, 'asset6.csv', 'trip6.csv')
        time.sleep(1)


    @timeout_decorator.timeout(seconds=300)
    def test_0101_create_assets_real_trip_1(self):
        # Create assets, Mobile for RealTrip 1
        create_asset_from_file(self, 'assetreal1.csv')
        create_mobileterminal_from_file(self, 'assetreal1.csv', 'mobileterminalreal1.csv')
        # Create assets, Mobile for RealTrip 2
        create_asset_from_file(self, 'assetreal2.csv')
        create_mobileterminal_from_file(self, 'assetreal2.csv', 'mobileterminalreal2.csv')
        # Create RealTrip 1-2
        create_trip_from_file(datetime.timedelta(hours=256), 'assetreal1.csv', 'tripreal1.csv')
        create_trip_from_file(datetime.timedelta(hours=254, minutes=16), 'assetreal2.csv', 'tripreal2.csv')


    @timeout_decorator.timeout(seconds=300)
    def test_0101b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'assetreal1.csv', 'tripreal1.csv')
        reload_page_and_goto_default(self)
        time.sleep(1)
        create_report_and_check_trip_position_reports(self, 'assetreal2.csv', 'tripreal2.csv')
        time.sleep(1)



class UnionVMSTestCaseExtra(unittest.TestCase):

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


    @timeout_decorator.timeout(seconds=180)
    def test_0052_create_assets_trip_1_2_3(self):
        # Startup browser and login
        UnionVMSTestCase.test_0052_create_assets_trip_1_2_3(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0052b_create_report_and_check_asset_in_reporting_view(self):
        # Startup browser and login
        UnionVMSTestCase.test_0052b_create_report_and_check_asset_in_reporting_view(self)


    @timeout_decorator.timeout(seconds=1000)
    def test_0053_create_assets_and_mobile_terminals_21_33(self):
        # Create assets 21-33 in the list
        for x in range(21, 34):
            create_one_new_asset_from_gui(self, x)
            create_one_new_mobile_terminal_via_asset_tab(self, x, x)
            time.sleep(1)


    @timeout_decorator.timeout(seconds=180)
    def test_0055_create_assets_trip_4(self):
        # Create assets, Mobile for Trip 4
        create_asset_from_file(self, 'asset4.csv')
        create_mobileterminal_from_file(self, 'asset4.csv', 'mobileterminal4.csv')
        create_trip_from_file(datetime.timedelta(hours=72), 'asset4.csv', 'trip4.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0055b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'asset4.csv', 'trip4.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0057_create_assets_trip_7(self):
        # Create assets, Mobile for Trip 7
        create_asset_from_file(self, 'asset7.csv')
        create_mobileterminal_from_file(self, 'asset7.csv', 'mobileterminal7.csv')
        create_trip_from_file(datetime.timedelta(hours=72), 'asset7.csv', 'trip7.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0058_create_assets_trip_8(self):
        # Create assets, Mobile for Trip 8
        create_asset_from_file(self, 'asset8.csv')
        create_mobileterminal_from_file(self, 'asset8.csv', 'mobileterminal8.csv')
        create_trip_from_file(datetime.timedelta(hours=24), 'asset8.csv', 'trip8.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0059_create_assets_trip_9(self):
        # Create assets, Mobile for Trip 9
        create_asset_from_file(self, 'asset9.csv')
        create_mobileterminal_from_file(self, 'asset9.csv', 'mobileterminal9.csv')
        create_trip_from_file(datetime.timedelta(hours=48), 'asset9.csv', 'trip9.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0102_create_assets_real_trip_2(self):
        # Create assets, Mobile for RealTrip 3
        create_asset_from_file(self, 'assetreal3.csv')
        create_mobileterminal_from_file(self, 'assetreal3.csv', 'mobileterminalreal3.csv')
        # Create RealTrip 3
        create_trip_from_file(datetime.timedelta(hours=192), 'assetreal3.csv', 'tripreal3.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0102b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'assetreal3.csv', 'tripreal3.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0103_create_assets_real_trip_3(self):
        # Create assets, Mobile for RealTrip 4a and 4b
        create_asset_from_file(self, 'assetreal4.csv')
        create_mobileterminal_from_file(self, 'assetreal4.csv', 'mobileterminalreal4.csv')
        # Create RealTrip 4a-4b
        create_trip_from_file(datetime.timedelta(hours=256), 'assetreal4.csv', 'tripreal4a.csv')
        create_trip_from_file(datetime.timedelta(hours=48), 'assetreal4.csv', 'tripreal4b.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0104_create_assets_real_trip_4(self):
        # Create assets, Mobile for RealTrip 5
        create_asset_from_file(self, 'assetreal5.csv')
        create_mobileterminal_from_file(self, 'assetreal5.csv', 'mobileterminalreal5.csv')
        # Create RealTrip 3
        create_trip_from_file(datetime.timedelta(hours=48), 'assetreal5.csv', 'tripreal5.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0104b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'assetreal5.csv', 'tripreal5.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0105_create_assets_real_trip_5(self):
        # Create assets, Mobile for RealTrip 6
        create_asset_from_file(self, 'assetreal6.csv')
        create_mobileterminal_from_file(self, 'assetreal6.csv', 'mobileterminalreal6.csv')
        # Create RealTrip 3
        create_trip_from_file(datetime.timedelta(hours=72), 'assetreal6.csv', 'tripreal6.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0105b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'assetreal6.csv', 'tripreal6.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0106_create_assets_real_trip_6(self):
        # Create assets, Mobile for RealTrip 7
        create_asset_from_file(self, 'assetreal7.csv')
        create_mobileterminal_from_file(self, 'assetreal7.csv', 'mobileterminalreal7.csv')
        # Create RealTrip 3
        create_trip_from_file(datetime.timedelta(hours=270), 'assetreal7.csv', 'tripreal7.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0107_create_assets_real_trip_7(self):
        # Create assets, Mobile for RealTrip 7
        create_asset_from_file(self, 'assetreal8.csv')
        create_mobileterminal_from_file(self, 'assetreal8.csv', 'mobileterminalreal8.csv')
        # Create RealTrip 3
        create_trip_from_file(datetime.timedelta(hours=270), 'assetreal8.csv', 'tripreal8.csv')




class UnionVMSTestCaseSpecial(unittest.TestCase):
    #
    #   NOTE: Test cases in this suite shall be executed one by one. The suite is NOT intended to be run in full.
    #

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


    # Injecting MTs for Test (via Asset tab)
    @timeout_decorator.timeout(seconds=1000)
    def test_0053test_server_create_assets_and_mobile_terminals_39_52(self):
        # Create Mobile Terminals 39-52 in the list
        # Note: Assets from National asset database (Fartyg2) must be synced before executing this test case
        # Asset (Number 39) does not exist anymore. Removed from Fartyg2
        for x in range(40, 53):
            create_one_new_mobile_terminal_via_asset_tab(self, x, x)
            time.sleep(1)


    # Injecting MTs for Test
    @timeout_decorator.timeout(seconds=180)
    def test_0053test_create_one_new_mobile_terminal_and_link_to_asset(self):
        # Create Mobile Terminals 39-52 in the list
        # Note: Assets from National asset database (Fartyg2) must be synced before executing this test case
        # Asset (Number 39) does not exist anymore. Removed from Fartyg2
        for x in range(40, 53):
            create_one_new_mobile_terminal_from_gui(self, x)
            link_asset_and_mobile_terminal(self, x)



    # Injecting MTs for Dev (via Asset tab)
    @timeout_decorator.timeout(seconds=1000)
    def test_0054dev_server_create_assets_and_mobile_terminals_53_66(self):
        # Create Mobile Terminals 53-66 in the list
        # Note: Assets from National asset database (Fartyg2) must be synced before executing this test case
        # Asset (Number 53) does not exist anymore. Removed from Fartyg2
        for x in range(54, 67):
            create_one_new_mobile_terminal_via_asset_tab(self, x, x)
            time.sleep(1)


    # Injecting MTs for Dev
    @timeout_decorator.timeout(seconds=1000)
    def test_0054dev_create_one_new_mobile_terminal_and_link_to_asset(self):
        # Create Mobile Terminals 53-66 in the list
        # Note: Assets from National asset database (Fartyg2) must be synced before executing this test case
        # Asset (Number 53) does not exist anymore. Removed from Fartyg2
        for x in range(54, 67):
            create_one_new_mobile_terminal_from_gui(self, x)
            link_asset_and_mobile_terminal(self, x)


    # Create Special Asset for Prod
    @timeout_decorator.timeout(seconds=180)
    def test_0055a_create_one_new_asset(self):
        # Create special asset (Number 52 - Test3 )
        create_one_new_asset_from_gui(self, 52)


    # Injecting MTs for Prod (All parts)
    @timeout_decorator.timeout(seconds=1000)
    def test_0055b_create_several_mobile_terminals_from_file(self):
        # Create mobile terminals from file with different values and link them to existing assets that are synced in from Fartyg2
        create_mobileterminal_from_file_based_on_link_file_without_assetfilename(self, tests900FileName[1], tests900FileName[2])


    @timeout_decorator.timeout(seconds=180)
    def test_0055c_create_several_additional_channels_for_mobile_terminals(self):
        # Create assets from file with several different values for filtering
        create_addtional_channels_for_mobileterminals_without_referenceDateTime_from_file(self, tests900FileName[3])



    @timeout_decorator.timeout(seconds=900)
    def test_0108_check_asset_data_from_wsdl(self):
        # Click on asset tab
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        # Wait for Fartyg2 to sync assets into the UVMS system.
        #time.sleep(600)
        # Click on the search button
        self.driver.find_element_by_id("asset-btn-simple-search").click()
        time.sleep(3)
        # Sort in Ext Mark column.
        self.driver.find_element_by_id("asset-sort-externalMarking").click()
        time.sleep(3)
        # Click on details button
        self.driver.find_element_by_id("asset-toggle-form").click()
        time.sleep(3)
        # Read Assets fields
        assetFlagStateValue = self.driver.find_element_by_id("asset-input-flagStateCode").text
        # Check that the IRCS value is correct
        assetIRCSValue = self.driver.find_element_by_id("asset-input-ircs").get_attribute("value")
        # Check that the Name value is correct
        assetNameValue = self.driver.find_element_by_id("asset-input-name").get_attribute("value")
        # Check that External Marking Value is correct
        assetExternalMarkingValue = self.driver.find_element_by_id("asset-input-externalMarking").get_attribute("value")
        # Check that the CFR value is correct
        assetCFRValue = self.driver.find_element_by_id("asset-input-cfr").get_attribute("value")
        # Check that the IMO value is correct
        assetIMOValue = self.driver.find_element_by_id("asset-input-imo").get_attribute("value")
        # Check that the HomePort value is correct
        assetHomeportValue = self.driver.find_element_by_id("asset-input-homeport").get_attribute("value")
        # Check that the Gear Type value is correct.
        assetgearTypeValue = self.driver.find_element_by_id("asset-input-gearType").text
        # Check that the MMSI value is correct
        assetMMSIValue = self.driver.find_element_by_id("asset-input-mmsi").get_attribute("value")
        # Check that the Length Type value is correct.
        assetLengthValueValue = self.driver.find_element_by_id("asset-input-lengthValue").get_attribute("value")
        # Check that the Gross Tonnage value is correct.
        assetGrossTonnageValue = self.driver.find_element_by_id("asset-input-grossTonnage").get_attribute("value")
        # Check that the Power value is correct.
        assetPowerValue = self.driver.find_element_by_id("asset-input-power").get_attribute("value")
        # Get all info from Fartyg2 about selected asset by using CFR
        assetInfoValue = get_asset_info_from_asset_database(assetCFRValue)
        # Check values
        self.assertEqual(assetFlagStateValue, assetInfoValue['iso3AlphaNation'])
        self.assertEqual(assetIRCSValue, assetInfoValue['ircs'])
        self.assertEqual(assetExternalMarkingValue, assetInfoValue['district'])
        self.assertEqual(assetCFRValue, assetInfoValue['cfr'])
        self.assertEqual(assetNameValue, assetInfoValue['vesselName'])
        self.assertEqual(assetIMOValue, assetInfoValue['imoNumber'])
        self.assertEqual(assetHomeportValue, assetInfoValue['defaultPort']['port'])
        self.assertEqual(assetLengthValueValue, assetInfoValue['loa'])
        self.assertEqual(assetIRCSValue, assetInfoValue['ircs'])


    def test_0199_test_wsdl(self):
        # test wsdl from Fartyg2 (NATIONAL_SERVICE_ENDPOINT)
        wsdl = 'http://osbutv.havochvatten.se:8011/esb/Vessel/v2?wsdl'
        client = zeep.Client(wsdl=wsdl)
        answerValue = client.service.getVesselByCFR('SWE000007033')
        print(answerValue['vesselName'])
        print('----------------------------------------------------')
        referenceDateTime = datetime.datetime(year=2007, month=1, day=1, hour=0, minute=0, second=0)
        answerValue2 = client.service.getVesselByCFRFromHistoric('SWE000007033', referenceDateTime)
        print(answerValue2)



class UnionVMSTestCasePerformance(unittest.TestCase):


    def setUp(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(1)


    def tearDown(self):
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0001b_change_default_configuration_parameters(self):
        # Startup browser and login
        UnionVMSTestCase.test_0001b_change_default_configuration_parameters(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0052_create_assets_trip_1_2_3(self):
        # Startup browser and login
        UnionVMSTestCase.test_0052_create_assets_trip_1_2_3(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0052b_create_report_and_check_asset_in_reporting_view(self):
        # Startup browser and login
        UnionVMSTestCase.test_0052b_create_report_and_check_asset_in_reporting_view(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0501_create_one_new_asset_and_mobile_terminal(self):
        # Create new asset (7th in the list)
        create_one_new_asset_from_gui(self, 7)
        create_one_new_mobile_terminal_via_asset_tab(self, 7, 7)


    @timeout_decorator.timeout(seconds=180)
    def test_0501b_generate_multiple_NAF_positions_7(self):
        # Create many NAF positions for asset 7
        speedValue = 8
        courseValue = 35
        # Get Current Date and time in UTC
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=18)
        latStrValue = lolaPositionValues[7][0][0]
        longStrValue = lolaPositionValues[7][0][1]
        latValue = float(latStrValue)
        longValue = float(longStrValue)
        # Send x number if NAF positions
        for x in range(500):
            earlierPositionTimeValue = earlierPositionTimeValue - datetime.timedelta(minutes=1)
            earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
            earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
            latValue = latValue - 0.001
            longValue = longValue - 0.001
            nafSource = generate_NAF_string(countryValue[7], ircsValue[7], cfrValue[7], externalMarkingValue[7], str("%.3f" % latValue), str("%.3f" % longValue), speedValue, courseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[7])
            nafSourceURLcoded = urllib.parse.quote_plus(nafSource)
            totalNAFrequest = httpNAFRequestString + nafSourceURLcoded
            # Generate request
            r = requests.get(totalNAFrequest)
            # Check if request is OK (200)
            if r.ok:
                print("200 OK")
            else:
                print("Request NOT OK!")


    @timeout_decorator.timeout(seconds=180)
    def test_0501c_generate_multiple_NAF_positions_7(self):
        # Create many NAF positions for asset 7
        speedValue = 8
        courseValue = 35
        # Get Current Date and time in UTC
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=24)
        latStrValue = lolaPositionValues[7][0][0]
        longStrValue = lolaPositionValues[7][0][1]
        latValue = float(latStrValue)
        longValue = float(longStrValue)
        # Send x number if NAF positions
        for x in range(500):
            earlierPositionTimeValue = earlierPositionTimeValue + datetime.timedelta(minutes=1)
            earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
            earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
            latValue = latValue - 0.001
            longValue = longValue - 0.001
            nafSource = generate_NAF_string(countryValue[7], ircsValue[7], cfrValue[7], externalMarkingValue[7], str("%.3f" % latValue), str("%.3f" % longValue), speedValue, courseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[7])
            nafSourceURLcoded = urllib.parse.quote_plus(nafSource)
            totalNAFrequest = httpNAFRequestString + nafSourceURLcoded
            # Generate request
            r = requests.get(totalNAFrequest)
            # Check if request is OK (200)
            if r.ok:
                print("200 OK")
            else:
                print("Request NOT OK!")



    @timeout_decorator.timeout(seconds=360)
    def test_0502_create_assets_and_mobile_terminals_8_17(self):
        # Create assets 8-17 in the list
        for x in range(8, 18):
            create_one_new_asset_from_gui(self, x)
            create_one_new_mobile_terminal_via_asset_tab(self, x, x)
            time.sleep(1)


    @timeout_decorator.timeout(seconds=180)
    def test_0502b_generate_multiple_NAF_positions_8_17(self):
        # Create many NAF positions for assets 8-17
        speedValue = 8
        courseValue = 35
        # Get Current Date and time in UTC
        currentUTCValue = datetime.datetime.utcnow()
        # Generate NAF positions for assets 8-17
        for x in range(8, 18):
            print(x)
            earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=18)
            latStrValue = lolaPositionValues[x][0][0]
            longStrValue = lolaPositionValues[x][0][1]
            latValue = float(latStrValue)
            longValue = float(longStrValue)
            # Send y number if NAF positions
            for y in range(50):
                earlierPositionTimeValue = earlierPositionTimeValue + datetime.timedelta(minutes=1)
                earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
                earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
                latValue = latValue - 0.001
                longValue = longValue - 0.001
                nafSource = generate_NAF_string(countryValue[x], ircsValue[x], cfrValue[x], externalMarkingValue[x], str("%.3f" % latValue), str("%.3f" % longValue), speedValue, courseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[x])
                nafSourceURLcoded = urllib.parse.quote_plus(nafSource)
                totalNAFrequest = httpNAFRequestString + nafSourceURLcoded
                # Generate request
                r = requests.get(totalNAFrequest)
                # Check if request is OK (200)
                if r.ok:
                    print("200 OK")
                else:
                    print("Request NOT OK!")


    @timeout_decorator.timeout(seconds=180)
    def test_0502c_generate_multiple_NAF_positions_8_17(self):
        # Create many NAF positions for assets 8-17
        speedValue = 8
        courseValue = 35
        # Get Current Date and time in UTC
        currentUTCValue = datetime.datetime.utcnow()
        # Generate NAF positions for assets 8-17
        for x in range(8, 18):
            print(x)
            earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=24)
            latStrValue = lolaPositionValues[x][0][0]
            longStrValue = lolaPositionValues[x][0][1]
            latValue = float(latStrValue)
            longValue = float(longStrValue)
            # Send y number if NAF positions
            for y in range(50):
                earlierPositionTimeValue = earlierPositionTimeValue + datetime.timedelta(minutes=1)
                earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
                earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
                latValue = latValue - 0.001
                longValue = longValue - 0.001
                nafSource = generate_NAF_string(countryValue[x], ircsValue[x], cfrValue[x], externalMarkingValue[x], str("%.3f" % latValue), str("%.3f" % longValue), speedValue, courseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[x])
                nafSourceURLcoded = urllib.parse.quote_plus(nafSource)
                totalNAFrequest = httpNAFRequestString + nafSourceURLcoded
                # Generate request
                r = requests.get(totalNAFrequest)
                # Check if request is OK (200)
                if r.ok:
                    print("200 OK")
                else:
                    print("Request NOT OK!")



class UnionVMSTestCaseRules(unittest.TestCase):


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


    @timeout_decorator.timeout(seconds=180)
    def test_0001d_create_two_new_assets_and_mobile_terminals_37_38(self):
        # Create new asset (7th in the list)
        create_one_new_asset_from_gui(self, 37)
        create_one_new_mobile_terminal_via_asset_tab(self, 37, 37)
        create_one_new_asset_from_gui(self, 38)
        create_one_new_mobile_terminal_via_asset_tab(self, 38, 38)


    def test_0034_create_speed_rule_one(self):
        # Startup browser and login
        UnionVMSTestCase.test_0034_create_speed_rule_one(self)


    def test_0035_modify_speed_rule_one_and_add_cfr_condition(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 2")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        # Click on edit rule icon
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[6]", "XPATH checked 3")
        time.sleep(2)
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        # Change Rule name
        wait_for_element_by_name_to_exist(wait, "name", "Name checked 4")
        time.sleep(2)
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys("Speed > " + str(reportedSpeedDefault[0]) + " CFR")
        # Change Description
        wait_for_element_by_name_to_exist(wait, "description", "Name checked 5")
        time.sleep(1)
        self.driver.find_element_by_name("description").clear()
        self.driver.find_element_by_name("description").send_keys("Speed > " + str(reportedSpeedDefault[0]) + " CFR")
        # Click on composite and select AND statement
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[8]", "XPATH checked 6")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[8]").click()
        wait_for_element_by_link_text_to_exist(wait, "AND", "Link text checked 7")
        time.sleep(1)
        self.driver.find_element_by_link_text("AND").click()
        # Click on add a new row and enter a second Asset-->CFR statement
        wait_for_element_by_css_selector_to_exist(wait, "fieldset > div.row > div.col-md-12 > div.addMoreLink", "CSS Selector checked 8")
        time.sleep(1)
        self.driver.find_element_by_css_selector("fieldset > div.row > div.col-md-12 > div.addMoreLink").click()
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[9]", "XPATH checked 9")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[9]").click()
        wait_for_element_by_xpath_to_exist(wait, "(//a[contains(text(),'(')])[13]", "XPATH checked 10")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//a[contains(text(),'(')])[13]").click()
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[10]", "XPATH checked 11")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[10]").click()
        wait_for_element_by_xpath_to_exist(wait, "(//a[contains(text(),'Asset')])[4]", "XPATH checked 12")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//a[contains(text(),'Asset')])[4]").click()
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[11]", "XPATH checked 13")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[11]").click()
        wait_for_element_by_link_text_to_exist(wait, "CFR", "Link text checked 14")
        time.sleep(1)
        self.driver.find_element_by_link_text("CFR").click()
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[12]", "XPATH checked 15")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[12]").click()
        wait_for_element_by_xpath_to_exist(wait, "(//a[contains(text(),'equal to')])[3]", "XPATH checked 16")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//a[contains(text(),'equal to')])[3]").click()
        wait_for_element_by_css_selector_to_exist(wait, "div.autoSuggestionWrapper.fullWidthDropdown > input[name=\"value\"]", "CSS Selector checked 17")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.autoSuggestionWrapper.fullWidthDropdown > input[name=\"value\"]").clear()
        self.driver.find_element_by_css_selector("div.autoSuggestionWrapper.fullWidthDropdown > input[name=\"value\"]").send_keys(cfrValue[37])
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[13]", "XPATH checked 18")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[13]").click()
        wait_for_element_by_xpath_to_exist(wait, "(//a[contains(text(),')')])[13]", "XPATH checked 19")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//a[contains(text(),')')])[13]").click()
        wait_for_element_by_css_selector_to_exist(wait, "span.link", "CSS Selector checked 20")
        time.sleep(1)
        self.driver.find_element_by_css_selector("span.link").click()
        # Click on Update rule button
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[4]", "XPATH checked 21")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        # Click on Yes button
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 22")
        time.sleep(2)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0036_generate_NAF_position_that_not_triggs_rule(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Generate NAF position report that satisfies the speed part but not the CFR part of the modified rule
        # Set Current Date and time in UTC 1 hours back
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
        earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
        earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')
        # Set Long/Lat
        latStrValue = lolaPositionValues[7][0][0]
        longStrValue = lolaPositionValues[7][0][1]
        # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
        nafSource = generate_NAF_string(countryValue[38], ircsValue[38], cfrValue[38], externalMarkingValue[38], latStrValue, longStrValue, reportedSpeedDefault[1], reportedCourseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[38])
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
        # Click on Alert tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Click on Notifications tab
        wait_for_element_by_link_text_to_exist(wait, "NOTIFICATIONS", "Link text checked 2")
        time.sleep(2)
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(5)
        # Try to find speed rule name in the Notification list (Should not exist)
        try:
            self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + " CFR" + "\"]").text)
        except NoSuchElementException:
            pass
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0036b_delay_one_minute(self):
        # Delay test case to secure minute change between generated NAF messages. Otherwise the MAF messages can be interpreted as duplicated messages.
        time.sleep(60)


    @timeout_decorator.timeout(seconds=180)
    def test_0037_generate_NAF_position_that_not_triggs_rule(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Generate NAF position report that not satisfies the speed part but the CFR part of the modified rule
        # Set Current Date and time in UTC 1 hours back
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
        earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
        earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')
        # Set Long/Lat
        latStrValue = lolaPositionValues[6][0][0]
        longStrValue = lolaPositionValues[6][0][1]
        # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
        nafSource = generate_NAF_string(countryValue[37], ircsValue[37], cfrValue[37], externalMarkingValue[37], latStrValue, longStrValue, reportedSpeedValue, reportedCourseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[37])
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
        # Click on Alert tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Click on Notifications tab
        wait_for_element_by_link_text_to_exist(wait, "NOTIFICATIONS", "Link text checked 2")
        time.sleep(2)
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(5)
        # Try to find speed rule name in the Notification list (Should not exist)
        try:
            self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + " CFR" + "\"]").text)
        except NoSuchElementException:
            pass
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0037b_delay_one_minute(self):
        # Delay test case to secure minute change between generated NAF messages. Otherwise the MAF messages can be interpreted as duplicated messages.
        time.sleep(60)


    @timeout_decorator.timeout(seconds=180)
    def test_0038_generate_NAF_position_that_triggs_rule(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Generate NAF position report that triggs the modified rule
        # Set Current Date and time in UTC 1 hours back
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
        earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
        earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')
        # Set Long/Lat
        latStrValue = lolaPositionValues[6][0][0]
        longStrValue = lolaPositionValues[6][0][1]
        # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
        nafSource = generate_NAF_string(countryValue[37], ircsValue[37], cfrValue[37], externalMarkingValue[37], latStrValue, longStrValue, reportedSpeedDefault[1], reportedCourseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[37])
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
        # Click on Alert tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Click on Notifications tab
        wait_for_element_by_link_text_to_exist(wait, "NOTIFICATIONS", "Link text checked 2")
        time.sleep(2)
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        # Check Asset and Rule names
        wait_for_element_by_link_text_to_exist(wait, vesselName[37], "Link text checked 3")
        time.sleep(3)
        self.assertEqual(vesselName[37], self.driver.find_element_by_link_text(vesselName[37]).text)
        self.assertEqual("Speed > " + str(reportedSpeedDefault[0]) + " CFR", self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + " CFR" + "\"]").text)
        # Click on details button
        wait_for_element_by_xpath_to_exist(wait, "//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button", "XPATH checked 4")
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        # Check Position parameters
        wait_for_element_by_css_selector_to_exist(wait, "div.value", "CSS Selector checked 5")
        time.sleep(3)
        self.assertEqual(countryValue[37], self.driver.find_element_by_css_selector("div.value").text)
        self.assertEqual(ircsValue[37], self.driver.find_element_by_xpath("//div[2]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[37], self.driver.find_element_by_xpath("//div[2]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue[37], self.driver.find_element_by_xpath("//div[2]/div[2]/div[4]/div").text)
        self.assertEqual(vesselName[37], self.driver.find_element_by_xpath("//div[2]/div[5]/div").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(lolaPositionValues[6][0][0], self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(lolaPositionValues[6][0][1], self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedDefault[1]) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        wait_for_element_by_xpath_to_exist(wait, "//div[7]/div/div/div/div/i", "XPATH checked 6")
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0039_modify_speed_rule_one_and_change_cfr_condition(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 2")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        # Click on edit rule icon
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[6]", "XPATH checked 3")
        time.sleep(2)
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        # Change Rule name
        wait_for_element_by_name_to_exist(wait, "name", "Name checked 4")
        time.sleep(2)
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys("Speed > " + str(reportedSpeedDefault[0]) + " NEW CFR")
        # Change Description
        wait_for_element_by_name_to_exist(wait, "description", "Name checked 5")
        time.sleep(1)
        self.driver.find_element_by_name("description").clear()
        self.driver.find_element_by_name("description").send_keys("Speed > " + str(reportedSpeedDefault[0]) + " NEW CFR")
        # Change the CFR value
        wait_for_element_by_css_selector_to_exist(wait, "div.autoSuggestionWrapper.fullWidthDropdown > input[name=\"value\"]", "CSS Selector checked 6")
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.autoSuggestionWrapper.fullWidthDropdown > input[name=\"value\"]").clear()
        self.driver.find_element_by_css_selector("div.autoSuggestionWrapper.fullWidthDropdown > input[name=\"value\"]").send_keys(cfrValue[38])
        # Click on Update rule button
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[4]", "XPATH checked 7")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        # Click on Yes button
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 8")
        time.sleep(2)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0040_generate_NAF_position_that_not_triggs_rule(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Generate NAF position report that not satisfies the CFR part of the modified rule
        # Set Current Date and time in UTC 1 hours back
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
        earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
        earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')
        # Set Long/Lat
        latStrValue = lolaPositionValues[6][0][0]
        longStrValue = lolaPositionValues[6][0][1]
        # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
        nafSource = generate_NAF_string(countryValue[37], ircsValue[37], cfrValue[37], externalMarkingValue[37], latStrValue, longStrValue, reportedSpeedDefault[1], reportedCourseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[37])
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
        # Click on Alert tab
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Click on Notifications tab
        wait_for_element_by_link_text_to_exist(wait, "NOTIFICATIONS", "Link text checked 2")
        time.sleep(2)
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(5)
        # Try to find speed rule name in the Notification list (Should not exist)
        try:
            self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + " NEW CFR" + "\"]").text)
        except NoSuchElementException:
            pass
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0041_modify_speed_rule_one_and_change_condition_from_AND_to_OR(self):
        # Set wait time for web driver
        wait = WebDriverWait(self.driver, WebDriverWaitTimeValue)
        # Select Alerts tab (Holding Table)
        wait_for_element_by_id_to_exist(wait, "uvms-header-menu-item-holding-table", "uvms-header-menu-item-holding-table checked 1")
        time.sleep(1)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        # Select Alerts tab (Rules)
        wait_for_element_by_xpath_to_exist(wait, "//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a", "XPATH checked 2")
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        # Click on edit rule icon
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='button'])[6]", "XPATH checked 3")
        time.sleep(2)
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        # Change Rule name
        wait_for_element_by_name_to_exist(wait, "name", "Name checked 4")
        time.sleep(2)
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys("Speed > " + str(reportedSpeedDefault[0]) + " NEW2 CFR")
        # Change Description
        wait_for_element_by_name_to_exist(wait, "description", "Name checked 5")
        time.sleep(1)
        self.driver.find_element_by_name("description").clear()
        self.driver.find_element_by_name("description").send_keys("Speed > " + str(reportedSpeedDefault[0]) + " NEW2 CFR")
        # Change condition state from AND to OR
        wait_for_element_by_xpath_to_exist(wait, "(//button[@id=''])[8]", "XPATH checked 6")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[8]").click()
        wait_for_element_by_link_text_to_exist(wait, "OR", "Link text checked 7")
        time.sleep(1)
        self.driver.find_element_by_link_text("OR").click()
        # Click on Update rule button
        wait_for_element_by_xpath_to_exist(wait, "(//button[@type='submit'])[4]", "XPATH checked 8")
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        # Click on Yes button
        wait_for_element_by_css_selector_to_exist(wait, "div.modal-footer > button.btn.btn-primary", "CSS Selector checked 9")
        time.sleep(2)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0042_generate_NAF_position_that_triggs_rule_on_cfr_part(self):
        # Generate NAF position report that triggs the CFR part of modified rule. That should now trigg the rule

        # Set Current Date and time in UTC 1 hours back
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
        earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
        earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')

        # Set Long/Lat
        latStrValue = lolaPositionValues[7][0][0]
        longStrValue = lolaPositionValues[7][0][1]

        # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
        nafSource = generate_NAF_string(countryValue[38], ircsValue[38], cfrValue[38], externalMarkingValue[38], latStrValue, longStrValue, reportedSpeedValue, reportedCourseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[38])
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

        # Click on Alert tab
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(8)
        # Click on Notifications tab
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(8)
        # Check Asset and Rule names
        self.assertEqual(vesselName[37], self.driver.find_element_by_link_text(vesselName[37]).text)
        self.assertEqual("Speed > " + str(reportedSpeedDefault[0]) + " NEW2 CFR", self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + " NEW2 CFR" + "\"]").text)
        # Click on details button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        time.sleep(2)
        # Check Position parameters
        self.assertEqual(countryValue[38], self.driver.find_element_by_css_selector("div.value").text)
        self.assertEqual(ircsValue[38], self.driver.find_element_by_xpath("//div[2]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[38], self.driver.find_element_by_xpath("//div[2]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue[38], self.driver.find_element_by_xpath("//div[2]/div[2]/div[4]/div").text)
        self.assertEqual(vesselName[38], self.driver.find_element_by_xpath("//div[2]/div[5]/div").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(lolaPositionValues[7][0][0], self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(lolaPositionValues[7][0][1], self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedValue) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(5)

    @timeout_decorator.timeout(seconds=180)
    def test_0042b_delay_one_minute(self):
        # Delay test case to secure minute change between generated NAF messages. Otherwise the MAF messages can be interpreted as duplicated messages.
        time.sleep(60)


    @timeout_decorator.timeout(seconds=180)
    def test_0043_generate_NAF_position_that_triggs_rule_on_speed_part(self):
        # Generate NAF position report that triggs the speed part of modified rule. That should now trigg the rule

        # Set Current Date and time in UTC 1 hours back
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
        earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
        earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')

        # Set Long/Lat
        latStrValue = lolaPositionValues[6][0][0]
        longStrValue = lolaPositionValues[6][0][1]

        # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
        nafSource = generate_NAF_string(countryValue[37], ircsValue[37], cfrValue[37], externalMarkingValue[37], latStrValue, longStrValue, reportedSpeedDefault[1], reportedCourseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[37])
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

        # Click on Alert tab
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(8)
        # Click on Notifications tab
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(8)
        # Check Asset and Rule names
        self.assertEqual(vesselName[37], self.driver.find_element_by_link_text(vesselName[37]).text)
        self.assertEqual("Speed > " + str(reportedSpeedDefault[0]) + " NEW2 CFR", self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + " NEW2 CFR" + "\"]").text)
        # Click on details button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        time.sleep(2)
        # Check Position parameters
        self.assertEqual(countryValue[37], self.driver.find_element_by_css_selector("div.value").text)
        self.assertEqual(ircsValue[37], self.driver.find_element_by_xpath("//div[2]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[37], self.driver.find_element_by_xpath("//div[2]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue[37], self.driver.find_element_by_xpath("//div[2]/div[2]/div[4]/div").text)
        self.assertEqual(vesselName[37], self.driver.find_element_by_xpath("//div[2]/div[5]/div").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(lolaPositionValues[6][0][0], self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(lolaPositionValues[6][0][1], self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedDefault[1]) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(5)


    def test_0044_remove_speed_rule_one(self):
        # Startup browser and login
        UnionVMSTestCase.test_0041_remove_speed_rule_one(self)


    def test_0050_create_user_area(self):
        # Startup browser and login
        # Click on Area Management tab
        self.driver.find_element_by_id("uvms-header-menu-item-areas").click()
        time.sleep(3)
        # Click on New are button
        self.driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        time.sleep(2)
        # Click on Coordinates button
        self.driver.find_element_by_css_selector("div.editingTools.text-center > div.btn-group > button.btn.btn-default").click()
        time.sleep(2)
        # Click and select WGS84 projection
        self.driver.find_element_by_xpath("//div[@id='area-management-side-panel']/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div/span").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("WGS 84").click()
        time.sleep(1)

        # Open saved csv file and read all area elements
        userAreaAllrows = get_elements_from_file(userAreaFileName)
        print(userAreaAllrows)
        # create_one_new_asset
        for x in range(0, len(userAreaAllrows)):
            # Click on "plus" button
            self.driver.find_element_by_xpath("//div[@id='area-management-side-panel']/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/button").click()
            time.sleep(1)
            # Enter Long Lat position
            self.driver.find_element_by_xpath("(//input[@type='text'])[" + str(6 + x*2) + "]").clear()
            self.driver.find_element_by_xpath("(//input[@type='text'])[" + str(6 + x*2) + "]").send_keys(userAreaAllrows[x][0])
            time.sleep(1)
            self.driver.find_element_by_xpath("(//input[@type='text'])[" + str(7 + x*2) + "]").clear()
            self.driver.find_element_by_xpath("(//input[@type='text'])[" + str(7 + x*2) + "]").send_keys(userAreaAllrows[x][1])
            time.sleep(1)
        # Click on Apply button
        self.driver.find_element_by_xpath("//div[@id='area-management-side-panel']/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/div/button[2]").click()
        time.sleep(1)
        # Enter User Area Name
        self.driver.find_element_by_name("userAreaName").clear()
        self.driver.find_element_by_name("userAreaName").send_keys(userAreaName)
        time.sleep(1)
        # Enter User Area Type Name
        self.driver.find_element_by_name("comboEditableInput").clear()
        self.driver.find_element_by_name("comboEditableInput").send_keys(userAreaTypeName)
        time.sleep(1)
        # Click on Save button to save the new User Area.
        self.driver.find_element_by_xpath("//div[@id='area-management-side-panel']/div/div[3]/div/div[2]/div[3]/div/button").click()
        time.sleep(3)



    @timeout_decorator.timeout(seconds=180)
    def test_0051_create_user_area_rule_one(self):
        # Select Alerts tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(1)
        # Select Alerts tab (Rules)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Click on create button
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(2)
        # Enter Rule name
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys(userAreaRuleNamne)
        time.sleep(1)
        # Enter Description
        self.driver.find_element_by_name("description").clear()
        self.driver.find_element_by_name("description").send_keys(userAreaRuleNamne)
        time.sleep(1)
        # Enter 1st part of the rule
        self.driver.find_element_by_xpath("(//button[@id=''])[3]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("(").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[4]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Area").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[5]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Type").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[7]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("USERAREA").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[8]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text(")").click()
        time.sleep(2)
        # Select "AND" statement
        self.driver.find_element_by_xpath("(//button[@id=''])[9]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("AND").click()
        time.sleep(2)
        # Click on add a new row and enter a second part of the rule statement
        self.driver.find_element_by_css_selector("fieldset > div.row > div.col-md-12 > div.addMoreLink").click()
        time.sleep(1)

        # Enter 2nd part of the rule
        self.driver.find_element_by_xpath("(//button[@id=''])[10]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("(").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[11]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Area").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div/div/form/fieldset[1]/div[2]/div[3]/table/tbody/tr[2]/td[5]/div/div/input").send_keys(userAreaName)
        #self.driver.find_element_by_name("value").send_keys(userAreaName)
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[14]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text(")").click()
        time.sleep(2)
        # Click on "Test rule definition"
        self.driver.find_element_by_css_selector("span.link").click()
        time.sleep(1)
        # Check validation of Rule
        self.assertEqual("Rule definition is valid.", self.driver.find_element_by_css_selector("span.success").text)
        time.sleep(2)
        # Submit the new Rule
        self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(5)
        # Change "Notify by email" to Yes
        self.driver.find_element_by_xpath("(//button[@id=''])[2]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Yes").click()
        time.sleep(5)


    @timeout_decorator.timeout(seconds=180)
    def test_0052_create_one_new_asset_and_mobile_terminal_34(self):
        # Create new asset (7th in the list)
        create_one_new_asset_from_gui(self, 34)
        create_one_new_mobile_terminal_via_asset_tab(self, 34, 34)



    @timeout_decorator.timeout(seconds=180)
    def test_0053_generate_NAF_position_that_not_triggs_rule(self):
        # Generate NAF position report that is outside defined user area.  The rule should NOT be triggered.

        # Set Current Date and time in UTC 1 hours back
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
        earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
        earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')

        # Set Long/Lat
        latStrValue = lolaPositionAreaValues[2][0]
        longStrValue = lolaPositionAreaValues[2][1]

        # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
        nafSource = generate_NAF_string(countryValue[34], ircsValue[34], cfrValue[34], externalMarkingValue[34], latStrValue, longStrValue, reportedSpeedDefault[1], reportedCourseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[34])
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

        # Click on Alert tab
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(5)
        # Click on Notifications tab
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(5)
        # Try to find speed rule name in the Notification list (Should not exist)
        try:
            self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + userAreaRuleNamne + "\"]").text)
        except NoSuchElementException:
            pass
        time.sleep(2)




    @timeout_decorator.timeout(seconds=180)
    def test_0054_generate_NAF_position_that_triggs_rule(self):
        # Generate NAF position report that is inside defined user area. The rule should be triggered.

        # Set Current Date and time in UTC 1 hours back
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
        earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
        earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')

        # Set Long/Lat
        latStrValue = lolaPositionAreaValues[4][0]
        longStrValue = lolaPositionAreaValues[4][1]

        # generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue)
        nafSource = generate_NAF_string(countryValue[34], ircsValue[34], cfrValue[34], externalMarkingValue[34], latStrValue, longStrValue, reportedSpeedDefault[1], reportedCourseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[34])
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

        # Click on Alert tab
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(8)
        # Click on Notifications tab
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(8)
        # Check Asset and Rule names
        self.assertEqual(vesselName[34], self.driver.find_element_by_link_text(vesselName[34]).text)
        self.assertEqual(userAreaRuleNamne, self.driver.find_element_by_css_selector("td[title=\"" + userAreaRuleNamne + "\"]").text)
        # Click on details button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        time.sleep(5)
        # Check Position parameters
        self.assertEqual(countryValue[34], self.driver.find_element_by_css_selector("div.value").text)
        self.assertEqual(ircsValue[34], self.driver.find_element_by_xpath("//div[2]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[34], self.driver.find_element_by_xpath("//div[2]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue[34], self.driver.find_element_by_xpath("//div[2]/div[2]/div[4]/div").text)
        self.assertEqual(vesselName[34], self.driver.find_element_by_xpath("//div[2]/div[5]/div").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(latStrValue, self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(longStrValue, self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedDefault[1]) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(5)




class UnionVMSTestCaseFiltering(unittest.TestCase):


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


    @timeout_decorator.timeout(seconds=180)
    def test_0201_create_several_assets_for_filtering(self):
        # Create assets from file with several different values for filtering
        create_asset_from_file(self, 'assets2xxxx.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0202_advanced_search_of_assets_fs_geartypes(self):
        # Test case tests advanced search functions filtering on flag state and geartypes. Also saving this search to group.
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('assets2xxxx.csv')
        # Click on asset tab
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on advanced search
        self.driver.find_element_by_css_selector("#asset-toggle-search-view > span").click()
        time.sleep(1)
        # Click on search button
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(3)
        # Click on sort IRCS
        self.driver.find_element_by_id("asset-sort-ircs").click()
        time.sleep(1)
        # Search for all assets with Flag State (F.S.) called "NOR"
        self.driver.find_element_by_id("asset-dropdown-search-flagstates").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-search-flagstates-item-1").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-search-flagstates").click()
        time.sleep(1)
        # Click on search button
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(5)
        # Get all assets with Flag State (F.S.) called "NOR" in the asset list.
        filteredAssetList = get_selected_elements_in_list_from_mainList(assetAllrows, 17, str(1))
        # Get the remaining assets in the filteredAssetList
        filteredAssetListNonSelected = get_remaining_elements_from_main_list(assetAllrows, filteredAssetList)

        # Check that assets in filteredAssetListSelected is presented in the Asset List view
        for x in range(0, len(filteredAssetList)):
            self.assertEqual(flagStateIndex[int(filteredAssetList[x][17])], self.driver.find_element_by_css_selector("td[title=\"" + flagStateIndex[int(filteredAssetList[x][17])] + "\"]").text)
            self.assertEqual(filteredAssetList[x][3], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetList[x][3] + "\"]").text)
            self.assertEqual(filteredAssetList[x][1], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetList[x][1] + "\"]").text)
            self.assertEqual(filteredAssetList[x][0], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetList[x][0] + "\"]").text)
            self.assertEqual(filteredAssetList[x][2], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetList[x][2] + "\"]").text)
            # self.assertEqual(gearTypeIndex[int(filteredAssetList[x][8])], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeIndex[int(filteredAssetList[x][8])] + "\"]").text)
            self.assertEqual(gearTypeIndex[int(filteredAssetList[x][8])], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[7]").text)
            self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)

        # Check that Asset from non-selected asset list (filteredAssetListNonSelected) does not exist in the visual asset list view.
        for x in range(0, len(filteredAssetListNonSelected)):
            try:
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][1] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][0] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][2] + "\"]").text)
            except NoSuchElementException:
                pass

        # Search for all assets with Flag State (F.S.) called "NOR" and gear type called "Pelagic"
        self.driver.find_element_by_id("asset-dropdown-search-gearType").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-search-gearType-item-2").click()
        time.sleep(1)
        # Click on search button
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(3)

        # Save current advanced filter to group
        self.driver.find_element_by_css_selector("#asset-btn-save-search > span").click()
        time.sleep(1)
        self.driver.find_element_by_name("name").clear()
        time.sleep(1)
        self.driver.find_element_by_name("name").send_keys(groupName[3])
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(1)

        # Get all assets with geartype Pelagic(2) in the filteredAssetList.
        filteredAssetListSelected = get_selected_elements_in_list_from_mainList(filteredAssetList, 8, str(2))
        # Get the remaining assets with geartype that is NOT Pelagic(2) in the filteredAssetList
        filteredAssetListNonSelected = get_remaining_elements_from_main_list(assetAllrows, filteredAssetListSelected)

        # Check that assets in filteredAssetListSelected is presented in the Asset List view
        for x in range(0, len(filteredAssetListSelected)):
            self.assertEqual(flagStateIndex[int(filteredAssetListSelected[x][17])], self.driver.find_element_by_css_selector("td[title=\"" + flagStateIndex[int(filteredAssetListSelected[x][17])] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][3], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][3] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][1], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][1] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][0], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][0] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][2], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][2] + "\"]").text)
            self.assertEqual(gearTypeIndex[int(filteredAssetListSelected[x][8])], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeIndex[int(filteredAssetListSelected[x][8])] + "\"]").text)
            self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)

        # Check that Asset from non-selected asset list (filteredAssetListNonSelected) does not exist in the visual asset list view.
        for x in range(0, len(filteredAssetListNonSelected)):
            try:
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][1] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][0] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][2] + "\"]").text)
            except NoSuchElementException:
                pass
        time.sleep(4)



    @timeout_decorator.timeout(seconds=180)
    def test_0202b_check_group_exported_to_file(self):
        # Test case checks that group from test_0202 is exported to file correctly.
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('assets2xxxx.csv')
        # Get all assets with Flag State (F.S.) called "NOR" in the asset list.
        filteredAssetList = get_selected_elements_in_list_from_mainList(assetAllrows, 17, str(1))
        # Get all assets with geartype Pelagic(2) in the filteredAssetList.
        filteredAssetListSelected = get_selected_elements_in_list_from_mainList(filteredAssetList, 8, str(2))
        # Get the remaining assets with geartype that is NOT Pelagic(2) in the filteredAssetList
        filteredAssetListNonSelected = get_remaining_elements_from_main_list(assetAllrows, filteredAssetListSelected)
        # Click on asset tab
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on sort IRCS
        self.driver.find_element_by_id("asset-sort-ircs").click()
        time.sleep(1)
        # Select Group 4 filter search
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search-item-0").click()
        time.sleep(5)
        # Select all assets in the list
        self.driver.find_element_by_id("asset-checkbox-select-all").click()
        time.sleep(2)
        # Save path to current dir
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Change to Download folder for current user
        downloadPath = get_download_path()
        os.chdir(downloadPath)
        print(os.path.abspath(os.path.dirname(__file__)))
        # Check if file exists. If so remove it
        if os.path.exists(assetFileName):
            os.remove(assetFileName)
        # Select Action "Export selection"
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Open saved csv file and read all elements to "allrows"
        allrows = get_elements_from_file_without_deleting_paths_and_rows(assetFileName)
        # Deleting header row
        del allrows[0]
        # Change back the path to current dir
        os.chdir(cwd)
        print(cwd)
        # Sort the allrows list (3rd Column)
        allrows.sort(key=lambda x: x[3])
        # Check that the elements in csv file is correct
        # Adapt filteredAssetListSelected list to the "format" as for exported CSV files
        # The result is saved in filteredAssetListSelectedCSVformat
        filteredAssetListSelectedCSVformat = adapt_asset_list_to_exported_CSV_file_standard(filteredAssetListSelected)
        # Sort the filteredAssetListSelectedCSVformat list (3rd Column)
        filteredAssetListSelectedCSVformat.sort(key=lambda x: x[3])
        # Check filteredAssetListSelectedCSVformat in allrows row by row
        resultExists = check_sublist_in_other_list_if_it_exists(filteredAssetListSelectedCSVformat, allrows)
        # Check if resultExists list includes just True states
        print(resultExists)
        # The test case shall pass if ALL boolean values in resultExists list are True
        self.assertTrue(checkAllTrue(resultExists))
        # Adapt filteredAssetListNonSelected list to the "format" as for exported CSV files
        # The result is saved in filteredAssetListNonSelectedCSVformat
        filteredAssetListNonSelectedCSVformat = adapt_asset_list_to_exported_CSV_file_standard(filteredAssetListNonSelected)
        # Sort the filteredAssetListNonSelectedCSVformat list (3rd Column)
        filteredAssetListNonSelectedCSVformat.sort(key=lambda x: x[3])
        # Check filteredAssetListNonSelectedCSVformat in allrows row by row
        resultExists = check_sublist_in_other_list_if_it_exists(filteredAssetListNonSelectedCSVformat, allrows)
        print(resultExists)
        # The test case shall pass if ALL of the boolean values in resultExists list are False
        self.assertFalse(checkAnyTrue(resultExists))
        time.sleep(5)


    @timeout_decorator.timeout(seconds=180)
    def test_0203_advanced_search_of_assets_length_power(self):
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('assets2xxxx.csv')
        # Click on asset tab
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on advanced search
        self.driver.find_element_by_css_selector("#asset-toggle-search-view > span").click()
        time.sleep(1)
        # Click on search button
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(3)
        # Click on sort IRCS
        self.driver.find_element_by_id("asset-sort-ircs").click()
        time.sleep(1)

        # Search for all assets with Length inteval (12-14,99) and Power interval "0-99"
        self.driver.find_element_by_id("asset-dropdown-search-lengthValue").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-search-lengthValue-item-1").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-search-power").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-search-power-item-0").click()
        time.sleep(1)
        # Click on search button
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(3)

        # Save current advanced filter to group
        self.driver.find_element_by_css_selector("#asset-btn-save-search > span").click()
        time.sleep(1)
        self.driver.find_element_by_name("name").clear()
        time.sleep(1)
        self.driver.find_element_by_name("name").send_keys(groupName[4])
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(5)

        # Get all assets with Length interval 12-14.99 in the assetAllrows.
        filteredAssetListSelected = get_selected_assets_from_assetList_interval(assetAllrows, 9, 12, 15)
        # Get all assets with Power interval 0-99 in the filteredAssetListSelected.
        filteredAssetListSelected = get_selected_assets_from_assetList_interval(filteredAssetListSelected, 11, 0, 100)
        # Get remaining assets that is found in assetAllrows but not in filteredAssetListSelected
        filteredAssetListNonSelected = get_remaining_elements_from_main_list(assetAllrows, filteredAssetListSelected)

        # Reload page
        self.driver.refresh()
        time.sleep(7)
        # Click on sort IRCS
        self.driver.find_element_by_id("asset-sort-ircs").click()
        time.sleep(1)
        # Select Group 5 filter search
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search-item-1").click()
        time.sleep(7)

        # Check that assets in filteredAssetListSelected is presented in the Asset List view
        for x in range(0, len(filteredAssetListSelected)):
            self.assertEqual(flagStateIndex[int(filteredAssetListSelected[x][17])], self.driver.find_element_by_css_selector("td[title=\"" + flagStateIndex[int(filteredAssetListSelected[x][17])] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][3], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][3] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][1], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][1] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][0], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][0] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][2], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][2] + "\"]").text)
            self.assertEqual(gearTypeIndex[int(filteredAssetListSelected[x][8])], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeIndex[int(filteredAssetListSelected[x][8])] + "\"]").text)
            self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)

        # Check that Asset from non-selected asset list (filteredAssetListNonSelected) does not exist in the visual asset list view.
        for x in range(0, len(filteredAssetListNonSelected)):
            try:
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][1] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][0] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][2] + "\"]").text)
            except NoSuchElementException:
                pass
        time.sleep(4)


    @timeout_decorator.timeout(seconds=180)
    def test_0203b_check_group_exported_to_file(self):
        # Test case checks that group from test_0203 is exported to file correctly.
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('assets2xxxx.csv')
        # Get all assets with Length interval 12-14.99 in the assetAllrows.
        filteredAssetListSelected = get_selected_assets_from_assetList_interval(assetAllrows, 9, 12, 15)
        # Get all assets with Power interval 0-99 in the filteredAssetListSelected.
        filteredAssetListSelected = get_selected_assets_from_assetList_interval(filteredAssetListSelected, 11, 0, 100)
        # Get remaining assets that is found in assetAllrows but not in filteredAssetListSelected
        filteredAssetListNonSelected = get_remaining_elements_from_main_list(assetAllrows, filteredAssetListSelected)
        # Click on asset tab
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on sort IRCS
        self.driver.find_element_by_id("asset-sort-ircs").click()
        time.sleep(1)
        # Select Group 5 filter search
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search-item-1").click()
        time.sleep(5)
        # Select all assets in the list
        self.driver.find_element_by_id("asset-checkbox-select-all").click()
        time.sleep(2)
        # Save path to current dir
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Change to Download folder for current user
        downloadPath = get_download_path()
        os.chdir(downloadPath)
        print(os.path.abspath(os.path.dirname(__file__)))
        # Check if file exists. If so remove it
        if os.path.exists(assetFileName):
            os.remove(assetFileName)
        # Select Action "Export selection"
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Open saved csv file and read all elements to "allrows"
        allrows = get_elements_from_file_without_deleting_paths_and_rows(assetFileName)
        # Deleting header row
        del allrows[0]
        # Change back the path to current dir
        os.chdir(cwd)
        print(cwd)
        # Sort the allrows list (3rd Column)
        allrows.sort(key=lambda x: x[3])
        # Check that the elements in csv file is correct
        # Adapt filteredAssetListSelected list to the "format" as for exported CSV files
        # The result is saved in filteredAssetListSelectedCSVformat
        filteredAssetListSelectedCSVformat = adapt_asset_list_to_exported_CSV_file_standard(filteredAssetListSelected)
        # Sort the filteredAssetListSelectedCSVformat list (3rd Column)
        filteredAssetListSelectedCSVformat.sort(key=lambda x: x[3])
        # Check filteredAssetListSelectedCSVformat in allrows row by row
        resultExists = check_sublist_in_other_list_if_it_exists(filteredAssetListSelectedCSVformat, allrows)
        # Check if resultExists list includes just True states
        print(resultExists)
        # The test case shall pass if ALL boolean values in resultExists list are True
        self.assertTrue(checkAllTrue(resultExists))
        # Adapt filteredAssetListNonSelected list to the "format" as for exported CSV files
        # The result is saved in filteredAssetListNonSelectedCSVformat
        filteredAssetListNonSelectedCSVformat = adapt_asset_list_to_exported_CSV_file_standard(filteredAssetListNonSelected)
        # Sort the filteredAssetListNonSelectedCSVformat list (3rd Column)
        filteredAssetListNonSelectedCSVformat.sort(key=lambda x: x[3])
        # Check filteredAssetListNonSelectedCSVformat in allrows row by row
        resultExists = check_sublist_in_other_list_if_it_exists(filteredAssetListNonSelectedCSVformat, allrows)
        print(resultExists)
        # The test case shall pass if ALL of the boolean values in resultExists list are False
        self.assertFalse(checkAnyTrue(resultExists))
        time.sleep(5)


    @timeout_decorator.timeout(seconds=180)
    def test_0204_advanced_search_of_assets_extmark_port(self):
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('assets2xxxx.csv')
        # Click on asset tab
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on advanced search
        self.driver.find_element_by_css_selector("#asset-toggle-search-view > span").click()
        time.sleep(1)
        # Click on search button
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(3)
        # Click on sort IRCS
        self.driver.find_element_by_id("asset-sort-ircs").click()
        time.sleep(1)

        # Search for all assets with Ext Mark value
        self.driver.find_element_by_id("asset-input-search-externalMarking").clear()
        self.driver.find_element_by_id("asset-input-search-externalMarking").send_keys(externalMarkingSearchValue[0])
        time.sleep(1)
        # Click on search button
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(3)

        # Get all assets with the marked value in the External Marking field in the asset list.
        filteredAssetList = get_selected_elements_in_list_from_mainList(assetAllrows, 3, externalMarkingSearchValue[0])
        # Sort the asset list
        filteredAssetList.sort(key=lambda x: x[3])

        # Get the remaining assets in the filteredAssetList
        filteredAssetListNonSelected = get_remaining_elements_from_main_list(assetAllrows, filteredAssetList)

        # Check that assets in filteredAssetListSelected is presented in the Asset List view
        for x in range(0, len(filteredAssetList)):
            self.assertEqual(flagStateIndex[int(filteredAssetList[x][17])], self.driver.find_element_by_css_selector("td[title=\"" + flagStateIndex[int(filteredAssetList[x][17])] + "\"]").text)
            self.assertEqual(filteredAssetList[x][3], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetList[x][3] + "\"]").text)
            self.assertEqual(filteredAssetList[x][1], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetList[x][1] + "\"]").text)
            self.assertEqual(filteredAssetList[x][0], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetList[x][0] + "\"]").text)
            self.assertEqual(filteredAssetList[x][2], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetList[x][2] + "\"]").text)
            self.assertEqual(gearTypeIndex[int(filteredAssetList[x][8])], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeIndex[int(filteredAssetList[x][8])] + "\"]").text)
            self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)

        # Check that Asset from non-selected asset list (filteredAssetListNonSelected) does not exist in the visual asset list view.
        for x in range(0, len(filteredAssetListNonSelected)):
            try:
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][1] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][0] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][2] + "\"]").text)
            except NoSuchElementException:
                pass
        time.sleep(1)

        # Search for all assets with Ext Mark value and Home port value
        self.driver.find_element_by_id("asset-input-search-homeport").clear()
        self.driver.find_element_by_id("asset-input-search-homeport").send_keys(homeportSearchValue[0])
        time.sleep(1)
        # Click on search button
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(3)

        # Save current advanced filter to group
        self.driver.find_element_by_css_selector("#asset-btn-save-search > span").click()
        time.sleep(1)
        self.driver.find_element_by_name("name").clear()
        time.sleep(1)
        self.driver.find_element_by_name("name").send_keys(groupName[5])
        time.sleep(1)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(5)

        # Get all assets with the marked value in the External Marking field in the asset list.
        filteredAssetListSelected = get_selected_elements_in_list_from_mainList(filteredAssetList, 7, homeportSearchValue[0])
        # Get remaining assets that is found in assetAllrows but not in filteredAssetListSelected
        filteredAssetListNonSelected = get_remaining_elements_from_main_list(assetAllrows, filteredAssetListSelected)

        # Reload page
        self.driver.refresh()
        time.sleep(7)
        # Click on sort IRCS
        self.driver.find_element_by_id("asset-sort-ircs").click()
        time.sleep(1)
        # Select Group 5 filter search
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        time.sleep(1)
        self.driver.find_element_by_id("asset-dropdown-saved-search-item-2").click()
        time.sleep(7)

        # Check that assets in filteredAssetListSelected is presented in the Asset List view
        for x in range(0, len(filteredAssetListSelected)):
            self.assertEqual(flagStateIndex[int(filteredAssetListSelected[x][17])], self.driver.find_element_by_css_selector("td[title=\"" + flagStateIndex[int(filteredAssetListSelected[x][17])] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][3], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][3] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][1], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][1] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][0], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][0] + "\"]").text)
            self.assertEqual(filteredAssetListSelected[x][2], self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListSelected[x][2] + "\"]").text)
            self.assertEqual(gearTypeIndex[int(filteredAssetListSelected[x][8])], self.driver.find_element_by_css_selector("td[title=\"" + gearTypeIndex[int(filteredAssetListSelected[x][8])] + "\"]").text)
            self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)

        # Check that Asset from non-selected asset list (filteredAssetListNonSelected) does not exist in the visual asset list view.
        for x in range(0, len(filteredAssetListNonSelected)):
            try:
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][1] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][0] + "\"]").text)
                self.assertFalse(self.driver.find_element_by_css_selector("td[title=\"" + filteredAssetListNonSelected[x][2] + "\"]").text)
            except NoSuchElementException:
                pass
        time.sleep(4)


    @timeout_decorator.timeout(seconds=180)
    def test_0205_create_several_mobile_terminals_for_filtering(self):
        # Create mobile terminals from file with several different values for filtering
        create_mobileterminal_from_file_based_on_link_file(self, 'assets2xxxx.csv', 'mobileterminals2xxxx.csv', 'linkassetmobileterminals2xxxx.csv')



    @timeout_decorator.timeout(seconds=360)
    def test_0206_search_of_mobile_terminals_serialnr_and_export_to_file(self):
        # Test case tests search functions filtering on Serial Number. Also export list result to file.
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('assets2xxxx.csv')
        # Open saved csv file and read all mobile terminal elements
        mobileTerminalAllrows = get_elements_from_file('mobileterminals2xxxx.csv')
        # Open saved csv file and read all linked elements between assets and mobile terminals
        linkAssetMobileTerminalAllrows = get_elements_from_file('linkassetmobileterminals2xxxx.csv')

        # Click on Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(5)
        # Sort on linked asset column
        self.driver.find_element_by_id("mt-sort-name").click()
        time.sleep(1)

        # Enter Serial Number search value
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(mobileTerminalSearchValue[0])
        # Click on search button
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(2)

        # Select all mobile terminals in the list
        self.driver.find_element_by_id("mt-checkbox-select-all").click()
        time.sleep(2)
        # Save path to current dir
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Change to Download folder for current user
        downloadPath = get_download_path()
        os.chdir(downloadPath)
        print(os.path.abspath(os.path.dirname(__file__)))
        # Check if file exists. If so remove it
        if os.path.exists(mobileTerminalFileName):
            os.remove(mobileTerminalFileName)
        # Select Action "Export selection"
        self.driver.find_element_by_id("mt-dropdown-actions").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Change back the path to current dir
        os.chdir(cwd)

        # Get all mobile terminal with Serial Number (F.S.) called "AA" in the asset list.
        filteredmobileTerminalList = get_selected_elements_in_list_from_mainList(mobileTerminalAllrows, 0, removeChar(mobileTerminalSearchValue[0], "*"))
        # Get the remaining mobile terminal in the filteredmobileTerminalList
        filteredmobileTerminalListNonSelected = get_remaining_elements_from_main_list(mobileTerminalAllrows, filteredmobileTerminalList)

        # Check that mobile terminals in filteredmobileTerminalList is presented in the Mobile Terminal List view
        for x in range(0, len(filteredmobileTerminalList)):
            # Get CFR Value based on Link list between assets and mobile terminals
            tempCFRValue = get_asset_cfr_via_link_list(linkAssetMobileTerminalAllrows, filteredmobileTerminalList[x][0])
            # Get asset name based on CFR value found in assetAllrows list
            tempAssetName = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 1)
            # Get asset name based on CFR value found in assetAllrows list
            tempMMSIValue = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 5)

            self.assertEqual(tempAssetName, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[2]/span[1]/a").text)
            self.assertEqual(filteredmobileTerminalList[x][0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[3]").text)
            self.assertEqual(filteredmobileTerminalList[x][6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[4]").text)
            self.assertEqual(filteredmobileTerminalList[x][5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[5]").text)
            self.assertEqual(transponderType[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[6]").text)
            self.assertEqual(filteredmobileTerminalList[x][4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[7]").text)
            self.assertEqual(tempMMSIValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[8]/span").text)

        # Check that Asset from non-selected mobile terminal list (filteredmobileTerminalListNonSelected) does not exist in the visual mobile terminal list view.
        for x in range(0, len(filteredmobileTerminalListNonSelected)):
            print("Checking that MT nr: " +str(x) + " shall NOT exist in the list view")
            # Get CFR Value based on Link list between assets and mobile terminals
            tempCFRValue = get_asset_cfr_via_link_list(linkAssetMobileTerminalAllrows, filteredmobileTerminalListNonSelected[x][0])
            # Get asset name based on CFR value found in assetAllrows list
            tempAssetName = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 1)
            # Get asset name based on CFR value found in assetAllrows list
            tempMMSIValue = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 5)

            # Loop around each possible row in the mobile terminal list view
            for y in range(0, len(mobileTerminalAllrows)):
                try:
                    self.assertNotEqual(tempAssetName, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(y + 1) + "]/td[2]/span[1]/a").text)
                    self.assertNotEqual(filteredmobileTerminalListNonSelected[x][0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(y + 1) + "]/td[3]").text)
                    self.assertNotEqual(filteredmobileTerminalListNonSelected[x][4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(y + 1) + "]/td[7]").text)
                    self.assertNotEqual(tempMMSIValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(y + 1) + "]/td[8]/span").text)
                except NoSuchElementException:
                    pass



    @timeout_decorator.timeout(seconds=180)
    def test_0206b_check_mobile_terminal_exported_to_file(self):
        # Test case checks that mobile terminals from test_0206 is exported to file correctly.
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('assets2xxxx.csv')
        # Open saved csv file and read all mobile terminal elements
        mobileTerminalAllrows = get_elements_from_file('mobileterminals2xxxx.csv')
        # Open saved csv file and read all linked elements between assets and mobile terminals
        linkAssetMobileTerminalAllrows = get_elements_from_file('linkassetmobileterminals2xxxx.csv')


        # Click on Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(5)
        # Sort on linked asset column
        self.driver.find_element_by_id("mt-sort-name").click()
        time.sleep(1)

        # Enter Serial Number search value
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(mobileTerminalSearchValue[0])
        # Click on search button
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(2)

        # Get all mobile terminal with Serial Number (F.S.) called "AA" in the asset list.
        filteredmobileTerminalListSelected = get_selected_elements_in_list_from_mainList(mobileTerminalAllrows, 0, removeChar(mobileTerminalSearchValue[0], "*"))
        # Get the remaining mobile terminal in the filteredmobileTerminalList
        filteredmobileTerminalListNonSelected = get_remaining_elements_from_main_list(mobileTerminalAllrows, filteredmobileTerminalListSelected)

        # Save path to current dir
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Change to Download folder for current user
        downloadPath = get_download_path()
        os.chdir(downloadPath)
        print(os.path.abspath(os.path.dirname(__file__)))
        # Open saved csv file and read all elements to "allrows"
        allrows = get_elements_from_file_without_deleting_paths_and_rows(mobileTerminalFileName)
        # Deleting header row
        del allrows[0]
        # Change back the path to current dir
        os.chdir(cwd)
        print(cwd)

        # Sort the allrows list (1st Column)
        allrows.sort(key=lambda x: x[0])
        print("----------allrows from file-----------------")
        print(allrows)
        # Check that the elements in csv file is correct
        # Adapt filteredmobileTerminalListSelected list to the "format" as for exported CSV files
        # The result is saved in filteredmobileTerminalListSelectedCSVformat
        filteredmobileTerminalListSelectedCSVformat = adapt_mobile_terminal_list_to_exported_CSV_file_standard(filteredmobileTerminalListSelected, assetAllrows, linkAssetMobileTerminalAllrows)
        print(filteredmobileTerminalListSelectedCSVformat)
        # Sort the filteredmobileTerminalListSelectedCSVformat list (1st Column)
        filteredmobileTerminalListSelectedCSVformat.sort(key=lambda x: x[0])
        # Check filteredmobileTerminalListSelectedCSVformat in allrows row by row
        resultExists = check_sublist_in_other_list_if_it_exists(filteredmobileTerminalListSelectedCSVformat, allrows)
        # Check if resultExists list includes just True states
        print(resultExists)
        # The test case shall pass if ALL boolean values in resultExists list are True
        self.assertTrue(checkAllTrue(resultExists))
        # Adapt filteredmobileTerminalListNonSelected list to the "format" as for exported CSV files
        # The result is saved in filteredmobileTerminalListNonSelectedCSVformat
        filteredmobileTerminalListNonSelectedCSVformat = adapt_mobile_terminal_list_to_exported_CSV_file_standard(filteredmobileTerminalListNonSelected, assetAllrows, linkAssetMobileTerminalAllrows)
        print(filteredmobileTerminalListNonSelectedCSVformat)
        # Sort the filteredmobileTerminalListNonSelectedCSVformat list (1st Column)
        filteredmobileTerminalListNonSelectedCSVformat.sort(key=lambda x: x[0])
        # Check filteredmobileTerminalListNonSelectedCSVformat in allrows row by row
        resultExists = check_sublist_in_other_list_if_it_exists(filteredmobileTerminalListNonSelectedCSVformat, allrows)
        print(resultExists)
        # The test case shall pass if ALL of the boolean values in resultExists list are False
        self.assertFalse(checkAnyTrue(resultExists))
        time.sleep(5)


    @timeout_decorator.timeout(seconds=360)
    def test_0207_search_of_mobile_terminals_member_nr_satellite_nr_and_export_to_file(self):
        # Test case tests search functions filtering on member and satellite Number. Also export list result to file.
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('assets2xxxx.csv')
        # Open saved csv file and read all mobile terminal elements
        mobileTerminalAllrows = get_elements_from_file('mobileterminals2xxxx.csv')
        # Open saved csv file and read all linked elements between assets and mobile terminals
        linkAssetMobileTerminalAllrows = get_elements_from_file('linkassetmobileterminals2xxxx.csv')

        # Click on Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(5)
        # Sort on linked asset column
        self.driver.find_element_by_id("mt-sort-name").click()
        time.sleep(1)

        # Enter Member Number and Satellite Number search value
        self.driver.find_element_by_id("mt-input-search-memberNumber").clear()
        self.driver.find_element_by_id("mt-input-search-memberNumber").send_keys(mobileTerminalSearchValue[1])
        self.driver.find_element_by_id("mt-input-search-satelliteNumber").clear()
        self.driver.find_element_by_id("mt-input-search-satelliteNumber").send_keys(mobileTerminalSearchValue[2])
        # Click on search button
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(2)

        # Select all mobile terminals in the list
        self.driver.find_element_by_id("mt-checkbox-select-all").click()
        time.sleep(2)
        # Save path to current dir
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Change to Download folder for current user
        downloadPath = get_download_path()
        os.chdir(downloadPath)
        print(os.path.abspath(os.path.dirname(__file__)))
        # Check if file exists. If so remove it
        if os.path.exists(mobileTerminalFileName):
            os.remove(mobileTerminalFileName)
        # Select Action "Export selection"
        self.driver.find_element_by_id("mt-dropdown-actions").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Change back the path to current dir
        os.chdir(cwd)

        # Get all mobile terminal with Member Number called "5" in the mobile terminal list.
        filteredmobileTerminalList = get_selected_elements_in_list_from_mainList(mobileTerminalAllrows, 6, removeChar(mobileTerminalSearchValue[1], "*"))
        # Get all mobile terminal with Member Number called "5"  PLUS Satellite Number called "1000" in the mobile terminal list.
        filteredmobileTerminalList = get_selected_elements_in_list_from_mainList(filteredmobileTerminalList, 4, removeChar(mobileTerminalSearchValue[2], "*"))

        # Get the remaining mobile terminal in the filteredmobileTerminalList
        filteredmobileTerminalListNonSelected = get_remaining_elements_from_main_list(mobileTerminalAllrows, filteredmobileTerminalList)

        # Check that mobile terminals in filteredmobileTerminalList is presented in the Mobile Terminal List view
        for x in range(0, len(filteredmobileTerminalList)):
            # Get CFR Value based on Link list between assets and mobile terminals
            tempCFRValue = get_asset_cfr_via_link_list(linkAssetMobileTerminalAllrows, filteredmobileTerminalList[x][0])
            # Get asset name based on CFR value found in assetAllrows list
            tempAssetName = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 1)
            # Get asset name based on CFR value found in assetAllrows list
            tempMMSIValue = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 5)

            self.assertEqual(tempAssetName, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[2]/span[1]/a").text)
            self.assertEqual(filteredmobileTerminalList[x][0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[3]").text)
            self.assertEqual(filteredmobileTerminalList[x][6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[4]").text)
            self.assertEqual(filteredmobileTerminalList[x][5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[5]").text)
            self.assertEqual(transponderType[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[6]").text)
            self.assertEqual(filteredmobileTerminalList[x][4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[7]").text)
            self.assertEqual(tempMMSIValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[8]/span").text)

        # Check that Asset from non-selected mobile terminal list (filteredmobileTerminalListNonSelected) does not exist in the visual mobile terminal list view.
        for x in range(0, len(filteredmobileTerminalListNonSelected)):
            print("Checking that MT nr: " +str(x) + " shall NOT exist in the list view")
            # Get CFR Value based on Link list between assets and mobile terminals
            tempCFRValue = get_asset_cfr_via_link_list(linkAssetMobileTerminalAllrows, filteredmobileTerminalListNonSelected[x][0])
            # Get asset name based on CFR value found in assetAllrows list
            tempAssetName = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 1)
            # Get asset name based on CFR value found in assetAllrows list
            tempMMSIValue = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 5)

            # Loop around each possible row in the mobile terminal list view
            for y in range(0, len(mobileTerminalAllrows)):
                try:
                    self.assertNotEqual(tempAssetName, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(y + 1) + "]/td[2]/span[1]/a").text)
                    self.assertNotEqual(filteredmobileTerminalListNonSelected[x][0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(y + 1) + "]/td[3]").text)
                    self.assertNotEqual(filteredmobileTerminalListNonSelected[x][4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(y + 1) + "]/td[7]").text)
                    self.assertNotEqual(tempMMSIValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(y + 1) + "]/td[8]/span").text)
                except NoSuchElementException:
                    pass



    @timeout_decorator.timeout(seconds=180)
    def test_0207b_check_mobile_terminal_exported_to_file(self):
        # Test case checks that mobile terminals from test_0207 is exported to file correctly.
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file('assets2xxxx.csv')
        # Open saved csv file and read all mobile terminal elements
        mobileTerminalAllrows = get_elements_from_file('mobileterminals2xxxx.csv')
        # Open saved csv file and read all linked elements between assets and mobile terminals
        linkAssetMobileTerminalAllrows = get_elements_from_file('linkassetmobileterminals2xxxx.csv')


        # Click on Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(5)
        # Sort on linked asset column
        self.driver.find_element_by_id("mt-sort-name").click()
        time.sleep(1)

        # Enter Member Number and Satellite Number search value
        self.driver.find_element_by_id("mt-input-search-memberNumber").clear()
        self.driver.find_element_by_id("mt-input-search-memberNumber").send_keys(mobileTerminalSearchValue[1])
        self.driver.find_element_by_id("mt-input-search-satelliteNumber").clear()
        self.driver.find_element_by_id("mt-input-search-satelliteNumber").send_keys(mobileTerminalSearchValue[2])
        # Click on search button
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(2)

        # Get all mobile terminal with Member Number called "5" in the mobile terminal list.
        filteredmobileTerminalListSelected = get_selected_elements_in_list_from_mainList(mobileTerminalAllrows, 6, removeChar(mobileTerminalSearchValue[1], "*"))
        # Get all mobile terminal with Member Number called "5"  PLUS Satellite Number called "1000" in the mobile terminal list.
        filteredmobileTerminalListSelected = get_selected_elements_in_list_from_mainList(filteredmobileTerminalListSelected, 4, removeChar(mobileTerminalSearchValue[2], "*"))

        # Get the remaining mobile terminal in the filteredmobileTerminalList
        filteredmobileTerminalListNonSelected = get_remaining_elements_from_main_list(mobileTerminalAllrows, filteredmobileTerminalListSelected)

        # Save path to current dir
        cwd = os.path.abspath(os.path.dirname(__file__))
        # Change to Download folder for current user
        downloadPath = get_download_path()
        os.chdir(downloadPath)
        print(os.path.abspath(os.path.dirname(__file__)))
        # Open saved csv file and read all elements to "allrows"
        allrows = get_elements_from_file_without_deleting_paths_and_rows(mobileTerminalFileName)
        # Deleting header row
        del allrows[0]
        # Change back the path to current dir
        os.chdir(cwd)
        print(cwd)

        # Sort the allrows list (1st Column)
        allrows.sort(key=lambda x: x[0])
        print("----------allrows from file-----------------")
        print(allrows)
        # Check that the elements in csv file is correct
        # Adapt filteredmobileTerminalListSelected list to the "format" as for exported CSV files
        # The result is saved in filteredmobileTerminalListSelectedCSVformat
        filteredmobileTerminalListSelectedCSVformat = adapt_mobile_terminal_list_to_exported_CSV_file_standard(filteredmobileTerminalListSelected, assetAllrows, linkAssetMobileTerminalAllrows)
        print(filteredmobileTerminalListSelectedCSVformat)
        # Sort the filteredmobileTerminalListSelectedCSVformat list (1st Column)
        filteredmobileTerminalListSelectedCSVformat.sort(key=lambda x: x[0])
        # Check filteredmobileTerminalListSelectedCSVformat in allrows row by row
        resultExists = check_sublist_in_other_list_if_it_exists(filteredmobileTerminalListSelectedCSVformat, allrows)
        # Check if resultExists list includes just True states
        print(resultExists)
        # The test case shall pass if ALL boolean values in resultExists list are True
        self.assertTrue(checkAllTrue(resultExists))
        # Adapt filteredmobileTerminalListNonSelected list to the "format" as for exported CSV files
        # The result is saved in filteredmobileTerminalListNonSelectedCSVformat
        filteredmobileTerminalListNonSelectedCSVformat = adapt_mobile_terminal_list_to_exported_CSV_file_standard(filteredmobileTerminalListNonSelected, assetAllrows, linkAssetMobileTerminalAllrows)
        print(filteredmobileTerminalListNonSelectedCSVformat)
        # Sort the filteredmobileTerminalListNonSelectedCSVformat list (1st Column)
        filteredmobileTerminalListNonSelectedCSVformat.sort(key=lambda x: x[0])
        # Check filteredmobileTerminalListNonSelectedCSVformat in allrows row by row
        resultExists = check_sublist_in_other_list_if_it_exists(filteredmobileTerminalListNonSelectedCSVformat, allrows)
        print(resultExists)
        # The test case shall pass if ALL of the boolean values in resultExists list are False
        self.assertFalse(checkAnyTrue(resultExists))
        time.sleep(5)



class UnionVMSTestCaseMobileTerminalChannels(unittest.TestCase):


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


    @timeout_decorator.timeout(seconds=180)
    def test_0301_create_several_assets_for_filtering(self):
        # Create assets from file with several different values for filtering
        create_asset_from_file(self, tests300FileName[0])


    @timeout_decorator.timeout(seconds=180)
    def test_0302_create_several_mobile_terminals_for_editing(self):
        # Create mobile terminals from file with different values.
        # NOTE: Several mobile terminals are added to the same asset.
        create_mobileterminal_from_file_based_on_link_file(self, tests300FileName[0], tests300FileName[1], tests300FileName[2])


    @timeout_decorator.timeout(seconds=180)
    def test_0302b_check_mobile_terminal_list(self):
        # Test case checks that mobile terminals from test_0302 presented correctly in the mobile terminal list.
        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file(tests300FileName[0])
        # Open saved csv file and read all mobile terminal elements
        mobileTerminalAllrows = get_elements_from_file(tests300FileName[1])
        # Open saved csv file and read all linked elements between assets and mobile terminals
        linkAssetMobileTerminalAllrows = get_elements_from_file(tests300FileName[2])

        # Sort mobileTerminalAllrows on 1st column (that is SerialNumber value)
        mobileTerminalAllrows.sort(key=lambda x: x[0])
        # Click on Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(5)
        # Sort on linked asset column
        self.driver.find_element_by_id("mt-sort-serialNumber").click()
        time.sleep(1)

        # Check that mobile terminals in filteredmobileTerminalList is presented in the Mobile Terminal List view
        for x in range(0, len(mobileTerminalAllrows)):
            # Get CFR Value based on Link list between assets and mobile terminals
            tempCFRValue = get_asset_cfr_via_link_list(linkAssetMobileTerminalAllrows, mobileTerminalAllrows[x][0])
            # Get asset name based on CFR value found in assetAllrows list
            tempAssetName = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 1)
            # Get asset name based on CFR value found in assetAllrows list
            tempMMSIValue = get_selected_asset_column_value_based_on_cfr(assetAllrows, tempCFRValue, 5)

            self.assertEqual(tempAssetName, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[2]/span[1]/a").text)
            self.assertEqual(mobileTerminalAllrows[x][0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[3]").text)
            self.assertEqual(mobileTerminalAllrows[x][6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[4]").text)
            self.assertEqual(mobileTerminalAllrows[x][5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[5]").text)
            self.assertEqual(transponderType[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[6]").text)
            self.assertEqual(mobileTerminalAllrows[x][4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[7]").text)
            self.assertEqual(tempMMSIValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[8]/span").text)

            # Get Status Value (Active/Inactive) for current mobile terminal in UPPER case.
            tempStatusValue = statusValue[int(mobileTerminalAllrows[x][14])]
            tempStatusValue = tempStatusValue.upper()
            self.assertEqual(tempStatusValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[9]/span").text)


    @timeout_decorator.timeout(seconds=180)
    def test_0303_create_several_additional_channels_for_mobile_terminals(self):
        # Set referenceDateTime to current UTC time
        referenceDateTime = datetime.datetime.utcnow()
        # Create assets from file with several different values for filtering
        create_addtional_channels_for_mobileterminals_from_file(self, tests300FileName[3], referenceDateTime)
        # Save referenceDateTime to file
        save_elements_to_file(referenceDateTimeFileName[0], referenceDateTime, True)


    def test_0304_check_additional_channels_for_mobile_terminals(self):
        # Test case checks that mobile terminals from test_0302 and test_0303 are presented correctly mobile terminal by mobile terminal.

        # Get referenceDateTime from file
        referenceDateTime = get_reference_date_time_from_file(referenceDateTimeFileName[0])

        referenceDateTimeValueString = datetime.datetime.strftime(referenceDateTime, '%Y-%m-%d %H:%M:%S')
        print(referenceDateTimeValueString)

        # Open saved csv file and read all channel elements
        channelAllrows = get_elements_from_file(tests300FileName[3])

        # Open saved csv file and read all mobile terminal elements
        mobileTerminalAllrows = get_elements_from_file(tests300FileName[1])

        # Check all channels and mobile terminal data (mobile terminal by mobile terminal)
        resultExists = check_channel_and_mobile_terminal_data(self, channelAllrows, mobileTerminalAllrows, referenceDateTime)
        self.assertTrue(resultExists)


    def test_0305_change_default_channel_for_one_mobile_terminal(self):
        # Test case changes the default channel for selected mobile terminal from test_0302 and test_0303

        # Get referenceDateTime from file
        referenceDateTime = get_reference_date_time_from_file(referenceDateTimeFileName[0])

        referenceDateTimeValueString = datetime.datetime.strftime(referenceDateTime, '%Y-%m-%d %H:%M:%S')
        print(referenceDateTimeValueString)

        # Open saved csv file and read all channel elements
        channelAllrows = get_elements_from_file(tests300FileName[3])
        # Sort the mobileTerminalAllrows list (1st Column)
        channelAllrows.sort(key=lambda x: x[0])

        # Open saved csv file and read all mobile terminal elements
        mobileTerminalAllrows = get_elements_from_file(tests300FileName[1])
        # Sort the mobileTerminalAllrows list (1st Column)
        mobileTerminalAllrows.sort(key=lambda x: x[0])

        # Create new channel list that includes channel data from mobileTerminalAllrows plus channelAllrows
        channelListPartFromMobileTerminal = get_channel_part_for_one_mobile_terminal_list(mobileTerminalAllrows, pollConfigDefaultChangeValue[0], pollConfigDefaultChangeValue[1], pollConfigDefaultChangeValue[2])
        channelTotalList = get_additional_list_result_from_from_two_channel_lists(channelAllrows, channelListPartFromMobileTerminal)
        # Sort the allrows list (1st Column)
        channelTotalList.sort(key=lambda x: x[0])


        # Click on Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(3)
        # Sort on linked asset column
        self.driver.find_element_by_id("mt-sort-serialNumber").click()
        time.sleep(1)

        # Search for mobile terminal via serial number (The 2nd serial number in mobileTerminalAllrows is used)
        self.driver.find_element_by_id("mt-input-search-serialNumber").clear()
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(mobileTerminalAllrows[1][0])
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(5)

        # Verifies that default DNID and Member Number is correct for the 2nd serial number in mobileTerminalAllrows list.
        self.assertEqual(mobileTerminalAllrows[1][6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(mobileTerminalAllrows[1][5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)

        # Click on detail button
        self.driver.find_element_by_id("mt-toggle-form").click()
        time.sleep(3)

        # Read all channels for selected Mobile Terminal
        notedChannelsList = read_all_channels_for_selected_Mobile_Terminal(self)

        # Loop all channels in the list and disable default parameter if default parameter is selected
        for x in range(0, len(notedChannelsList)):
            print(notedChannelsList[x])
            # Disable default parameter if default parameter is selected
            if notedChannelsList[x][4] == "1":
                # Note: Xpath is needed here to change the value for the radio button. Element ID does not work.
                self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/div[4]/div/div[2]/form/fieldset/div/div[3]/div[" + str(x + 3) + "]/div/div[2]/div[4]/label").click()
                time.sleep(2)

        # Loop all channels in the list and set default parameter where the first default parameter is zero in the notedChannelsList
        for x in range(0, len(notedChannelsList)):
            print(notedChannelsList[x])
            # Disable default parameter if default parameter is selected
            if notedChannelsList[x][4] == "0":
                # Note: Xpath is needed here to change the value for the radio button. Element ID does not work.
                self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/div[4]/div/div[2]/form/fieldset/div/div[3]/div[" + str(x + 3) + "]/div/div[2]/div[4]/label").click()
                time.sleep(1)

        # Click on Save button
        self.driver.find_element_by_id("menu-bar-update").click()
        # Enter Comment in comment field
        self.driver.find_element_by_name("comment").clear()
        self.driver.find_element_by_name("comment").send_keys(commentValue)
        time.sleep(1)
        # Click on Update button
        self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
        time.sleep(3)
        # Click on Cancel
        self.driver.find_element_by_id("menu-bar-cancel").click()
        time.sleep(3)

        # Search for mobile terminal via serial number (The 2nd serial number in mobileTerminalAllrows is used)
        self.driver.find_element_by_id("mt-input-search-serialNumber").clear()
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(mobileTerminalAllrows[1][0])
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(3)

        # Verifies that new default DNID and Member Number is correct for the 2nd serial number in channelAllrows list.
        self.assertEqual(channelAllrows[1][6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(channelAllrows[1][5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)

        # Click on detail button
        self.driver.find_element_by_id("mt-toggle-form").click()
        time.sleep(3)

        # Read all channels for selected Mobile Terminal
        notedChannelsList = read_all_channels_for_selected_Mobile_Terminal(self)


        # Open saved csv file and read all channel elements (Note modified file)
        channelAllrows = get_elements_from_file(tests300FileName[4])
        # Sort the mobileTerminalAllrows list (1st Column)
        channelAllrows.sort(key=lambda x: x[0])

        # Create new channel list that includes channel data from mobileTerminalAllrows plus channelAllrows
        channelListPartFromMobileTerminal = get_channel_part_for_one_mobile_terminal_list(mobileTerminalAllrows, pollConfigDefaultChangeValue[0], pollConfigDefaultChangeValue[1], pollConfigDefaultChangeValue[2])
        channelTotalList = get_additional_list_result_from_from_two_channel_lists(channelAllrows, channelListPartFromMobileTerminal)
        # Sort the allrows list (1st Column)
        channelTotalList.sort(key=lambda x: x[0])


        # Convert hour value in channelTotalList to correct Datetime format and save it in channelTotalListDateTimeFormat. This action makes it easier to compare later with the resultList
        channelTotalListDateTimeFormat = convertHoursValueInListToDateTimeFormat(channelTotalList, referenceDateTime)
        # Remove Mobile Terminal and Channel position data in channelTotalListDateTimeFormat. This action makes it easier to compare later with the resultList
        channelTotalListDateTimeFormatToCompare = removeLastNumberElementsInListRow(channelTotalListDateTimeFormat, 2)

        # Compare notedChannelsList read from GUI and read channelTotalListDateTimeFormatToCompare from file and return result.
        resultExists = compareChannelLists(notedChannelsList, channelTotalListDateTimeFormatToCompare)
        print(resultExists)
        self.assertTrue(resultExists)


    def test_0306_delete_channel_for_one_mobile_terminal(self):
        # Test case changes the default channel for selected mobile terminal from test_0302 and test_0303

        # Get referenceDateTime from file
        referenceDateTime = get_reference_date_time_from_file(referenceDateTimeFileName[0])

        referenceDateTimeValueString = datetime.datetime.strftime(referenceDateTime, '%Y-%m-%d %H:%M:%S')
        print(referenceDateTimeValueString)

        # Open saved csv file and read all channel elements
        channelAllrows = get_elements_from_file(tests300FileName[3])
        # Sort the mobileTerminalAllrows list (1st Column)
        channelAllrows.sort(key=lambda x: x[0])

        # Open saved csv file and read all mobile terminal elements
        mobileTerminalAllrows = get_elements_from_file(tests300FileName[1])
        # Sort the mobileTerminalAllrows list (1st Column)
        mobileTerminalAllrows.sort(key=lambda x: x[0])

        # Create new channel list that includes channel data from mobileTerminalAllrows plus channelAllrows
        channelListPartFromMobileTerminal = get_channel_part_for_one_mobile_terminal_list(mobileTerminalAllrows, pollConfigDefaultChangeValue[0], pollConfigDefaultChangeValue[1], pollConfigDefaultChangeValue[2])
        channelTotalList = get_additional_list_result_from_from_two_channel_lists(channelAllrows, channelListPartFromMobileTerminal)
        # Sort the allrows list (1st Column)
        channelTotalList.sort(key=lambda x: x[0])


        # Click on Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(3)
        # Sort on linked asset column
        self.driver.find_element_by_id("mt-sort-serialNumber").click()
        time.sleep(1)

        # Search for mobile terminal via serial number (The 9th serial number in mobileTerminalAllrows is used)
        self.driver.find_element_by_id("mt-input-search-serialNumber").clear()
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(mobileTerminalAllrows[8][0])
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(5)

        # Verifies that default DNID and Member Number is correct for the 9th serial number in mobileTerminalAllrows list.
        self.assertEqual(mobileTerminalAllrows[8][6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(mobileTerminalAllrows[8][5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)

        # Click on detail button
        self.driver.find_element_by_id("mt-toggle-form").click()
        time.sleep(3)

        # Read all channels for selected Mobile Terminal
        notedChannelsList = read_all_channels_for_selected_Mobile_Terminal(self)

        # Click on delete button for the 1st channel in the list
        self.driver.find_element_by_id("mt-0-channel-0-removeChannel").click()
        time.sleep(1)

        # Click on Save button
        self.driver.find_element_by_id("menu-bar-update").click()
        # Enter Comment in comment field
        self.driver.find_element_by_name("comment").clear()
        self.driver.find_element_by_name("comment").send_keys(commentValue)
        time.sleep(1)
        # Click on Update button
        self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
        time.sleep(3)
        # Click on Cancel
        self.driver.find_element_by_id("menu-bar-cancel").click()
        time.sleep(3)

        # Verifies that default DNID and Member Number is correct for the 2nd serial number in notedChannelsList list. The 1st DNID and Member is now deleted.
        self.assertEqual(notedChannelsList[1][6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(notedChannelsList[1][5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)
        time.sleep(3)

        # Click on detail button
        self.driver.find_element_by_id("mt-toggle-form").click()
        time.sleep(3)

        # Read all channels for selected Mobile Terminal
        notedChannelsList = read_all_channels_for_selected_Mobile_Terminal(self)

        # Checks the number of channels read. If the list does not consists of one channel then something is wrong
        if len(notedChannelsList) == 1:
            oneChannel = True
        else:
            oneChannel = False
        self.assertTrue(oneChannel)



class UnionVMSTestCaseAudit(unittest.TestCase):


    def setUp(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)


    def tearDown(self):
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0401_change_default_configuration_parameters(self):
        # Startup browser and login
        UnionVMSTestCase.test_0001b_change_default_configuration_parameters(self)



    @timeout_decorator.timeout(seconds=180)
    def test_0402_check_config_update_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Filtering on Update Operation
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Update").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(1)
        # Click on Search button
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)

        # Check config update value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)

        # Get saved date/time from file to compare with current value in list row
        referenceDateTime = get_reference_date_time_from_file(referenceDateTimeFileName[1])
        # Convert to string format incl removing the second part
        referenceDateTimeValueString = datetime.datetime.strftime(referenceDateTime, '%Y-%m-%d %H:%M')
        # Get the real date and time in the list row.
        realDateTimeValueString = self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[5]").text
        # Remove second part from string, that is the 3 last characters in the string
        realDateTimeValueString = realDateTimeValueString[:-3]
        self.assertEqual(referenceDateTimeValueString, realDateTimeValueString)

        self.assertEqual(auditLogsObjectAffectedValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[6]/span").text)

        # Check config update value in audit list 2nd row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(auditLogsOperationValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[4]").text)

        # Get saved date/time from file to compare with current value in list row
        referenceDateTime = get_reference_date_time_from_file(referenceDateTimeFileName[0])
        # Convert to string format incl removing the second part
        referenceDateTimeValueString = datetime.datetime.strftime(referenceDateTime, '%Y-%m-%d %H:%M')
        # Get the real date and time in the list row.
        realDateTimeValueString = self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[5]").text
        # Remove second part from string, that is the 3 last characters in the string
        realDateTimeValueString = realDateTimeValueString[:-3]
        self.assertEqual(referenceDateTimeValueString, realDateTimeValueString)

        self.assertEqual(auditLogsObjectAffectedValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[6]/span").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0403_generate_NAF_position_for_unknown_asset_and_check_holding_table(self):
        # Startup browser and login
        UnionVMSTestCase.test_0001c_generate_NAF_position_for_unknown_asset_and_check_holding_table(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0404_check_alert_update_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Alerts sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ALARMS > span").click()
        time.sleep(3)

        # Check Alert value in audit list 1st row
        self.assertEqual(defaultSystemName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)

        # Get saved date/time from file to compare with current value in list row
        referenceDateTime = get_reference_date_time_from_file(referenceDateTimeFileName[0])
        # Convert to string format incl removing the second part
        referenceDateTimeValueString = datetime.datetime.strftime(referenceDateTime, '%Y-%m-%d %H:%M')
        # Get the real date and time in the list row.
        realDateTimeValueString = self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[5]").text
        # Remove second part from string, that is the 3 last characters in the string
        realDateTimeValueString = realDateTimeValueString[:-3]
        self.assertEqual(referenceDateTimeValueString, realDateTimeValueString)

        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0405_test_0002_create_one_new_asset(self):
        # Startup browser and login
        UnionVMSTestCase.test_0002_create_one_new_asset(self)


    def test_0406_check_asset_creation_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[2], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0407_create_one_new_mobile_terminal(self):
        # Startup browser and login
        UnionVMSTestCase.test_0004_create_one_new_mobile_terminal(self)


    def test_0408_check_mobile_terminal_creation_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0409_link_asset_and_mobile_terminal(self):
        # Startup browser and login
        UnionVMSTestCase.test_0006_link_asset_and_mobile_terminal(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0410_check_link_asset_and_mobile_terminal_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[2], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0411_generate_and_verify_manual_position(self):
        # Startup browser and login
        UnionVMSTestCase.test_0007_generate_and_verify_manual_position(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0412_check_manual_position_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#POSITION_REPORTS > span").click()
        time.sleep(3)

        # Check Alert value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[4], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)

        # Check config update value in audit list 2nd row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[5], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0413_generate_NAF_and_verify_position(self):
        # Startup browser and login
        UnionVMSTestCase.test_0007_generate_NAF_and_verify_position(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0414_check_NAF_position_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#POSITION_REPORTS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultNAFName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=300)
    def test_0415_create_assets_2_3_4_5_6(self):
        # Create assets 3-6 in the list
        for x in range(1, 6):
            create_one_new_asset_from_gui(self, x)
            time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0416_create_two_assets_to_group_and_check_group(self):
        # Startup browser and login
        UnionVMSTestCase.test_0018_create_two_assets_to_group_and_check_group(self)



    @timeout_decorator.timeout(seconds=180)
    def test_0417_check_asset_group_creation_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[7], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0418_change_global_settings_change_date_format(self):
        # Startup browser and login
        UnionVMSTestCase.test_0030_change_global_settings_change_date_format(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0419_change_global_settings_change_date_format(self):
        # Startup browser and login
        UnionVMSTestCase.test_0030_change_global_settings_change_date_format(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0420_check_config_date_time_update_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Filtering on Update Operation
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Update").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(1)
        # Click on Search button
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        # Check config update value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[6]/span").text)
        # Check config update value in audit list 2nd row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(auditLogsOperationValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[6]/span").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0421_create_one_new_asset_and_mobile_terminal(self):
        # Startup browser and login
        UnionVMSTestCase.test_0043_create_one_new_asset_and_mobile_terminal(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0422_generate_manual_poll_and_check(self):
        # Startup browser and login
        UnionVMSTestCase.test_0046_generate_manual_poll_and_check(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0423_check_poll_creation_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[8], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)
        time.sleep(2)



    @timeout_decorator.timeout(seconds=180)
    def test_0424_create_modify_and_check_asset_history(self):
        # Startup browser and login
        UnionVMSTestCase.test_0047_create_modify_and_check_asset_history(self)



    @timeout_decorator.timeout(seconds=180)
    def test_0425_check_asset_creation_and_modifocation_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[2], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)

        # Check config update value in audit list 2nd row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[2], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_xpath("(//a[contains(text(),'" + auditLogsObjectAffectedValue[2] + "')])[2]").text)
        time.sleep(2)



    @timeout_decorator.timeout(seconds=180)
    def test_0426_create_one_new_mobile_terminal(self):
        # Startup browser and login
        UnionVMSTestCase.test_0050_create_one_new_mobile_terminal(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0427_check_mobile_terminal_creation_and_modifocation_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)

        # Check config update value in audit list 2nd row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(auditLogsOperationValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr[2]/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_xpath("(//a[contains(text(),'" + auditLogsObjectAffectedValue[2] + "')])[2]").text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0428_archive_and_check_mobile_terminal(self):
        # Startup browser and login
        UnionVMSTestCase.test_0050b_archive_and_check_mobile_terminal(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0429_check_mobile_terminal_archiving_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)
        time.sleep(2)


    @timeout_decorator.timeout(seconds=180)
    def test_0430_archive_and_check_asset(self):
        # Startup browser and login
        UnionVMSTestCase.test_0051_archive_and_check_asset(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0431_check_asset_archiving_change_in_audit_log(self):
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        # Click on Asset and Terminals sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(3)

        # Check Asset and Terminals value in audit list 1st row
        self.assertEqual(defaultUserName, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[2]").text)
        self.assertEqual(auditLogsOperationValue[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(auditLogsObjectTypeValue[2], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(auditLogsObjectAffectedValue[2], self.driver.find_element_by_link_text(auditLogsObjectAffectedValue[2]).text)
        time.sleep(2)



if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=get_test_report_path(), verbosity=2),failfast=False, buffer=False, catchbreak=False)
