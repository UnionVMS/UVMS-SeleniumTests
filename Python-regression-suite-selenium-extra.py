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
import platform

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
    moduleDbVersionMap = {  # 'UVMS-AssetModule-APP': '4.0.8',
        # 'UVMS-ConfigModule-APP': '4.0.6',
        # 'UVMS-AuditModule-APP': '4.0.6',
        # 'UVMS-ExchangeModule-APP': '4.0.9',
        # 'UVMS-MovementModule-APP': '4.0.9',
        # 'UVMS-MobileTerminalModule-APP': '4.0.6',
        # 'UVMS-RulesModule-APP': '3.0.20',
        # 'UVMS-SpatialModule-DB': '1.0.5',
        # 'UVMS-ReportingModule-DB': '1.0.4',
        # 'UVMS-User-APP': '2.0.7',
        # 'UVMS-ActivityModule-APP': '1.0.6',
        # 'UVMS-MDRCacheModule-DB': '0.5.2'
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

    print("Will checkout uvms modules to uvmsCheckoutPath:" + uvmsCheckoutPath)
    distutils.dir_util.mkpath(uvmsCheckoutPath)

    for m, v in moduleDbVersionMap.items():
        print('Checkout:' + m + " version:" + v)
        distutils.dir_util.mkpath(uvmsCheckoutPath + "/" + m)
        moduleBasePath = uvmsCheckoutPath + "/" + m + "/" + m + "-" + modulePrefixDownloadMap.get(m) + v
        print("check dir already exist:" + moduleBasePath)
        if not os.path.isdir(moduleBasePath):
            print(uvmsGitHubPath + m + "/archive/" + modulePrefixDownloadMap.get(m) + v + ".zip")
            url = urllib.request.urlopen(uvmsGitHubPath + m + "/archive/" + modulePrefixDownloadMap.get(m) + v + ".zip")
            zipfile = ZipFile(BytesIO(url.read()))
            zipfile.extractall(uvmsCheckoutPath + "/" + m + "/")
            print("check dir already exist:" + moduleBasePath)
        if os.path.isdir(moduleBasePath):
            print("execute liquidbase:" + m)
            if os.path.isdir(moduleBasePath + "/LIQUIBASE"):
                os.chdir(moduleBasePath + "/LIQUIBASE")
            if os.path.isdir(moduleBasePath + "/liquibase"):
                os.chdir(moduleBasePath + "/liquibase")
            print(os.path.abspath(os.path.dirname(__file__)))
            runSubProcess(
                ['mvn', 'liquibase:dropAll', 'liquibase:update', '-P', 'postgres,exec,testdata', dbURLjdbcString], True)
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

        cur.execute(
            """UPDATE rules.sanityrule SET sanityrule_expression = 'mobileTerminalConnectId == null && pluginType != "NAF"' WHERE sanityrule_expression = 'mobileTerminalConnectId == null';""")

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
    # Maximize browser window
    cls.driver.maximize_window()
    # Login to test user admin
    # cls.driver.get("https://unionvmstest.havochvatten.se/unionvms/")
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
        cls.driver = None


def create_one_new_asset_from_gui(self, vesselNumber):
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
    self.driver.find_element_by_id("asset-input-externalMarking").send_keys(externalMarkingValue[vesselNumber])
    # Enter CFR Value
    self.driver.find_element_by_id("asset-input-cfr").send_keys(cfrValue[vesselNumber])
    # Enter IMO Value
    self.driver.find_element_by_id("asset-input-imo").send_keys(imoValue[vesselNumber])
    # Enter HomePort Value
    self.driver.find_element_by_id("asset-input-homeport").send_keys(homeportValue[vesselNumber])
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
    time.sleep(1)
    # Main Contact Name Value
    self.driver.find_element_by_id("asset-input-contact-name-0").send_keys(contactNameValue[vesselNumber])
    # Main E-mail Value
    self.driver.find_element_by_id("asset-input-contact-email-0").send_keys(contactEmailValue[vesselNumber])
    # Main Contact Number Value
    self.driver.find_element_by_id("asset-input-contact-number-0").send_keys(contactPhoneNumberValue[vesselNumber])
    # Click on Save Asset button
    self.driver.find_element_by_id("menu-bar-save").click()
    time.sleep(5)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(3)


def create_one_new_asset_from_gui_with_parameters(self, parameterList):
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


def create_one_new_mobile_terminal_from_gui(self, mobileTerminalNumber):
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


def create_one_new_mobile_terminal_via_asset_tab(self, mobileTerminalNumber, vesselNumber):
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


def create_one_new_mobile_terminal_via_asset_tab_with_parameters(self, vesselName, parameterList):
    # Click on asset tab
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(1)
    # Search for created asset
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName)
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(7)
    # Click on details button
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(7)
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


