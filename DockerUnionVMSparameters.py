# UnionVMSparameters.py:

# Globals
# Assets
countryValue = ['SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'NOR', 'NOR', 'SWE']
ircsValue = ["F1001", "F1002", "F1003", "F1004", "F1005", "F1006", "F1007", "F3001", "F4001", "F4002", "F4003", "F4004", "F4005", "F4006", "F4007", "F4008", "F4009", "F4010", "F5001", "F5002", "F5003", "F6001", "F6002", "F6003", "F6004", "F6005", "F6006", "F6007", "F6008", "F6009", "F6010", "F6011", "F6012", "F6013", "F1991", "F2991", "F3991", "F5XXX"]
vesselName = ["Ship1001", "Ship1002", "Ship1003", "Ship1004", "Ship1005", "Ship1006", "ShipHAV", "Ship3001", "Ship4001", "Ship4002", "Ship4003", "Ship4004", "Ship4005", "Ship4006", "Ship4007", "Ship4008", "Ship4009", "Ship4010", "Ship5001", "Ship5002", "Ship5003", "Ship6001", "Ship6002", "Ship6003", "Ship6004", "Ship6005", "Ship6006", "Ship6007", "Ship6008", "Ship6009", "Ship6010", "Ship6011", "Ship6012", "Ship6013", "Ship1991", "Ship2991", "Ship3991", "Ship5XXX"]
cfrValue = ["SWE0000F1001", "SWE0000F1002", "SWE0000F1003", "SWE0000F1004", "SWE0000F1005", "SWE0000F1006", "SWE0000F1007", "SWE0000F3001", "SWE0000F4001", "SWE0000F4002", "SWE0000F4003", "SWE0000F4004", "SWE0000F4005", "SWE0000F4006", "SWE0000F4007", "SWE0000F4008", "SWE0000F4009", "SWE0000F4010", "SWE0000F5001", "SWE0000F5002", "SWE0000F5003", "SWE0000F6001", "SWE0000F6002", "SWE0000F6003", "SWE0000F6004", "SWE0000F6005", "SWE0000F6006", "SWE0000F6007", "SWE0000F6008", "SWE0000F6009", "SWE0000F6010", "SWE0000F6011", "SWE0000F6012", "SWE0000F6013", "SWE0000F1991", "SWE0000F2991", "SWE0000F3991", "SWE00005XXX"]
externalMarkingValue = ["EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT4", "EXT4", "EXT4"]
imoValue = ["1916207", "9618120", "0973312", "3013298", "7061109", "9270601", "1036970", "3819442", "2443125", "4254223", "4233524", "4244235", "5324425", "4522436", "3452274", "2435824", "4945232", "0342552", "5215234", "5243225", "3542523", "0621430", "3262004", "3360024", "4206034", "6304025", "2043066", "2470360", "0324860", "6040239", "0620431", "4210136", "2243016", "2304631", "0261991", "0262991", "0263991", "0265000"]
mmsiValue = ["832233130", "333012932", "043312023", "413223310", "223031243", "302134323", "133243420", "343210352", "411202050", "105004222", "020140523", "124500024", "045500122", "650200214", "024701205", "540100282", "910202450", "201025005", "005512201", "010252052", "205510032", "150060102", "201065002", "136020500", "640200501", "602050510", "601520060", "601000527", "001060528", "901500026", "150012006", "012651100", "011025026", "320601510", "302331991", "302332991", "302333991", "302335000"]
licenseTypeValue = "MOCK-license-DB"
licenseValue = "YES"
homeportValue = ["GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GBG", "GBG", "GOT"]
gearTypeValue = ["Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Dermersal", "Pelagic", "Pelagic", "Pelagic"]
lengthValue = ["14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "14", "15", "15", "15"]
grossTonnageValue = ["3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "2", "2", "2"]
powerValue = ["1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "900", "900", "900"]
producernameValue ="Mikael"
producercodeValue = ""
contactNameValue = ["Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Greater", "Mikael Greatest", "Mikael Greatest"]
contactEmailValue = ["mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great2@great.com", "mikael.great3@great.com", "mikael.great3@great.com"]
contactPhoneNumberValue = ["+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4673443443", "+4673553553", "+4673553553"]
assetHeadline = ("F. S.", "Ext. marking", "Name", "IRCS", "CFR", "Gear Type", "License type", "Last report")
noteUser = ["Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G"]
notesLicenseHolder = ["Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big"]
notesContact = ["Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master" "Mr Master"]
notesSheetNumber = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
commentValue = "some note comment."

# Mobile Terminals
serialNoValue = ["M0101", "2M010", "13M00", "0M014", "1050M", "6M010", "T6EBT4490478", "030M1", "4M100", "2M400", "0403M", "4M004", "M0540", "0604M", "0047M", "8M004", "400M9", "04M01", "5100M", "2050M", "003M5", "ED6T2947F0T6", "497T259D809T", "0E74DE479TDT", "3T349B47TF50", "CTT7499007D3", "9340DT0T9071", "0483A9T739BT", "968FD4T70ETD", "5097T7E2T46E", "T09674F1F2T1", "428T9017ATC5", "54914TTA0927", "907ATB991TF4", "M1991", "M2991", "M3991", "M5000"]
transceiverType = ["Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Sailor 6140M MiniC", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Type A", "Type A", "Type A", "Type A"]
softwareVersion = "A"
antennaVersion = "A"
satelliteNumber = ["0S110", "1S002", "1300S", "S0140", "S0051", "16S00", "910746225", "0103S", "00S14", "24S00", "30S04", "0404S", "054S0", "004S6", "400S7", "4S800", "4009S", "040S1", "0510S", "0025S", "50S03", "661002114", "604263811", "612015664", "026472416", "155541672", "120616148", "654472025", "213456613", "716542196", "251747106", "364614281", "194660127", "170666214", "S1991", "S2991", "S3991", "S5000"]
dnidNumber = ["0101", "2100", "1003", "0041", "5100", "0061", "47051", "1300", "4100", "2400", "0430", "0440", "0540", "6004", "7040", "4080", "0094", "0041", "0051", "0250", "0053", "50417", "01457", "07541", "17540", "40175", "54701", "74501", "50741", "14570", "50471", "51407", "17540", "75401", "1991", "2991", "3991", "5000"]
memberIdnumber = ["100", "100", "100", "100", "100", "100", "255", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "100", "100", "100", "100"]
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
                      [["58.662", "17.129"], ["58.661", "17.137"]],
                      [["58.662", "17.129"], ["58.661", "17.137"]],
                      [["57.554", "11.893"], ["57.554", "11.893"]],
                      [["63.703", "20.621"], ["63.703", "20.621"]],
                      [["63.659", "20.608"], ["63.659", "20.608"]],
                      [["63.624", "20.598"], ["63.624", "20.598"]],
                      [["63.597", "20.602"], ["63.597", "20.602"]],
                      [["63.577", "20.603"], ["63.577", "20.603"]],
                      [["63.553", "20.599"], ["63.553", "20.599"]],
                      [["63.519", "20.553"], ["63.519", "20.553"]],
                      [["63.500", "20.547"], ["63.500", "20.547"]],
                      [["63.449", "20.510"], ["63.449", "20.510"]],
                      [["63.403", "20.457"], ["63.403", "20.457"]]]



# lolaSpeedCourseTripValues [Position Report number x, Asset Number y, lat=0/long=1/speed=2/course=3 z]

lolaSpeedCourseTripValues= [[["57.681", "11.6478", "10", "252"], ["57.951837", "11.556286", "0", "271"], ["59.863", "19.130", "5", "340"]],
                            [["57.626013", "11.356717", "10", "174"], ["57.964829", "11.402715", "5", "346"], ["59.786", "19.140", "5", "197"]],
                            [["57.458007", "11.378829", "10", "150"], ["58.126604", "11.330559", "10", "346"], ["59.712", "19.099", "5", "178"]],
                            [["57.314663", "11.533749", "10", "142"], ["58.287459", "11.242123", "10", "348"], ["59.628", "19.102", "10", "184"]],
                            [["57.181033", "11.724252", "10", "159"], ["58.447167", "11.177056", "10", "347"], ["59.464", "19.077", "10", "178"]],
                            [["57.028407", "11.847069", "10", "147"], ["58.560552", "11.127009", "10", "332"], ["59.300", "19.084", "10", "217"]],
                            [["56.891504", "12.022709", "10", "175"], ["58.706508", "10.979955", "10", "336"], ["59.170", "18.894", "10", "208"]],
                            [["56.725921", "12.050378", "10", "136"], ["58.859826", "10.849251", "10", "31"], ["59.023", "18.741", "10", "237"]],
                            [["56.605656", "12.264073", "10", "112"], ["58.928393", "10.927695", "10", "71"], ["58.933", "18.473", "10", "232"]],
                            [["56.543136", "12.545422", "10", "115"], ["58.923874", "11.088947", "5", "0"], ["58.828", "18.224", "5", "285"]],
                            [["56.472983", "12.819032", "10", "161"], ["58.937", "11.171477", "0", "0"], ["58.850", "18.068", "5", "324"]],
                            [["56.435436", "12.843660", "5", "180"], ["58.937", "11.171477", "0", "0"], ["58.850", "18.068", "5", "324"]]]

# Audit Parameters
auditLogsHeadline = ("Username", "Operation", "Object type", "Date")



# Mixed parameters
reportedSpeedValue = 5
reportedCourseValue = 180

appServerName = "localhost"
dbServerName = "db71u"
hostdbServerName = "localhost"

httpNAFRequestString = "http://" + appServerName + ":28080/naf/rest/message/"
httpUnionVMSurlString = "http://" + appServerName + ":28080/unionvms/"
connectToDatabaseString = "dbname='"+ dbServerName + "' user='postgres' host='" + hostdbServerName + "' password='postgres'" + " port='25432'"
dbURLjdbcString = "-Ddb.url=jdbc:postgresql://" + hostdbServerName + ":25432/" + dbServerName


sourceValue= ('NAF', 'MANUAL')
groupName = ("Grupp 1", "Grupp 2", "Grupp 3")
speedUnitTypesInText = ("knots", "kilometers per hour", "miles per hour")
speedUnitTypesShort = ("kts", "km/h", "mph")
reportedSpeedDefault = [8, 10, 12]
rulesHeadlineNames = ["Rule name", "Last triggered", "Date updated", "Updated by", "Notification", "Notify by email", "Status", "Actions"]

uvmsGitHubPath = 'https://github.com/UnionVMS/'

uvmsCheckoutPath = "/tmp/git-uvms-database"

testResultPathLinux = "/var/lib/jenkins/workspace/UVMS-Docker-dev-test-frontend/release-test/target/failsafe-reports"
testResultPathWindows = 'C:\\test-reports'

targetPathLinux = "/var/lib/jenkins/workspace/UVMS-Docker-dev-test-frontend/release-test/target"
targetPathWindows = "C:\\UVMS-Docker-uvms-docker\\release-test\\target"

downloadPathLinux = "/var/lib/jenkins/Downloads"
downloadPathWindow = "\Downloads"

defaultUserName = "vms_admin_com"
defaultUserNamePassword = "password"

blackColorRGBA = "rgba(51, 51, 51, 1)"
greyColorRGBA = "rgba(153, 153, 153, 1)"
