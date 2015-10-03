""" quick simple csv parser """

import csv


def extract_csv_wiu():

    with open('PTC_IP_WIU.csv', 'r') as csvfile:

        reader = csv.DictReader(csvfile)
        dicto = {}
        somelist = []
        for row in reader:

            location = row['Location']
            wiu_name = row['WIU Name']
            wiu_address = row['WIU Address']

            if wiu_address and wiu_name is not '':
                somelist.append({'location': location, 'wiu_name': wiu_name, 'wiu_address':wiu_address})

        print somelist
        csvfile.close()

extract_csv_wiu()