def check_new_asset_exists(self, vesselNumber):
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(5)
    # Search for the new created asset in the asset list
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumber])
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(5)
    # Check that the new asset exists in the list.
    self.assertEqual(vesselName[vesselNumber],
                     self.driver.find_element_by_css_selector("td[title=\"" + vesselName[vesselNumber] + "\"]").text)
    time.sleep(1)
    # Click on details button for new asset
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(5)
    # Check that the F.S value is correct.
    self.assertEqual(countryValue[vesselNumber], self.driver.find_element_by_id("asset-input-countryCode").text)
    # Check that the IRCS value is correct
    self.assertEqual(ircsValue[vesselNumber], self.driver.find_element_by_id("asset-input-ircs").get_attribute("value"))
    # Check that the Name value is correct
    self.assertEqual(vesselName[vesselNumber],
                     self.driver.find_element_by_id("asset-input-name").get_attribute("value"))
    # Check that External Marking Value is correct
    self.assertEqual(externalMarkingValue[vesselNumber],
                     self.driver.find_element_by_id("asset-input-externalMarking").get_attribute("value"))
    # Check that the CFR value is correct
    self.assertEqual(cfrValue[vesselNumber], self.driver.find_element_by_id("asset-input-cfr").get_attribute("value"))
    # Check that the IMO value is correct
    self.assertEqual(imoValue[vesselNumber], self.driver.find_element_by_id("asset-input-imo").get_attribute("value"))
    # Check that the HomePort value is correct
    self.assertEqual(homeportValue[vesselNumber],
                     self.driver.find_element_by_id("asset-input-homeport").get_attribute("value"))
    # Check that the Gear Type value is correct.
    self.assertEqual(gearTypeValue[vesselNumber], self.driver.find_element_by_id("asset-input-gearType").text)
    # Check that the MMSI value is correct
    self.assertEqual(mmsiValue[vesselNumber], self.driver.find_element_by_id("asset-input-mmsi").get_attribute("value"))
    # Check that the License Type value is correct.
    self.assertEqual(licenseTypeValue, self.driver.find_element_by_id("asset-input-licenseType").text)
    # Check that the Length Type value is correct.
    self.assertEqual(lengthValue[vesselNumber],
                     self.driver.find_element_by_id("asset-input-lengthValue").get_attribute("value"))
    # Check that the Gross Tonnage value is correct.
    self.assertEqual(grossTonnageValue[vesselNumber],
                     self.driver.find_element_by_id("asset-input-grossTonnage").get_attribute("value"))
    # Check that the Power value is correct.
    self.assertEqual(powerValue[vesselNumber],
                     self.driver.find_element_by_id("asset-input-power").get_attribute("value"))
    # Check that the Producer Name value is correct.
    #
    # Needs to be updated according to asset database
    #
    #
    # self.assertEqual("Mikael", self.driver.find_element_by_id("asset-input-producername").get_attribute("value"))
    # Check that the Producer Code value is correct.
    self.assertEqual(producercodeValue,
                     self.driver.find_element_by_id("asset-input-producercode").get_attribute("value"))
    # Click on the Contacts tab
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    time.sleep(1)
    # Check that the Contact Name value is correct.
    self.assertEqual(contactNameValue[vesselNumber],
                     self.driver.find_element_by_id("asset-input-contact-name-0").get_attribute("value"))
    # Check that the E-mail value is correct.
    self.assertEqual(contactEmailValue[vesselNumber],
                     self.driver.find_element_by_id("asset-input-contact-email-0").get_attribute("value"))
    # Check that the E-mail value is correct.
    self.assertEqual(contactPhoneNumberValue[vesselNumber],
                     self.driver.find_element_by_id("asset-input-contact-number-0").get_attribute("value"))
    time.sleep(5)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(3)


