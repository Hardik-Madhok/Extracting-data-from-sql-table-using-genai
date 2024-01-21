import numpy as np
import pandas as pd
import streamlit as st
import openai
import sqlite3
import traceback

def create_prompt(userquery):
    prompt = """Given an input question, first create a syntatically correct sqlite query to run on the following tables.
    
    Tables and columns Metadata is given below and each table data is seperated by '####'
    ####
    1. Table 'Customer':
    - Column CustomerID: it is a unique ID for each customer, \
    - Column CN: it is Customer Name, \
    - Column ContactN: it is Contact Name, \
    - Column Addrs: it is Customer Address, \
    - Column Ct : it is the city of Customer, \
    - Column PCode : it is Postal Code for Customer, \
    - Column Cntry : it is the customer country.

    ####
    2. Table 'Orders':
    - Column OrderId : it is unique ID of each order, \
    - Column CustID : it is the customer ID,\
    - Column EmployeeID : it is the employee ID,\
    - Column OrderDate : It is the date on which order is placed, \
    - Column ShipperID : It is the shipperID.

    ####
    3. Table 'Products':
    - Column ProductID : It is the unique ID of each product, \
    - Column ProductName : It is the name of the product, \
    - Column SupplierID : It is the Supplier ID, \
    - Column CategoryID : It is the category id of product.
    - Column Unit : It is the number of unit in each product. 
    - Column Price : It is the price of the product. \
    
    ####
    4. Table 'OrderDetails':
    - Column OrderDetailID : it is the ID of each order detail, \
    - Column OrdrID : it is the order ID, \
    - Column ProductID : It is the id of product, \
    - Column Quantity : It is the quantity ordered.

    ####
    5. Table 'Categories': 
    - Column categoryID : it is the unique id for each category, \
    - Column CategoryName : it is the name of category. \
    - Column Description : it is the description of category. 

    ####
    6. Table 'Employee':
    - Column EmployeeID : it is the unique ID for each employee, \
    - Column LastName : it is the last name of employee, \
    - Column FirstName : it is the firstname of employee , \
    - Column BirthDate : it is the date of birth of employee, \
    - Column Notes : it is the note given by the employee.

    ####
    7. Table 'Suppliers':
    - Column SupplierID : it is the unique id for each supplier, \
    - Column SupplierName : it is the name of suppliers, \
    - Column ContactName : it is the contact name for supplier, \
    - Column Address : it is the address of the supplier, \
    - Column City : it is the city of supplier. 
    - Column PostalCodeV : it is the postal code of supplier, \
    - Column Country : it is the country of supplier,\
    - Column Phone : it is the phone number of supplier,

    ####

    '''Question:""" + userquery + "'''"
    return prompt

def generate_sqlquery(prompt_input):
    response = openai.Completion.create(
        engine= " ",
        prompt=prompt_input,
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.3,
    )
    return response.choices[0].text
#openai key
openai.api_key = 'OPENAI_API_KEY'

#Setting up page configuration 
st.set_page_config(
    page_title= 'Your page title',
    page_icon = 'Page Icon',
    layout = "wide",
)

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

#dashboard title
st.title("Give title")

#connecting with sqlite3
file = "Enter your file"
conn= sqlite3.connect(file)
# Input box for user query
userquery = st.text_input('Please type your query')
#print (prompt)
prompt = create_prompt(userquery)
try:
    if st.button('Query'):
        flag=0
        sqlquery = generate_sqlquery(prompt)
        print(sqlquery)
        df = pd.read_sql_query(sqlquery, conn)
        st.markdown("### Detailed Data view")
        st.dataframe(df)

except Exception as e:
    print(traceback.format_exc())
    st.error("Unable to process request")


