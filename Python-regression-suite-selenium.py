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
import csv
import codecs
import xmlrunner
import distutils.dir_util
from io import BytesIO
from zipfile import ZipFile
import urllib.request

# Import parameters from parameter file
from UnionVMSparameters import *


def externalError(process):
   print("Process '%s' returned code %s" % (process.args, process.returncode))
   #print("Run time: %s " % (time.time() - startTime))
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
    
    uvmsGitHubPath = 'https://github.com/UnionVMS/'
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
            print(os.getcwd())
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


def startup_browser_and_login_to_unionVMS(cls):
    # Start Chrome browser
    cls.driver = webdriver.Chrome()
    #cls.driver = webdriver.Firefox()
    # Maximize browser window
    cls.driver.maximize_window()
    # Login to test user admin
    #cls.driver.get("https://unionvmstest.havochvatten.se/unionvms/")
    cls.driver.implicitly_wait(10)
    cls.driver.get(httpUnionVMSurlString)
    time.sleep(2)

    # if Hav och vatten proxy page is presented, then autologin
    try:
        if cls.driver.find_element_by_xpath("/html/head/title"):
            cls.driver.switch_to.frame("content")
            cls.driver.find_element_by_css_selector("img[alt=\"Automatisk inloggning\"]").click()
            time.sleep(2)
    except:
        pass


    # if Pop-up windows exists then click cancel
    try:
        if cls.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/form"):
            cls.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/form/div[3]/button[2]").click()
            time.sleep(2)
    except:
        pass

    cls.driver.find_element_by_id("userId").send_keys(defaultUserName)
    cls.driver.find_element_by_id(defaultUserNamePassword).send_keys(defaultUserNamePassword)
    time.sleep(2)
    cls.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div/div[2]/div[3]/div[2]/form/div[3]/div/button"). \
        click()
    time.sleep(2)
    cls.driver.find_element_by_partial_link_text("AdminAll").click()


def shutdown_browser(cls):
    if (hasattr(cls, 'driver') and cls.driver is not None):
        cls.driver.quit()
        cls.driver = None;


def create_one_new_asset_from_gui(self, vesselNumber):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    # Click on asset tab
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(10)
    # Click on new Asset button
    self.driver.find_element_by_id("asset-btn-create").click()
    time.sleep(2)
    # Select F.S value
    self.driver.find_element_by_id("asset-input-countryCode").click()
    self.driver.find_element_by_id("asset-input-countryCode-item-2").click()
    # Enter IRCS value
    self.driver.find_element_by_id("asset-input-ircs").send_keys(ircsValue[vesselNumber])
    # Enter Name value
    self.driver.find_element_by_id("asset-input-name").send_keys(vesselName[vesselNumber])
    # Enter External Marking Value
    self.driver.find_element_by_id("asset-input-externalMarking").send_keys(externalMarkingValue)
    # Enter CFR Value
    self.driver.find_element_by_id("asset-input-cfr").send_keys(cfrValue[vesselNumber])
    # Enter IMO Value
    self.driver.find_element_by_id("asset-input-imo").send_keys(imoValue[vesselNumber])
    # Enter HomePort Value
    self.driver.find_element_by_id("asset-input-homeport").send_keys(homeportValue)
    # Select Gear Type value
    self.driver.find_element_by_id("asset-input-gearType").click()
    self.driver.find_element_by_id("asset-input-gearType-item-0").click()
    # Enter MMSI Value
    self.driver.find_element_by_id("asset-input-mmsi").send_keys(mmsiValue[vesselNumber])
    # Select License Type value
    self.driver.find_element_by_id("asset-input-licenseType").click()
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-licenseType-item-0").click()
    # Length Value
    self.driver.find_element_by_id("asset-input-lengthValue").send_keys(lengthValue)
    # Gross Tonnage Value
    self.driver.find_element_by_id("asset-input-grossTonnage").send_keys(grossTonnageValue)
    # Main Power Value
    self.driver.find_element_by_id("asset-input-power").send_keys(powerValue)
    # Main Producer Name Value
    self.driver.find_element_by_id("asset-input-producername").send_keys(producernameValue)
    # Main Producer Code Value
    self.driver.find_element_by_id("asset-input-producercode").send_keys(producercodeValue)
    # Click on the Contacts tab
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    time.sleep(1)
    # Main Contact Name Value
    self.driver.find_element_by_id("asset-input-contact-name-0").send_keys(contactNameValue)
    # Main E-mail Value
    self.driver.find_element_by_id("asset-input-contact-email-0").send_keys(contactEmailValue)
    # Main Contact Number Value
    self.driver.find_element_by_id("asset-input-contact-number-0").send_keys(contactPhoneNumberValue)
    # Click on Save Asset button
    self.driver.find_element_by_id("menu-bar-save").click()
    time.sleep(5)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(3)
    # Shutdown browser
    shutdown_browser(self)


def create_one_new_asset_from_gui_with_parameters(self, parameterList):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    # Click on asset tab
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(1)
    # Click on new Asset button
    self.driver.find_element_by_id("asset-btn-create").click()
    time.sleep(2)
    # Select F.S value
    self.driver.find_element_by_id("asset-input-countryCode").click()
    self.driver.find_element_by_id("asset-input-countryCode-item-2").click()
    # Enter IRCS value
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
    self.driver.find_element_by_id("asset-input-gearType").click()
    self.driver.find_element_by_id("asset-input-gearType-item-0").click()
    # Enter MMSI Value
    self.driver.find_element_by_id("asset-input-mmsi").send_keys(parameterList[5])
    # Select License Type value
    self.driver.find_element_by_id("asset-input-licenseType").click()
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
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    time.sleep(1)
    # Main Contact Name Value
    self.driver.find_element_by_id("asset-input-contact-name-0").send_keys(parameterList[14])
    # Main E-mail Value
    self.driver.find_element_by_id("asset-input-contact-email-0").send_keys(parameterList[15])
    # Main Contact Number Value
    self.driver.find_element_by_id("asset-input-contact-number-0").send_keys(parameterList[16])
    # Click on Save Asset button
    self.driver.find_element_by_id("menu-bar-save").click()
    time.sleep(10)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(3)
    # Shutdown browser
    shutdown_browser(self)



def create_one_new_mobile_terminal_from_gui(self, mobileTerminalNumber):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(2)
    # Click on new terminal button
    self.driver.find_element_by_id("mt-btn-create").click()
    time.sleep(3)
    # Select Transponder system
    self.driver.find_element_by_id("mt-0-typeAndPlugin").click()
    time.sleep(1)
#    self.driver.find_element_by_link_text("Inmarsat-C : twostage").click()
    self.driver.find_element_by_link_text("Inmarsat-C : Thrane&Thrane").click()
    time.sleep(1)
    # Enter serial number
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
    self.driver.find_element_by_id("mt-0-channel-0-frequencyExpected").send_keys(expectedFrequencyHours)
    # Grace period
    self.driver.find_element_by_id("mt-0-channel-0-frequencyGrace").send_keys(gracePeriodFrequencyHours)
    # In port
    self.driver.find_element_by_id("mt-0-channel-0-frequencyPort").send_keys(inPortFrequencyHours)
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
    # Shutdown browser
    shutdown_browser(self)

def create_one_new_mobile_terminal_via_asset_tab(self, mobileTerminalNumber, vesselNumber):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    # Click on asset tab
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(10)
    # Search for created asset
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumber])
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(10)
    # Click on details button
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(10)
    # Click on add new terminal button
    self.driver.find_element_by_id("menu-bar-vessel-add-terminal").click()
    time.sleep(1)
    # Select Transponder system
    self.driver.find_element_by_id("mt-0-typeAndPlugin").click()
    time.sleep(1)
