import unittest
import time
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

# Globals
# Assets
countryValue = 'SWE'
ircsValue = ["F1001", "F1002", "F1003", "F1004", "F1005", "F1006"]
vesselName = ["Fartyg1001", "Fartyg1002", "Fartyg1003", "Fartyg1004", "Fartyg1005", "Fartyg1006"]
cfrValue = ["SWE0000F1001", "SWE0000F1002", "SWE0000F1003", "SWE0000F1004", "SWE0000F1005", "SWE0000F1006"]
externalMarkingValue = "EXT3"
#imoValue = str(random.randint(0, 9999999))
#imoValue = imoValue.zfill(7)
imoValue = ["0261917", "0261918", "0233917", "0233918", "0761901", "0761902"]
#mmsiValue = str(random.randint(0, 999999999))
#mmsiValue = mmsiValue.zfill(9)
mmsiValue = ["302331238", "302331239", "302331240", "302331241", "302331242", "302331243"]
homeportValue = "GOT"
assetHeadline = ("F. S.", "Ext. marking", "Name", "IRCS", "CFR", "Gear Type", "License type", "Last report")
producercodeValue = "1"
# Mobile Terminals
serialNoValue = ["M1001", "M1002", "M1003", "M1004", "M1005", "M1006"]
#transceiverType = str(random.randint(1, 100))
transceiverType = "Type A"
#softwareVersionList = ['A', 'B', 'C']
#softwareVersion = random.choice(softwareVersionList)
softwareVersion = "A"
antennaVersion = "A"
#satelliteNumber = str(random.randint(1, 999999999))
satelliteNumber = ["S1001", "S1002", "S1003", "S1004", "S1005", "S1006"]
#dnidNumber = str(random.randint(1, 99999))
dnidNumber = ["1001", "1002", "1003", "1004", "1005", "1006"]
#memberIdnumber = str(random.randint(100, 499))
memberIdnumber = "100"
installedByName = "Mike Great"
expectedFrequencyHours = "2"
expectedFrequencyMinutes = "0"
gracePeriodFrequencyHours = "15"
gracePeriodFrequencyMinutes = "0"
inPortFrequencyHours = "3"
inPortFrequencyMinutes = "0"
deltaTimeValue = 4
transponderType = ("Iridium", "Inmarsat-C")
mobileTerminalHeadline = ("Linked asset", "Serial no.", "Member no.", "DNID", "Transponder type", "Satellite no.", "MMSI no.", "Status")
# lolaPositionValues [Asset number x, lola position route y, lat=0/lon=1 z]
lolaPositionValues = [[["57.326", "16.996"], ["57.327", "16.997"]],
                      [["57.934", "11.592"], ["57.935", "11.593"]],
                      [["56.647", "12.840"], ["56.646", "12.834"]],
                      [["56.659", "16.378"], ["56.659", "16.381"]],
                      [["57.266", "16.480"], ["57.267", "16.487"]],
                      [["58.662", "17.129"], ["58.661", "17.137"]]]

# Mixed parameters
reportedSpeedValue = 5
reportedCourseValue = 180
httpNAFRequestString = "http://livm73t:28080/naf/rest/message/"
sourceValue= ('NAF', 'MANUAL')
groupName = ("Grupp 1", "Grupp 2", "Grupp 3")
speedUnitTypesInText = ("knots", "kilometers per hour", "miles per hour")
speedUnitTypesShort = ("kts", "km/h", "mph")
reportedSpeedDefault = [8, 10, 12]
rulesHeadlineNames = ["Rule name", "Last triggered", "Date updated", "Updated by", "Notification", "Notify by email", "Status", "Actions"]


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
    moduleNames = ['Asset', 'MobileTerminal', 'Movement', 'Rules']
    for i in range(len(moduleNames)):
        os.chdir("C:\\git-modules\\UVMS-" + moduleNames[i] + "Module-DB\\LIQUIBASE")
        print(os.getcwd())
        # Reset current Module database
        runSubProcess(['mvn', 'liquibase:dropAll', 'liquibase:update', '-P', 'postgres',
                       '-Ddb.url=jdbc:postgresql://livmdb71t.havochvatten.se:5432/db71t'], True)
        time.sleep(1)

def populateIridiumImarsatCData():
    try:
        conn = psycopg2.connect("dbname='db71t' user='postgres' host='livmdb71t' password='postgres'")
        print("Yeeahh I am in!!!")
        cur = conn.cursor()

        # Add rows to mobterm.plugin table
        cur.execute("""SELECT * from mobterm.plugin""")
        rows = cur.fetchall()
        print("\nPrint out of Database db71t (Before):\n")
        for row in rows:
            print(row[0:])
        cur.execute("""INSERT INTO mobterm.plugin VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                    (1050, 'siriusone', 'eu.europa.ec.fisheries.uvms.plugins.iridium.siriusone', 'IRIDIUM', False,
                     'siriusone', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                    (1056, 'twostage', 'eu.europa.ec.fisheries.uvms.plugins.inmarsat', 'INMARSAT_C', False,
                     'twostage', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""SELECT * from mobterm.plugin""")
        rows = cur.fetchall()
        print("\nPrint out of Database db71t (After):\n")
        for row in rows:
            print(row[0:])
        conn.commit()

        # Add rows to mobterm.plugin_capability
        cur.execute("""SELECT * from mobterm.plugin_capability""")
        rows = cur.fetchall()
        print("\nPrint out of Database db71t (Before 2):\n")
        for row in rows:
            print(row[0:])
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1051, 1050, 'MULTIPLE_OCEAN', 'FALSE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1052, 1050, 'ONLY_SINGLE_OCEAN', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1053, 1050, 'SAMPLING', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1054, 1050, 'CONFIGURABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1055, 1050, 'POLLABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1057, 1056, 'POLLABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1058, 1056, 'CONFIGURABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1059, 1056, 'ONLY_SINGLE_OCEAN', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1060, 1056, 'SAMPLING', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1061, 1056, 'MULTIPLE_OCEAN', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""SELECT * from mobterm.plugin_capability""")
        rows = cur.fetchall()
        print("\nPrint out of Database db71t (After 2):\n")
        for row in rows:
            print(row[0:])
        conn.commit()

    except:
        print("I am unable to connect to the database")
    cur.close()
    conn.close()


