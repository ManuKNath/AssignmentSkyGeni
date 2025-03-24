import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




finance_csv = pd.read_csv('data/finanical_information.csv')
client_csv = pd.read_csv('data/industry_client_details.csv')
payment_csv = pd.read_csv('data/payment_information.csv')
subscription_csv = pd.read_csv('data/subscription_information.csv')






print('1. How many finance lending and blockchain clients does the organization have?') 

client_bc_fl = client_csv[(client_csv['industry'] == 'Block Chain') | (client_csv['industry'] == 'Finance Lending')]

print(client_bc_fl.shape[0])




print('2. Which industry in the organization has the highest renewal rate?')

renewed_client = subscription_csv[subscription_csv['renewed'] == True]

merged_df = pd.merge(renewed_client, client_csv, on='client_id', how='left')

merged_df.industry.value_counts().head(1)

industry_dist = merged_df.groupby('industry').size()


# Plotting the bar chart
plt.figure(figsize=(8, 5))
industry_dist.plot(kind='bar', color='skyblue')  # Create a bar chart
plt.title('Distribution of renewal rate vs industry')  # Title of the chart
plt.xlabel('Industry')  # X-axis label
plt.ylabel('Count')  # Y-axis label
plt.xticks(rotation=0)  # Rotate x-axis labels for better readability
plt.grid(axis='y')  # Add grid lines for better readability
plt.show()  # Display the plot




print('3. What was the average inflation rate when their subscriptions were renewed?')

gaming_clients_df = merged_df[merged_df.industry == 'Gaming']

# Converting date columns to date format.
gaming_clients_df.start_date = pd.to_datetime(gaming_clients_df.start_date)
gaming_clients_df.end_date = pd.to_datetime(gaming_clients_df.end_date)

# Creating new coloumns for identifying quaters.
gaming_clients_df['start_date_Q'] = gaming_clients_df['start_date'].dt.to_period('Q')
gaming_clients_df['end_date_Q'] = gaming_clients_df['end_date'].dt.to_period('Q')

# Copying finance csv to add Quater column.
finance_csv_copy = finance_csv.copy()

finance_csv_copy.start_date = pd.to_datetime(finance_csv_copy.start_date)
finance_csv_copy.end_date = pd.to_datetime(finance_csv_copy.end_date)

finance_csv_copy['start_date_Q'] = finance_csv_copy['start_date'].dt.to_period('Q')
finance_csv_copy['end_date_Q'] = finance_csv_copy['end_date'].dt.to_period('Q')



# Creating Dataframe to collect applicable quaters.
inflation_rate_df = finance_csv_copy.head(0)


for index, row in gaming_clients_df.iterrows():
    inflation_rate_df = pd.concat([inflation_rate_df, finance_csv_copy[(finance_csv_copy['start_date_Q']>=row.start_date_Q) & 
                                                                       (finance_csv_copy['start_date_Q']<=row.end_date_Q)]])

# Removing duplicates to avoid multiple inflation rates from same quater.
inflation_rate_df_unique = inflation_rate_df.drop_duplicates()

print(round(inflation_rate_df_unique.inflation_rate.mean(), 2))




print('4. What is the median amount paid each year for all payment methods?')

payment_analysis_df = payment_csv.copy()

payment_analysis_df['year'] = payment_analysis_df['payment_date'].dt.year

payment_year_median = payment_analysis_df.groupby(['year', 'payment_method'])['amount_paid'].median().reset_index()


# # Plotting
plt.figure(figsize=(10, 6))

# Set the width of the bars
bar_width = 0.2
# Get unique years and payment methods
years = payment_year_median['year'].unique()
payment_methods = payment_year_median['payment_method'].unique()

# Create an array for the x positions of the bars
x_positions = np.arange(len(years))

# Create a bar chart for each payment method
for i, method in enumerate(payment_methods):
    subset = payment_year_median[payment_year_median['payment_method'] == method]
    # Offset the x positions for each payment method
    plt.bar(x_positions + i * bar_width, subset['amount_paid'], width=bar_width, label=method, alpha=0.7)

plt.title('Median Amount Paid by Year and Payment Method')
plt.xlabel('Year')
plt.ylabel('Median Amount Paid')
plt.xticks(x_positions + bar_width * (len(payment_methods) - 1) / 2, years)  # Center the x-ticks
plt.legend(title='Payment Method')
plt.grid(axis='y')

# Show the plot
plt.tight_layout()
plt.show()