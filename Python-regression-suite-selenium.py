import unittest
import time
import datetime
import random
import sys
from unittest.case import _AssertRaisesContext

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import os
import psycopg2
import requests
import urllib.request

# Globals
# Assets
countryValue = 'SWE'
ircsValue = ["F1001", "F1002"]
vesselName = ["Fartyg1001", "Fartyg1002"]
cfrValue = ["SWE0000F1001", "SWE0000F1002"]
externalMarkingValue = "EXT3"
#imoValue = str(random.randint(0, 9999999))
#imoValue = imoValue.zfill(7)
imoValue = ["0261917", "0261918"]
#mmsiValue = str(random.randint(0, 999999999))
#mmsiValue = mmsiValue.zfill(9)
mmsiValue = ["302331238", "302331239"]
homeportValue = "GOT"
# Mobile Terminals
serialNoValue = ["M1001", "M1002"]
#transceiverType = str(random.randint(1, 100))
transceiverType = "Type A"
#softwareVersionList = ['A', 'B', 'C']
#softwareVersion = random.choice(softwareVersionList)
softwareVersion = "A"
antennaVersion = "A"
#satelliteNumber = str(random.randint(1, 999999999))
satelliteNumber = ["S1001", "S1002"]
#dnidNumber = str(random.randint(1, 99999))
dnidNumber = ["1001", "1002"]
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
# lolaPositionValues [Asset number x, lola position route y, lat=0 / lon=1]
lolaPositionValues = [[["57.326", "16.996"], ["57.327", "16.997"]],
                      [["57.934", "11.592"], ["57.935", "11.593"]]]

