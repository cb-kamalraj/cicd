"""This script is for merging multiple raw file of subscription to
generate a consolidated single subscription file in required format and order"""

import csv
from datetime import datetime
from collections import OrderedDict
from ordered_set import OrderedSet

subs_folder = "./subscriptions/"
DATE = datetime.now()
output_file = "Subscription_out_" + str(DATE) + ".csv"

# Required files to be merged
subscription = subs_folder + "Subscriptions.csv"
subs_addons = subs_folder + "SubscriptionAddons.csv"
subs_contracts = subs_folder + "SubscriptionContracts.csv"
subs_coupons = subs_folder + "SubscriptionCoupons.csv"
subs_discounts = subs_folder + "SubscriptionDiscounts.csv"
subs_comments = subs_folder + "SubscriptionComments.csv"

SUBSCRIPTION = OrderedDict()
prefix = ""
print("Reading main subscription file")
with open(subscription, 'r') as subs:
    reader = csv.DictReader(subs)
    for row in reader:
        sub_id = row['subscriptions.id']
        # Creating temp dictionary for each subscription id
        temp = OrderedDict()
        # print("Reading for the subscriptions id ---> {}".format(sub_id))
        temp['subscription_id'] = prefix + row['subscriptions.id']
        temp['item_plan_id[0]'] = row['subscriptions.plan_id']
        temp['item_quantity[0]'] = row['subscriptions.plan_quantity']
        temp['item_unit_price[0]'] = row['subscriptions.plan_unit_price']
        sub_status = row['subscriptions.status']
        temp['status'] = sub_status
        temp['subscription_start_date'] = row['subscriptions.start_date']
        if sub_status.lower() != "cancelled":
            temp['subscription_trial_start'] = row['subscriptions.trial_start']
            temp['subscription_trial_end'] = row['subscriptions.trial_end']
            temp['subscription_current_term_start'] = row['subscriptions.current_term_start']
            temp['subscription_current_term_end'] = row['subscriptions.current_term_end']
        temp['subscription_billing_cycles'] = row['subscriptions.remaining_billing_cycles']
        temp['subscription_created_at'] = row['subscriptions.created_at']
        temp['subscription_started_at'] = row['subscriptions.started_at']
        if sub_status.lower() != "non renewing":
            temp['subscription_cancelled_at'] = row['subscriptions.cancelled_at']
        temp['customer_id'] = prefix + row['customers.id']

        # shipping address
        temp['shipping_first_name'] = row['addresses.first_name']
        temp['shipping_last_name'] = row['addresses.last_name']
        temp['shipping_email'] = row['addresses.email']
        temp['shipping_company'] = row['addresses.company']
        phone = row['addresses.phone']
        try:
            ph = int(phone)
            if not ph > 0:
                phone = ''
        except:
            pass
        temp['shipping_phone'] = phone
        temp['shipping_address_line1'] = row['addresses.addr']
        temp['shipping_address_line2'] = row['addresses.extended_addr']
        temp['shipping_address_line3'] = row['addresses.extended_addr2']
        temp['shipping_city'] = row['addresses.city']
        temp['shipping_state'] = row['addresses.state']
        temp['shipping_country'] = row['addresses.country']
        temp['shipping_zip'] = row['addresses.zip']

        # temp['shipping_state_code'] = row['addresses.state_code']
        # temp['customer_first_name'] = row['customers.first_name']
        # temp['customer_last_name'] = row['customers.last_name']
        # temp['customer_email'] = row['customers.email']
        temp['subscriptions_po_number'] = row['subscriptions.po_number']
        temp['subscription_auto_collection'] = row['subscriptions.auto_collection']
        temp['subscription_pause_date'] = row['subscriptions.pause_date']
        temp['subscription_resume_date'] = row['subscriptions.resume_date']
        # temp['subscription_plan_amount'] = row['subscriptions.plan_amount']
        temp['subscription_plan_quantity_in_decimal'] = row['subscriptions.plan_quantity_in_decimal']
        temp['subscription_plan_unit_price_in_decimal'] = row['subscriptions.plan_unit_price_in_decimal']


        # custome fields
        try:
            temp['cf_reseller_paying'] = row['subscriptions.cf_reseller_paying']
        except:
            temp['cf_reseller_paying'] = ''
        try:
            temp['cf_contract_tenure'] = row['subscriptions.cf_contract_tenure']
        except:
            temp['cf_contract_tenure'] = ''
        try:
            temp['cf_business_type'] = row['subscriptions.cf_business_type']
        except:
            temp['cf_business_type'] = ''
        try:
            temp['cf_auto_renewal'] = row['subscriptions.cf_auto_renewal']
        except:
            temp['cf_auto_renewal'] = ''
        try:
            temp['cf_reseller_name'] = row['subscriptions.cf_reseller_name']
        except:
            temp['cf_reseller_name'] = ''
        try:
            temp['cf_order_term_same_as_invoice_term'] = row['subscriptions.cf_order_term_same_as_invoice_term']
        except:
            temp['cf_order_term_same_as_invoice_term'] = ''
        try:
            temp['cf_order_term'] = row['subscriptions.cf_order_term']
        except:
            temp['cf_order_term'] = ''
        try:
            temp['cf_order_end_date'] = row['subscriptions.cf_order_end_date']
        except:
            temp['cf_order_end_date'] = ''
        try:
            temp['cf_tfc_midterm_downgrade'] = row['subscriptions.cf_tfc_midterm_downgrade']
        except:
            temp['cf_tfc_midterm_downgrade'] = ''
        try:
            temp['cf_tier_volume_pricing'] = row['subscriptions.cf_tier_volume_pricing']
        except:
            temp['cf_tier_volume_pricing'] = ''
        try:
            temp['cf_crm_deal_id'] = row['subscriptions.cf_crm_deal_id']
        except:
            temp['cf_crm_deal_id'] = ''
        # try:
        #     temp['net_term_days'] = row['customers.net_term_days']
        # except:
        #     temp['net_term_days'] = ''
        # Storing the temp dictionary as value and corresponding sub id as key in main dictionary
        SUBSCRIPTION[sub_id] = temp

