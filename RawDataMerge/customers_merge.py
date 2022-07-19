import csv
from _datetime import datetime
from JenkinsParams import params
import os
import shutil

jo = params
DATE = datetime.now()
DATE.strftime("%m-%d-%Y-%H-%M-%S")

# cust_folder = "/Users/cb-kamal/Documents/MigrationQAFramework/QA_Framework_New/TestData/RawData/Customers/"



def customers_merge(client_name, unzipped_folder, validationType, Merge_Results_Path):
    results_path = Merge_Results_Path+ "/" + client_name
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    if validationType == 'DS1' and (not os.path.exists(results_path+ "/" + 'DS1')):
        os.mkdir(results_path+ "/" + 'DS1')
    elif validationType == 'DS3' and (not os.path.exists(results_path+ "/" + 'DS3')):
        os.mkdir(results_path + "/" + 'DS3')

    output_file = results_path + "/" + validationType + "/"+ validationType+"_Customers" +str(DATE) + ".csv"
    customers = unzipped_folder +"/" + 'Customers.csv'

    with open(customers, 'r') as cust:
        reader = csv.reader(cust)
        headers = next(reader)
        final_header = [value.strip().replace(' ', '_') for value in headers]
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(final_header)
            for row in reader:
                writer.writerow(row)
    print("Removed spaces in column names and file is ready..")