#latitudePositionValue = ["57.326", "57.934"]
#longitudePositionValue = ["16.996", "11.592"]
reportedSpeedValue = 5
reportedCourseValue = 180
httpNAFRequestString = "http://livm73t:28080/naf/rest/message/"
SourceValue= ('NAF', 'MANUAL')

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
                    (1051, 1050, 'ONLY_SINGLE_OCEAN', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1052, 1050, 'SAMPLING', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1053, 1050, 'MULTIPLE_OCEAN', 'FALSE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1054, 1050, 'CONFIGURABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1055, 1050, 'POLLABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1057, 1056, 'MULTIPLE_OCEAN', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1058, 1056, 'ONLY_SINGLE_OCEAN', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1059, 1056, 'SAMPLING', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1060, 1056, 'POLLABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
        cur.execute("""INSERT INTO mobterm.plugin_capability VALUES (%s, %s, %s, %s, %s, %s);""",
                    (1061, 1056, 'CONFIGURABLE', 'TRUE', datetime.datetime.utcnow(), 'UVMS'))
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
        self.driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        self.driver.find_element_by_link_text(countryValue).click()
        # Enter IRCS value
        self.driver.find_element_by_name("ircs").send_keys(ircsValue[0])
        # Enter Name value
        self.driver.find_element_by_name("name").send_keys(vesselName[0])
        # Enter External Marking Value
        self.driver.find_element_by_name("externalMarking").send_keys(externalMarkingValue)
        # Enter CFR Value
        self.driver.find_element_by_name("cfr").send_keys(cfrValue[0])
        # Enter IMO Value
        self.driver.find_element_by_name("imo").send_keys(imoValue[0])
        # Enter HomePort Value
        self.driver.find_element_by_name("homeport").send_keys(homeportValue)
        # Select Gear Type value
        self.driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        self.driver.find_element_by_link_text("Dermersal").click()
        # Enter MMSI Value
        self.driver.find_element_by_name("mmsi").send_keys(mmsiValue[0])
        # Select License Type value
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
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
        self.driver.find_element_by_name("producercode").send_keys("123")
        # Main Contact Name Value
        self.driver.find_element_by_name("contactName").send_keys("Mikael Great")
        # Main E-mail Value
        self.driver.find_element_by_name("email").send_keys("mikael.glemne@havochvatten.se")
        # Main Contact Number Value
        self.driver.find_element_by_name("contactNumber").send_keys("+46720456789")
        # Note comments
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/form/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/textarea"). \
            send_keys("This is some notes!")
        # Click on Save Asset button
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/form/div[1]/div[1]/div[2]/div/div[3]/button[2]").\
            click()
        # Leave new asset view
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/form/div[1]/div[1]/div[2]/div/div[4]/i").\
            click()
        time.sleep(3)
        # Shutdown browser
        shutdown_browser(self)


    def test_03_check_new_asset_exists(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Search for the new created asset in the asset list
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[1]/form/div/div/div/div[1]/div/div/div/div[1]/input").\
            send_keys(vesselName[0])
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div/button").click()
        time.sleep(5)
        # Check that the new asset exists in the list.
        self.assertEqual(vesselName[0],self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        time.sleep(1)
        # Click on details button for new asset
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr/td[10]/button/i").click()
        time.sleep(5)
        # Check that the F.S value is correct.
        self.assertEqual(countryValue,self.driver.find_element_by_xpath("(//button[@type='button'])[4]").text)
        # Check that the IRCS value is correct
        self.assertEqual(ircsValue[0], self.driver.find_element_by_name("ircs").get_attribute("value"))
        # Check that the Name value is correct
        self.assertEqual(vesselName[0], self.driver.find_element_by_name("name").get_attribute("value"))
        # Check that External Marking Value is correct
        self.assertEqual("EXT3", self.driver.find_element_by_name("externalMarking").get_attribute("value"))
        # Check that the CFR value is correct
        self.assertEqual(cfrValue[0], self.driver.find_element_by_name("cfr").get_attribute("value"))
        # Check that the IMO value is correct
        self.assertEqual(imoValue[0], self.driver.find_element_by_name("imo").get_attribute("value"))
        # Check that the HomePort value is correct
        self.assertEqual("GOT", self.driver.find_element_by_name("homeport").get_attribute("value"))
        # Check that the Gear Type value is correct.
        self.assertEqual("Dermersal",self.driver.find_element_by_xpath(
            "(//button[@type='button'])[5]").text)
        # Check that the MMSI value is correct
        self.assertEqual(mmsiValue[0], self.driver.find_element_by_name("mmsi").get_attribute("value"))
        # Check that the License Type value is correct.
        self.assertEqual("MOCK-license-DB",self.driver.find_element_by_xpath(
            "(//button[@type='button'])[6]").text)
        # Check that the Length Type value is correct.
        self.assertEqual("14", self.driver.find_element_by_name("lengthValue").get_attribute("value"))
        # Check that the Gross Tonnage value is correct.
        self.assertEqual("3", self.driver.find_element_by_name("grossTonnage").get_attribute("value"))
        # Check that the Power value is correct.
        self.assertEqual("1300", self.driver.find_element_by_name("power").get_attribute("value"))
        # Check that the Producer Name value is correct.
        self.assertEqual("Mikael", self.driver.find_element_by_name("producername").get_attribute("value"))
        # Check that the Producer Code value is correct.
        self.assertEqual("123", self.driver.find_element_by_name("producercode").get_attribute("value"))
        # Check that the Contact Name value is correct.
        self.assertEqual("Mikael Great", self.driver.find_element_by_name("contactName").get_attribute("value"))
        # Check that the E-mail value is correct.
        self.assertEqual("mikael.glemne@havochvatten.se", self.driver.find_element_by_name(
            "email").get_attribute("value"))
        # Check that the E-mail value is correct.
        self.assertEqual("+46720456789", self.driver.find_element_by_name("contactNumber").get_attribute("value"))
        # Check that the Note comments value is correct.
        self.assertEqual("This is some notes!",self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/form/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/textarea").\
                         get_attribute("value"))
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    def test_04_create_one_new_mobile_terminal(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Click on new terminal button
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div/div/div/div/div[2]/button").\
            click()
        time.sleep(3)
        # Select Transponder system
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//button[@type='button'])[21]"))) # Waits until element exists
        element.click()
        self.driver.find_element_by_link_text("Inmarsat-C : twostage").click()
        time.sleep(1)
        # Enter serial number
        self.driver.find_element_by_name("serialNumber").send_keys(serialNoValue[0])
        # Enter Transceiver type
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[2]/div/form/fieldset/div[2]/div/div[1]/div[2]/input").\
            send_keys(transceiverType)
        # Enter Software Version
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[2]/div/form/fieldset/div[2]/div/div[1]/div[3]/input").\
            send_keys(softwareVersion)
        # Enter Antenna
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[2]/div/form/fieldset/div[2]/div/div[1]/div[4]/input").\
            send_keys(antennaVersion)
        # Enter Satellite Number
        self.driver.find_element_by_name("sattelite_number").send_keys(satelliteNumber[0])
        # Enter DNID Number
        self.driver.find_element_by_name("dnid").send_keys(dnidNumber[0])
        # Enter Member Number
        self.driver.find_element_by_name("memberId").send_keys(memberIdnumber)
        # Enter Installed by
        self.driver.find_element_by_xpath("(//input[@type='text'])[37]").send_keys(installedByName)
        # Expected frequency
        self.driver.find_element_by_xpath("(//input[@type='number'])[2]").send_keys(expectedFrequencyHours)
        # Grace period
        self.driver.find_element_by_xpath("(//input[@type='number'])[4]").send_keys(gracePeriodFrequencyHours)
        # In port
        self.driver.find_element_by_xpath("(//input[@type='number'])[6]").send_keys(inPortFrequencyHours)
        # Click on save button
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[1]/div[2]/div/div[2]/button[1]").\
            click()
        time.sleep(5)
        # Leave new asset view
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[1]/div[2]/div/div[3]/i").\
            click()
        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)


    def test_05_check_new_mobile_terminal_exists(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Enter Serial Number in field
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/div/form/div/div/div/div[1]/div[2]/div[2]/input"). \
            send_keys(serialNoValue[0])
        # Click in search button
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/div/form/div/div/div/div[2]/div[2]/div[1]/button"). \
            click()
        time.sleep(5)
        # Check Serial Number in the list
        self.assertEqual(serialNoValue[0], self.driver.find_element_by_css_selector("td.statusColored.ng-binding").text)
        # Check Member Number in the list
        self.assertEqual(memberIdnumber, self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        # Check DNID Number in the list
        self.assertEqual(dnidNumber[0], self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)

        # Click on details button
        self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
        time.sleep(2)

        # Check Transceiver Type
        self.assertEqual(transceiverType, self.driver.find_element_by_xpath("(//input[@type='text'])[27]").get_attribute("value"))
        # Check Software Version
        self.assertEqual(softwareVersion, self.driver.find_element_by_xpath("(//input[@type='text'])[28]").get_attribute("value"))
        # Check Satellite Number
        self.assertEqual(satelliteNumber[0], self.driver.find_element_by_name("sattelite_number").get_attribute("value"))
        # Check Antenna Version
        self.assertEqual(antennaVersion, self.driver.find_element_by_xpath("(//input[@type='text'])[29]").get_attribute("value"))
        # Check DNID Number
        self.assertEqual(dnidNumber[0], self.driver.find_element_by_name("dnid").get_attribute("value"))
        # Check Member Number
        self.assertEqual(memberIdnumber, self.driver.find_element_by_name("memberId").get_attribute("value"))
        # Check Installed by Name
        self.assertEqual(installedByName, self.driver.find_element_by_xpath("(//input[@type='text'])[37]").get_attribute("value"))

        # Leave new asset view
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[1]/div[2]/div/div[3]/i").\
            click()

        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)

    def test_06_link_asset_and_mobile_terminal(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Enter Serial Number in field
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/div/form/div/div/div/div[1]/div[2]/div[2]/input"). \
            send_keys(serialNoValue[0])
        # Click in search button
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/div/form/div/div/div/div[2]/div[2]/div[1]/button"). \
            click()
        time.sleep(5)

        # Click on details button
        self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
        time.sleep(2)
        # Click on Link Asset
        self.driver.find_element_by_id("assignVesselLink").click()
        time.sleep(2)
        # Enter Asset Name and clicks on the search button
        self.driver.find_element_by_xpath("(//input[@type='text'])[25]").send_keys(vesselName[0])
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)
        # Click on connect button
        self.driver.find_element_by_css_selector("td.textAlignRight > button.btn.btn-primary").click()
        # Click on Link button
        time.sleep(2)
        self.driver.find_element_by_xpath("(//button[@type='button'])[13]").click()
        # Enter Reason comment
        self.driver.find_element_by_name("comment").send_keys("Need to connect this mobile terminal with this asset.")
        time.sleep(2)
        # Click on Link button 2
        self.driver.find_element_by_xpath("(//button[@type='button'])[66]").click()
        time.sleep(2)
        # Close page
        self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/i").click()
        time.sleep(1)
        # Shutdown browser
        shutdown_browser(self)

    def test_07_generate_and_verify_manual_position(self):
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
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys("F1001")
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(10)

        # Enter IRCS for newly created position
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.driver.find_element_by_xpath("//input[@type='text']").clear()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
        # Click on search button
        self.driver.find_element_by_link_text("Custom").click()
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(5)

        # Verifies position data
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td.ng-binding").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(earlierPositionTimeValueString, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[6]").text)
        self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[7]").text)
        self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[8]").text)
        self.assertEqual("%.2f" % reportedSpeedValue + " kts", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[10]").text)
        self.assertEqual(str(reportedCourseValue) + u"°", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[12]").text)
        self.assertEqual(SourceValue[1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[14]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    def test_08_generate_NAF_and_verify_position(self):
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
        nafSource = nafSource + str(reportedSpeedValue * 10)
        nafSource = nafSource + "//CO/"
        nafSource = nafSource + str(reportedCourseValue)
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
        time.sleep(2)

        # Enter IRCS for newly created position
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.driver.find_element_by_xpath("//input[@type='text']").clear()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
        # Click on search button
        self.driver.find_element_by_link_text("Custom").click()
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(5)

        # Enter Vessel to verify position data
        self.assertEqual(countryValue, self.driver.find_element_by_css_selector("td.ng-binding").text)
        self.assertEqual(externalMarkingValue, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[3]").text)
        self.assertEqual(ircsValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        self.assertEqual(earlierPositionDateTimeValueString, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[6]").text)
        self.assertEqual(lolaPositionValues[0][0][0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[7]").text)
        self.assertEqual(lolaPositionValues[0][0][1], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[8]").text)
        self.assertEqual("%.2f" % reportedSpeedValue + " kts", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[10]").text)
        self.assertEqual(str(reportedCourseValue) + u"°", self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[12]").text)
        self.assertEqual(SourceValue[0], self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[14]").text)
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)

    def test_09_create_second_new_asset(self):
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
        self.driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        self.driver.find_element_by_link_text(countryValue).click()
        # Enter IRCS value
        self.driver.find_element_by_name("ircs").send_keys(ircsValue[1])
        # Enter Name value
        self.driver.find_element_by_name("name").send_keys(vesselName[1])
        # Enter External Marking Value
        self.driver.find_element_by_name("externalMarking").send_keys(externalMarkingValue)
        # Enter CFR Value
        self.driver.find_element_by_name("cfr").send_keys(cfrValue[1])
        # Enter IMO Value
        self.driver.find_element_by_name("imo").send_keys(imoValue[1])
        # Enter HomePort Value
        self.driver.find_element_by_name("homeport").send_keys(homeportValue)
        # Select Gear Type value
        self.driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        self.driver.find_element_by_link_text("Dermersal").click()
        # Enter MMSI Value
        self.driver.find_element_by_name("mmsi").send_keys(mmsiValue[1])
        # Select License Type value
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
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
        self.driver.find_element_by_name("producercode").send_keys("123")
        # Main Contact Name Value
        self.driver.find_element_by_name("contactName").send_keys("Mikael Great")
        # Main E-mail Value
        self.driver.find_element_by_name("email").send_keys("mikael.glemne@havochvatten.se")
        # Main Contact Number Value
        self.driver.find_element_by_name("contactNumber").send_keys("+46720456789")
        # Note comments
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/form/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/textarea"). \
            send_keys("This is some notes!")
        # Click on Save Asset button
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/form/div[1]/div[1]/div[2]/div/div[3]/button[2]"). \
            click()
        # Leave new asset view
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/form/div[1]/div[1]/div[2]/div/div[4]/i"). \
            click()
        time.sleep(3)
        # Shutdown browser
        shutdown_browser(self)

    def test_10_check_new_asset_exists(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        # Search for the new created asset in the asset list
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-assets").click()
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[1]/form/div/div/div/div[1]/div/div/div/div[1]/input"). \
            send_keys(vesselName[1])
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[1]/form/div/div/div/div[1]/div/div/div/div[3]/div/div/button").click()
        time.sleep(5)
        # Check that the new asset exists in the list.
        self.assertEqual(vesselName[1], self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        time.sleep(1)
        # Click on details button for new asset
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/span/table/tbody/tr/td[10]/button/i").click()
        time.sleep(5)
        # Check that the F.S value is correct.
        self.assertEqual(countryValue, self.driver.find_element_by_xpath("(//button[@type='button'])[4]").text)
        # Check that the IRCS value is correct
        self.assertEqual(ircsValue[1], self.driver.find_element_by_name("ircs").get_attribute("value"))
        # Check that the Name value is correct
        self.assertEqual(vesselName[1], self.driver.find_element_by_name("name").get_attribute("value"))
        # Check that External Marking Value is correct
        self.assertEqual("EXT3", self.driver.find_element_by_name("externalMarking").get_attribute("value"))
        # Check that the CFR value is correct
        self.assertEqual(cfrValue[1], self.driver.find_element_by_name("cfr").get_attribute("value"))
        # Check that the IMO value is correct
        self.assertEqual(imoValue[1], self.driver.find_element_by_name("imo").get_attribute("value"))
        # Check that the HomePort value is correct
        self.assertEqual("GOT", self.driver.find_element_by_name("homeport").get_attribute("value"))
        # Check that the Gear Type value is correct.
        self.assertEqual("Dermersal", self.driver.find_element_by_xpath(
            "(//button[@type='button'])[5]").text)
        # Check that the MMSI value is correct
        self.assertEqual(mmsiValue[1], self.driver.find_element_by_name("mmsi").get_attribute("value"))
        # Check that the License Type value is correct.
        self.assertEqual("MOCK-license-DB", self.driver.find_element_by_xpath(
            "(//button[@type='button'])[6]").text)
        # Check that the Length Type value is correct.
        self.assertEqual("14", self.driver.find_element_by_name("lengthValue").get_attribute("value"))
        # Check that the Gross Tonnage value is correct.
        self.assertEqual("3", self.driver.find_element_by_name("grossTonnage").get_attribute("value"))
        # Check that the Power value is correct.
        self.assertEqual("1300", self.driver.find_element_by_name("power").get_attribute("value"))
        # Check that the Producer Name value is correct.
        self.assertEqual("Mikael", self.driver.find_element_by_name("producername").get_attribute("value"))
        # Check that the Producer Code value is correct.
        self.assertEqual("123", self.driver.find_element_by_name("producercode").get_attribute("value"))
        # Check that the Contact Name value is correct.
        self.assertEqual("Mikael Great", self.driver.find_element_by_name("contactName").get_attribute("value"))
        # Check that the E-mail value is correct.
        self.assertEqual("mikael.glemne@havochvatten.se", self.driver.find_element_by_name(
            "email").get_attribute("value"))
        # Check that the E-mail value is correct.
        self.assertEqual("+46720456789", self.driver.find_element_by_name("contactNumber").get_attribute("value"))
        # Check that the Note comments value is correct.
        self.assertEqual("This is some notes!", self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div/form/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/textarea"). \
                         get_attribute("value"))
        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    def test_11_create_second_new_mobile_terminal(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Click on new terminal button
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[2]/div/div/div/div/div[2]/button").\
            click()
        time.sleep(3)
        # Select Transponder system
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//button[@type='button'])[21]"))) # Waits until element exists
        element.click()
        self.driver.find_element_by_link_text("Inmarsat-C : twostage").click()
        time.sleep(1)
        # Enter serial number
        self.driver.find_element_by_name("serialNumber").send_keys(serialNoValue[1])
        # Enter Transceiver type
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[2]/div/form/fieldset/div[2]/div/div[1]/div[2]/input").\
            send_keys(transceiverType)
        # Enter Software Version
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[2]/div/form/fieldset/div[2]/div/div[1]/div[3]/input").\
            send_keys(softwareVersion)
        # Enter Antenna
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[2]/div/form/fieldset/div[2]/div/div[1]/div[4]/input").\
            send_keys(antennaVersion)
        # Enter Satellite Number
        self.driver.find_element_by_name("sattelite_number").send_keys(satelliteNumber[1])
        # Enter DNID Number
        self.driver.find_element_by_name("dnid").send_keys(dnidNumber[1])
        # Enter Member Number
        self.driver.find_element_by_name("memberId").send_keys(memberIdnumber)
        # Enter Installed by
        self.driver.find_element_by_xpath("(//input[@type='text'])[37]").send_keys(installedByName)
        # Expected frequency
        self.driver.find_element_by_xpath("(//input[@type='number'])[2]").send_keys(expectedFrequencyHours)
        # Grace period
        self.driver.find_element_by_xpath("(//input[@type='number'])[4]").send_keys(gracePeriodFrequencyHours)
        # In port
        self.driver.find_element_by_xpath("(//input[@type='number'])[6]").send_keys(inPortFrequencyHours)
        # Click on save button
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[1]/div[2]/div/div[2]/button[1]").\
            click()
        time.sleep(5)
        # Leave new asset view
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[1]/div[2]/div/div[3]/i").\
            click()
        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)

    def test_12_check_second_new_mobile_terminal_exists(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Enter Serial Number in field
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/div/form/div/div/div/div[1]/div[2]/div[2]/input"). \
            send_keys(serialNoValue[1])
        # Click in search button
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/div/form/div/div/div/div[2]/div[2]/div[1]/button"). \
            click()
        time.sleep(5)
        # Check Serial Number in the list
        self.assertEqual(serialNoValue[1], self.driver.find_element_by_css_selector("td.statusColored.ng-binding").text)
        # Check Member Number in the list
        self.assertEqual(memberIdnumber, self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[4]").text)
        # Check DNID Number in the list
        self.assertEqual(dnidNumber[1], self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[5]").text)

        # Click on details button
        self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
        time.sleep(2)

        # Check Transceiver Type
        self.assertEqual(transceiverType, self.driver.find_element_by_xpath("(//input[@type='text'])[27]").get_attribute("value"))
        # Check Software Version
        self.assertEqual(softwareVersion, self.driver.find_element_by_xpath("(//input[@type='text'])[28]").get_attribute("value"))
        # Check Satellite Number
        self.assertEqual(satelliteNumber[1], self.driver.find_element_by_name("sattelite_number").get_attribute("value"))
        # Check Antenna Version
        self.assertEqual(antennaVersion, self.driver.find_element_by_xpath("(//input[@type='text'])[29]").get_attribute("value"))
        # Check DNID Number
        self.assertEqual(dnidNumber[1], self.driver.find_element_by_name("dnid").get_attribute("value"))
        # Check Member Number
        self.assertEqual(memberIdnumber, self.driver.find_element_by_name("memberId").get_attribute("value"))
        # Check Installed by Name
        self.assertEqual(installedByName, self.driver.find_element_by_xpath("(//input[@type='text'])[37]").get_attribute("value"))

        # Leave new asset view
        self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[4]/div[1]/div[2]/div/div[3]/i").\
            click()

        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)


    def test_13_unlink_asset_and_mobile_terminal(self):
        # Startup browser and login
        startup_browser_and_login_to_unionVMS(self)
        time.sleep(5)
        # Select Mobile Terminal tab
        self.driver.find_element_by_id("uvms-header-menu-item-communication").click()
        time.sleep(2)
        # Enter Serial Number in field
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/div/form/div/div/div/div[1]/div[2]/div[2]/input"). \
            send_keys(serialNoValue[0])
        # Click in search button
        self.driver.find_element_by_xpath(
            "//*[@id='content']/div[1]/div[3]/div[2]/div/div/div/div/div[1]/div/div/form/div/div/div/div[2]/div[2]/div[1]/button"). \
            click()
        time.sleep(5)
        # Click on details button
        self.driver.find_element_by_xpath(
            "//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[3]/div/div/div/div/span/table/tbody/tr/td[10]/button").click()
        time.sleep(2)
        # Click on unlinking button
        self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div/button").click()
        time.sleep(1)

        # Enter comment and click on unlinking button
        self.driver.find_element_by_name("comment").send_keys("Unlink Asset and MT.")
        self.driver.find_element_by_xpath("(//button[@type='button'])[65]").click()

        time.sleep(2)
        # Shutdown browser
        shutdown_browser(self)


    def test_14_generate_manual_position_with_no_connected_responder_and_verify_holding_table(self):
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
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys("F1001")
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(10)

        # Enter IRCS for newly created position
        self.driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        self.driver.find_element_by_xpath("//input[@type='text']").clear()
        self.driver.find_element_by_xpath("//input[@type='text']").send_keys(ircsValue[0])
        # Click on search button
        self.driver.find_element_by_link_text("Custom").click()
        self.driver.find_element_by_xpath("(//button[@type='submit'])[2]").click()
        time.sleep(5)

        # Verifies that time stamp for the generated position does not exist
        self.assertNotEqual(earlierPositionTimeValueString, self.driver.find_element_by_xpath("//div[@id='content']/div/div[3]/div[2]/div/div[2]/div/div[4]/div/div/div/div/span/table/tbody/tr/td[6]").text)
        time.sleep(2)

        # Select Alarms tab (Holding Table)
        self.driver.find_element_by_id("uvms-header-menu-item-holding-table").click()
        time.sleep(2)

        # Select filter "Transponder not found"
        self.driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        self.driver.find_element_by_link_text("Transponder not found").click()
        time.sleep(2)






        time.sleep(5)
        # Shutdown browser
        shutdown_browser(self)


    def test_special(self):
        a = datetime.datetime.utcnow()
        b = a - datetime.timedelta(hours=3)
        print(datetime.datetime.strftime(a, '%Y-%m-%d %H:%M:%S'))
        print(datetime.datetime.strftime(b, '%Y-%m-%d %H:%M:%S'))

        a = 13.9412
        b = "%.2f" % a
        print(b)
        print("%.2f" % reportedSpeedValue + " kts")
        print(u"180°")
        print(str(reportedCourseValue) + u"°")
        if (str(reportedCourseValue) + u"°" == "180°"):
            print("YES!!!!")
        else:
            print("NO!")

        print(lolaPositionValues[1][1][0])


if __name__ == '__main__':
    unittest.main()
#unittest.main()