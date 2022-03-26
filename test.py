import pandas as pd

dict_test = {
    'col1': [1, 2, 3],
    'col2': [4, 5, 6]
}

df_test = pd.DataFrame(dict_test)

df_test.to_excel('item_list.xlsx', index=False, sheet_name='item_list')
print('Process finished')