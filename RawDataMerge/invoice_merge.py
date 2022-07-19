import csv
from datetime import datetime
from collections import OrderedDict
import pandas as pd

invoice_folder = "/Users/cb-kamal/Documents/MigrationQAFramework/QA_Framework_New/TestData/RawData/Invoices/"
DATE = datetime.now()
DATE.strftime("%m-%d-%Y-%H:%M:%S")
output_file = "DS1_Invoice_out_" + str(DATE) + ".csv"

# Required files to be merged
invoices = invoice_folder + "Invoices.csv"
line_items = invoice_folder + "LineItems.csv"
line_item_taxes = invoice_folder + "LineItemTaxes.csv"
transactions = invoice_folder + "Transactions.csv"
applied_cn = invoice_folder + "AppliedCreditNotes.csv"
adjusted_cn = invoice_folder + "AdjustmentCreditNotes.csv"
invoice_properties = invoice_folder + "InvoiceProperties.csv"
coupons = invoice_folder + "Coupons.csv"

INVOICES = OrderedDict()
# Reading invoices file
with open(invoices, 'r') as invoice:
    reader = csv.DictReader(invoice)
    for row in reader:
        inv_id = row['Invoice Number']
        # Creating temp dictionary for each subscription id
        temp = OrderedDict()
        # print("Reading for the Invoice id ---> {}".format(inv_id))
        temp['customer_id'] = row['Customer Id']
        temp['subscription_id'] = row['Subscription Id']
        temp['Invoice_number'] = inv_id
        temp['invoice_date'] = row['Invoice Date']
        temp['invoice_total'] = row['Amount']
        temp['status'] = row['Status']
        temp['vat_number'] = row['Vat Number']
        temp['po_number'] = row['PO Number']
        temp['currency_code'] = row['Currency']
        temp['net_term_days'] = row['Net Term Days']
        temp['due_date'] = row['Due Date']
        temp['payment_date'] = row['Paid On']
        temp['payment_amount'] = row['Payments']
        INVOICES[inv_id] = temp
# print(ItemLevelTaxesDic)
# Reading Invoice properties file
with open(invoice_properties, 'r') as props:
    reader = csv.DictReader(props)
    for row in reader:
        inv_id = row['Invoice Number']
        # billing address
        INVOICES[inv_id]['billing_first_name'] = row['Billing Address First Name']
        INVOICES[inv_id]['billing_last_name'] = row['Billing Address Last Name']
        INVOICES[inv_id]['billing_email'] = row['Billing Address Email']
        INVOICES[inv_id]['billing_company'] = row['Billing Address Company']
        INVOICES[inv_id]['billing_phone'] = row['Billing Address Phone']
        INVOICES[inv_id]['billing_address_line1'] = row['Billing Address Line1']
        INVOICES[inv_id]['billing_address_line2'] = row['Billing Address Line2']
        INVOICES[inv_id]['billing_address_line3'] = row['Billing Address Line3']
        INVOICES[inv_id]['billing_city'] = row['Billing Address City']
        INVOICES[inv_id]['billing_state'] = row['Billing Address State']
        INVOICES[inv_id]['billing_address_state_code'] = row['Billing Address State Code']
        INVOICES[inv_id]['billing_country'] = row['Billing Address Country']
        INVOICES[inv_id]['billing_zip'] = row['Billing Address Zip']
        # shipping address
        INVOICES[inv_id]['shipping_first_name'] = row['Shipping Address First Name']
        INVOICES[inv_id]['shipping_last_name'] = row['Shipping Address Last Name']
        INVOICES[inv_id]['shipping_email'] = row['Shipping Address Email']
        INVOICES[inv_id]['shipping_company'] = row['Shipping Address Company']
        INVOICES[inv_id]['shipping_phone'] = row['Shipping Address Phone']
        INVOICES[inv_id]['shipping_address_line1'] = row['Shipping Address Line1']
        INVOICES[inv_id]['shipping_address_line2'] = row['Shipping Address Line2']
        INVOICES[inv_id]['shipping_address_line3'] = row['Shipping Address Line3']
        INVOICES[inv_id]['shipping_city'] = row['Shipping Address City']
        INVOICES[inv_id]['shipping_state'] = row['Shipping Address State']
        INVOICES[inv_id]['shipping_address_state_code'] = row['Shipping Address State Code']
        INVOICES[inv_id]['shipping_country'] = row['Shipping Address Country']
        INVOICES[inv_id]['shipping_zip'] = row['Shipping Address Zip']

