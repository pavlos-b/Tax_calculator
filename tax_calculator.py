import requests
import lxml.html as lh
import pandas as pd
import string


def get_data():
    url='https://tradingeconomics.com/country-list/sales-tax-rate'
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')

    #Check the length of the first 12 rows
    #[len(T) for T in tr_elements[:12]]

    tr_elements = doc.xpath('//tr')
    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        #print ('%d:%s'%(i,name))
        col.append((name,[]))
    
    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]
    
        #If row is not of size 10, the //tr data is not from our table 
        if len(T)!=5:
            break
    
        #i is the index of our column
        i=0
    
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1
    Dict={title:column for (title,column) in col}
    #df=pd.DataFrame(Dict)
    #df.head()

    #Clear the data
    alphabet_list = list(string.ascii_uppercase)
    for i in range(len(Dict['Country'])):
        Dict["Country"][i] = Dict["Country"][i].replace('\r\n', '').strip()
        Dict["Last "][i] = str(Dict["Last "][i]).replace('\r\n', '').replace(' ', '')
        Dict["Last "][i] = float(Dict["Last "][i])
        Dict["Previous "][i] = str(Dict["Previous "][i]).replace('\r\n', '').replace(' ', '')
        Dict["Previous "][i] = float(Dict["Previous "][i])
        Dict["Reference"][i] = Dict["Reference"][i].replace('\r\n', '').replace(' ', '')
        Dict[" Unit"][i] = Dict[" Unit"][i].replace('\r\n', '').replace(' ', '')
    
    #Create a new dictionary with Country and Tax info
    tax_dict = {}
    for j in range(len(Dict['Country'])):
        tax_dict[Dict["Country"][j]] = Dict["Last "][j]
    
    return tax_dict

    #from collections import OrderedDict 
    #sort_tax_dict = OrderedDict(sorted(tax_dict.items())) 
    
def tax_calculator(tax_dict):
    while True: 
        try: 
            cost = int(input("Please provide a product cost price in EUR: "))
        except: 
            print('This is not a cost. Try again.')
        else: 
            break
    
    while True: 
        country = (input("For which country do you wish to know the tax? Please give the name in English : ")).lower().capitalize()
        c = country.split(" ")
        country = ""
        for i in range(len(c)):
            cp = c[i].capitalize()
            country += (" " + cp)
        country = country.strip()
        if country not in tax_dict: 
            view_countries = input('Unknown country. Would you like to view the list of all countries? Type y/n: ')
            if view_countries == "y":
                for key in sorted(tax_dict):
                    print(key)
            else: 
                continue
        else: 
            break
    
    #Cost after tax
    new_cost = cost + (cost * tax_dict[country] / 100)
    
    print("The tax in %s is %d" %(country, tax_dict[country]) + '%.')
    print("The cost after tax is {} EUR.".format(new_cost))


def main():
    tax_data = get_data()
    tax_calculator(tax_data)
    print('Test')

if __name__ == "__main__":
    main()

   