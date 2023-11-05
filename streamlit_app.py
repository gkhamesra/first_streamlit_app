#created the python file

import streamlit

streamlit.title('My Parents\' new healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket smoothie')
streamlit.text('🐔 Hard boiled free range egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#let's put a pick list here
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# new section to display fruityvice response
streamlit.header("Fruityvice Fruit Advice!")

import requests
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json()) # outputs the response as is

# normalizes the json
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# creates a table out of the normalized json
streamlit.dataframe(fruityvice_normalized)


import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list;")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_add = streamlit.text_input('Which fruit would you like to add?')
if fruit_add is not None:
  streamlit.write('Thank you for adding ', fruit_add)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values ('from streamlit');")