def check_current_asset_pop_up_history_items(self, vesselNumber):
    # Check the values in the pop up window
    self.assertEqual(countryValue[vesselNumber],
                     self.driver.find_element_by_css_selector("div.historyValues > div.col-md-6 > b").text)
    self.assertEqual(ircsValue[vesselNumber], self.driver.find_element_by_xpath("//div[3]/b").text)
    self.assertEqual(vesselName[vesselNumber], self.driver.find_element_by_xpath("//div[4]/b").text)
    self.assertEqual(imoValue[vesselNumber], self.driver.find_element_by_xpath("//div[7]/b").text)
    self.assertEqual(homeportValue[vesselNumber], self.driver.find_element_by_xpath("//div[8]/b").text)
    self.assertEqual(mmsiValue[vesselNumber], self.driver.find_element_by_xpath("//div[9]/b").text)
    self.assertEqual(licenseValue, self.driver.find_element_by_xpath("//div[10]/b").text)
    self.assertEqual(licenseTypeValue, self.driver.find_element_by_xpath("//div[11]/b").text)
    self.assertEqual(contactNameValue[vesselNumber], self.driver.find_element_by_css_selector("div.col-md-12 > b").text)
    self.assertEqual(contactEmailValue[vesselNumber], self.driver.find_element_by_xpath("//li/div[2]/b").text)
    self.assertEqual(contactPhoneNumberValue[vesselNumber], self.driver.find_element_by_xpath("//li/div[3]/b").text)
    self.assertEqual(gearTypeValue[vesselNumber], self.driver.find_element_by_xpath("//div[17]/b").text)
    self.assertEqual(powerValue[vesselNumber] + " kW", self.driver.find_element_by_xpath("//div[19]/b").text)
    self.assertEqual(lengthValue[vesselNumber] + " m LOA", self.driver.find_element_by_xpath("//div[20]/b").text)
    time.sleep(1)


def check_second_contact_in_current_asset_pop_up_history_items(self, vesselNumber):
    # Check the values in the pop up window
    self.assertEqual(contactNameValue[vesselNumber], self.driver.find_element_by_xpath("//li[2]/div/b").text)
    self.assertEqual(contactEmailValue[vesselNumber], self.driver.find_element_by_xpath("//li[2]/div[2]/b").text)
    self.assertEqual(contactPhoneNumberValue[vesselNumber], self.driver.find_element_by_xpath("//li[2]/div[3]/b").text)
    time.sleep(1)


def click_on_selected_asset_history_event(self, numberEvent):
    # Select if the numberEvent is zero (in other words, the 1st in the Asset History Event List
    if numberEvent == 0:
        self.driver.find_element_by_css_selector("td").click()
    else:
        self.driver.find_element_by_xpath(
            "(//tr[@id='asset-btn-history-item']/td)[" + str((numberEvent * 2) + 1) + "]").click()


def check_asset_history_list(self, vesselNumberList, secondContactVesselNumberList):
    # Go through the history for one asset and compare the values towards the asset values controled by the vesselNumberList
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(5)
    # Search for selected asset in the asset list
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumberList[0]])
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(5)
    # Click on details button
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(7)
    # Click on History tab
    self.driver.find_element_by_css_selector("#HISTORY > span").click()
    time.sleep(2)
    # Click on and check the items in the History list
    for y in range(len(vesselNumberList)):
        # Click on y-th item in the History list
        click_on_selected_asset_history_event(self, y)
        time.sleep(2)
        # Check the values in the pop up window
        check_current_asset_pop_up_history_items(self, vesselNumberList[y])
        # Check the second contact info if available
        if secondContactVesselNumberList[y] != 0:
            check_second_contact_in_current_asset_pop_up_history_items(self, secondContactVesselNumberList[y])
        # Close History pop up window
        self.driver.find_element_by_css_selector("div.modal-footer > #asset-btn-close-history").click()
        time.sleep(2)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(3)