#    self.driver.find_element_by_link_text("Inmarsat-C : twostage").click()
    self.driver.find_element_by_link_text("Inmarsat-C : Thrane&Thrane").click()
    time.sleep(1)
    # Enter serial number
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
    self.driver.find_element_by_id("mt-0-channel-0-frequencyExpected").send_keys(expectedFrequencyHours)
    # Grace period
    self.driver.find_element_by_id("mt-0-channel-0-frequencyGrace").send_keys(gracePeriodFrequencyHours)
    # In port
    self.driver.find_element_by_id("mt-0-channel-0-frequencyPort").send_keys(inPortFrequencyHours)
    # Activate Mobile Terminal button
    self.driver.find_element_by_id("mt-0-activation").click()
    time.sleep(3)
    # Click on save button
    self.driver.find_element_by_xpath("//*[@id='menu-bar-update']").click()
    time.sleep(5)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)
    # Shutdown browser
    shutdown_browser(self)

def create_one_new_mobile_terminal_via_asset_tab_with_parameters(self, vesselName, parameterList):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    # Click on asset tab
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(1)
    # Search for created asset
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName)
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(3)
    # Click on details button
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(3)
    # Click on add new terminal button
    self.driver.find_element_by_id("menu-bar-vessel-add-terminal").click()
    time.sleep(1)
    # Select Transponder system
    self.driver.find_element_by_id("mt-0-typeAndPlugin").click()
    time.sleep(1)
#    self.driver.find_element_by_link_text("Inmarsat-C : twostage").click()
    self.driver.find_element_by_link_text("Inmarsat-C : Thrane&Thrane").click()
    time.sleep(1)
    # Enter serial number
    self.driver.find_element_by_id("mt-0-serialNumber").send_keys(parameterList[0])
    # Enter Transceiver type
    self.driver.find_element_by_id("mt-0-tranciverType").send_keys(parameterList[1])
    # Enter Software Version
    self.driver.find_element_by_id("mt-0-softwareVersion").send_keys(parameterList[2])
    # Enter Antenna
    self.driver.find_element_by_id("mt-0-antenna").send_keys(parameterList[3])
    # Enter Satellite Number
    self.driver.find_element_by_id("mt-0-satelliteNumber").send_keys(parameterList[4])
    # Enter DNID Number
    self.driver.find_element_by_name("dnid").send_keys(parameterList[5])
    # Enter Member Number
    self.driver.find_element_by_name("memberId").send_keys(parameterList[6])
    # Enter Installed by
    self.driver.find_element_by_id("mt-0-channel-0-installedBy").send_keys(parameterList[7])
    # Expected frequency
    self.driver.find_element_by_id("mt-0-channel-0-frequencyExpected").send_keys(parameterList[8])
    # Grace period
    self.driver.find_element_by_id("mt-0-channel-0-frequencyGrace").send_keys(parameterList[10])
    # In port
    self.driver.find_element_by_id("mt-0-channel-0-frequencyPort").send_keys(parameterList[12])
    # Activate Mobile Terminal button
    self.driver.find_element_by_id("mt-0-activation").click()
    time.sleep(3)
    # Click on save button
    self.driver.find_element_by_xpath("//*[@id='menu-bar-update']").click()
    time.sleep(5)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)
    # Shutdown browser
    shutdown_browser(self)




def check_new_asset_exists(self, vesselNumber):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(5)
    # Search for the new created asset in the asset list
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumber])
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(5)
    # Check that the new asset exists in the list.
    self.assertEqual(vesselName[vesselNumber], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[vesselNumber] + "\"]").text)
    time.sleep(1)
    # Click on details button for new asset
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(5)
    # Check that the F.S value is correct.
    self.assertEqual(countryValue, self.driver.find_element_by_id("asset-input-countryCode").text)
    # Check that the IRCS value is correct
    self.assertEqual(ircsValue[vesselNumber], self.driver.find_element_by_id("asset-input-ircs").get_attribute("value"))
    # Check that the Name value is correct
    self.assertEqual(vesselName[vesselNumber], self.driver.find_element_by_id("asset-input-name").get_attribute("value"))
    # Check that External Marking Value is correct
    self.assertEqual(externalMarkingValue, self.driver.find_element_by_id("asset-input-externalMarking").get_attribute("value"))
    # Check that the CFR value is correct
    self.assertEqual(cfrValue[vesselNumber], self.driver.find_element_by_id("asset-input-cfr").get_attribute("value"))
    # Check that the IMO value is correct
    self.assertEqual(imoValue[vesselNumber], self.driver.find_element_by_id("asset-input-imo").get_attribute("value"))
    # Check that the HomePort value is correct
    self.assertEqual(homeportValue, self.driver.find_element_by_id("asset-input-homeport").get_attribute("value"))
    # Check that the Gear Type value is correct.
    self.assertEqual(gearTypeValue, self.driver.find_element_by_id("asset-input-gearType").text)
    # Check that the MMSI value is correct
    self.assertEqual(mmsiValue[vesselNumber], self.driver.find_element_by_id("asset-input-mmsi").get_attribute("value"))
    # Check that the License Type value is correct.
    self.assertEqual(licenseTypeValue, self.driver.find_element_by_id("asset-input-licenseType").text)
    # Check that the Length Type value is correct.
    self.assertEqual(lengthValue, self.driver.find_element_by_id("asset-input-lengthValue").get_attribute("value"))
    # Check that the Gross Tonnage value is correct.
    self.assertEqual(grossTonnageValue, self.driver.find_element_by_id("asset-input-grossTonnage").get_attribute("value"))
    # Check that the Power value is correct.
    self.assertEqual(powerValue, self.driver.find_element_by_id("asset-input-power").get_attribute("value"))
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
    time.sleep(1)
    # Check that the Contact Name value is correct.
    self.assertEqual(contactNameValue, self.driver.find_element_by_id("asset-input-contact-name-0").get_attribute("value"))
    # Check that the E-mail value is correct.
    self.assertEqual(contactEmailValue, self.driver.find_element_by_id("asset-input-contact-email-0").get_attribute("value"))
    # Check that the E-mail value is correct.
    self.assertEqual(contactPhoneNumberValue, self.driver.find_element_by_id("asset-input-contact-number-0").get_attribute("value"))
    time.sleep(5)
    # Shutdown browser
    shutdown_browser(self)

