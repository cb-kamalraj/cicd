import os

# Class1
import shutil
from customers_merge import customers_merge


def jenkins_read():

        ClientName = os.getenv("ClientName")
        DS1_zip_files = os.getenv("DS1_zip_Files")
        DS3_zip_files = os.getenv("DS3_zip_Files")
        Merge_Results_Path = os.getenv("Merge_Results_Path")

        # DS1_zip_files = os.getenv("DS1_zip_Files")
        # DS3_zip_files = '/Users/cb-kamal/Downloads/customers_ganesh-test_19_Jul_2022_15_07_13.zip,'
        # Merge_Results_Path = '/Users/cb-kamal/Downloads'

        DS1_zip_files = DS1_zip_files.split(',')
        DS3_zip_files = DS3_zip_files.split(',')

        for i in (DS1_zip_files):
            if 'customers' in i.lower():
                customer_unzipped_folder = i.split('.zip')[0]
                if not os.path.exists(customer_unzipped_folder):
                    os.mkdir(customer_unzipped_folder)
                shutil.unpack_archive(i, customer_unzipped_folder)
                customers_merge(ClientName, customer_unzipped_folder, 'DS1', Merge_Results_Path)

            elif 'subscriptions' in i.lower():
                pass

            elif 'invoices' in i.lower():
                pass

            else:
                pass

        for i in (DS3_zip_files):
            if 'customers' in i.lower():
                customer_unzipped_folder = i.split('.zip')[0]
                if not os.path.exists(customer_unzipped_folder):
                    os.mkdir(customer_unzipped_folder)
                shutil.unpack_archive(i, customer_unzipped_folder)
                customers_merge(ClientName, customer_unzipped_folder, 'DS3', Merge_Results_Path)

            elif 'subscriptions' in i.lower():
                pass

            elif 'invoices' in i.lower():
                pass

            else:
                pass

        # print(DS1_CustomersRawData_ZipFilePath)
        # print(DS1_SubscriptionsRawData_ZipFilePath)
        # print(DS1_InvoicesRawData_ZipFilePath)
        # print(DS3_CustomersRawData_ZipFilePath)
        # print(DS3_SubscriptionsRawData_ZipFilePath)
        # print(DS3_InvoicesRawData_ZipFilePath)

jenkins_read()