def modify_one_new_asset_from_gui(self, oldVesselNumber, newVesselNumber):
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(5)
    # Search for selected asset in the asset list
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[oldVesselNumber])
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(5)
    # Click on details button
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(7)
    # Select F.S value
    self.driver.find_element_by_id("asset-input-countryCode").click()
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-countryCode-item-1").click()
    # Enter IRCS value
    self.driver.find_element_by_id("asset-input-ircs").clear()
    self.driver.find_element_by_id("asset-input-ircs").send_keys(ircsValue[newVesselNumber])
    time.sleep(1)
    # Enter Name value
    self.driver.find_element_by_id("asset-input-name").clear()
    self.driver.find_element_by_id("asset-input-name").send_keys(vesselName[newVesselNumber])
    time.sleep(1)
    # Enter External Marking Value
    self.driver.find_element_by_id("asset-input-externalMarking").clear()
    self.driver.find_element_by_id("asset-input-externalMarking").send_keys(externalMarkingValue[newVesselNumber])
    time.sleep(1)
    # Enter CFR Value
    self.driver.find_element_by_id("asset-input-cfr").clear()
    self.driver.find_element_by_id("asset-input-cfr").send_keys(cfrValue[newVesselNumber])
    time.sleep(1)
    # Enter IMO Value
    self.driver.find_element_by_id("asset-input-imo").clear()
    self.driver.find_element_by_id("asset-input-imo").send_keys(imoValue[newVesselNumber])
    time.sleep(1)
    # Enter HomePort Value
    self.driver.find_element_by_id("asset-input-homeport").clear()
    self.driver.find_element_by_id("asset-input-homeport").send_keys(homeportValue[newVesselNumber])
    time.sleep(1)
    # Select Gear Type value
    self.driver.find_element_by_id("asset-input-gearType").click()
    time.sleep(1)
    self.driver.find_element_by_id("asset-input-gearType-item-2").click()
    # Enter MMSI Value
    self.driver.find_element_by_id("asset-input-mmsi").clear()
    self.driver.find_element_by_id("asset-input-mmsi").send_keys(mmsiValue[newVesselNumber])
    time.sleep(1)
    # Select License Type value
    # Not changed
    time.sleep(1)
    # Length Value
    self.driver.find_element_by_id("asset-input-lengthValue").clear()
    self.driver.find_element_by_id("asset-input-lengthValue").send_keys(lengthValue[newVesselNumber])
    time.sleep(1)
    # Gross Tonnage Value
    self.driver.find_element_by_id("asset-input-grossTonnage").clear()
    self.driver.find_element_by_id("asset-input-grossTonnage").send_keys(grossTonnageValue[newVesselNumber])
    time.sleep(1)
    # Main Power Value
    self.driver.find_element_by_id("asset-input-power").clear()
    self.driver.find_element_by_id("asset-input-power").send_keys(powerValue[newVesselNumber])
    time.sleep(1)
    # Main Producer Name Value
    #  self.driver.find_element_by_id("asset-input-producername").send_keys(producernameValue) Should be included when this works
    # Main Producer Code Value
    #  self.driver.find_element_by_id("asset-input-producercode").send_keys(producercodeValue) Should be included when this works
    # Click on the Contacts tab
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    time.sleep(1)
    # Main Contact Name Value
    self.driver.find_element_by_id("asset-input-contact-name-0").clear()
    self.driver.find_element_by_id("asset-input-contact-name-0").send_keys(contactNameValue[newVesselNumber])
    time.sleep(1)
    # Main E-mail Value
    self.driver.find_element_by_id("asset-input-contact-email-0").clear()
    self.driver.find_element_by_id("asset-input-contact-email-0").send_keys(contactEmailValue[newVesselNumber])
    time.sleep(1)
    # Main Contact Number Value
    self.driver.find_element_by_id("asset-input-contact-number-0").clear()
    self.driver.find_element_by_id("asset-input-contact-number-0").send_keys(contactPhoneNumberValue[newVesselNumber])
    time.sleep(10)
    # Click on Save Asset button
    self.driver.find_element_by_id("menu-bar-update").click()
    time.sleep(5)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(3)


