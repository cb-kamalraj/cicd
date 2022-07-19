import csv
from collections import OrderedDict
from ordered_set import OrderedSet

creditNotesParent_folder = "/Users/cb-kamal/Documents/MigrationQAFramework/QA_Framework_New/TestData/RawData/"
output_file = "../TestData/RawData/Freshbilling_CreditNotes_DS1.csv"
crediNotes = creditNotesParent_folder + "CreditNotes.csv"
crediNotesLineItems = creditNotesParent_folder + "CreditNoteLineItems.csv"
crediNotesAllocatedInvoice = creditNotesParent_folder + "AllocatedInvoices.csv"

CreditNotesDictionary = {}

with open(crediNotes, 'r') as creds:
    reader = csv.DictReader(creds)
    # next(reader)
    credNote_temp = ''
    j = 1
    for i in reader:
        temp = {}
        creditNoteId = i['Credit Note Number']
        print("Credit Note Number is --->" + creditNoteId)
        temp['subscription_id'] = i['Credit Note Number']
        if creditNoteId != credNote_temp:
            j = 1
        else:
            j += 1
        temp['credit_note_reference_invoice_id[' + str(j) + ']'] = i['Reference Invoice Number']
        temp['credit_note_type[' + str(j) + ']'] = i['Type']
        temp['credit_note_reason_code[' + str(j) + ']'] = i['Reason Code']
        temp['credit_note_date[' + str(j) + ']'] = i['Date']
        temp['credit_note_total[' + str(j) + ']'] = i['Total']
        temp['customer_id[' + str(j) + ']'] = i['Customer Id']
        sub_temp = credNote_temp
        CreditNotesDictionary[creditNoteId] = temp
    print(CreditNotesDictionary)

#Adding Credit Note Line Items
with open(crediNotesLineItems, 'r') as lineitems:
    reader = csv.DictReader(lineitems)
    temp = ''
    j = 1
    lineitemsList = ["Plan", "Adhoc", "Addon", "Plan Item Price", "Addon Item Price", "Charge Item Price"]
    for i in reader:
        creditNoteId = i['Credit Note Number']
        if i['Entity Type'] in lineitemsList:
            if creditNoteId != temp:
                j = 1
            else:
                j += 1
            CreditNotesDictionary[creditNoteId]['line_items_reference_line_item_id[' + str(j) + ']'] = i['Line Item Id']
            CreditNotesDictionary[creditNoteId]['line_items_date_from[' + str(j) + ']'] = i['Date From']
            CreditNotesDictionary[creditNoteId]['line_items_date_to[' + str(j) + ']'] = i['Date To']
            CreditNotesDictionary[creditNoteId]['line_items_description[' + str(j) + ']'] = i['Description']
            CreditNotesDictionary[creditNoteId]['line_items_unit_amount[' + str(j) + ']'] = i['Unit Amount']
            CreditNotesDictionary[creditNoteId]['line_items_quantity[' + str(j) + ']'] = i['Quantity']
            CreditNotesDictionary[creditNoteId]['line_items_amount[' + str(j) + ']'] = i['Amount']
            temp = creditNoteId


# Adding Allocated Invoices
with open(crediNotesAllocatedInvoice, 'r') as alcInvoice:
    reader = csv.DictReader(alcInvoice)
    temp = ''
    j = 1
    for i in reader:
        creditNoteId = i['CreditNote Number']
        if creditNoteId != temp:
            j = 1
        else:
            j += 1
        CreditNotesDictionary[creditNoteId]['Allocated_invoice_customer[id]['+str(j) + ']'] = i['Customer Id']
        CreditNotesDictionary[creditNoteId]['Allocated_Invoice_number[' + str(j) + ']'] = i['Invoice Number']
        CreditNotesDictionary[creditNoteId]['transaction[amount][' + str(j) + ']'] = i['Amount']
        CreditNotesDictionary[creditNoteId]['Allocated_Date[' + str(j) + ']'] = i['Allocated At']
        temp = creditNoteId

# write combined data to csv
a = OrderedSet([])
for i in list(CreditNotesDictionary.values()):
    [a.add(k) for k in list(i.keys())]

headers = list(a)
with open(output_file, 'w', newline='') as out:
    writer = csv.DictWriter(out, fieldnames=headers, delimiter=',')
    writer.writeheader()
    for row in CreditNotesDictionary.values():
        writer.writerow(row)
