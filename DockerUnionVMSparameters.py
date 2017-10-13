# UnionVMSparameters.py:

# Globals
# Assets
countryValue = 'SWE'
ircsValue = ["F1001", "F1002", "F1003", "F1004", "F1005", "F1006", "F1007", "F3001", "F4001", "F4002", "F4003", "F4004", "F4005", "F4006", "F4007", "F4008", "F4009", "F4010", "F5010", "F5011", "F5012", "F5013", "F5014", "F5015", "F5016", "F5017", "F5018", "F5019", "F5020", "F5021", "F5022"]
vesselName = ["Fartyg1001", "Fartyg1002", "Fartyg1003", "Fartyg1004", "Fartyg1005", "Fartyg1006", "FartygHAV", "Fartyg3001", "Fartyg4001", "Fartyg4002", "Fartyg4003", "Fartyg4004", "Fartyg4005", "Fartyg4006", "Fartyg4007", "Fartyg4008", "Fartyg4009", "Fartyg4010"]
cfrValue = ["SWE0000F1001", "SWE0000F1002", "SWE0000F1003", "SWE0000F1004", "SWE0000F1005", "SWE0000F1006", "SWE0000F1007", "SWE0000F3001", "SWE0000F4001", "SWE0000F4002", "SWE0000F4003", "SWE0000F4004", "SWE0000F4005", "SWE0000F4006", "SWE0000F4007", "SWE0000F4008", "SWE0000F4009", "SWE0000F4010"]
externalMarkingValue = "EXT3"
imoValue = ["0235554", "0545545", "0878322", "0378734", "0956383", "0293462", "0647354", "4674545", "4564545", "1223232", "3232322", "8792322", "4344432", "5643222", "7878888", "3434232", "7676738", "3232333"]
mmsiValue = ["778883333", "999384323", "767266327", "983982632", "223332567", "656778623", "897792323", "663232565", "455433234", "435456558", "899843455", "788756788", "356343565", "434233456", "666776767", "353464344", "984787453", "435632424"]
licenseTypeValue = "MOCK-license-DB"
homeportValue = "GOT"
gearTypeValue = "Dermersal"
lengthValue = "14"
grossTonnageValue = "3"
powerValue = "1300"
producernameValue ="Mikael"
producercodeValue = ""
contactNameValue = "Mikael Great"
contactEmailValue = "mikael.great@great.com"
contactPhoneNumberValue = "+4672112112"
assetHeadline = ("F. S.", "Ext. marking", "Name", "IRCS", "CFR", "Gear Type", "License type", "Last report")

# Mobile Terminals
serialNoValue = ["M1001", "M1002", "M1003", "M1004", "M1005", "M1006", "M4694", "M3001", "M4001", "M4002", "M4003", "M4004", "M4005", "M4006", "M4007", "M4008", "M4009", "M4010"]
transceiverType = ["Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Sailor 6140M MiniC", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A"]
softwareVersion = "A"
antennaVersion = "A"
satelliteNumber = ["S1001", "S1002", "S1003", "S1004", "S1005", "S1006", "S2321", "S3001", "S4001", "S4002", "S4003", "S4004", "S4005", "S4006", "S4007", "S4008", "S4009", "S4010"]
dnidNumber = ["1001", "1002", "1003", "1004", "1005", "1006", "2323", "3001", "4001", "4002", "4003", "4004", "4005", "4006", "4007", "4008", "4009", "4010"]
memberIdnumber = ["100", "100", "100", "100", "100", "100", "255", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100"]
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

#Jenkins job settings
uvmsCheckoutPath = "/tmp/git-uvms-database-scripts"
testResultPath = 'target/failsafe-reports'