def archive_one_asset_from_gui(self, vesselNumber):
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(5)
    # Search for selected asset in the asset list
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumber])
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(5)
    # Click on details button
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(7)
    # Click on delete button (Archive)
    self.driver.find_element_by_id("menu-bar-archive").click()
    time.sleep(5)
    # Add some comment to the asset that shall be archived
    self.driver.find_element_by_name("comment").send_keys("Archive this asset!")
    time.sleep(3)
    # Click on Yes button
    self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
    time.sleep(5)


def check_asset_archived(self, vesselNumber):
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(5)
    # Search for selected asset in the asset list
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[vesselNumber])
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(5)
    # Check that vessel name is greyed out
    color_value = self.driver.find_element_by_css_selector(
        "td[title=\"" + vesselName[35] + "\"]").value_of_css_property("color")
    self.assertEqual(greyColorRGBA, color_value)
    time.sleep(4)
    # Click on details button
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(4)
    # Try to click on delete (archive) button. Shall not exist.
    try:
        self.assertFalse(self.driver.find_element_by_id("menu-bar-archive").click())
    except NoSuchElementException:
        pass
    time.sleep(4)


def add_contact_to_existing_asset(self, currentVesselNumber, newVesselNumber):
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(5)
    # Search for selected asset in the asset list
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[currentVesselNumber])
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(5)
    # Click on details button
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(7)
    # Click on the Contacts tab
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    time.sleep(1)
    self.driver.find_element_by_id("asset-btn-add-contact").click()
    time.sleep(1)
    # Add a second contact contactNameValue, contactEmailValue and contactPhoneNumberValue
    self.driver.find_element_by_id("asset-input-contact-name-1").click()
    self.driver.find_element_by_id("asset-input-contact-name-1").clear()
    self.driver.find_element_by_id("asset-input-contact-name-1").send_keys(contactNameValue[newVesselNumber])
    self.driver.find_element_by_id("asset-input-contact-email-1").clear()
    self.driver.find_element_by_id("asset-input-contact-email-1").send_keys(contactEmailValue[newVesselNumber])
    self.driver.find_element_by_id("asset-input-contact-number-1").clear()
    self.driver.find_element_by_id("asset-input-contact-number-1").send_keys(contactPhoneNumberValue[newVesselNumber])
    time.sleep(1)
    self.driver.find_element_by_id("menu-bar-update").click()
    time.sleep(1)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(3)


def check_contacts_to_existing_asset(self, currentVesselNumber, newVesselNumber):
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    time.sleep(5)
    # Search for selected asset in the asset list
    self.driver.find_element_by_id("asset-input-simple-search").clear()
    self.driver.find_element_by_id("asset-input-simple-search").send_keys(vesselName[currentVesselNumber])
    self.driver.find_element_by_id("asset-btn-simple-search").click()
    time.sleep(5)
    # Click on details button
    self.driver.find_element_by_id("asset-toggle-form").click()
    time.sleep(7)
    # Click on the Contacts tab
    self.driver.find_element_by_xpath("//*[@id='CONTACTS']/span").click()
    time.sleep(1)
    # Check contacts info
    self.assertEqual(contactNameValue[currentVesselNumber],
                     self.driver.find_element_by_id("asset-input-contact-name-0").get_attribute("value"))
    self.assertEqual(contactEmailValue[currentVesselNumber],
                     self.driver.find_element_by_id("asset-input-contact-email-0").get_attribute("value"))
    self.assertEqual(contactPhoneNumberValue[currentVesselNumber],
                     self.driver.find_element_by_id("asset-input-contact-number-0").get_attribute("value"))
    self.assertEqual(contactNameValue[newVesselNumber],
                     self.driver.find_element_by_id("asset-input-contact-name-1").get_attribute("value"))
    self.assertEqual(contactEmailValue[newVesselNumber],
                     self.driver.find_element_by_id("asset-input-contact-email-1").get_attribute("value"))
    self.assertEqual(contactPhoneNumberValue[newVesselNumber],
                     self.driver.find_element_by_id("asset-input-contact-number-1").get_attribute("value"))
    time.sleep(3)