def populateSanityRuleData():
    try:
        conn = psycopg2.connect("dbname='db71t' user='postgres' host='livmdb71t' password='postgres'")
        print("Yeeahh I am in!!!")
        cur = conn.cursor()
        cur.execute("""SELECT * from rules.sanityrule""")
        rows = cur.fetchall()
        print("\nPrint out of Database db71t (Before):\n")
        for row in rows:
            print(row[0:])

        cur.execute("""UPDATE rules.sanityrule SET sanityrule_expression = 'mobileTerminalConnectId == null && pluginType != "NAF"' WHERE sanityrule_expression = 'mobileTerminalConnectId == null';""")

        cur.execute("""SELECT * from rules.sanityrule""")
        print("\nPrint out of Database db71t (After):\n")
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
    cls.driver.get("http://livm73t:28080/unionvms/")
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

    cls.driver.find_element_by_id("userId").send_keys("vms_admin_com")
    cls.driver.find_element_by_id("password").send_keys("password")
    time.sleep(2)
    cls.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div/div[2]/div[3]/div[2]/form/div[3]/div/button"). \
        click()
    time.sleep(2)
    cls.driver.find_element_by_partial_link_text("AdminAll").click()


def shutdown_browser(cls):
    cls.driver.quit()


def create_one_new_asset_from_gui(self, vesselNumber):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    self.driver.implicitly_wait(10)
    # Click on asset tab
    time.sleep(5)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    # Click on new Asset button
    self.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/button").click()
    time.sleep(2)
    # Select F.S value
    self.driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
    self.driver.find_element_by_link_text(countryValue).click()
    # Enter IRCS value
    self.driver.find_element_by_name("ircs").send_keys(ircsValue[vesselNumber])
    # Enter Name value
    # self.driver.find_element_by_name("name").send_keys(vesselName[vesselNumber]) --- seems not to work anymore
    self.driver.find_element_by_css_selector("input[name=\"name\"]").send_keys(vesselName[vesselNumber])
    # Enter External Marking Value
    self.driver.find_element_by_name("externalMarking").send_keys(externalMarkingValue)
    # Enter CFR Value
    self.driver.find_element_by_name("cfr").send_keys(cfrValue[vesselNumber])
    # Enter IMO Value
    self.driver.find_element_by_name("imo").send_keys(imoValue[vesselNumber])
    # Enter HomePort Value
    self.driver.find_element_by_name("homeport").send_keys(homeportValue)
    # Select Gear Type value
    self.driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
    self.driver.find_element_by_link_text("Dermersal").click()
    # Enter MMSI Value
    self.driver.find_element_by_name("mmsi").send_keys(mmsiValue[vesselNumber])
    # Select License Type value
    self.driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
    time.sleep(1)
    self.driver.find_element_by_link_text("MOCK-license-DB").click()
    # Length Value
    self.driver.find_element_by_name("lengthValue").send_keys("14")
    # Gross Tonnage Value
    self.driver.find_element_by_name("grossTonnage").send_keys("3")
    # Main Power Value
    self.driver.find_element_by_name("power").send_keys("1300")
    # Main Producer Name Value
    self.driver.find_element_by_name("producername").send_keys("Mikael")
    # Main Producer Code Value
    self.driver.find_element_by_name("producercode").send_keys(producercodeValue)
    # Main Contact Name Value
    self.driver.find_element_by_id("contact-name").send_keys("Mikael Great")
    # Main E-mail Value
    self.driver.find_element_by_id("contact-email").send_keys("mikael.glemne@havochvatten.se")
    # Main Contact Number Value
    self.driver.find_element_by_id("contact-number").send_keys("+46720456789")
    # Click on Save Asset button
    self.driver.find_element_by_id("menu-bar-save").click()
    time.sleep(3)
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
    self.driver.find_element_by_id("mob-term-add-terminal").click()
    time.sleep(3)
    # Select Transponder system
    element = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[@type='button'])[18]")))  # Waits until element exists
    element.click()
    self.driver.find_element_by_link_text("Inmarsat-C : twostage").click()
    time.sleep(1)
    # Enter serial number
    self.driver.find_element_by_id("mob-term-form-details-serial-number").send_keys(serialNoValue[mobileTerminalNumber])
    # Enter Transceiver type
    self.driver.find_element_by_id("mob-term-form-details-transceiver-type").send_keys(transceiverType)
    # Enter Software Version
    self.driver.find_element_by_id("mob-term-form-details-software-version").send_keys(softwareVersion)
    # Enter Antenna
    self.driver.find_element_by_id("mob-term-form-details-antenna").send_keys(antennaVersion)
    # Enter Satellite Number
    self.driver.find_element_by_id("mob-term-form-details-satelite-number").send_keys(satelliteNumber[mobileTerminalNumber])
    # Enter DNID Number
    #self.driver.find_element_by_id("mob-term-form-details-dnid-0").send_keys(dnidNumber[mobileTerminalNumber]) --- seems not to work anymore
    self.driver.find_element_by_name("dnid").send_keys(dnidNumber[mobileTerminalNumber])
    # Enter Member Number
    # self.driver.find_element_by_id("mob-term-form-details-member-number-0").send_keys(memberIdnumber) --- seems not to work anymore
    self.driver.find_element_by_name("memberId").send_keys(memberIdnumber)
    # Enter Installed by
    # self.driver.find_element_by_id("mob-term-form-details-installed-by-0").send_keys(installedByName) --- seems not to work anymore
    self.driver.find_element_by_xpath("(//input[@type='text'])[36]").send_keys(installedByName)
    # Expected frequency
    self.driver.find_element_by_xpath("(//input[@type='number'])[2]").send_keys(expectedFrequencyHours)
    # Grace period
    self.driver.find_element_by_xpath("(//input[@type='number'])[4]").send_keys(gracePeriodFrequencyHours)
    # In port
    self.driver.find_element_by_xpath("(//input[@type='number'])[6]").send_keys(inPortFrequencyHours)
    # Activate Mobile Terminal button
    #self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[1]/div[4]/div[2]/div/form/fieldset/div[1]/div[1]/div[5]/div/label[2]/div").click()
    self.driver.find_element_by_id("mob-term-form-details-slider").click()
    time.sleep(2)
    # Click on save button
    self.driver.find_element_by_id("menu-bar-save").click()
    time.sleep(5)
    # Leave new asset view
    self.driver.find_element_by_id("menu-bar-cancel").click()
    time.sleep(2)
    # Shutdown browser
    shutdown_browser(self)


