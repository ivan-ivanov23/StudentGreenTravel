import pandas as pd

df = pd.read_excel('data\emission_factors.xlsx')

# Transform the dataframe to a dictionary with key the Method and value the Emission Factor
factors = df.set_index('Method')['Factor'].to_dict()
print(factors)