# reading addons file
print("Reading addons file")
with open(subs_addons, 'r') as addon:
    reader = csv.DictReader(addon)
    temp = ''
    count = 1
    for row in reader:
        sub_id = row['Subscription Id']
        # sub_id = '111'
        if sub_id != temp:
            count = 1
        else:
            count += 1
        SUBSCRIPTION[sub_id]['items_price_id[' + str(count) + ']'] = row['Addon Id']
        SUBSCRIPTION[sub_id]['items_quantity[' + str(count) + ']'] = row['Addon Quantity']
        SUBSCRIPTION[sub_id]['items_unit_price[' + str(count) + ']'] = row['Addon Unit Price']
        # SUBSCRIPTION[sub_id]['item_amount[' + str(count) + ']'] = row['Addon Amount']
        temp = sub_id

# reading coupons file
print("Reading coupons file")
with open(subs_coupons, 'r') as addon:
    temp = ''
    count = 0
    reader = csv.DictReader(addon)
    for row in reader:
        sub_id = row['Subscription Id']
        # sub_id = '111'
        if sub_id != temp:
            count = 0
        else:
            count += 1
        SUBSCRIPTION[sub_id]['coupon['+str(count) + ']'] = row['Coupon Id']
        temp = sub_id

# Getting the keys from all the dictionary to construct header
print("Constructing headers")
columns = []
for data in list(SUBSCRIPTION.values()):
    for key in list(data.keys()):
        if key not in columns:
            columns.append(key)
orders = ['items_', 'coupon']
headers, headers2 = [], []
for order in orders:
    for column in columns:
        if (order in column) and (column not in headers2):
            headers2.append(column)

for column in columns:
    if column not in headers2:
        headers.append(column)
headers.extend(headers2)

# write combined data to csv
with open(output_file, 'w', newline='', encoding='utf-8') as out:
    writer = csv.DictWriter(out, fieldnames=headers, delimiter=',')
    writer.writeheader()
    for _, row in SUBSCRIPTION.items():
        writer.writerow(row)
print('Subscription file is generated')