def check_new_asset_exists(self, vesselNumber):
    # Startup browser and login
    startup_browser_and_login_to_unionVMS(self)
    # Search for the new created asset in the asset list
    time.sleep(5)
    self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
    self.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[1]/form/div/div/div/div[1]/div/div/div/div[1]/input"). \
        send_keys(vesselName[vesselNumber])
    self.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div/button").click()
    time.sleep(5)
    # Check that the new asset exists in the list.
    self.assertEqual(vesselName[vesselNumber], self.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr/td[4]").text)
    time.sleep(1)
    # Click on details button for new asset
    self.driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr/td[10]/button/i").click()
    time.sleep(5)
    # Check that the F.S value is correct.
    self.assertEqual(countryValue, self.driver.find_element_by_xpath("(//button[@type='button'])[3]").text)
    # Check that the IRCS value is correct
    self.assertEqual(ircsValue[vesselNumber], self.driver.find_element_by_name("ircs").get_attribute("value"))
    # Check that the Name value is correct
    # self.assertEqual(vesselName[vesselNumber], self.driver.find_element_by_name("name").get_attribute("value")) ---- seems not to work anymore
    self.assertEqual(vesselName[vesselNumber], self.driver.find_element_by_css_selector("input[name=\"name\"]").get_attribute("value"))
    # Check that External Marking Value is correct
    self.assertEqual("EXT3", self.driver.find_element_by_name("externalMarking").get_attribute("value"))
    # Check that the CFR value is correct
    self.assertEqual(cfrValue[vesselNumber], self.driver.find_element_by_name("cfr").get_attribute("value"))
    # Check that the IMO value is correct
    self.assertEqual(imoValue[vesselNumber], self.driver.find_element_by_name("imo").get_attribute("value"))
    # Check that the HomePort value is correct
    self.assertEqual("GOT", self.driver.find_element_by_name("homeport").get_attribute("value"))
    # Check that the Gear Type value is correct.
    self.assertEqual("Dermersal", self.driver.find_element_by_xpath(
        "(//button[@type='button'])[4]").text)
    # Check that the MMSI value is correct
    self.assertEqual(mmsiValue[vesselNumber], self.driver.find_element_by_name("mmsi").get_attribute("value"))
    # Check that the License Type value is correct.
    self.assertEqual("MOCK-license-DB", self.driver.find_element_by_xpath(
        "(//button[@type='button'])[5]").text)
    # Check that the Length Type value is correct.
    self.assertEqual("14", self.driver.find_element_by_name("lengthValue").get_attribute("value"))
    # Check that the Gross Tonnage value is correct.
    self.assertEqual("3", self.driver.find_element_by_name("grossTonnage").get_attribute("value"))
    # Check that the Power value is correct.
    self.assertEqual("1300", self.driver.find_element_by_name("power").get_attribute("value"))
    # Check that the Producer Name value is correct.
    #
    # Needs to be updated according to asset database
    #
    #
    # self.assertEqual("Mikael", self.driver.find_element_by_name("producername").get_attribute("value"))
    # Check that the Producer Code value is correct.
    self.assertEqual(producercodeValue, self.driver.find_element_by_name("producercode").get_attribute("value"))
    # Check that the Contact Name value is correct.
    self.assertEqual("Mikael Great", self.driver.find_element_by_name("contactName").get_attribute("value"))
    # Check that the E-mail value is correct.
    self.assertEqual("mikael.glemne@havochvatten.se", self.driver.find_element_by_id("contact-email").get_attribute("value"))
    # Check that the E-mail value is correct.
    self.assertEqual("+46720456789", self.driver.find_element_by_id("contact-number").get_attribute("value"))
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
    self.assertEqual(memberIdnumber, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
    # Check DNID Number in the list
    self.assertEqual(dnidNumber[mobileTerminalNumber], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)
    # Click on details button
    self.driver.find_element_by_xpath(
        "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
    time.sleep(2)
    # Check Transceiver Type
    self.assertEqual(transceiverType, self.driver.find_element_by_id("mob-term-form-details-transceiver-type").get_attribute("value"))
    # Check Software Version
    self.assertEqual(softwareVersion, self.driver.find_element_by_id("mob-term-form-details-software-version").get_attribute("value"))
    # Check Satellite Number
    self.assertEqual(satelliteNumber[mobileTerminalNumber], self.driver.find_element_by_id("mob-term-form-details-satelite-number").get_attribute("value"))
    # Check Antenna Version
    self.assertEqual(antennaVersion, self.driver.find_element_by_id("mob-term-form-details-antenna").get_attribute("value"))
    # Check DNID Number
    self.assertEqual(dnidNumber[mobileTerminalNumber], self.driver.find_element_by_name("dnid").get_attribute("value"))
    # Check Member Number
    self.assertEqual(memberIdnumber, self.driver.find_element_by_name("memberId").get_attribute("value"))
    # Check Installed by Name
    self.assertEqual(installedByName, self.driver.find_element_by_xpath("(//input[@type='text'])[36]").get_attribute("value"))
    # Leave new asset view
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
    time.sleep(1)
    self.driver.find_element_by_css_selector("li.audittab").click()
    time.sleep(1)
    # Click on Global setting subtab under Configuration Tab
    self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[2]").click()
    time.sleep(1)
    # Set Speed format to knots
    self.driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
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
    # Enter IRCS value
    self.driver.find_element_by_name("ircs").send_keys(ircsValue[0])
    time.sleep(3)
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
    self.driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
    time.sleep(5)
    # Click on Confirm button
    self.driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
    time.sleep(5)
    # Enter IRCS for newly created position
    self.driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
    time.sleep(2)
    self.driver.find_element_by_link_text("Custom").click()
    self.driver.find_element_by_xpath("//input[@type='text']").clear()
    self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
    # Click on search button
    self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
    time.sleep(5)
    # Verifies position data
    self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
    self.assertEqual(externalMarkingValue, self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
    self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
    self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
    # Bug UVMS-3249 self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[6]").text)
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
    self.driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
    self.driver.find_element_by_link_text("Custom").click()
    self.driver.find_element_by_xpath("//input[@type='text']").clear()
    self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
    # Click on search button
    self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
    time.sleep(5)
    # Enter Vessel to verify position data
    self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
    self.assertEqual(externalMarkingValue,
                     self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
    self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
    self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
    # Bug UVMS-3249 self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr[1]/td[6]").text)
    self.assertEqual(lolaPositionValues[0][0][0],
                     self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][0] + "\"]").text)
    self.assertEqual(lolaPositionValues[0][0][1],
                     self.driver.find_element_by_css_selector("td[title=\"" + lolaPositionValues[0][0][1] + "\"]").text)
    self.assertEqual("%.2f" % speedValue + " kts", self.driver.find_element_by_css_selector(
        "td[title=\"" + "%.2f" % speedValue + " kts" + "\"]").text)
    self.assertEqual(str(courseValue) + "°", self.driver.find_element_by_css_selector(
        "td[title=\"" + str(courseValue) + "°" + "\"]").text)
    self.assertEqual(sourceValue[1],
                     self.driver.find_element_by_css_selector("td[title=\"" + sourceValue[1] + "\"]").text)
    time.sleep(5)
    return earlierPositionDateTimeValueString





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
#    @classmethod
#    def setUpClass(cls):
        #startup_browser_and_login_to_unionVMS(cls)

#    @classmethod
#    def tearDownClass(cls):
        #shutdown_browser(cls)

    def test_01_reset_database_union_vms(self):
        # Save current default dir path
        default_current_dir = os.getcwd()
        # Reset Module Database
        resetModuleDatabase()
        # Return to default current dir
        os.chdir(default_current_dir)
        # Populate Iridium Imarsat-C Data
        populateIridiumImarsatCData()
        # Populate Sanity Rule Data
        populateSanityRuleData()
        time.sleep(15)

    def test_02_create_one_new_asset(self):
        # Create new asset (first in the list)
        create_one_new_asset_from_gui(self, 0)

    def test_03_check_new_asset_exists(self):
        # Check new asset (first in the list)
        check_new_asset_exists(self, 0)

    def test_04_create_one_new_mobile_terminal(self):
        # Create new Mobile Terminal (first in the list)
        create_one_new_mobile_terminal_from_gui(self, 0)


    def test_05_check_new_mobile_terminal_exists(self):
        # Check new Mobile Terminal (first in the list)
        check_new_mobile_terminal_exists(self, 0)


    def test_06_link_asset_and_mobile_terminal(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Enter Serial Number in field
        self.driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(serialNoValue[0])
        # Click in search button
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(5)
        # Click on details button
        self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
        time.sleep(3)
        # Click on Link Asset
        self.driver.find_element_by_id("assignVesselLink").click()
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
        #self.driver.find_element_by_xpath("(//button[@type='button'])[13]").click()
        # Enter Reason comment
        self.driver.find_element_by_name("comment").send_keys("Need to connect this mobile terminal with this asset.")
        time.sleep(2)
        # Click on Link button 2
        #self.driver.find_element_by_xpath("(//button[@type='button'])[66]").click()
        self.driver.find_element_by_css_selector("div.modal-footer > div.row > div.col-md-12 > button.btn.btn-primary").click()
        time.sleep(2)
        # Close page
        self.driver.find_element_by_id("menu-bar-cancel").click()
        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)

    def test_07_generate_and_verify_manual_position(self):
        # Create a manual position and verify the position
        generate_and_verify_manual_position(self, reportedSpeedValue, reportedCourseValue)
        # Shutdown browser
        shutdown_browser(self)


    def test_08_generate_NAF_and_verify_position(self):
        # Create a NAF position and verify the position
        generate_NAF_and_verify_position(self,reportedSpeedValue,reportedCourseValue)
        # Shutdown browser
        shutdown_browser(self)


    def test_09_create_second_new_asset(self):
        # Create new asset (second in the list)
        create_one_new_asset_from_gui(self, 1)

    def test_10_check_new_asset_exists(self):
        # Check new asset (second in the list)
        check_new_asset_exists(self, 1)

    def test_11_create_second_new_mobile_terminal(self):
        # Create new Mobile Terminal (second in the list)
        create_one_new_mobile_terminal_from_gui(self, 1)

    def test_12_check_second_new_mobile_terminal_exists(self):
        # Check new Mobile Terminal (second in the list)
        check_new_mobile_terminal_exists(self, 1)

    def test_13_unlink_asset_and_mobile_terminal(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Enter Serial Number in field
        self.driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(serialNoValue[0])
        # Click in search button
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(5)
        # Click on details button
        self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
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

    def test_14_generate_manual_position_with_no_connected_transponder_and_verify_holding_table(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Positions tab
        self.driver.find_element_by_id("uvms-header-menu-item-movement").click()
        time.sleep(2)
        # Click on New manual report
        self. driver.find_element_by_xpath("//button[@type='submit']").click()
        # Enter IRCS value
        self.driver.find_element_by_name("ircs").send_keys(ircsValue[0])
        time.sleep(3)
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
        self.driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        time.sleep(5)
        # Click on Confirm button
        self.driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        time.sleep(5)
        # Enter IRCS for newly created position
        self.driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        self.driver.find_element_by_link_text("Custom").click()
        self.driver.find_element_by_xpath("//input[@type='text']").clear()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
        # Click on search button
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(5)
        # Verifies that time stamp for the generated position does not exist
        self.assertNotEqual(earlierPositionTimeValueString, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[6]").text)
        time.sleep(2)
        # Select Alarms tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(2)
        # Select filter "Transponder not found"
        self.driver.find_element_by_xpath("(//button[@type='button'])[7]").click()
        self.driver.find_element_by_link_text("Transponder not found").click()
        time.sleep(2)
        # Click on search button
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)
        # Check Asset name
        self.assertEqual(vesselName[0], self.driver.find_element_by_link_text(vesselName[0]).text)
        # Click on Details button
        self.driver.find_element_by_xpath("(//button[@type='button'])[10]").click()
        time.sleep(2)
        # Check Position report fields
        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[2]/div[3]/div[2]/div/div[2]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_xpath("//div[2]/div[2]/div[2]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_xpath("//div[3]/div[2]/div[3]/div[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[2]/div[4]/div[2]").text)
        # Bug UVMS-3249 self.assertEqual(earlierPositionTimeValueString, self.driver.find_element_by_xpath("//div[7]/div/div[2]/div").text)
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

    def test_15_link_asset_to_another_mobile_terminal(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Enter Serial Number in field
        self.driver.find_element_by_xpath("(//input[@type='text'])[7]").send_keys(serialNoValue[1])
        # Click in search button
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(5)
        # Click on details button
        self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
        time.sleep(2)
        # Click on Link Asset
        self.driver.find_element_by_id("assignVesselLink").click()
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

    def test_16_generate_and_verify_manual_position(self):
        # Startup browser and login
        UnionVMSTestCase.test_07_generate_and_verify_manual_position(self)

    def test_17_create_assets_3_4_5_6(self):
        # Create assets 3-6 in the list
        for x in range(2, 6):
            create_one_new_asset_from_gui(self, x)
            time.sleep(1)

    def test_18_create_two_assets_to_group_and_check_group(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Search for "fartyg"
        self.driver.find_element_by_xpath("(//input[@type='text'])[18]").send_keys("fartyg")
        self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
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
            self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/thead/tr/th[4]/a/span/span").click()
            time.sleep(1)
        # Select Fartyg1001 and Fartyg1002 by click
        self.driver.find_element_by_css_selector("td.checkboxContainer > input[type=\"checkbox\"]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        # Select Action "Save as Group"
        self.driver.find_element_by_xpath("(//button[@name='name'])[10]").click()
        self.driver.find_element_by_link_text("Save as Group").click()
        time.sleep(1)
        # Enter Group name and click on save button
        self.driver.find_element_by_css_selector("form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]").send_keys(groupName[0])
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(8)
        # Check that Grupp 1 has been created
        self.driver.find_element_by_xpath("(//button[@type='button'])[12]").click()
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
        self.assertEqual("Dermersal", self.driver.find_element_by_css_selector("td[title=\"Dermersal\"]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_css_selector("td[title=\"MOCK-license-DB\"]").text)
        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[1], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[1] + "\"]").text)
        self.assertEqual(ircsValue[1], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[1] + "\"]").text)
        self.assertEqual(cfrValue[1], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[1] + "\"]").text)
        self.assertEqual("Dermersal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)

    def test_19_add_two_assets_to_group_and_check_group(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Search for "fartyg"
        self.driver.find_element_by_xpath("(//input[@type='text'])[18]").clear()
        self.driver.find_element_by_xpath("(//input[@type='text'])[18]").send_keys("fartyg")
        self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
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
            self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/thead/tr/th[4]/a/span/span").click()
            time.sleep(2)
        # Select Fartyg1005 and Fartyg1006 by click
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[6]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[7]").click()
        # Select Action "Add to Group"
        self.driver.find_element_by_xpath("(//button[@name='name'])[10]").click()
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
        self.driver.find_element_by_xpath("(//button[@type='button'])[12]").click()
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
        self.assertEqual("Dermersal", self.driver.find_element_by_css_selector("td[title=\"Dermersal\"]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_css_selector("td[title=\"MOCK-license-DB\"]").text)

        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[1], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[1] + "\"]").text)
        self.assertEqual(ircsValue[1], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[1] + "\"]").text)
        self.assertEqual(cfrValue[1], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[1] + "\"]").text)
        self.assertEqual("Dermersal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)

        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[3]").text)
        self.assertEqual(vesselName[4], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[4] + "\"]").text)
        self.assertEqual(ircsValue[4], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[4] + "\"]").text)
        self.assertEqual(cfrValue[4], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[4] + "\"]").text)
        self.assertEqual("Dermersal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[7]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[3]/td[8]").text)

        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[3]").text)
        self.assertEqual(vesselName[5], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[5] + "\"]").text)
        self.assertEqual(ircsValue[5], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[5] + "\"]").text)
        self.assertEqual(cfrValue[5], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[5] + "\"]").text)
        self.assertEqual("Dermersal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[7]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[4]/td[8]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)



    def test_20_remove_one_asset_group_and_check_group(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on saved groups
        self.driver.find_element_by_xpath("(//button[@type='button'])[12]").click()
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        time.sleep(2)
        # Click on Grupp 1
        self.driver.find_element_by_link_text(groupName[0]).click()
        #self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div/form/div/div/div/div/div/div/div/div[2]/div/div/div/div/ul/li[2]/a/span").click()
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
            self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/thead/tr/th[4]/a/span/span").click()
            time.sleep(1)

        # Select Fartyg1002 and Fartyg1005
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[4]").click()
        time.sleep(1)
        # Click on action button
        self.driver.find_element_by_xpath("(//button[@name='name'])[10]").click()
        time.sleep(1)
        # Remove selected assets from Grupp 1
        self.driver.find_element_by_link_text("Remove from Group").click()
        time.sleep(5)
        # Reload page
        self.driver.refresh()
        time.sleep(10)
        # Click on saved groups
        self.driver.find_element_by_xpath("(//button[@type='button'])[12]").click()
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        time.sleep(2)
        # Click on Grupp 1
        self.driver.find_element_by_link_text(groupName[0]).click()
        #self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div/form/div/div/div/div/div/div/div/div[2]/div/div/div/div/ul/li[2]/a/span").click()
        time.sleep(5)
        # Check Assets in Group
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual("Dermersal", self.driver.find_element_by_css_selector("td[title=\"Dermersal\"]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_css_selector("td[title=\"MOCK-license-DB\"]").text)
        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[5], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[5] + "\"]").text)
        self.assertEqual(ircsValue[5], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[5] + "\"]").text)
        self.assertEqual(cfrValue[5], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[5] + "\"]").text)
        self.assertEqual("Dermersal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    def test_21_create_second_group_and_add_assets_to_group(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Search for "fartyg"
        self.driver.find_element_by_xpath("(//input[@type='text'])[18]").clear()
        self.driver.find_element_by_xpath("(//input[@type='text'])[18]").send_keys("fartyg")
        self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
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
            self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/thead/tr/th[4]/a/span/span").click()
            time.sleep(1)
        # Select Fartyg1003 and Fartyg1005 by click
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[4]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[6]").click()
        # Select Action "Save as Group"
        self.driver.find_element_by_xpath("(//button[@name='name'])[10]").click()
        self.driver.find_element_by_link_text("Save as Group").click()
        time.sleep(1)
        # Enter Group name and click on save button
        self.driver.find_element_by_css_selector("form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]").send_keys(groupName[1])
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(8)
        # Check that Grupp 2 has been created
        self.driver.find_element_by_xpath("(//button[@type='button'])[12]").click()
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
        self.assertEqual("Dermersal", self.driver.find_element_by_css_selector("td[title=\"Dermersal\"]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_css_selector("td[title=\"MOCK-license-DB\"]").text)
        self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[2]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        self.assertEqual(vesselName[4], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[4] + "\"]").text)
        self.assertEqual(ircsValue[4], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[4] + "\"]").text)
        self.assertEqual(cfrValue[4], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[4] + "\"]").text)
        self.assertEqual("Dermersal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[2]/td[8]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)



    def test_22_delete_second_group_and_check(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on "saved groups" drop box
        self.driver.find_element_by_xpath("(//button[@type='button'])[12]").click()
        time.sleep(2)
        # Click on delete button for Grupp 2
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div/form/div/div/div/div/div/div/div/div[2]/div/div/div/div/ul/li[3]/span").click()
        time.sleep(2)
        # Click on confirmation button
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(5)
        # Reload page
        self.driver.refresh()
        time.sleep(10)
        # Check that Grupp 1 exists and Grupp 2 does not exist
        self.driver.find_element_by_xpath("(//button[@type='button'])[12]").click()
        time.sleep(1)
        self.assertEqual(groupName[0], self.driver.find_element_by_link_text(groupName[0]).text)
        try:
            self.assertFalse(self.driver.find_element_by_link_text(groupName[1]).text)
        except NoSuchElementException:
            pass
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    def test_23_advanced_search_of_assets(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Click on advanced search
        self.driver.find_element_by_css_selector("div.col-md-10.searchFooter > a > span").click()
        time.sleep(1)
        # Search for all External Marking called "EXT3"(externalMarkingValue)
        self.driver.find_element_by_id("searchextno").send_keys(externalMarkingValue)
        self.driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()
        time.sleep(8)

        # Get asset name values in the list
        assetList = []
        for x in range(6):
            tempAssetName = self.driver.find_element_by_xpath(
                "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) +"]/td[4]").text
            assetList.append(tempAssetName)
        # Check if asset list is not sorted
        if sorted(assetList) != assetList:
            # Sort on "Name" by click on "Name" once
            self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/thead/tr/th[4]/a/span/span").click()
            time.sleep(1)

        # Check Assets in List
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td[title=\"" + countryValue + "\"]").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_css_selector("td[title=\"" + externalMarkingValue + "\"]").text)
        self.assertEqual(vesselName[0], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[0] + "\"]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[0] + "\"]").text)
        self.assertEqual(cfrValue[0], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[0] + "\"]").text)
        self.assertEqual("Dermersal", self.driver.find_element_by_css_selector("td[title=\"Dermersal\"]").text)
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_css_selector("td[title=\"MOCK-license-DB\"]").text)
        for x in [1,2,3,4,5]:
            self.assertEqual(countryValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[2]").text)
            self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[3]").text)
            self.assertEqual(vesselName[x], self.driver.find_element_by_css_selector("td[title=\"" + vesselName[x] + "\"]").text)
            self.assertEqual(ircsValue[x], self.driver.find_element_by_css_selector("td[title=\"" + ircsValue[x] + "\"]").text)
            self.assertEqual(cfrValue[x], self.driver.find_element_by_css_selector("td[title=\"" + cfrValue[x] + "\"]").text)
            self.assertEqual("Dermersal", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[7]").text)
            self.assertEqual("MOCK-license-DB", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr[" + str(x+1) + "]/td[8]").text)
        time.sleep(3)
        # Click on save group button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div/form/div/div/div/div[3]/a[2]/span").click()
        # Enter Grupp name "Grupp 3" and click on save button
        self.driver.find_element_by_css_selector("form[name=\"saveForm\"] > div.form-group > input[name=\"name\"]").send_keys(groupName[2])
        self.driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-primary").click()
        time.sleep(5)
        # Reload page
        self.driver.refresh()
        time.sleep(10)
        # Check that Grupp 3 exists in the list
        self.driver.find_element_by_xpath("(//button[@type='button'])[12]").click()
        self.assertEqual(groupName[2], self.driver.find_element_by_link_text(groupName[2]).text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    def test_24_export_assets_to_excel_file(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Click on asset tab
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        time.sleep(5)
        # Search for "fartyg"
        self.driver.find_element_by_xpath("(//input[@type='text'])[18]").clear()
        self.driver.find_element_by_xpath("(//input[@type='text'])[18]").send_keys("fartyg")
        self.driver.find_element_by_xpath("(//button[@type='submit'])[3]").click()
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
            self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/thead/tr/th[4]/a/span/span").click()
            time.sleep(1)
        # Select Fartyg1001 and Fartyg1002 by click
        self.driver.find_element_by_css_selector("td.checkboxContainer > input[type=\"checkbox\"]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        time.sleep(2)
        # Select Action "Export selection"
        self.driver.find_element_by_xpath("(//button[@name='name'])[10]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection").click()
        time.sleep(3)
        # Change to Download folder for current user
        home = expanduser("~")
        os.chdir(home)
        os.chdir(".\Downloads")
        # Open saved csv file and read all elements to "allrows"
        ifile  = open('assets.csv', "rt", encoding="utf8")
        reader = csv.reader(ifile, delimiter=';')
        allrows =['']
        for row in reader:
            print(row)
            allrows.append(row)
        ifile.close()
        del allrows[0]
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
                self.assertEqual("Dermersal", allrows[y][5])
                self.assertEqual("MOCK-license-DB", allrows[y][6])
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)



    def test_25_create_new_mobile_terminal_3_6(self):
        # Create new Mobile Terminal (Number 3-6 in the list)
        for x in [2,3,4,5]:
            create_one_new_mobile_terminal_from_gui(self, x)


    def test_26_export_mobile_terminals_to_excel_file(self):
        # Startup browser and login
        # Continue ...
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(7)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(5)
        # Search on MemberID 100
        self.driver.find_element_by_xpath("(//input[@type='text'])[9]").send_keys(memberIdnumber)
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)

        # Sort on "Serial no"
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]/a/span/span").click()
        time.sleep(2)

        # Select Not linked row number 2-4 by click
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[3]").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[4]").click()
        time.sleep(2)

        # Save row information for rows 2-4 in the list
        allrowsbackup = ['']
        currentrow = []

        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[1]/td[2]/span[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[6]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[7]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[8]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[9]/span").text)
        allrowsbackup.append(currentrow)

        currentrow = []
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[2]/span[1]/a").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[5]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[6]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[7]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[8]/span").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[2]/td[9]/span").text)
        allrowsbackup.append(currentrow)

        currentrow = []
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[2]/span[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[3]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[4]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[5]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[6]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[7]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[8]").text)
        currentrow.append(self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr[3]/td[9]/span").text)
        allrowsbackup.append(currentrow)

        del allrowsbackup[0]
        print("-------------------- SAVE START-----------------------")
        print(allrowsbackup)
        print("-------------------- SAVE END-----------------------")


        # Select Action "Export selection"
        self.driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Export selection").click()
        time.sleep(3)

        # Change to Download folder for current user
        home = expanduser("~")
        os.chdir(home)
        os.chdir(".\Downloads")

        # Open saved csv file and read all elements to "allrows"
        ifile  = open('mobileTerminals.csv', "rt", encoding="utf8")
        reader = csv.reader(ifile, delimiter=';')
        allrows =['']
        for row in reader:
            allrows.append(row)
        ifile.close()
        del allrows[0]
        print("-------------------- READ START-----------------------")
        print(allrows)
        print("-------------------- READ END-----------------------")


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




    def test_27_view_audit_log(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(7)
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(7)
        # Click on all sub tabs under Audit Log Tab
        for x in [2, 3, 4, 5, 6, 7]:
            self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[" + str(x) + "]/span").click()
            time.sleep(2)
        self.driver.find_element_by_css_selector("li.audittab > span").click()
        time.sleep(2)
        # Check sub tab names
        self.assertEqual("ALL", self.driver.find_element_by_css_selector("li.audittab.active > span").text)
        self.assertEqual("EXCHANGE", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[2]/span").text)
        self.assertEqual("POSITION REPORTS", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[3]/span").text)
        self.assertEqual("ASSETS AND TERMINALS", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[4]/span").text)
        self.assertEqual("GIS", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[5]/span").text)
        self.assertEqual("ALERTS", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[6]/span").text)
        self.assertEqual("ACCESS CONTROL", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[7]/span").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    def test_28_view_audit_log_with_interval(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(7)
        # Select Audit Log tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()

        time.sleep(7)

        # continue ...
        # Bug UVMS-3051 needs to be fixed first

        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    def test_29_view_configuration_pages(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(7)
        # Select Admin tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("CONFIGURATION").click()
        time.sleep(1)
        self.driver.find_element_by_css_selector("li.audittab").click()
        time.sleep(1)
        # Click on all sub tabs under Configuration Tab
        for x in [2, 3, 4, 5, 6]:
            self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[" + str(x) + "]").click()
            time.sleep(2)
        time.sleep(5)
        # Check sub tab names
        self.assertEqual("SYSTEM MONITOR", self.driver.find_element_by_css_selector("li.audittab").text)
        self.assertEqual("GLOBAL SETTINGS", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[2]").text)
        self.assertEqual("REPORTING", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[3]").text)
        self.assertEqual("MDR", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[4]").text)
        self.assertEqual("ASSETS", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[5]").text)
        self.assertEqual("MOBILE TERMINALS", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[6]").text)
        self.assertEqual("EXCHANGE", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[7]").text)

        # Shutdown browser
        shutdown_browser(self)


    def test_30_change_global_settings_change_date_format(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Admin tab
        self.driver.find_element_by_id("uvms-header-menu-item-audit-log").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("CONFIGURATION").click()
        time.sleep(1)
        self.driver.find_element_by_css_selector("li.audittab").click()
        time.sleep(1)
        # Click on Global setting subtab under Configuration Tab
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/ul/li[2]").click()
        time.sleep(1)
        # Check that Date format is correct
        try:
            radiobuttonDate1 = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[3]/div/ng-include/div/div/div[1]/div[2]/div[1]/ul/li[1]/label/input").is_selected()
        except:
            print("Did NOT find selected radio button")
            radiobuttonDate1 = False
        try:
            radiobuttonDate2 = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[3]/div/ng-include/div/div/div[1]/div[2]/div[1]/ul/li[2]/label/input").is_selected()
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

    def test_31_change_global_settings_change_speed_format(self):
        # Change and check speed unit type for Global Settings
        for x in [2,1,0]:
            change_and_check_speed_format(self,x)


    def test_32_check_view_help_text(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Click on User Guide icon (Question mark icon)
        self.driver.find_element_by_xpath("//a[contains(@href, '#/help')]").click()
        time.sleep(3)
        # Check User guide page
        self.assertEqual("Table of contents", self.driver.find_element_by_css_selector("h3").text)
        time.sleep(1)
        self.assertEqual("Welcome to Union VMS", self.driver.find_element_by_id("welcome").text)
        time.sleep(5)

        # Shutdown browser
        shutdown_browser(self)


    def test_33_check_alerts_view(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Alerts tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(3)
        # Check List Headlines for Holding Table
        self.assertEqual("Date triggered (UTC)", self.driver.find_element_by_css_selector("span > span").text)
        self.assertEqual("Object affected", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]/a/span/span").text)
        self.assertEqual("Rule", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[4]").text)
        # Select Alerts tab (Notifications)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[2]/a").click()
        time.sleep(2)
        # Check List Headlines for Notifications
        self.assertEqual("Date triggered (UTC)", self.driver.find_element_by_css_selector("span > span").text)
        self.assertEqual("Object affected", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]/a/span/span").text)
        self.assertEqual("Rule", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[4]").text)
        # Select Alerts tab (Rules)
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div[1]/div/div/ul/li[3]/a").click()
        time.sleep(2)
        # Check List Headlines for Rules List
        self.assertEqual("Rule name", self.driver.find_element_by_css_selector("span > span").text)
        self.assertEqual("Last triggered", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]/a/span/span").text)
        self.assertEqual("Date updated", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[4]/a/span/span").text)
        time.sleep(5)

        # Shutdown browser
        shutdown_browser(self)


    def test_34_create_speed_rule_one(self):
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
        self.driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        time.sleep(2)
        # Enter Rule name
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys("Speed > " + str(reportedSpeedDefault[0]))
        # Enter Description
        self.driver.find_element_by_name("description").clear()
        self.driver.find_element_by_name("description").send_keys("Speed > " + str(reportedSpeedDefault[0]))
        # Enter Rule Speed > 8
        self.driver.find_element_by_css_selector("div[name=\"startOperator\"] > button[name=\"name\"]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("(").click()
        time.sleep(1)
        self.driver.find_element_by_css_selector("div[name=\"criteria\"] > button[name=\"name\"]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Position").click()
        time.sleep(1)
        self.driver.find_element_by_css_selector("div[name=\"subCriteria\"] > button[name=\"name\"]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Reported speed").click()
        time.sleep(1)
        self.driver.find_element_by_css_selector("div[name=\"conditionTypes\"] > button[name=\"name\"]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text(">").click()
        time.sleep(1)
        self.driver.find_element_by_name("value").click()
        time.sleep(1)
        self.driver.find_element_by_name("value").clear()
        time.sleep(1)
        self.driver.find_element_by_name("value").send_keys(reportedSpeedDefault[0])
        time.sleep(1)
        self.driver.find_element_by_css_selector("div[name=\"endOperator\"] > button[name=\"name\"]").click()
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
        self.driver.find_element_by_xpath("(//button[@name='name'])[3]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("Yes").click()
        #self.driver.find_element_by_xpath("(//a[contains(text(),'Yes')])[3]").click()
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)

    def test_35_verify_created_speed_rule_one(self):
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
        self.assertEqual(rulesHeadlineNames[0], self.driver.find_element_by_css_selector("span > span").text)
        self.assertEqual(rulesHeadlineNames[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[3]/a/span/span").text)
        self.assertEqual(rulesHeadlineNames[2], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[4]/a/span/span").text)
        self.assertEqual(rulesHeadlineNames[3], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[5]/a/span/span").text)
        self.assertEqual(rulesHeadlineNames[4], self.driver.find_element_by_css_selector("th.notifyByTicket").text)
        self.assertEqual(rulesHeadlineNames[5], self.driver.find_element_by_css_selector("th.notifyByEmail").text)
        self.assertEqual(rulesHeadlineNames[6], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[3]/div/div/div/div/span/table/thead/tr/th[8]/a/span/span").text)
        # Check speed rule parameters
        self.assertEqual("Speed > " + str(reportedSpeedDefault[0]), self.driver.find_element_by_css_selector("td.statusColored.truncate-text").text)
        self.assertEqual("Yes", self.driver.find_element_by_xpath("(//button[@name='name'])[2]").text)
        self.assertEqual("Yes", self.driver.find_element_by_xpath("(//button[@name='name'])[3]").text)
        self.assertEqual("ACTIVE", self.driver.find_element_by_css_selector("span.label.label-success").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)

    def test_36_create_manual_position_with_speed_that_triggs_rule_one(self):
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
        # Bug UVMS-3249 self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedDefault[0] + 1) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()
        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)


    def test_37_create_NAF_position_with_speed_that_triggs_rule_one(self):
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
        # Bug UVMS-3249 self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_css_selector("div.col-md-9 > div.value").text)
        self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_xpath("//div[5]/div[3]/div").text)
        self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_xpath("//div[5]/div[4]/div").text)
        self.assertEqual(str(reportedSpeedDefault[0] + 1) + " kts", self.driver.find_element_by_xpath("//div[5]/div[5]/div").text)
        self.assertEqual(str(reportedCourseValue) + "°", self.driver.find_element_by_xpath("//div[6]/div").text)
        # Close position window
        self.driver.find_element_by_xpath("//div[7]/div/div/div/div/i").click()

        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)





    def test_special(self):
        a = datetime.datetime.utcnow()
        b = a - datetime.timedelta(hours=3)
        print(datetime.datetime.strftime(a, '%Y-%m-%d %H:%M:%S'))
        print(datetime.datetime.strftime(b, '%Y-%m-%d %H:%M:%S'))

        s1 = []
        s1.append('test1')
        s1.append('test2')
        print(s1)

        for x in range(6):
            print(x)


        a = 13.9412
        b = "%.2f" % a
        print(b)
        print("%.2f" % reportedSpeedValue + " kts")
        print("%.0f" % reportedSpeedValue + " kts")
        print("%f" % reportedSpeedValue + " kts")
        print(u"180°")
        print(str(reportedCourseValue) + u"°")
        if (str(reportedCourseValue) + u"°" == "180°"):
            print("YES!!!!")
        else:
            print("NO!")

        print(lolaPositionValues[5][1][0])
        print(lolaPositionValues[5][1][1])


        for x in range(2, 6):
            print ("We're on time %d" % (x))

        for x in [2,3, 6]:
            print ("We're on time %d" % (x))


        print("td[title=\"SWE\"]")
        print("td[title=\"" + countryValue + "\"]")

        home = expanduser("~")
        print(home)
        os.chdir(home)
        os.chdir(".\Downloads")
        print(os.getcwd())
        print ("--------------------------------------------------------------------")


        allrowsbackup = ['']
        for x in [0,1,2]:
            currentrow = []
            currentrow.append("Ett")
            currentrow.append("Två")
            currentrow.append("Tre")
            currentrow.append("Fyra")
            allrowsbackup.append(currentrow)
        print(allrowsbackup)


        print ("-------------------------------LISTA-------------------------------------")


        kalle = [8, 10, 12]

        print(kalle[0])


        """
        ifile  = open('assets.csv', "rt", encoding="utf8")
        #ifile = open('assets.csv', "rt")
        reader = csv.reader(ifile, delimiter=';')
        count = 0
        allrows =['']
        for row in reader:
            print(row)
            allrows.append(row)
        ifile.close()
        print ("--------------------------------------------------------------------")
        print (allrows)
        print ("--------------------------------------------------------------------")
        del allrows[0]
        print (allrows)
        for x in range(len(allrows)):
            print(allrows[x])
        print ("--------------------------------------------------------------------")
        print ("--------------------------------------------------------------------")
        print ("--------------------------------------------------------------------")
        for y in range(len(allrows)):
            #if not (y == 0):
                for x in range(len(allrows[y])):
                    print(allrows[y][x])
        """

    def test_special_2(self):
        populateIridiumImarsatCData()

    def test_special_3(self):
        populateSanityRuleData()

if __name__ == '__main__':
    unittest.main()
#unittest.main()