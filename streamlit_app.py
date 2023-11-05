#created the python file

import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents\' new healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket smoothie')
streamlit.text('🐔 Hard boiled free range egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#let's put a pick list here
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# new section to display fruityvice response
streamlit.header("Fruityvice Fruit Advice!")

# adding custom function
def fruityvice_fruit_choice(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    #streamlit.write('The user entered ', fruit_choice)
    back_from_function = fruityvice_fruit_choice(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

# don't run anything post this
#streamlit.stop()

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
  with my_cnx.cursor() as my_curr:
    my_curr.execute("select * from fruit_load_list;")
    return my_curr.fetchall()

# add a button to load a fruit
if streamlit.button("Get fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  streamlit.dataframe(my_data_row)



#my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values ('from streamlit');")

# allow the user to add fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_curr:
    my_curr.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values ('from streamlit')"
    return "Thanks for adding "+ new_fruit

fruit_add = streamlit.text_input('Which fruit would you like to add?')
if stramlit.button('Add a fruit to the list'):
    #streamlit.write('Thank you for adding ', fruit_add)
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(fruit_add)
    streamlit.text(back_from_function)