def check_new_mobile_terminal_exists(self, mobileTerminalNumber):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    # Select Mobile Terminal tab
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(2)
    # Enter Serial Number in
    self.driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(serialNoValue[mobileTerminalNumber])
    # Click in search button
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(5)
    # Check Serial Number in the list
    self.assertEqual(serialNoValue[mobileTerminalNumber], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[3]").text)
    # Check Member Number in the list
    self.assertEqual(memberIdnumber[mobileTerminalNumber], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
    # Check DNID Number in the list
    self.assertEqual(dnidNumber[mobileTerminalNumber], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)
    # Click on details button
    self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
    time.sleep(2)
    # Check Serial Number
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
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)
    # Shutdown browser
    shutdown_browser(self)

def link_asset_and_mobile_terminal(self, mobileTerminalNumber):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    # Select Mobile Terminal tab
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(2)
    # Enter Serial Number in field
    self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(serialNoValue[mobileTerminalNumber])
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
    self.driver.find_element_by_xpath("(//input[@type='text'])[23]").send_keys(ircsValue[mobileTerminalNumber])
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(2)
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
    # Shutdown browser
    shutdown_browser(self)


def change_and_check_speed_format(self,unitNumber):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    # Select Admin tab
    self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
    time.sleep(5)
    self.driver.find_element_by_link_text("CONFIGURATION").click()
    time.sleep(3)
    # Click on Global setting subtab under Configuration Tab
    self.driver.find_element_by_css_selector("#globalSettings > span").click()
    time.sleep(1)
    # Set Speed format to knots
    self.driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
    time.sleep(1)
    self.driver.find_element_by_link_text(speedUnitTypesInText[unitNumber]).click()
    time.sleep(2)
    # Click on Position Tab to check correct speed unit
    self.driver.find_element_by_id("uvms-header-menu-item-movement").click()
    time.sleep(5)
    currentSpeedValue = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[11]").text
    print("Current: " +  currentSpeedValue + " Short Unit: " + speedUnitTypesShort[unitNumber])
    if currentSpeedValue.find(speedUnitTypesShort[unitNumber]) == -1:
        foundCorrectUnit = False
    else:
        foundCorrectUnit = True
    self.assertTrue(foundCorrectUnit)
    time.sleep(5)
    # Shutdown browser
    shutdown_browser(self)



def generate_and_verify_manual_position(self,speedValue,courseValue):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    # Select Positions tab
    self.driver.find_element_by_id("uvms-header-menu-item-movement").click()
    time.sleep(2)
    # Click on New manual report
    self. driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(2)
    # Enter IRCS value
    self.driver.find_element_by_name("ircs").send_keys(ircsValue[0])
    time.sleep(5)
    self.driver.find_element_by_css_selector("strong").click()
    time.sleep(2)
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
    self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
    time.sleep(5)
    # Click on Confirm button
    self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
    time.sleep(20)
    # Enter IRCS for newly created position
    self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
    time.sleep(2)
    self.driver.find_element_by_link_text("Custom").click()
    self.driver.find_element_by_xpath("//input[@type='text']").clear()
    self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
    time.sleep(5)
    # Click on search button
    self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
    time.sleep(5)
    # Verifies position data
    self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
    self.assertEqual(externalMarkingValue, self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
    self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
    self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
    self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[6]").text)
    self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][0] + "\"]").text)
    self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][1] + "\"]").text)
    self.assertEqual("%.2f" % speedValue + " kts", self.driver.find_element_by_css_selector("td[title=\"" + "%.2f" % speedValue + " kts" + "\"]").text)
    self.assertEqual(str(courseValue) + "°", self.driver.find_element_by_css_selector("td[title=\"" + str(courseValue) + "°" + "\"]").text)
    self.assertEqual(sourceValue[1], self.driver.find_element_by_css_selector("td[title=\"" + sourceValue[1] + "\"]").text)
    time.sleep(5)
    return earlierPositionDateTimeValueString


def generate_NAF_and_verify_position(self,speedValue,courseValue):
    # Get Current Date and time in UTC
    currentUTCValue = datetime.datetime.utcnow()
    earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
    earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
    earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
    earlierPositionDateTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:00')
    # Generate NAF string to send
    nafSource = '//SR//FR/'
    nafSource = nafSource + countryValue
    nafSource = nafSource + "//AD/UVM//TM/POS//RC/"
    nafSource = nafSource + ircsValue[0]
    nafSource = nafSource + "//IR/"
    nafSource = nafSource + cfrValue[0]
    nafSource = nafSource + "//XR/"
    nafSource = nafSource + externalMarkingValue
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
    nafSource = nafSource + countryValue
    nafSource = nafSource + "//ER//"
    nafSourceURLcoded = urllib.parse.quote_plus(nafSource)
    totalNAFrequest = httpNAFRequestString + nafSourceURLcoded
    # Generate request
    r = requests.get(totalNAFrequest)
    # Check if request is OK (200)
    if r.ok:
        print("200 OK")
    else:
        print("Request NOT OK!")
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    time.sleep(5)
    # Select Positions tab
    self.driver.find_element_by_id("uvms-header-menu-item-movement").click()
    time.sleep(7)
    # Enter IRCS for newly created position
    self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
    self.driver.find_element_by_link_text("Custom").click()
    self.driver.find_element_by_xpath("//input[@type='text']").clear()
    self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
    time.sleep(5)
    # Click on search button
    self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
    time.sleep(5)
    # Enter Vessel to verify position data
    self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
    self.assertEqual(externalMarkingValue,
                     self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
    self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
    self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
    self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[6]").text)
    self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][0] + "\"]").text)
    self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][1] + "\"]").text)
    self.assertEqual("%.2f" % speedValue + " kts", self.driver.find_element_by_css_selector("td[title=\"" + "%.2f" % speedValue + " kts" + "\"]").text)
    self.assertEqual(str(courseValue) + "°", self.driver.find_element_by_css_selector("td[title=\"" + str(courseValue) + "°" + "\"]").text)
    self.assertEqual(sourceValue[0], self.driver.find_element_by_css_selector("td[title=\"" + sourceValue[0] + "\"]").text)
    time.sleep(5)
    return earlierPositionDateTimeValueString

def generate_NAF_string(self,countryValue,ircsValue,cfrValue,externalMarkingValue,latValue,longValue,speedValue,courseValue,dateValue,timeValue,vesselNameValue):
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
    print('Inside generate_NAF_string 1: ' + str(speedValue))
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

def get_elements_from_file(self, fileName):
    print('----------------------------')
    cwd = os.getcwd()
    print('Current working dir: ' + cwd)
    print('Open file: ' + fileName)
    print('----------------------------')
    # Open csv file and return all elements in list
    ifile = open(fileName, "rt", encoding="utf8")
    reader = csv.reader(ifile, delimiter=';')
    allRows = ['']
    for row in reader:
        allRows.append(row)
    ifile.close()
    del allRows[0]
    return allRows


def create_asset_from_file(self, assetFileName):
    # Create asset (assetFileName)

    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(self, assetFileName)

    # create_one_new_asset
    for x in range(1, len(assetAllrows)):
        create_one_new_asset_from_gui_with_parameters(self, assetAllrows[x])


def create_mobileterminal_from_file(self, assetFileName, mobileTerminalFileName):
    # Create Mobile Terminal for mentioned asset (assetFileName, mobileTerminalFileName)

    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(self, assetFileName)

    # Open saved csv file and read all mobile terminal elements
    mobileTerminalAllrows = get_elements_from_file(self, mobileTerminalFileName)

    # create_one new mobile terminal for mentioned asset
    for x in range(1, len(assetAllrows)):
        create_one_new_mobile_terminal_via_asset_tab_with_parameters(self, assetAllrows[x][1], mobileTerminalAllrows[x])