COUPONS = {}
# Reading coupons file
with open(coupons, 'r') as coupon:
    reader = csv.DictReader(coupon)
    for row in reader:
        COUPONS[row['Coupon Id']] = row['Apply On'].lower()

LINEITEM = OrderedDict()
# Reading line items file and checking for coupons discount
with open(line_items, 'r') as line:
    reader = csv.DictReader(line)
    for row in reader:
        line_item_id = row['Line Item Id']
        inv_id = row['Invoice Number']
        temp = OrderedDict()
        temp['invoice_id'] = inv_id
        temp['tax_rate'] = row['Tax Rate']

        if row['Entity Type'].lower() in ['coupon', 'discount']:
            if row['Entity Id'] not in COUPONS:
                print(row['Entity Id'])
            elif COUPONS[row['Entity Id']] == 'invoice amount':
                temp['discount_entity_type'] = row['Entity Type']
                temp['discount_entity_id'] = row['Entity Id']
                temp['discount_description'] = row['Description']
                temp['discount_amount'] = row['Amount']
            else:
                temp['item_level_discount_entity_id'] = row['Entity Id']
                temp['item_level_discount_amount'] = row['Amount']

        elif row['Entity Type'].lower() == 'promotional credits':
            temp['discount_entity_type'] = row['Entity Type']
            temp['discount_entity_id'] = row['Entity Id']
            temp['discount_description'] = row['Description']
            temp['discount_amount'] = row['Amount']
            # temp['promotional_credits_entity_type'] = row['Entity Type']
            # temp['promotional_credits_description'] = row['Description']
            # temp['promotional_credits_amount'] = row['Amount']

        elif row['Entity Type'].lower() == 'tax':
            temp['taxes_entity_id'] = row['Entity Id']
            temp['taxes_description'] = row['Description']
            temp['taxes_amount'] = row['Amount']
        else:
            temp['line_items_entity_type'] = row['Entity Type']
            temp['line_items_entity_id'] = row['Entity Id']
            temp['line_items_date_from'] = row['Date From']
            temp['line_items_date_to'] = row['Date To']
            temp['line_items_description'] = row['Description']
            temp['line_items_unit_amount'] = row['Unit Amount']
            temp['line_items_quantity'] = row['Quantity']
            temp['line_items_amount'] = row['Amount']
            temp['line_items_id'] = line_item_id
        LINEITEM[line_item_id] = temp

LItemp = {}
print("Adding line items to invoices")
for _, data in LINEITEM.items():
    inv_id = data['invoice_id']
    if not 'tax_rate' in INVOICES[inv_id] and (data['tax_rate'] not in [0, 0.0, '']):
        INVOICES[inv_id]['tax_rate'] = data['tax_rate']
    if inv_id not in LItemp:
        LItemp[inv_id] = {'plan': [], 'addon': [], 'line_items_id_forTax': []}
    if 'line_items_entity_type' in data:
        LItemp[inv_id]['line_items_id_forTax'].append(data['line_items_id'])
        if data['line_items_entity_type'] in ['Plan Item Price', 'Plan']:
            LItemp[inv_id]['plan'].append(data)
        else:
            LItemp[inv_id]['addon'].append(data)