def check_new_mobile_terminal_exists(self, mobileTerminalNumber):
    # Select Mobile Terminal tab
    self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
    time.sleep(2)
    # Enter Serial Number in
    self.driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(serialNoValue[mobileTerminalNumber])
    # Click in search button
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(5)
    # Check Serial Number in the list
    self.assertEqual(serialNoValue[mobileTerminalNumber], self.driver.find_element_by_xpath(
        "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[3]").text)
    # Check Member Number in the list
    self.assertEqual(memberIdnumber[mobileTerminalNumber], self.driver.find_element_by_xpath(
        "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
    # Check DNID Number in the list
    self.assertEqual(dnidNumber[mobileTerminalNumber], self.driver.find_element_by_xpath(
        "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)
    # Click on details button
    self.driver.find_element_by_xpath(
        "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
    time.sleep(2)
    # Check Serial Number
    self.assertEqual(serialNoValue[mobileTerminalNumber],
                     self.driver.find_element_by_id("mt-0-serialNumber").get_attribute("value"))
    # Check Transceiver Type
    self.assertEqual(transceiverType[mobileTerminalNumber],
                     self.driver.find_element_by_id("mt-0-tranciverType").get_attribute("value"))
    # Check Software Version
    self.assertEqual(softwareVersion, self.driver.find_element_by_id("mt-0-softwareVersion").get_attribute("value"))
    # Check Satellite Number
    self.assertEqual(satelliteNumber[mobileTerminalNumber],
                     self.driver.find_element_by_id("mt-0-satelliteNumber").get_attribute("value"))
    # Check Antenna Version
    self.assertEqual(antennaVersion, self.driver.find_element_by_id("mt-0-antenna").get_attribute("value"))
    # Check DNID Number
    self.assertEqual(dnidNumber[mobileTerminalNumber], self.driver.find_element_by_name("dnid").get_attribute("value"))
    # Check Member Number
    self.assertEqual(memberIdnumber[mobileTerminalNumber],
                     self.driver.find_element_by_name("memberId").get_attribute("value"))
    # Check Installed by Name
    self.assertEqual(installedByName,
                     self.driver.find_element_by_id("mt-0-channel-0-installedBy").get_attribute("value"))
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def link_asset_and_mobile_terminal(self, mobileTerminalNumber):
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
    self.driver.find_element_by_css_selector(
        "div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
    time.sleep(2)
    # Close page
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)


def change_and_check_speed_format(self, unitNumber):
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
    currentSpeedValue = self.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[11]").text
    print("Current: " + currentSpeedValue + " Short Unit: " + speedUnitTypesShort[unitNumber])
    if currentSpeedValue.find(speedUnitTypesShort[unitNumber]) == -1:
        foundCorrectUnit = False
    else:
        foundCorrectUnit = True
    self.assertTrue(foundCorrectUnit)
    time.sleep(5)


def generate_and_verify_manual_position(self, speedValue, courseValue):
    # Select Positions tab
    self.driver.find_element_by_id("uvms-header-menu-item-movement").click()
    time.sleep(7)
    # Click on New manual report
    self.driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(7)
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
    self.assertEqual(countryValue[0],
                     self.driver.find_element_by_css_selector("td[title=\"" + countryValue[0] + "\"]").text)
    self.assertEqual(externalMarkingValue[0],
                     self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue[0] + "\"]").text)
    self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
    self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
    self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[6]").text)
    self.assertEqual(lolaPositionValues[0][0][0],
                     self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][0] + "\"]").text)
    self.assertEqual(lolaPositionValues[0][0][1],
                     self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][1] + "\"]").text)
    self.assertEqual("%.2f" % speedValue + " kts", self.driver.find_element_by_css_selector(
        "td[title=\"" + "%.2f" % speedValue + " kts" + "\"]").text)
    self.assertEqual(str(courseValue) + "°",
                     self.driver.find_element_by_css_selector("td[title=\"" + str(courseValue) + "°" + "\"]").text)
    self.assertEqual(sourceValue[1],
                     self.driver.find_element_by_css_selector("td[title=\"" + sourceValue[1] + "\"]").text)
    time.sleep(5)
    return earlierPositionDateTimeValueString