def create_trip_from_file(self,deltaTimeValue, assetFileName, tripFileName):
    # Create Trip for mentioned asset and Mobile Terminal(assetFileName, tripFileName)

    # Set Current Date and time in UTC 24h back
    currentUTCValue = datetime.datetime.utcnow()
    currentPositionTimeValue = currentUTCValue - deltaTimeValue

    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(self, assetFileName)

    # Open saved csv file and read all trip elements for asset
    assetTripAllrows = get_elements_from_file(self, tripFileName)

    # create trip for mentioned asset and mobile terminal
    for x in range(1, len(assetAllrows)):
        # create number of position reports for the newly created asset/mobile terminal
        for y in range(1, len(assetTripAllrows)):
            # Create one position report via NAF
            currentPositionTimeValue = currentPositionTimeValue + datetime.timedelta(
                minutes=int(assetTripAllrows[y][5]))
            currentPositionDateValueString = datetime.datetime.strftime(currentPositionTimeValue, '%Y%m%d')
            currentPositionTimeValueString = datetime.datetime.strftime(currentPositionTimeValue, '%H%M')
            nafSource = generate_NAF_string(self, countryValue, assetAllrows[x][0], assetAllrows[x][2], assetAllrows[x][3], str("%.3f" % float(assetTripAllrows[y][1])), str("%.3f" % float(assetTripAllrows[y][0])), float(assetTripAllrows[y][3]), assetTripAllrows[y][4], currentPositionDateValueString, currentPositionTimeValueString, assetAllrows[x][1])
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
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(self, assetFileName)
    # Open saved csv file and read all trip elements for asset
    assetTripAllrows = get_elements_from_file(self, tripFileName)
    time.sleep(5)
    # Create a new Report
    # Select Reporting tab
    self.driver.find_element_by_id("uvms-header-menu-item-reporting").click()
    time.sleep(15)
    # Click on New Report button
    self.driver.find_element_by_xpath("(//button[@type='button'])[18]").click()
    time.sleep(2)
    # Enter reporting name (based on 1st ircs name from asset file)
    reportName = "Test (only " + assetAllrows[1][0] +")"
    self.driver.find_element_by_id("reportName").send_keys(reportName)
    # Enter Start and end Date Time
    currentUTCValue = datetime.datetime.utcnow()
    startTimeValue = currentUTCValue - datetime.timedelta(hours=336) # 2 weeks back
    endTimeValue = currentUTCValue + datetime.timedelta(hours=336) # 2 weeks ahead
    self.driver.find_element_by_id("report-start-date-picker").send_keys(startTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(1)
    self.driver.find_element_by_id("report-end-date-picker").send_keys(endTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(1)
    # Select asset view
    self.driver.find_element_by_link_text("Select assets").click()
    time.sleep(2)
    # Enter asset value
    self.driver.find_element_by_xpath("(//input[@type='text'])[13]").send_keys(assetAllrows[1][0])
    time.sleep(5)
    # Select Asset and save
    self.driver.find_element_by_xpath("(//button[@type='button'])[27]").click()
    time.sleep(5)
    self.driver.find_element_by_xpath("(//button[@type='button'])[31]").click()
    time.sleep(5)
    self.driver.find_element_by_xpath("(//button[@type='button'])[35]").click()
    time.sleep(5)
    # Run the new report
    self.driver.find_element_by_xpath("(//button[@type='button'])[19]").click()
    time.sleep(10)
    # Click on Tabular view icon
    self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
    time.sleep(2)
    # Click on Date column tab (To sort on Date)
    self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/thead/tr[3]/th[5]/div").click()
    time.sleep(2)

    # Check the 5 first positions for mentioned asset
    for y in range(1, 6):
        self.assertEqual(str("%.3f" % float(assetTripAllrows[y][0])), self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[6]/div").text)
        self.assertEqual(str("%.3f" % float(assetTripAllrows[y][1])), self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[7]/div").text)
        # Special case if speed is zero (No decimals then)
        if float(assetTripAllrows[y][3]) == 0:
            self.assertEqual(assetTripAllrows[y][3] + " kts", self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[9]/div").text)
        else:
            #self.assertEqual(str("%.5f" % float(assetTripAllrows[y][3])) + " kts", self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[9]/div").text)
            # Compare expected value with 5 decimals that only has 4 decimals resolution
            self.assertEqual(str("%.5f" % float(str("%.4f" % float(assetTripAllrows[y][3])))) + " kts", self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[9]/div").text)
        self.assertEqual(assetTripAllrows[y][4] + "°", self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[11]/div").text)
    time.sleep(5)

    shutdown_browser(self)



if os.name == 'nt':
    # We redefine timeout_decorator on windows
    class timeout_decorator:
        @staticmethod
        def timeout(*args, **kwargs):
            return lambda f: f # return a no-op decorator
else:
    import timeout_decorator

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

    def tearDown(self):
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=1000)
    def test_0001_reset_database_union_vms(self):
        # Create Browser
        self.driver = webdriver.Chrome()
        # Save current default dir path
        default_current_dir = os.getcwd()
        # Reset Module Database
        resetModuleDatabase()
        # Return to default current dir
        os.chdir(default_current_dir)
        # Populate Iridium Imarsat-C Data
        populateIridiumImarsatCData()
        # Populate Sanity Rule Data
        #populateSanityRuleData()
        time.sleep(15)


    @timeout_decorator.timeout(seconds=180)
    def test_0001b_change_default_configuration_parameters(self):
        # The test case changes Default home page to asset and Coordinates format to dd.mmm
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # if Reporting Query List is presented, then close it
        try:
            if self.driver.find_element_by_css_selector("h4.modal-title"):
                self.driver.find_element_by_xpath("//div[@id='map']/div[5]/div/div/div/div/div/i").click()
                time.sleep(2)
        except:
            pass
        # Select Admin tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("CONFIGURATION").click()
        time.sleep(3)
        # Click on Global setting subtab under Configuration Tab
        self.driver.find_element_by_css_selector("#globalSettings > span").click()
        time.sleep(1)
        # Click to change Coordinates format to dd.mmm
        self.driver.find_element_by_xpath("(//input[@name='coordinateFormat'])[2]").click()
        time.sleep(7)
        # Click to change Default home page to Asset page
        self.driver.find_element_by_xpath("//button[@id='']").click()
        time.sleep(5)
        self.driver.find_element_by_id("-item-2").click()
        time.sleep(5)

        # Shutdown browser
        shutdown_browser(self)

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
    def test_0007_generate_and_verify_manual_position(self):
        # Create a manual position and verify the position
        generate_and_verify_manual_position(self, reportedSpeedValue, reportedCourseValue)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0008_generate_NAF_and_verify_position(self):
        # Create a NAF position and verify the position
        generate_NAF_and_verify_position(self,reportedSpeedValue,reportedCourseValue)
        # Shutdown browser
        shutdown_browser(self)


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
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Enter Serial Number in field
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(serialNoValue[0])
        # Click in search button
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(5)
        # Click on details button
        self.driver.find_element_by_id("mt-toggle-form").click()
        time.sleep(2)
        # Click on unlinking button
        self.driver.find_element_by_id("menu-bar-unlink").click()
        time.sleep(1)
        # Enter comment and click on unlinking button
        self.driver.find_element_by_name("comment").send_keys("Unlink Asset and MT.")
        self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0014_generate_manual_position_with_no_connected_transponder_and_verify_holding_table(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Positions tab
        self.driver.find_element_by_id("uvms-header-menu-item-movement").click()
        time.sleep(2)
        # Click on New manual report
        self. driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(3)
        # Enter IRCS value
        self.driver.find_element_by_name("ircs").send_keys(ircsValue[0])
        time.sleep(5)
        self.driver.find_element_by_css_selector("strong").click()
        time.sleep(2)
        # Get Current Date and time in UTC
        currentUTCValue = datetime.datetime.utcnow()
        earlierPositionTimeValue = currentUTCValue - datetime.timedelta(hours=deltaTimeValue)
        earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y-%m-%d %H:%M:%S')
        self.driver.find_element_by_id("manual-movement-date-picker").clear()
        self.driver.find_element_by_id("manual-movement-date-picker").send_keys(earlierPositionTimeValueString)
        # Enter Position, Speed and Course
        self.driver.find_element_by_name("latitude").clear()
        self.driver.find_element_by_name("latitude").send_keys(lolaPositionValues[0][0][0])
        self.driver.find_element_by_name("longitude").clear()
        self.driver.find_element_by_name("longitude").send_keys(lolaPositionValues[0][0][1])
        self.driver.find_element_by_name("measuredSpeed").send_keys("5")
        self.driver.find_element_by_name("course").send_keys("180")
        # Click on Save Button
        self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
        time.sleep(5)
        # Click on Confirm button
        self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
        time.sleep(15)
        # Enter IRCS for newly created position
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Custom").click()
        self.driver.find_element_by_xpath("//input[@type='text']").clear()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
        # Click on search button
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(5)
        # Verifies that time stamp for the generated position that does not exist
        self.assertNotEqual(earlierPositionTimeValueString, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[6]").text)
        time.sleep(2)
        # Select Alarms tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(4)
        # Select filter "Transponder not found"
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Transponder not found").click()
        time.sleep(2)
        # Click on search button
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)
        # Check Asset name
        self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
        # Click on Details button
        self.driver.find_element_by_xpath("(//button[@type='button'])[9]").click()
        time.sleep(2)
        # Check Position report fields
        self.assertEqual(countryValue, self.driver.find_element_by_xpath("/html/body/div[7]/div/div/div[2]/div[3]/div[2]/div[1]/div").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_xpath("//div[3]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_xpath("//div[3]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[3]/div[2]/div[4]/div").text)
        self.assertEqual(earlierPositionTimeValueString, self.driver.find_element_by_xpath("//div[7]/div/div[2]/div").text)
        self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_xpath("//div[7]/div[2]/div/div").text)
        self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_xpath("//div[7]/div[2]/div[2]/div").text)
        self.assertEqual("%.0f" % reportedSpeedValue + " kts", self.driver.find_element_by_xpath("//div[7]/div[2]/div[3]/div").text)
        self.assertEqual(str(reportedCourseValue) + " °", self.driver.find_element_by_xpath("//div[7]/div[2]/div[4]/div").text)
        time.sleep(2)
        # Close Report Window
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0015_link_asset_to_another_mobile_terminal(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Enter Serial Number in field
        self.driver.find_element_by_id("mt-input-search-serialNumber").send_keys(serialNoValue[1])
        # Click in search button
        self.driver.find_element_by_id("mt-btn-advanced-search").click()
        time.sleep(5)
        # Click on details button
        self.driver.find_element_by_id("mt-toggle-form").click()
        time.sleep(2)
        # Click on Link Asset
        self.driver.find_element_by_id("mt-btn-assign-asset").click()
        time.sleep(2)
        # Enter Asset Name and clicks on the search button
        self.driver.find_element_by_xpath("(//input[@type='text'])[23]").send_keys(vesselName[0])
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)
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
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0016_generate_and_verify_manual_position(self):
        # Startup browser and login
        UnionVMSTestCase.test_0007_generate_and_verify_manual_position(self)


    @timeout_decorator.timeout(seconds=300)
    def test_0017_create_assets_3_4_5_6(self):
        # Create assets 3-6 in the list
        for x in range(2, 6):
            create_one_new_asset_from_gui(self, x)
            time.sleep(1)


    @timeout_decorator.timeout(seconds=180)
    def test_0018_create_two_assets_to_group_and_check_group(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Search for "fartyg"
        self.driver.find_element_by_id("asset-input-simple-search").send_keys("fartyg")
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
        # Select Fartyg1001 and Fartyg1002 by click
        self.driver.find_element_by_css_selector("td.checkboxContainer > input[type=\"checkbox\"]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        # Select Action "Save as Group"
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Save as Group").click()
        time.sleep(1)
        # Enter Group name and click on save button
        self.driver.find_element_by_css_selector("form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]").send_keys(groupName[0])
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(8)
        # Check that Grupp 1 has been created
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        time.sleep(1)
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        time.sleep(2)
        # Click on Grupp 1
        self.driver.find_element_by_link_text(groupName[0]).click()
        time.sleep(5)
        # Check Assets in Group
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)
        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[1], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[1] + "\"]").text)
        self.assertEqual(ircsValue[1], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[1] + "\"]").text)
        self.assertEqual(cfrValue[1], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[1] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0019_add_two_assets_to_group_and_check_group(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Search for "fartyg"
        self.driver.find_element_by_id("asset-input-simple-search").send_keys("fartyg")
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
            time.sleep(2)
        # Select Fartyg1005 and Fartyg1006 by click
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[6]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[7]").click()
        # Select Action "Add to Group"
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        time.sleep(2)
        self.driver.find_element_by_link_text("Add to Group").click()
        time.sleep(2)
        # Select "Grupp 1" and click on save button
        self.driver.find_element_by_id("saveGroupDropdown").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(),'Grupp 1')]").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(5)
        # Check that Grupp 1 has been created
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        time.sleep(1)
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        time.sleep(2)
        # Click on Grupp 1
        self.driver.find_element_by_link_text(groupName[0]).click()
        time.sleep(5)
        # Check Assets in Group
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)

        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[1], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[1] + "\"]").text)
        self.assertEqual(ircsValue[1], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[1] + "\"]").text)
        self.assertEqual(cfrValue[1], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[1] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)

        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[3]").text)
        self.assertEqual(vesselName[4], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[4] + "\"]").text)
        self.assertEqual(ircsValue[4], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[4] + "\"]").text)
        self.assertEqual(cfrValue[4], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[4] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[8]").text)

        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[3]").text)
        self.assertEqual(vesselName[5], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[5] + "\"]").text)
        self.assertEqual(ircsValue[5], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[5] + "\"]").text)
        self.assertEqual(cfrValue[5], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[5] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[8]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)

	
    @timeout_decorator.timeout(seconds=180)
    def test_0020_remove_one_asset_group_and_check_group(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on saved groups
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        time.sleep(2)
        # Click on Grupp 1
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
        time.sleep(1)
        # Click on action button
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        time.sleep(1)
        # Remove selected assets from Grupp 1
        self.driver.find_element_by_link_text("Remove from Group").click()
        time.sleep(5)
        # Reload page
        self.driver.refresh()
        time.sleep(10)
        # Click on saved groups
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        time.sleep(2)
        # Click on Grupp 1
        self.driver.find_element_by_link_text(groupName[0]).click()
        time.sleep(5)
        # Check Assets in Group
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)
        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[5], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[5] + "\"]").text)
        self.assertEqual(ircsValue[5], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[5] + "\"]").text)
        self.assertEqual(cfrValue[5], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[5] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0021_create_second_group_and_add_assets_to_group(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Search for "fartyg"
        self.driver.find_element_by_id("asset-input-simple-search").send_keys("fartyg")
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
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Save as Group").click()
        time.sleep(1)
        # Enter Group name and click on save button
        self.driver.find_element_by_css_selector("form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]").send_keys(groupName[1])
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(8)
        # Check that Grupp 2 has been created
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        time.sleep(1)
        self.assertEqual(groupName[1], self.driver.find_element_by_link_text(groupName[1]).text)
        time.sleep(2)
        # Click on Grupp 2
        self.driver.find_element_by_link_text(groupName[1]).click()
        time.sleep(5)
        # Check Assets in Group
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
        self.assertEqual(vesselName[2], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[2] + "\"]").text)
        self.assertEqual(ircsValue[2], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[2] + "\"]").text)
        self.assertEqual(cfrValue[2], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[2] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)
        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[4], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[4] + "\"]").text)
        self.assertEqual(ircsValue[4], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[4] + "\"]").text)
        self.assertEqual(cfrValue[4], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[4] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0022_delete_second_group_and_check(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on "saved groups" drop box
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        time.sleep(2)
        # Click on delete button for Grupp 2
        self.driver.find_element_by_id("asset-dropdown-saved-search-delete-item-1").click()
        time.sleep(2)
        # Click on confirmation button
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(5)
        # Reload page
        self.driver.refresh()
        time.sleep(10)
        # Check that Grupp 1 exists and Grupp 2 does not exist
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        time.sleep(1)
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        try:
            self.assertFalse(self.driver.find_element_by_link_text(groupName[1]).text)
        except NoSuchElementException:
            pass
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0023_advanced_search_of_assets(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on advanced search
        self.driver.find_element_by_css_selector("#asset-toggle-search-view > span").click()
        time.sleep(1)
        # Search for all External Marking called "EXT3"(externalMarkingValue)
        self.driver.find_element_by_id("asset-input-search-externalMarking").send_keys(externalMarkingValue)
        self.driver.find_element_by_id("asset-btn-advanced-search").click()
        time.sleep(7)

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
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual(gearTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + gearTypeValue + "\"]").text)
        self.assertEqual(licenseTypeValue, self.driver.find_element_by_css_selector("td[title=\"" + licenseTypeValue + "\"]").text)
        for x in [1,2,3,4,5]:
            self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[2]").text)
            self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[3]").text)
            self.assertEqual(vesselName[x], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[x] + "\"]").text)
            self.assertEqual(ircsValue[x], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[x] + "\"]").text)
            self.assertEqual(cfrValue[x], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[x] + "\"]").text)
            self.assertEqual(gearTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[7]").text)
            self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[8]").text)
        time.sleep(3)
        # Click on save group button
        self.driver.find_element_by_css_selector("#asset-btn-save-search > span").click()
        self.driver.find_element_by_css_selector("form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]").send_keys(groupName[2])
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(5)
        # Reload page
        self.driver.refresh()
        time.sleep(10)
        # Check that Grupp 3 exists in the list
        self.driver.find_element_by_id("asset-dropdown-saved-search").click()
        self.assertEqual(groupName[2], self.driver.find_element_by_link_text(groupName[2]).text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0024_export_assets_to_excel_file(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Search for "fartyg"
        self.driver.find_element_by_id("asset-input-simple-search").send_keys("fartyg")
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
        # Select Fartyg1001 and Fartyg1002 by click
        self.driver.find_element_by_css_selector("td.checkboxContainer > input[type=\"checkbox\"]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        time.sleep(2)
        # Select Action "Export selection"
        self.driver.find_element_by_id("asset-dropdown-actions").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Save path to current dir
        cwd = os.getcwd()
        # Change to Download folder for current user
        home = expanduser("~")
        os.chdir(home)
        os.chdir(downloadPath)
        print(os.getcwd())
        # Open saved csv file and read all elements to "allrows"
        ifile  = open('assets.csv', "rt", encoding="utf8")
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
                self.assertEqual(countryValue, allrows[y][0])
                self.assertEqual(externalMarkingValue, allrows[y][1])
                self.assertEqual(vesselName[y-1], allrows[y][2])
                self.assertEqual(ircsValue[y-1], allrows[y][3])
                self.assertEqual(cfrValue[y-1], allrows[y][4])
                self.assertEqual(gearTypeValue, allrows[y][5])
                self.assertEqual(licenseTypeValue, allrows[y][6])
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=300)
    def test_0025_create_new_mobile_terminal_3_6(self):
        # Create new Mobile Terminal (Number 3-6 in the list)
        for x in [2,3,4,5]:
            create_one_new_mobile_terminal_from_gui(self, x)


    @timeout_decorator.timeout(seconds=180)
    def test_0026_export_mobile_terminals_to_excel_file(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(7)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(5)
        # Search on MemberID 100
        self.driver.find_element_by_xpath("(//input[@type='text'])[9]").send_keys(memberIdnumber[0])
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)
        # Sort on "Serial no"
        self.driver.find_element_by_id("mt-sort-serialNumber").click()
        time.sleep(3)
        # Select Not linked row number 2-4 by click
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[4]").click()
        time.sleep(2)
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
        # Select Action "Export selection"
        self.driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Save path to current dir
        cwd = os.getcwd()
        # Change to Download folder for current user
        home = expanduser("~")
        os.chdir(home)
        os.chdir(downloadPath)
        print(os.getcwd())
        # Open saved csv file and read all elements to "allrows"
        ifile  = open('mobileTerminals.csv', "rt", encoding="utf8")
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

        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0027_view_audit_log(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(7)
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(7)
        # Click on all sub tabs under Audit Log Tab
        self.driver.find_element_by_css_selector("#EXCHANGE > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#POSITION_REPORTS > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#GIS > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#ALARMS > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#ACCESS_CONTROL > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#ALL > span").click()
        time.sleep(2)
        # Check sub tab names
        self.assertEqual("ALL", self.driver.find_element_by_css_selector("#ALL > span").text)
        self.assertEqual("EXCHANGE", self.driver.find_element_by_css_selector("#EXCHANGE > span").text)
        self.assertEqual("POSITION REPORTS", self.driver.find_element_by_css_selector("#POSITION_REPORTS > span").text)
        self.assertEqual("ASSETS AND TERMINALS", self.driver.find_element_by_css_selector("#ASSETS_AND_TERMINALS > span").text)
        self.assertEqual("GIS", self.driver.find_element_by_css_selector("#GIS > span").text)
        self.assertEqual("ALERTS", self.driver.find_element_by_css_selector("#ALARMS > span").text)
        self.assertEqual("ACCESS CONTROL", self.driver.find_element_by_css_selector("#ACCESS_CONTROL > span").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0028_view_audit_and_export_log_to_file(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(7)
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(7)
        # Enter User Name in the Username field
        self.driver.find_element_by_xpath("//input[@type='text']").clear()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(defaultUserName)
        time.sleep(1)
        # Filter on Create Operation
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[3]/div/div[1]/div/div/form/div/div/div/div[1]/div[2]/div/div/ul/li[5]/a").click()
        time.sleep(1)
        # Click on search button
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(5)
        # Check that the 4 first items in the Audit list are Mobile Terminals logs
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
        # Select row number 1-4 by click
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[4]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[5]").click()
        # Select Action "Export selection"
        self.driver.find_element_by_id("admin-dropdown-actions").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection to CSV").click()
        time.sleep(3)
        # Save path to current dir
        cwd = os.getcwd()
        # Change to Download folder for current user
        home = expanduser("~")
        os.chdir(home)
        os.chdir(downloadPath)
        print(os.getcwd())
        # Open saved csv file and read all elements to "allrows"
        ifile  = open('auditLogs.csv', "rt", encoding="utf8")
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

        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0029_view_configuration_pages(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(7)
        # Select Admin tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("CONFIGURATION").click()
        time.sleep(2)
        # Click on all sub tabs under Configuration Tab
        self.driver.find_element_by_css_selector("#globalSettings > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#reporting > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#asset > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#mobileTerminal > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#exchange > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("#systemMonitor > span").click()
        time.sleep(5)
        # Check sub tab names
        self.assertEqual("SYSTEM MONITOR", self.driver.find_element_by_css_selector("#systemMonitor > span").text)
        self.assertEqual("GLOBAL SETTINGS", self.driver.find_element_by_css_selector("#globalSettings > span").text)
        self.assertEqual("REPORTING", self.driver.find_element_by_css_selector("#reporting > span").text)
        self.assertEqual("ASSETS", self.driver.find_element_by_css_selector("#asset > span").text)
        self.assertEqual("MOBILE TERMINALS", self.driver.find_element_by_css_selector("#mobileTerminal > span").text)
        self.assertEqual("EXCHANGE", self.driver.find_element_by_css_selector("#exchange > span").text)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0030_change_global_settings_change_date_format(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Admin tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("CONFIGURATION").click()
        time.sleep(3)
        # Click on Global setting subtab under Configuration Tab
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
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0030b_change_global_settings_change_date_format(self):
        # Startup browser and login
        UnionVMSTestCase.test_0030_change_global_settings_change_date_format(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0031_change_global_settings_change_speed_format(self):
        # Change and check speed unit type for Global Settings
        for x in [2,1,0]:
            change_and_check_speed_format(self,x)


    @timeout_decorator.timeout(seconds=180)
    def test_0032_check_view_help_text(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Click on User Guide icon (Question mark icon)
        # Note: User Guide page is opened in a new tab
        self.driver.find_element_by_xpath("//div[4]/a/i").click()
        time.sleep(10)
        # Switch tab focus for Selenium to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(3)
        # Check User guide page
        self.assertEqual("Union VMS - User Manual", self.driver.find_element_by_id("title-text").text)
        time.sleep(3)
        self.assertEqual("Welcome to Union VMS!", self.driver.find_element_by_xpath("//*[@id='main-content']/div[3]/ul/li[1]/span/a").text)
        time.sleep(5)

        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0033_check_alerts_view(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Alerts tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(3)
        # Check List Headlines for Holding Table
        self.assertEqual("Date triggered (UTC)", self.driver.find_element_by_css_selector("th.st-sort.st-sort-descent").text)
        self.assertEqual("Object affected", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]").text)
        self.assertEqual("Rule", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[4]").text)
        # Select Alerts tab (Notifications)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[2]/a").click()
        time.sleep(2)
        # Check List Headlines for Notifications
        self.assertEqual("Date triggered (UTC)", self.driver.find_element_by_css_selector("th.st-sort.st-sort-descent").text)
        self.assertEqual("Object affected", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]").text)
        self.assertEqual("Rule", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[4]").text)
        # Select Alerts tab (Rules)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Check List Headlines for Rules List
        self.assertEqual("Rule name", self.driver.find_element_by_css_selector("th.st-sort").text)
        self.assertEqual("Last triggered", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]").text)
        self.assertEqual("Date updated", self.driver.find_element_by_css_selector("th.st-sort.st-sort-descent").text)
        time.sleep(5)

        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0034_create_speed_rule_one(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
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
        self.driver.find_element_by_name("name").send_keys("Speed > " + str(reportedSpeedDefault[0]))
        time.sleep(1)
        # Enter Description
        self.driver.find_element_by_name("description").clear()
        self.driver.find_element_by_name("description").send_keys("Speed > " + str(reportedSpeedDefault[0]))
        time.sleep(1)
        # Enter Rule Speed > 8
        self.driver.find_element_by_xpath("(//button[@id=''])[3]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("(").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[4]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Position").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[5]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Reported speed").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[6]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text(">").click()
        time.sleep(1)
        self.driver.find_element_by_name("value").click()
        time.sleep(1)
        self.driver.find_element_by_name("value").clear()
        time.sleep(1)
        self.driver.find_element_by_name("value").send_keys(reportedSpeedDefault[0])
        time.sleep(1)
        self.driver.find_element_by_xpath("(//button[@id=''])[7]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text(")").click()
        time.sleep(2)
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
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0035_verify_created_speed_rule_one(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(7)
        # Select Alerts tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(2)
        # Select Alerts tab (Rules)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Check Headline Names
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
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0036_create_manual_position_with_speed_that_triggs_rule_one(self):
        # Create a manual position and verify the position
        earlierPositionDateTimeValueString = generate_and_verify_manual_position(self, reportedSpeedDefault[0] + 1, reportedCourseValue)

        # Click on Alert tab
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(5)
        # Click on Notifications tab
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(5)
        # Check Asset and Rule names
        self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
        self.assertEqual("Speed > " + str(reportedSpeedDefault[0]), self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + "\"]").text)
        # Click on details button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        time.sleep(2)
        # Check Position parameters
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("div.value").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[2]/div[2]/div[4]/div").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_xpath("//div[2]/div[5]/div").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedDefault[0] + 1) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0037_create_NAF_position_with_speed_that_triggs_rule_one(self):
        # Create a NAF position and verify the position
        earlierPositionDateTimeValueString = generate_NAF_and_verify_position(self, reportedSpeedDefault[0] + 1, reportedCourseValue)

        # Click on Alert tab
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(5)
        # Click on Notifications tab
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(5)
        # Check Asset and Rule names
        self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
        self.assertEqual("Speed > " + str(reportedSpeedDefault[0]), self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + "\"]").text)
        # Click on details button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        time.sleep(2)
        # Check Position parameters
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("div.value").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[2]/div").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[3]/div").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[2]/div[2]/div[4]/div").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_xpath("//div[2]/div[5]/div").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedDefault[0] + 1) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()

        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0038_inactivate_speed_rule_one_and_check(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Alerts tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(2)
        # Select Alerts tab (Rules)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Click on edit rule icon
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        time.sleep(2)
        # Click on selection drop down button
        self.driver.find_element_by_xpath("(//button[@id=''])[2]").click()
        time.sleep(2)
        # Select "Inactive" state
        self.driver.find_element_by_link_text("Inactive").click()
        time.sleep(2)
        # Click on update button
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(2)
        # Click on confirmation button
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(4)
        # Check that rule one is in inactive state
        self.assertEqual("INACTIVE", self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/span").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0039_create_manual_position_with_speed_that_not_triggs_speed_rule_one(self):
        # Create a manual position and verify the position
        earlierPositionDateTimeValueString = generate_and_verify_manual_position(self, reportedSpeedDefault[0] + 1, reportedCourseValue)
        # Click on Alert tab
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(5)
        # Click on Notifications tab
        self.driver.find_element_by_link_text("NOTIFICATIONS").click()
        time.sleep(5)
        # Get Asset and Rule names
        tempAsset = self.driver.find_element_by_link_text(vesselName[0]).text
        tempRuleName = self.driver.find_element_by_css_selector("td[title=\"Speed > " + str(reportedSpeedDefault[0]) + "\"]").text
        # Click on details button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/button").click()
        time.sleep(2)
        # Check that time is not correct
        self.assertNotEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        print(earlierPositionDateTimeValueString)
        print(self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0040_activate_speed_rule_one_and_check(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Alerts tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(2)
        # Select Alerts tab (Rules)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Click on edit rule icon
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        time.sleep(2)
        # Click on selection drop down button
        self.driver.find_element_by_xpath("(//button[@id=''])[2]").click()
        time.sleep(2)
        # Select "Inactive" state
        self.driver.find_element_by_link_text("Active").click()
        time.sleep(2)
        # Click on update button
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(2)
        # Click on confirmation button
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(4)
        # Check that rule one is in active state
        self.assertEqual("ACTIVE", self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]/span").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0041_remove_speed_rule_one(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Alerts tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(1)
        # Select Alerts tab (Rules)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Click on delete button icon
        self.driver.find_element_by_xpath("(//button[@type='button'])[8]").click()
        time.sleep(1)
        # Click on Yes button to comfirm
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0042_check_speed_rule_one_removed(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Alerts tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(1)
        # Select Alerts tab (Rules)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Try to find speed rule element)
        try:
            self.assertFalse(self.driver.find_element_by_css_selector("td.statusColored.truncate-text").text)
        except NoSuchElementException:
            pass
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0043_create_one_new_asset_and_mobile_terminal(self):
        # Create new asset (7th in the list)
        create_one_new_asset_from_gui(self, 6)
        create_one_new_mobile_terminal_via_asset_tab(self, 6, 6)


    @timeout_decorator.timeout(seconds=180)
    def test_0046_generate_manual_poll_and_check(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Polling tab
        self.driver.find_element_by_id("uvms-header-menu-item-polling-logs").click()
        time.sleep(5)
        # Click on new New poll button
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/div/ul/li[2]/a").click()
        #self.driver.find_element_by_link_text("New poll").click()
        time.sleep(2)
        # Search for IRCS
        self.driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(ircsValue[6])
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(5)
        # Select IRCS in the list
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/span/div/table/tbody/tr/td[6]/button").click()
        time.sleep(1)
        # Click on next button
        self.driver.find_element_by_css_selector("div.col-md-12.textAlignRight > button.btn.btn-primary").click()
        time.sleep(1)
        # Enter comment in comment field
        self.driver.find_element_by_name("comment").send_keys("The best comment to IRCS " + ircsValue[6])
        time.sleep(1)
        # Submit poll
        self.driver.find_element_by_css_selector("div.col-md-8.textAlignRight > button.btn.btn-primary").click()
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
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
        create_trip_from_file(self, datetime.timedelta(hours=72), 'asset1.csv', 'trip1.csv')
        create_trip_from_file(self, datetime.timedelta(hours=72), 'asset2.csv', 'trip2.csv')
        create_trip_from_file(self, datetime.timedelta(hours=72), 'asset3.csv', 'trip3.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0052b_create_report_and_check_asset_in_reporting_view(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)

        # Open saved csv file and read all asset elements
        assetAllrows = get_elements_from_file(self, 'asset1.csv')

        print(assetAllrows[1][0])

        time.sleep(5)
        # Select Reporting tab
        self.driver.find_element_by_id("uvms-header-menu-item-reporting").click()
        time.sleep(5)
        # Enter reporting name (based on 1st ircs name from asset file)
        reportName = "Test (only " + assetAllrows[1][0] +")"
        self.driver.find_element_by_id("reportName").send_keys(reportName)
        # Enter Start and end Date Time
        currentUTCValue = datetime.datetime.utcnow()
        startTimeValue = currentUTCValue - datetime.timedelta(hours=336) # 2 weeks back
        endTimeValue = currentUTCValue + datetime.timedelta(hours=336) # 2 weeks ahead
        self.driver.find_element_by_id("report-start-date-picker").send_keys(startTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)
        self.driver.find_element_by_id("report-end-date-picker").send_keys(endTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)
        # Select asset view
        self.driver.find_element_by_link_text("Select assets").click()
        time.sleep(2)
        # Enter asset value
        self.driver.find_element_by_xpath("(//input[@type='text'])[13]").send_keys(assetAllrows[1][0])
        time.sleep(2)
        # Select Asset and save
        self.driver.find_element_by_xpath("(//button[@type='button'])[26]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("(//button[@type='button'])[30]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("(//button[@type='button'])[33]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("(//button[@type='button'])[19]").click()
        time.sleep(10)
        # Click on Tabular view icon
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        time.sleep(2)
        # Click on Tracks tab
        self.driver.find_element_by_xpath("//*[@id='map']/div[6]/div/div/div/div/div/div[1]/ul/li[3]/a").click()
        time.sleep(2)
        # Check that only one row exist with 1st ircs name from asset file
        self.assertEqual(assetAllrows[1][0], self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div[3]/div/table/tbody/tr/td[3]/div").text)
        try:
            self.assertFalse(self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div[3]/div/table/tbody/tr[2]/td[3]/div").text)
        except NoSuchElementException:
            pass
        time.sleep(5)


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
        create_trip_from_file(self, datetime.timedelta(hours=72), 'asset4.csv', 'trip4.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0055b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'asset4.csv', 'trip4.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0056_create_assets_trip_5_and_6(self):
        # Create assets, Mobile for Trip 5
        create_asset_from_file(self, 'asset5.csv')
        create_mobileterminal_from_file(self, 'asset5.csv', 'mobileterminal5.csv')
        # Create assets, Mobile for Trip 6
        create_asset_from_file(self, 'asset6.csv')
        create_mobileterminal_from_file(self, 'asset6.csv', 'mobileterminal6.csv')
        # Create Trip 5-6
        create_trip_from_file(self, datetime.timedelta(hours=72), 'asset5.csv', 'trip5.csv')
        create_trip_from_file(self, datetime.timedelta(hours=61, minutes=40), 'asset6.csv', 'trip6.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0056b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'asset5.csv', 'trip5.csv')
        create_report_and_check_trip_position_reports(self, 'asset6.csv', 'trip6.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0057_create_assets_trip_7(self):
        # Create assets, Mobile for Trip 7
        create_asset_from_file(self, 'asset7.csv')
        create_mobileterminal_from_file(self, 'asset7.csv', 'mobileterminal7.csv')
        create_trip_from_file(self, datetime.timedelta(hours=72), 'asset7.csv', 'trip7.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0058_create_assets_trip_8(self):
        # Create assets, Mobile for Trip 8
        create_asset_from_file(self, 'asset8.csv')
        create_mobileterminal_from_file(self, 'asset8.csv', 'mobileterminal8.csv')
        create_trip_from_file(self, datetime.timedelta(hours=24), 'asset8.csv', 'trip8.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0059_create_assets_trip_9(self):
        # Create assets, Mobile for Trip 9
        create_asset_from_file(self, 'asset9.csv')
        create_mobileterminal_from_file(self, 'asset9.csv', 'mobileterminal9.csv')
        create_trip_from_file(self, datetime.timedelta(hours=48), 'asset9.csv', 'trip9.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0101_create_assets_real_trip_1(self):
        # Create assets, Mobile for RealTrip 1
        create_asset_from_file(self, 'assetreal1.csv')
        create_mobileterminal_from_file(self, 'assetreal1.csv', 'mobileterminalreal1.csv')
        # Create assets, Mobile for RealTrip 2
        create_asset_from_file(self, 'assetreal2.csv')
        create_mobileterminal_from_file(self, 'assetreal2.csv', 'mobileterminalreal2.csv')
        # Create RealTrip 1-2
        create_trip_from_file(self, datetime.timedelta(hours=256), 'assetreal1.csv', 'tripreal1.csv')
        create_trip_from_file(self, datetime.timedelta(hours=254, minutes=16), 'assetreal2.csv', 'tripreal2.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0101b_create_report_and_check_position_reports(self):
        # Create report and check the 1st five position reports in table list
        create_report_and_check_trip_position_reports(self, 'assetreal1.csv', 'tripreal1.csv')
        create_report_and_check_trip_position_reports(self, 'assetreal2.csv', 'tripreal2.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0102_create_assets_real_trip_2(self):
        # Create assets, Mobile for RealTrip 3
        create_asset_from_file(self, 'assetreal3.csv')
        create_mobileterminal_from_file(self, 'assetreal3.csv', 'mobileterminalreal3.csv')
        # Create RealTrip 3
        create_trip_from_file(self, datetime.timedelta(hours=192), 'assetreal3.csv', 'tripreal3.csv')


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
        create_trip_from_file(self, datetime.timedelta(hours=256), 'assetreal4.csv', 'tripreal4a.csv')
        create_trip_from_file(self, datetime.timedelta(hours=48), 'assetreal4.csv', 'tripreal4b.csv')


    @timeout_decorator.timeout(seconds=180)
    def test_0104_create_assets_real_trip_4(self):
        # Create assets, Mobile for RealTrip 5
        create_asset_from_file(self, 'assetreal5.csv')
        create_mobileterminal_from_file(self, 'assetreal5.csv', 'mobileterminalreal5.csv')
        # Create RealTrip 3
        create_trip_from_file(self, datetime.timedelta(hours=48), 'assetreal5.csv', 'tripreal5.csv')


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
        create_trip_from_file(self, datetime.timedelta(hours=72), 'assetreal6.csv', 'tripreal6.csv')


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
        create_trip_from_file(self, datetime.timedelta(hours=270), 'assetreal7.csv', 'tripreal7.csv')



    @timeout_decorator.timeout(seconds=180)
    def test_0501_create_one_new_asset_and_mobile_terminal(self):
        # Create new asset (7th in the list)
        create_one_new_asset_from_gui(self, 7)
        create_one_new_mobile_terminal_via_asset_tab(self, 7, 7)


    @timeout_decorator.timeout(seconds=180)
    def test_0501b_generate_multiple_NAF_positions_7(self):
        # Create Browser
        self.driver = webdriver.Chrome()
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
            nafSource = generate_NAF_string(self, countryValue, ircsValue[7], cfrValue[7], externalMarkingValue, str("%.3f" % latValue), str("%.3f" % longValue), speedValue, courseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[7])
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
        # Create Browser
        self.driver = webdriver.Chrome()
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
                earlierPositionTimeValue = earlierPositionTimeValue - datetime.timedelta(minutes=1)
                earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
                earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
                latValue = latValue - 0.001
                longValue = longValue - 0.001
                nafSource = generate_NAF_string(self, countryValue, ircsValue[x], cfrValue[x], externalMarkingValue, str("%.3f" % latValue), str("%.3f" % longValue), speedValue, courseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[x])
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
    def test_special(self):
        # Create assets 8-17 in the list
        for x in range(18, 20):
            print(x)

        print("----------------------------")

        for y in range(1, 2):
            print(y)


        currentUTCValue = datetime.datetime.utcnow()
        startTimeValue = currentUTCValue - datetime.timedelta(hours=336) # 2 weeks back
        endTimeValue = currentUTCValue + datetime.timedelta(hours=336) # 2 weeks ahead
        print(startTimeValue.strftime("%Y-%m-%d %H:%M:%S"))
        print(endTimeValue.strftime("%Y-%m-%d %H:%M:%S"))

        print("%.3f" % 48.7)

        print(datetime.timedelta(hours=24, minutes=43))

        speedValue = 11.1965442765546
        str1 = str("%.0f" % (speedValue * 10))
        print(str1)
        str1 = str(speedValue * 10)
        print(str1)
        print('---------------------------------')
        speedValueString = str(speedValue)
        str2 = str("%.5f" % float(speedValueString))
        print(str2)
        str3 = str("%.4f" % float(speedValueString))
        print(str3)
        str4 = str("%.5f" % float(str3))
        print(str4)
        print(str("%.5f" % float(str("%.4f" % float(speedValueString)))))





if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=testResultPath, verbosity=2),failfast=False, buffer=False, catchbreak=False)