for inv_id, value in LItemp.items():
    count = 0
    for data in value['plan']:
        INVOICES[inv_id]['line_items_entity_type[' + str(count) + ']'] = data['line_items_entity_type']
        INVOICES[inv_id]['line_items_entity_id[' + str(count) + ']'] = data['line_items_entity_id']
        INVOICES[inv_id]['line_items_description[' + str(count) + ']'] = data['line_items_description']
        INVOICES[inv_id]['line_items_date_from[' + str(count) + ']'] = data['line_items_date_from']
        INVOICES[inv_id]['line_items_date_to[' + str(count) + ']'] = data['line_items_date_to']
        INVOICES[inv_id]['line_items_quantity[' + str(count) + ']'] = data['line_items_quantity']
        INVOICES[inv_id]['line_items_unit_amount[' + str(count) + ']'] = data['line_items_unit_amount']
        INVOICES[inv_id]['line_items_amount[' + str(count) + ']'] = data['line_items_amount']
        INVOICES[inv_id]['line_items_id[' + str(count) + ']'] = data['line_items_id']
        count += 1
    for data in value['addon']:
        INVOICES[inv_id]['line_items_entity_type[' + str(count) + ']'] = data['line_items_entity_type']
        INVOICES[inv_id]['line_items_entity_id[' + str(count) + ']'] = data['line_items_entity_id']
        INVOICES[inv_id]['line_items_description[' + str(count) + ']'] = data['line_items_description']
        INVOICES[inv_id]['line_items_date_from[' + str(count) + ']'] = data['line_items_date_from']
        INVOICES[inv_id]['line_items_date_to[' + str(count) + ']'] = data['line_items_date_to']
        INVOICES[inv_id]['line_items_quantity[' + str(count) + ']'] = data['line_items_quantity']
        INVOICES[inv_id]['line_items_unit_amount[' + str(count) + ']'] = data['line_items_unit_amount']
        INVOICES[inv_id]['line_items_amount[' + str(count) + ']'] = data['line_items_amount']
        INVOICES[inv_id]['line_items_id[' + str(count) + ']'] = data['line_items_id']
        count += 1

