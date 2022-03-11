import streamlit as st
import pandas as pd























# dummy_dictionary = {}
# dummy_dictionary["Name"] = ["John","Deep","Julia","Kate","Sandy"]
# dummy_dictionary["MonthSales"] = [25,30,35,40,45]
# dummy_dictionary["Other"] = [25,30,35,40,45]
#
#
#
#
# dummy_data = pd.DataFrame(dummy_dictionary)
# st.table(dummy_data)
#
#
#
#
# def turn_dataframe_into_nice_table(df,target_container):
#     num_of_cols = len(df.columns)
#     column_titles = list(df.columns)
#
#
#     subdivisions = st.columns(num_of_cols)
#     for col_i in range(num_of_cols):
#         subdivisions[col_i].subheader(column_titles[col_i])
#
#
#     for index, row in df.iterrows():            # Iterate over each row
#         for cell_i in range(num_of_cols):       # Iterate over each cell in row
#             subdivisions[cell_i].write(row[column_titles[cell_i]])
#
#
#
# turn_dataframe_into_nice_table(dummy_data,st)
