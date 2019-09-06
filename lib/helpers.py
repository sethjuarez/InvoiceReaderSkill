import json

personMap = {
    "Name": "Name",
    "Address": "Address",
    "City": "City",
    "State": "StateProvince",
    "Postal Code": "PostalCode",
    "Country": "Country",
}

companyMap = {
    "Company": "Name",
    "Company Address": "Address",
    "Company City": "City",
    "Company State": "StateProvince",
    "Company Postal Code": "PostalCode",
    "Company Country": "Country",
}

invoiceMap = {
    "Invoice No.": "InvoiceId",
    "Order Date": "OrderDate",
    "Subtotal": "SubTotal",
    "Total Discount": "TotalDiscount",
    "Tax Rate": "TaxRate",
    "Total Tax": "TotalTax",
    "Total": "Total",
}

lineItemMap = {
    "Itm": "ItemId",
    "Qty": "Quantity",
    "Description": "Description",
    "Price": "Price",
    "Discount": "DiscountTotal",
    "(Pct)": "Discount",
    "Tax": "Tax",
    "LineTotal": "LineTotal",
}

def convert(data):
    o = {}

    # python dictionaries are fun
    keyPairs = { items["key"][0]["text"]: items["value"][0]["text"] if len(items["value"]) > 0 else "" 
                 for items in data["pages"][0]["keyValuePairs"] }

    tableItems = { col["header"][0]["text"]: [entry[0]["text"] for entry in col["entries"]]
                  for col in data["pages"][0]["tables"][0]["columns"] }

    o = { v: keyPairs[k] for k, v in invoiceMap.items() }
    o['company'] = { v: keyPairs[k] for k, v in companyMap.items() }
    o['person'] = { v: keyPairs[k] for k, v in personMap.items() }

    o['keyPairs'] = keyPairs
    o['tableItems'] = tableItems

    

    return o