# print("Adding line items to invoices")
# for _, data in LINEITEM.items():
#     inv_id = data['invoice_id']
#     if not 'tax_rate' in INVOICES[inv_id] and (data['tax_rate'] not in [0, 0.0, '']):
#         INVOICES[inv_id]['tax_rate'] = data['tax_rate']
#
#     if ('Plan' in etype_list[inv_id] or 'Plan Item Price' in etype_list[inv_id]) and inv_id not in temp:
#         p_count = 1
#     elif ('Plan' not in etype_list[inv_id] or 'Plan Item Price' not in etype_list[inv_id]) and inv_id not in temp:
#         p_count = 0
#
#     if 'line_items_entity_type' in data and (data['line_items_entity_type'] == 'Plan' or data['line_items_entity_type'] == 'Plan Item Price'):
#         INVOICES[inv_id]['line_items_entity_type[' + str(0) + ']'] = data['line_items_entity_type']
#         INVOICES[inv_id]['line_items_entity_id[' + str(0) + ']'] = data['line_items_entity_id']
#         INVOICES[inv_id]['line_items_description[' + str(0) + ']'] = data['line_items_description']
#         INVOICES[inv_id]['line_items_date_from[' + str(0) + ']'] = data['line_items_date_from']
#         INVOICES[inv_id]['line_items_date_to[' + str(0) + ']'] = data['line_items_date_to']
#         INVOICES[inv_id]['line_items_quantity[' + str(0) + ']'] = data['line_items_quantity']
#         INVOICES[inv_id]['line_items_unit_amount[' + str(0) + ']'] = data['line_items_unit_amount']
#         INVOICES[inv_id]['line_items_amount[' + str(0) + ']'] = data['line_items_amount']
#         INVOICES[inv_id]['line_items_id[' + str(0) + ']'] = data['line_items_id']
#         temp[inv_id] = -1
#     elif 'line_items_entity_type' in data:
#         if inv_id in temp:
#             count += 1
#             temp[inv_id] = count
#         else:
#             count = p_count
#         INVOICES[inv_id]['line_items_entity_type[' + str(count) + ']'] = data['line_items_entity_type']
#         INVOICES[inv_id]['line_items_entity_id[' + str(count) + ']'] = data['line_items_entity_id']
#         INVOICES[inv_id]['line_items_description[' + str(count) + ']'] = data['line_items_description']
#         INVOICES[inv_id]['line_items_date_from[' + str(count) + ']'] = data['line_items_date_from']
#         INVOICES[inv_id]['line_items_date_to[' + str(count) + ']'] = data['line_items_date_to']
#         INVOICES[inv_id]['line_items_quantity[' + str(count) + ']'] = data['line_items_quantity']
#         INVOICES[inv_id]['line_items_unit_amount[' + str(count) + ']'] = data['line_items_unit_amount']
#         INVOICES[inv_id]['line_items_amount[' + str(count) + ']'] = data['line_items_amount']
#         INVOICES[inv_id]['line_items_id[' + str(count) + ']'] = data['line_items_id']
#         temp[inv_id] = count
# print("Item Level Taxes Dic: "+ str(ItemLevelTaxesDic))
# count = 0
# temp = ''
# print("Adding line items to invoices for ItemLeveltaxes")
# for _, data in LINEITEM.items():
#     inv_id = data['invoice_id']
#     if inv_id == 'FW27415':
#         print()
#     if 'line_items_entity_type' in data:
#         if inv_id == temp:
#             count += 1
#         else:
#             count = 0
#         ItemLevelTaxesDic[inv_id]['line_items_id[' + str(count) + ']'] = data['line_items_id']
#         temp = inv_id
# print("ItemLevelTax Dictionary : " +str(ItemLevelTaxesDic['FW27415']))

print("Adding taxes to invoice")
count = 0
temp = set()
for _, data in LINEITEM.items():
    inv_id = data['invoice_id']
    if 'taxes_entity_id' in data:
        if inv_id in temp:
            count += 1
        else:
            count = 0
        INVOICES[inv_id]['taxes_name[' + str(count) + ']'] = data['taxes_entity_id']
        INVOICES[inv_id]['taxes_description[' + str(count) + ']'] = data['taxes_description']
        INVOICES[inv_id]['taxes_amount[' + str(count) + ']'] = data['taxes_amount'].replace('-', '')
        temp.add(inv_id)
# read line item taxes file
line_taxes = OrderedDict()
with open(line_item_taxes, 'r') as tax:
    print("In the line item taxes")
    reader = csv.DictReader(tax)
    for row in reader:
        if row['Line Item Id'] in line_taxes and row['Tax Name'] != "":
            line_taxes[row['Line Item Id']].append([row['Tax Name'], row['Tax Amount']])
        else:
            if row['Tax Name'] != "":
                line_taxes[row['Line Item Id']] = [[row['Tax Name'], row['Tax Amount']]]

print("Adding line item taxes to invoices")
temp = OrderedDict()

# for key, value in LItemp.items():
#     if key == 'FW27415':
#         print(key)
#     temp[key] = []
#     count = 0
#     for i in range(15):
#         if 'line_items_id[' + str(i) + ']' in value['line_items_id_forTax']:
#             temp[key].append(value['line_items_id[' + str(i) + ']'])
#     for line_id in temp[key]:
#         if line_id in line_taxes:
#             for item in line_taxes[line_id]:
#                 INVOICES[key]['line_item_tax_name[' + str(count) + ']'] = item[0]
#                 INVOICES[key]['line_item_tax_amount[' + str(count) + ']'] = item[1].replace('-', '')
#                 count += 1
for key, value in LItemp.items():
    if key == 'FW27415':
       print(key)
    count = 0
    line_items = value['line_items_id_forTax']
    for line_id in line_items:
        if line_id in line_taxes:
            for item in line_taxes[line_id]:
                INVOICES[key]['line_item_tax_name[' + str(count) + ']'] = item[0]
                INVOICES[key]['line_item_tax_amount[' + str(count) + ']'] = item[1].replace('-', '')
                count += 1


