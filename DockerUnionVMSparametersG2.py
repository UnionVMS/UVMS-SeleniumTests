# UnionVMSparameters.py:

# Globals
# Assets
countryValue = ['SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'NOR', 'NOR', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE', 'SWE']
countryValueFull = ['Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Norway', 'Norway', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden', 'Sweden']
ircsValue = ["F1001", "F1002", "F1003", "F1004", "F1005", "F1006", "F1007", "F3001", "F4001", "F4002", "F4003", "F4004", "F4005", "F4006", "F4007", "F4008", "F4009", "F4010", "F5001", "F5002", "F5003", "F6001", "F6002", "F6003", "F6004", "F6005", "F6006", "F6007", "F6008", "F6009", "F6010", "F6011", "F6012", "F6013", "F1991", "F2991", "F3991", "F5XXX", "F6YYY", "F6001", "F6002", "F6003", "F6004", "F6005", "F6006", "F6007", "F6008", "F6009", "F6010", "F6011", "F6012", "F6013", "F6014", "F6001", "F6002", "F6003", "F6004", "F6005", "F6006", "F6007", "F6008", "F6009", "F6010", "F6011", "F6012", "F6013", "F6014"]
vesselName = ["Ship1001", "Ship1002", "Ship1003", "Ship1004", "Ship1005", "Ship1006", "ShipHAV", "Ship3001", "Ship4001", "Ship4002", "Ship4003", "Ship4004", "Ship4005", "Ship4006", "Ship4007", "Ship4008", "Ship4009", "Ship4010", "Ship5001", "Ship5002", "Ship5003", "Ship6001", "Ship6002", "Ship6003", "Ship6004", "Ship6005", "Ship6006", "Ship6007", "Ship6008", "Ship6009", "Ship6010", "Ship6011", "Ship6012", "Ship6013", "Ship1991", "Ship2991", "Ship3991", "Ship5XXX", "Ship6YYY", "Ship6001", "Ship6002", "Ship6003", "Ship6004", "Ship6005", "Ship6006", "Ship6007", "Ship6008", "Ship6009", "Ship6010", "Ship6011", "Ship6012", "Ship6013", "Ship6014", "Ship6001", "Ship6002", "Ship6003", "Ship6004", "Ship6005", "Ship6006", "Ship6007", "Ship6008", "Ship6009", "Ship6010", "Ship6011", "Ship6012", "Ship6013", "Ship6014"]
cfrValue = ["SWE0000F1001", "SWE0000F1002", "SWE0000F1003", "SWE0000F1004", "SWE0000F1005", "SWE0000F1006", "SWE0000F1007", "SWE0000F3001", "SWE0000F4001", "SWE0000F4002", "SWE0000F4003", "SWE0000F4004", "SWE0000F4005", "SWE0000F4006", "SWE0000F4007", "SWE0000F4008", "SWE0000F4009", "SWE0000F4010", "SWE0000F5001", "SWE0000F5002", "SWE0000F5003", "SWE0000F6001", "SWE0000F6002", "SWE0000F6003", "SWE0000F6004", "SWE0000F6005", "SWE0000F6006", "SWE0000F6007", "SWE0000F6008", "SWE0000F6009", "SWE0000F6010", "SWE0000F6011", "SWE0000F6012", "SWE0000F6013", "SWE0000F1991", "SWE0000F2991", "SWE0000F3991", "SWE0000F5XXX", "SWE0000F6YYY", "SWE0000F6001", "SWE0000F6002", "SWE0000F6003", "SWE0000F6004", "SWE0000F6005", "SWE0000F6006", "SWE0000F6007", "SWE0000F6008", "SWE0000F6009", "SWE0000F6010", "SWE0000F6011", "SWE0000F6012", "SWE0000F6013", "SWE0000F6014", "SWE0000F6001", "SWE0000F6002", "SWE0000F6003", "SWE0000F6004", "SWE0000F6005", "SWE0000F6006", "SWE0000F6007", "SWE0000F6008", "SWE0000F6009", "SWE0000F6010", "SWE0000F6011", "SWE0000F6012", "SWE0000F6013", "SWE0000F6014"]
externalMarkingValue = ["EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT4", "EXT4", "EXT4", "EXT4", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3", "EXT3"]
externalMarkingSearchValue = ["GG"]
imoValue = ["1916207", "9618120", "0973312", "3013298", "7061109", "9270601", "1036970", "3819442", "2443125", "4254223", "4233524", "4244235", "5324425", "4522436", "3452274", "2435824", "4945232", "0342552", "5215234", "5243225", "3542523", "0621430", "3262004", "3360024", "4206034", "6304025", "2043066", "2470360", "0324860", "6040239", "0620431", "4210136", "2243016", "2304631", "0261991", "0262991", "0263991", "0265000", "0266000", "0621430", "3262004", "3360024", "4206034", "6304025", "2043066", "2470360", "0324860", "6040239", "0620431", "4210136", "2243016", "2304631", "2304632", "0621430", "3262004", "3360024", "4206034", "6304025", "2043066", "2470360", "0324860", "6040239", "0620431", "4210136", "2243016", "2304631", "2304632"]
mmsiValue = ["832233130", "333012932", "043312023", "413223310", "223031243", "302134323", "133243420", "343210352", "411202050", "105004222", "020140523", "124500024", "045500122", "650200214", "024701205", "540100282", "910202450", "201025005", "005512201", "010252052", "205510032", "150060102", "201065002", "136020500", "640200501", "602050510", "601520060", "601000527", "001060528", "901500026", "150012006", "012651100", "011025026", "320601510", "302331991", "302332991", "302333991", "302335000", "302336000", "150060102", "201065002", "136020500", "640200501", "602050510", "601520060", "601000527", "001060528", "901500026", "150012006", "012651100", "011025026", "320601510", "320601511", "150060102", "201065002", "136020500", "640200501", "602050510", "601520060", "601000527", "001060528", "901500026", "150012006", "012651100", "011025026", "320601510", "320601511"]
licenseTypeValue = "MOCK-license-DB"
licenseValue = "YES"
homeportValue = ["GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GBG", "GBG", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT", "GOT"]
homeportSearchValue = ["SET"]
gearTypeValue = ["Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Pelagic", "Pelagic", "Pelagic", "Pelagic", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal", "Demersal"]
lengthOverAllValue = ["14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "15.00", "15.00", "15.00", "15.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00", "14.00"]
lengthBetweenPerpendicularsValue = ["20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "25.00", "25.00", "25.00", "25.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00", "20.00"]
grossTonnageValue = ["3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "2", "2", "2", "2", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3", "3"]
grossTonnageTypeValue = ["LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "OSLO", "OSLO", "OSLO", "OSLO", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON", "LONDON"]
powerValue = ["1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "900", "900", "900", "900", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300", "1300"]
productOrgNameValue = ["Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "2", "2", "2", "2", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas", "Kalle Snodas"]
productOrgCodeValue = ["9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "2", "2", "2", "2", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111", "9600001111"]
contactNameValue = ["Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Greater", "Mikael Greatest", "Mikael Greatest", "Mikael Greatest", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great", "Mikael Great"]
contactTypeValue = ["Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "+Organization2", "+Organization3", "+Organization4", "+Organization5", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization", "Organization"]
contactEmailValue = ["mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great2@great.com", "mikael.great3@great.com", "mikael.great3@great.com", "mikael.great3@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com", "mikael.great@great.com"]
contactPhoneNumberValue = ["+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4673443443", "+4673553553", "+4673553553", "+4673553553", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112", "+4672112112"]
contactCountryValue = ["SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "NOR", "NOR", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE", "SWE"]
contactCityValue = ["Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Awaytown", "Awaytown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown", "Hometown"]
contactStreetValue = ["Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Old Street 456", "Old Street 456", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123", "Best Street 123"]
contactZipCodeValue = ["12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "54321", "54321", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345", "12345"]

assetHeadline = ("F. S.", "Ext. marking", "Name", "IRCS", "CFR", "Gear Type", "License type", "Last report")
noteUser = ["Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G", "Mike G"]
notesLicenseHolder = ["Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big", "Greg Big"]
notesContact = ["Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master", "Mr Master"]
notesSheetNumber = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
commentValue = "some note comment."
flagStateIndex = ["DNK", "NOR", "SWE"]
gearTypeIndex = ["Demersal", "Demersal and pelagic", "Pelagic", "Unknown"]
assetFileName = 'assets.csv'
assetFileNameListOLD = ["asset1.csv", "asset2.csv", "asset3.csv", "asset4.csv", "asset5.csv", "asset6.csv", "asset7.csv", "asset8.csv", "asset9.csv", "assetreal1.csv", "assetreal2.csv", "assetreal3.csv", "assetreal4.csv", "assetreal5.csv", "assetreal6.csv", "assetreal7.csv", "assetreal8.csv"]
assetFileNameList = ["asset1G2.csv", "asset2G2.csv", "asset3G2.csv", "asset4G2.csv", "asset5G2.csv", "asset6G2.csv", "asset7G2.csv", "asset8G2.csv", "asset9G2.csv", "assetreal1G2.csv", "assetreal2G2.csv", "assetreal3G2.csv", "assetreal4G2.csv", "assetreal5G2.csv", "assetreal6G2.csv", "assetreal7G2.csv", "assetreal8G2.csv"]

# Mobile Terminals
serialNoValue = ["M0101", "2M010", "13M00", "0M014", "1050M", "6M010", "T6EBT4490478", "030M1", "4M100", "2M400", "0403M", "4M004", "M0540", "0604M", "0047M", "8M004", "400M9", "04M01", "5100M", "2050M", "003M5", "ED6T2947F0T6", "497T259D809T", "0E74DE479TDT", "3T349B47TF50", "CTT7499007D3", "9340DT0T9071", "0483A9T739BT", "968FD4T70ETD", "5097T7E2T46E", "T09674F1F2T1", "428T9017ATC5", "54914TTA0927", "907ATB991TF4", "M1991", "M2991", "M3991", "M5000", "M6000", "ED6T2947F0T6", "497T259D809T", "0E74DE479TDT", "3T349B47TF50", "CTT7499007D3", "9340DT0T9071", "0483A9T739BT", "968FD4T70ETD", "5097T7E2T46E", "T09674F1F2T1", "428T9017ATC5", "54914TTA0927", "907ATB991TF4", "907ATB991TF5", "ED6T2947F0T6", "497T259D809T", "0E74DE479TDT", "3T349B47TF50", "CTT7499007D3", "9340DT0T9071", "0483A9T739BT", "968FD4T70ETD", "5097T7E2T46E", "T09674F1F2T1", "428T9017ATC5", "54914TTA0927", "907ATB991TF4", "907ATB991TF5"]
transceiverType = ["Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Sailor 6140M MiniC", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Type A", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Type A", "Type A", "Type A", "Type A", "Type A", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC", "Sailor 6140M MiniC"]
softwareVersion = "A"
antennaVersion = "A"
satelliteNumber = ["1001", "1002", "1300", "1400", "5100", "1600", "910746225", "1031", "1400", "2400", "3004", "4040", "54000", "4600", "4007", "4S800", "4009", "4010", "5100", "2500", "5003", "661002114", "604263811", "612015664", "26472416", "155541672", "120616148", "654472025", "213456613", "716542196", "251747106", "364614281", "194660127", "170666214", "1991", "2991", "3991", "5000", "6000", "661002114", "604263811", "612015664", "026472416", "155541672", "120616148", "654472025", "213456613", "716542196", "251747106", "364614281", "194660127", "170666214", "170666215", "661002114", "604263811", "612015664", "226472416", "155541672", "120616148", "654472025", "213456613", "716542196", "251747106", "364614281", "194660127", "170666214", "170666215"]
dnidNumber = ["10101", "12100", "10003", "10041", "51000", "10061", "47051", "13000", "41000", "24000", "10430", "10440", "10540", "16004", "17040", "14080", "10094", "10041", "10051", "10250", "10053", "50417", "10457", "17541", "17540", "40175", "54701", "74501", "50741", "14570", "50471", "51407", "17540", "75401", "19991", "29991", "39991", "50000", "60000", "50417", "10457", "17541", "17540", "40175", "54701", "74501", "50741", "14570", "50471", "51407", "27540", "75401", "75402", "50417", "11457", "17541", "17540", "40175", "54701", "74501", "50741", "14570", "50471", "51407", "17540", "75401", "75402"]
memberIdnumber = ["100", "100", "100", "100", "100", "100", "255", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "100", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "100", "100", "100", "100", "100", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
activeState = ["1", "1", "0", "0", "0", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "0", "0", "0", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
landStation = ["EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK", "EIK"]
channelName = ["VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS", "VMS"]
installedByName = "Mike Great"
expectedFrequencyHours = "0"
expectedFrequencyMinutes = "2"
gracePeriodFrequencyHours = "0"
gracePeriodFrequencyMinutes = "15"
inPortFrequencyHours = "0"
inPortFrequencyMinutes = "3"
deltaTimeValue = 4
deltaTimeBigValue = 48
transponderType = ("Iridium", "Inmarsat-C")
mobileTerminalHeadline = ("Linked asset", "Serial no.", "Member no.", "DNID", "Transponder type", "Satellite no.", "MMSI no.", "Status")
mobileTerminalFileName = 'mobileTerminals.csv'
mobileTerminalFileNameList = ["mobileterminal1G2.csv", "mobileterminal2G2.csv", "mobileterminal3G2.csv", "mobileterminal4G2.csv", "mobileterminal5G2.csv", "mobileterminal6G2.csv", "mobileterminal7G2.csv", "mobileterminal8G2.csv", "mobileterminal9G2.csv", "mobileterminalreal1G2.csv", "mobileterminalreal2G2.csv", "mobileterminalreal3G2.csv", "mobileterminalreal4G2.csv", "mobileterminalreal5G2.csv", "mobileterminalreal6G2.csv", "mobileterminalreal7G2.csv", "mobileterminalreal8G2.csv"]
mobileTerminalSearchValue = ["*AA*","*5*","*1000*"]
statusValue = ("Inactive", "Active")
channelDefaultName = "VMS"
pollConfigDefaultValue = ["1", "1", "1"]
pollConfigDefaultChangeValue = ["1", "1", "0"]

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


# lolaPositionAreaValues [lola position route y, lat=0/lon=1 z]
lolaPositionAreaValues = [["58.031", "14.441"],
                          ["58.032", "14.432"],
                          ["58.035", "14.386"],
                          ["58.033", "14.368"],
                          ["58.033", "14.355"]]


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

# Trip Parameters
tripFileNameList = ["trip1.csv", "trip2.csv", "trip3.csv", "trip4.csv", "trip5.csv", "trip6.csv", "trip7.csv", "trip8.csv", "trip9.csv", "tripreal1.csv", "tripreal2.csv", "tripreal3.csv", "tripreal4.csv", "tripreal5.csv", "tripreal6.csv", "tripreal7.csv", "tripreal8.csv"]

# Movement Parameters
movementHeadline = ("F.S", "Ext. marking", "IRCS", "Name", "Time", "Lat.", "Long.", "Status", "MS", "CS", "Course", "Msg. Type", "Source")
movementFileName = 'movements.csv'


# Audit Parameters
auditLogsHeadline = ("Username", "Operation", "Object type", "Date")
auditLogsFileName = 'auditLogs.csv'
auditLogsOperationValue = ("Update", "Create", "Linked", "Archive")
auditLogsObjectTypeValue = ("Setting", "Alarm", "Asset", "Mobile Terminal", "Manual position report", "Temporary position report", "Automatic position report", "Asset Group", "Poll")
auditLogsObjectAffectedValue = ("defaultHomePage", "coordinateFormat", "See object", "dateTimeFormat")

# Area Management Parameters
userAreaFileName = "area1.csv"
userAreaName = "Area1"
userAreaTypeName = "AREATYPE1"

# Rule Parameters
userAreaRuleNamne = "Area 1 Triggered"

# Map Export Parameters
mapTitle = "Map Title"
mapSubTitle = "Map sub Title"
mapDescription = "Map Description"
mapPrefixFileName = "unionvms"
mapSuffixFileName = ".pdf"

# Mixed parameters
startDateTimeDefault = "1970-01-01 00:00:00"
stopDateTimeDefault = "2070-01-01 00:00:00"

# Realtime Map Parameters
capTracksMinValue = 20000

# Mixed parameters
reportedSpeedValue = 5
reportedCourseValue = 180

linkTextValue = "Custom"
WebDriverWaitTimeValue = 30

appServerName = "localhost"
dbServerName = "db71u"
hostdbServerName = "localhost"

# appServerName = "liaswf05p"
# dbServerName = "db71p"
# hostdbServerName = "livmdb71p"

# appServerName = "liaswf05t"
# dbServerName = "db71t"
# hostdbServerName = "livmdb71t"

# appServerName = "liaswf05u"
# dbServerName = "unionvmsdev"
# hostdbServerName = "livmdb71u"

# appServerName = "localhost"
# dbServerName = "db71u"
# hostdbServerName = "localhost"

httpNationalServiceEndpointString = 'http://osbutv.havochvatten.se:8011/esb/Vessel/v2?wsdl'
httpNAFRequestString = "http://" + appServerName + ":28080/naf/rest/message/"
httpUnionVMSurlString = "http://" + appServerName + ":28080/unionvms/"
httpRealMapUrlString = "http://" + appServerName + ":28080/"
httpUSMUrlString = "http://" + appServerName + ":28080/unionvms/usm-administration/rest/authenticate"
httpUrlRestAssetString = "http://" + appServerName + ":28080/unionvms/asset/rest/asset"
httpHavProxyString = "http://" + appServerName + ":28080/unionvms/hav-vessel-proxy-cache/rest/vessel"
connectToDatabaseString = "dbname='"+ dbServerName + "' user='postgres' host='" + hostdbServerName + "' password='postgres'"
if hostdbServerName == "localhost":
    connectToDatabaseString = "dbname='"+ dbServerName + "' user='postgres' host='" + hostdbServerName + "' password='postgres'" + " port='25432'"

dbURLjdbcString = "-Ddb.url=jdbc:postgresql://" + hostdbServerName + ":5432/" + dbServerName
if hostdbServerName == "localhost":
    dbURLjdbcString = "-Ddb.url=jdbc:postgresql://" + hostdbServerName + ":25432/" + dbServerName



sourceValue= ('NAF', 'MANUAL')
groupName = ("Group 1", "Group 2", "Group 3", "Group 4", "Group 5", "Group 6")
speedUnitTypesInText = ("knots", "kilometers per hour", "miles per hour")
speedUnitTypesShort = ("kts", "km/h", "mph")
reportedSpeedDefault = [8, 10, 12]
lengthInterval = ("0-11,99", "12-14,99", "15-17,99", "18-23,99", "24+")
rulesHeadlineNames = ["Rule name", "Last triggered", "Date updated", "Updated by", "Notification", "Notify by email", "Status", "Actions"]

uvmsGitHubPath = 'https://github.com/UnionVMS/'

uvmsCheckoutPath = "/tmp/git-uvms-database"

testResultPathLinux = "/var/lib/jenkins/workspace/UVMS-Docker-frontend-test/unionvms-test/target/failsafe-reports"

testResultPathWindows = 'C:\\test-reports'

targetPathLinux = "/var/lib/jenkins/workspace/UVMS-Docker-frontend-test/unionvms-test/target"

targetPathWindows = "C:\\UVMS-Docker-uvms-docker\\unionvms-test\\target"

#downloadPathLinux = "/var/lib/jenkins/Downloads"
downloadPathLinux = "/var/lib/jenkins/workspace/UVMS-Docker-frontend-test/unionvms-test/target"

downloadPathWindow = "\Downloads"

referenceDateTimeFileName = ('referenceDateTime1.csv', 'referenceDateTime2.csv', 'referenceDateTime3.csv')

tests200FileName = ['assets2xxxxG2.csv', 'mobileterminals2xxxxG2.csv', 'linkassetmobileterminals2xxxxG2.csv']
tests300FileName = ['assets3xxxxG2.csv', 'mobileterminals3xxxxG2.csv', 'linkassetmobileterminals3xxxxG2.csv', 'channelstomobileterminals3xxxxG2.csv', 'channelstomobileterminals3bxxxG2.csv']
tests900FileName = ['assetsALLxxG2.csv', 'mobileterminalsALLxxG2.csv', 'linkassetmobileterminalsALLxxG2.csv', 'channelstomobileterminalsALLxxG2.csv', 'channelstomobileterminalALLxxxG2.csv']

defaultSystemName = "UVMS"
defaultNAFName = "NAF"
defaultUserName = "vms_admin_se"
defaultUserNamePassword = "password"
defaultContext = "AdminAllUVMS"

# defaultUserName = "vms_admin_com"
# defaultUserNamePassword = "password"
# defaultContext = "AdminAll"

# defaultUserName = "vms_admin_se"
# defaultUserNamePassword = "password"
# defaultContext = "AdminAllUVMS"

blackColorRGBA = "rgba(51, 51, 51, 1)"
greyColorRGBA = "rgba(153, 153, 153, 1)"

defaultSleepTimeValue = 0.2