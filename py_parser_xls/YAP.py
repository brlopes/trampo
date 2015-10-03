""" Yet Another Parser, excel cells to list of dictionaries data structure """
""" extract data from xls, converts coord and creates list of dictionaries """
import openpyxl
import string


def convert_coordinates(cor, vMsg='V2'):
    """This function converts coordinates to decimal format.
    ex: 61:123.123N to 61.22, etc
    """
    if vMsg == 'V0':
        return 'N/A'
    elif cor[-1:] == 'N':
        return str(float(cor[:cor.find(':')]) + float(cor[cor.find(':') + 1:cor.find('N')])/60)
    elif cor[-1:] == 'S':
        return '-' + str(float(cor[:cor.find(':')]) + float(cor[cor.find(':') + 1:cor.find('S')])/60)
    elif cor[-1:] == 'E':
        return str(float(cor[:cor.find(':')]) + float(cor[cor.find(':') + 1:cor.find('E')])/60)
    elif cor[-1:] == 'W':
        return '-' + str(float(cor[:cor.find(':')]) + float(cor[cor.find(':') + 1:cor.find('W')])/60)
    else:
        # logger.error('TRACE: %s', traceback.format_exc())
        raise Exception("Coordinate conversion error")
        return 0


def get_bases():

    wb = openpyxl.load_workbook(filename=':D')
    ws = wb.active

    baseListDict = []

    for row in ws.rows:

        baseName = str(row[0].value)
        baseID = str(row[39].value)

        baseIP = str(row[32].value)

        # if str(row[29].value) != 'None':
        if (str(row[30].value) != 'None' and str(row[30].value) != 'LONG') and '(' in row[0].value:

            coords = [tuple((convert_coordinates(str(row[30].value)[[row[30].value.find(char) for char in row[30].value if char in string.digits][0]:].strip(), 'V1') + ',' + convert_coordinates(str(row[29].value)[[row[29].value.find(char) for char in row[29].value if char in string.digits][0]:].strip(), 'V1')).split(','))]
            baseListDict.append({'name': baseName, 'ID': baseID, 'LAT/LON': coords, 'IP': baseIP})
        # return baseListDict
    print baseListDict


def get_waysides():

    wb = openpyxl.load_workbook(filename=':D')
    ws = wb.get_sheet_by_name('Waysides & WMS')
    waysideListDict = []

    for row in ws.rows:
        # import pdb; pdb.set_trace()
        if(str(row[14].value) != '' and str(row[14].value) != 'None' and str(row[14].value) != 'LONG'):

            fullname = str(row[0].value)
            waysideName = fullname.split()
            ID = waysideName[0]
            name = waysideName[2]

            coords = tuple((convert_coordinates(str(row[14].value)[[row[14].value.find(char) for char in row[14].value if char in string.digits][0]:].strip(), 'V1') + ',' + convert_coordinates(str(row[13].value)[[row[13].value.find(char) for char in row[13].value if char in string.digits][0]:].strip(), 'V1')).split(','))
            waysideListDict.append({'name': name, 'ID': ID, 'LAT/LON': coords})

    print waysideListDict
    # return baseListDict

get_waysides()