print('Adding discounts to invoices')
count = 0
temp = set()
for _, data in LINEITEM.items():
    inv_id = data['invoice_id']
    if 'discount_entity_type' in data:
        if inv_id in temp:
            count += 1
        else:
            count = 0
        INVOICES[inv_id]['discount_entity_type[' + str(count) + ']'] = data['discount_entity_type']
        INVOICES[inv_id]['discount_entity_id[' + str(count) + ']'] = data['discount_entity_id']
        INVOICES[inv_id]['discount_description[' + str(count) + ']'] = data['discount_description']
        INVOICES[inv_id]['discount_amount[' + str(count) + ']'] = data['discount_amount'].replace('-', '')
        temp.add(inv_id)

print('Adding item level discount')
count = 0
temp = set()
for _, data in LINEITEM.items():
    inv_id = data['invoice_id']
    if 'item_level_discount_entity_id' in data:
        if inv_id in temp:
            count += 1
        else:
            count = 0
        INVOICES[inv_id]['item_level_discounts_entity_id[' + str(count) + ']'] = data['item_level_discount_entity_id']
        INVOICES[inv_id]['item_level_discounts_amount[' + str(count) + ']'] = data['item_level_discount_amount'].replace('-', '')
        temp.add(inv_id)

# count = 0
# temp = set()
# print("Adding promotional credits")
# for _, data in LINEITEM.items():
#     inv_id = data['invoice_id']
#     if 'promotional_credits_entity_type' in data:
#         if inv_id in temp:
#             count += 1
#         else:
#             count = 0
#         INVOICES[inv_id]['promotional_credits_entity_type[' + str(count) + ']'] = data['promotional_credits_entity_type']
#         INVOICES[inv_id]['promotional_credits_description[' + str(count) + ']'] = data['promotional_credits_description']
#         INVOICES[inv_id]['promotional_credits_amount[' + str(count) + ']'] = data['promotional_credits_amount'].replace('-', '')
#         temp.add(inv_id)

print("Adding transaction payment method")
with open(transactions, 'r') as trans:
    reader = csv.DictReader(trans)
    temp = {}
    count = 0
    for row in reader:
        inv_ids = row['Invoice Number'].split(',')
        for inv_id in inv_ids:
            inv_id = inv_id.strip()
            if row['Status'].lower() == 'success':
                if inv_id not in temp:
                    temp[inv_id] = 0
                else:
                    temp[inv_id] += 1
                INVOICES[inv_id]['payment_method[' + str(temp[inv_id]) + ']'] = row['Payment Method']

print('Constructing header')
columns = []
# Getting the keys from all the dictionary to construct header
for data in list(INVOICES.values()):
    for key in list(data.keys()):
        if key not in columns:
            columns.append(key)

orders = ['taxes_', 'discount_', 'payment_method', 'line_items_', 'line_item_tax_', 'item_level_discounts_']
headers = []
headers2 = []
for order in orders:
    for column in columns:
        if (order in column) and (column not in headers2):
            headers2.append(column)

for column in columns:
    if column not in headers2:
        headers.append(column)
headers.extend(headers2)
print("done")

# print(INVOICES['FW31392']['line_items_entity_type[1]'])
print('Started to write to file')
with open(output_file, 'w', newline='', encoding='utf-8') as out:
    writer = csv.DictWriter(out, fieldnames=headers, delimiter=',')
    writer.writeheader()
    for _, row in INVOICES.items():
        writer.writerow(row)
print('Invoice file is generated')

# Check for taxes and transactions
