import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s new Healthy Dinner')

streamlit.header('Breakfast Favorites')
streamlit.text('π«π Omega 3 & Bluberry Oatmeal')
streamlit.text('π₯¬Kale, Spinach & Rocket Smoothie')
streamlit.text('π₯Hard-Boiled Free-Range Egg')
streamlit.text('π₯π₯ͺ Avocado Toast')
               
streamlit.header('ππ₯­ Build Your Own Fruit Smoothie π₯π')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# create the repeatable code block ( called a function)
def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    
# New section to display fruitvice api responce
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice: 
        streamlit.error("Please select a fruit to get information")
   else:
        back_from_function = get_fruitvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()

streamlit.header("View Our Fruit List - Add Your Fvorites!")
# Snowflake related functions
def get_fuit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("SELECT * from fruit_load_list")
         return my_cur.fetchall()
        
# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fuit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)
    
# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
         return "Thanks for adding " + new_fruit
        
add_my_fruit = streamlit.text_input('What fruit would you like to add?')   
if streamlit.button('Add a fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_snx.close()
    streamlit.text(back_from_function)
    

    
    
# don't run anything past here
streamlit.stop()
# import snowflake.connector


my_cur = my_cnx.cursor()

streamlit.dataframe(my_data_rows)



streamlit.write('Thanks for adding ', add_my_fruit)

# this will not work correctly, but just go with it for now


 # import requests

# streamlit.text(fruityvice_response.json()) # just writes the data to the screen

# take the json version of the reponce and normalize it 

# Display the table on the page.