def generate_NAF_and_verify_position(self, speedValue, courseValue):
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
    # Generate request
    r = requests.get(totalNAFrequest)
    # Check if request is OK (200)
    if r.ok:
        print("200 OK")
    else:
        print("Request NOT OK!")
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
    self.assertEqual(countryValue[0],
                     self.driver.find_element_by_css_selector("td[title=\"" + countryValue[0] + "\"]").text)
    self.assertEqual(externalMarkingValue[0],
                     self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue[0] + "\"]").text)
    self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
    self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
    self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[6]").text)
    self.assertEqual(lolaPositionValues[0][0][0],
                     self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][0] + "\"]").text)
    self.assertEqual(lolaPositionValues[0][0][1],
                     self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][1] + "\"]").text)
    self.assertEqual("%.2f" % speedValue + " kts", self.driver.find_element_by_css_selector(
        "td[title=\"" + "%.2f" % speedValue + " kts" + "\"]").text)
    self.assertEqual(str(courseValue) + "°",
                     self.driver.find_element_by_css_selector("td[title=\"" + str(courseValue) + "°" + "\"]").text)
    self.assertEqual(sourceValue[0],
                     self.driver.find_element_by_css_selector("td[title=\"" + sourceValue[0] + "\"]").text)
    time.sleep(5)
    return earlierPositionDateTimeValueString


def generate_NAF_string(self, countryValue, ircsValue, cfrValue, externalMarkingValue, latValue, longValue, speedValue,
                        courseValue, dateValue, timeValue, vesselNameValue):
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
    del allRows[0]
    # Change back the path to current dir
    os.chdir(cwd)
    print(cwd)
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


def create_trip_from_file(self, deltaTimeValue, assetFileName, tripFileName):
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
            nafSource = generate_NAF_string(self, countryValue[0], assetAllrows[x][0], assetAllrows[x][2],
                                            assetAllrows[x][3], str("%.3f" % float(assetTripAllrows[y][1])),
                                            str("%.3f" % float(assetTripAllrows[y][0])), float(assetTripAllrows[y][3]),
                                            assetTripAllrows[y][4], currentPositionDateValueString,
                                            currentPositionTimeValueString, assetAllrows[x][1])
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
    # Open saved csv file and read all asset elements
    assetAllrows = get_elements_from_file(self, assetFileName)
    # Open saved csv file and read all trip elements for asset
    assetTripAllrows = get_elements_from_file(self, tripFileName)
    time.sleep(10)
    # Create a new Report
    # Select Reporting tab
    self.driver.find_element_by_id("uvms-header-menu-item-reporting").click()
    time.sleep(15)
    # Click on New Report button
    self.driver.find_element_by_xpath("(//button[@type='button'])[18]").click()
    time.sleep(2)
    # Enter reporting name (based on 1st ircs name from asset file)
    reportName = "Test (only " + assetAllrows[1][0] + ")"
    self.driver.find_element_by_id("reportName").send_keys(reportName)
    # Enter Start and end Date Time
    currentUTCValue = datetime.datetime.utcnow()
    startTimeValue = currentUTCValue - datetime.timedelta(hours=336)  # 2 weeks back
    endTimeValue = currentUTCValue + datetime.timedelta(hours=336)  # 2 weeks ahead
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
    self.driver.find_element_by_xpath(
        "//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/thead/tr[3]/th[5]/div").click()
    time.sleep(2)
    # Check the 5 first positions for mentioned asset
    for y in range(1, 6):
        self.assertEqual(str("%.3f" % float(assetTripAllrows[y][0])), self.driver.find_element_by_xpath(
            "//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[6]/div").text)
        self.assertEqual(str("%.3f" % float(assetTripAllrows[y][1])), self.driver.find_element_by_xpath(
            "//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[7]/div").text)
        # Special case if speed is zero (No decimals then)
        if float(assetTripAllrows[y][3]) == 0:
            self.assertEqual(assetTripAllrows[y][3] + " kts", self.driver.find_element_by_xpath(
                "//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(
                    y) + "]/td[9]/div").text)
        else:
            # self.assertEqual(str("%.5f" % float(assetTripAllrows[y][3])) + " kts", self.driver.find_element_by_xpath("//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(y) + "]/td[9]/div").text)
            # Compare expected value with 5 decimals that only has 4 decimals resolution
            self.assertEqual(str("%.5f" % float(str("%.4f" % float(assetTripAllrows[y][3])))) + " kts",
                             self.driver.find_element_by_xpath(
                                 "//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(
                                     y) + "]/td[9]/div").text)
        self.assertEqual(assetTripAllrows[y][4] + "°", self.driver.find_element_by_xpath(
            "//div[@id='map']/div[6]/div/div/div/div/div/div[2]/div/div/table/tbody/tr[" + str(
                y) + "]/td[11]/div").text)
    time.sleep(5)


def reload_page_and_goto_default(self):
    # Reload page and goto default page
    self.driver.get(httpUnionVMSurlString)


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
        return targetPathWindows
    else:
        return targetPathLinux


def get_test_report_path():
    # Get correct download path
    if platform.system() == "Windows":
        return testResultPathWindows
    else:
        return testResultPathLinux


if os.name == 'nt':
    # We redefine timeout_decorator on windows
    class timeout_decorator:
        @staticmethod
        def timeout(*args, **kwargs):
            return lambda f: f  # return a no-op decorator
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
        time.sleep(5)


    def tearDown(self):
        shutdown_browser(self)


    @timeout_decorator.timeout(seconds=180)
    def test_0001b_change_default_configuration_parameters(self):
        # The test case changes Default home page to asset and Coordinates format to dd.mmm
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
    def test_0107_create_assets_real_trip_7(self):
        # Create assets, Mobile for RealTrip 7
        create_asset_from_file(self, 'assetreal8.csv')
        create_mobileterminal_from_file(self, 'assetreal8.csv', 'mobileterminalreal8.csv')
        # Create RealTrip 3
        create_trip_from_file(self, datetime.timedelta(hours=270), 'assetreal8.csv', 'tripreal8.csv')


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
            nafSource = generate_NAF_string(self, countryValue[7], ircsValue[7], cfrValue[7], externalMarkingValue[7], str("%.3f" % latValue), str("%.3f" % longValue), speedValue, courseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[7])
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
                earlierPositionTimeValue = earlierPositionTimeValue - datetime.timedelta(minutes=1)
                earlierPositionDateValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%Y%m%d')
                earlierPositionTimeValueString = datetime.datetime.strftime(earlierPositionTimeValue, '%H%M')
                latValue = latValue - 0.001
                longValue = longValue - 0.001
                nafSource = generate_NAF_string(self, countryValue[x], ircsValue[x], cfrValue[x], externalMarkingValue[x], str("%.3f" % latValue), str("%.3f" % longValue), speedValue, courseValue, earlierPositionDateValueString, earlierPositionTimeValueString, vesselName[x])
                nafSourceURLcoded = urllib.parse.quote_plus(nafSource)
                totalNAFrequest = httpNAFRequestString + nafSourceURLcoded
                # Generate request
                r = requests.get(totalNAFrequest)
                # Check if request is OK (200)
                if r.ok:
                    print("200 OK")
                else:
                    print("Request NOT OK!")






if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=get_test_report_path(), verbosity=2),failfast=False, buffer=False, catchbreak=False)
