import pandas as pd
import os

df = pd.read_csv("RROI_Input_06-14-2024.csv")
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%Y-%m-%d')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')  

print(df.shape)
columns_to_replace = ['Impressions','Clicks','Media_Cost', 'Video_Views','GRPs']
df[columns_to_replace] = df[columns_to_replace].fillna(0).replace('', 0)
# 1.Axe Cross

Axe_Cross = df[df['Brand'].isin(['Axe'])]
Axe_Cross_1 = Axe_Cross[Axe_Cross['Category'].isin(['Cross-Category'])]
Axe_Cross_1.to_excel("INC13_Axe Cross Category_Raw_Data_17062024.xlsx",index=True)

#2.Degree Cross

Degree_Cross = df[df['Brand'].isin(['Degree'])]
Degree_Cross_1 = Degree_Cross[Degree_Cross['Category'].isin(['Cross-Category'])]
Degree_Cross_1.to_excel("INC13_Degree Cross Category_Raw_Data_17062024.xlsx",index=True)

#3.DMC Cross

DMC_Cross = df[df['Brand'].isin(['Dove Men+Care'])]
DMC_Cross_1 = DMC_Cross[DMC_Cross['Category'].isin(['Cross-Category'])]
DMC_Cross_1.to_excel("INC15_DMC Cross_Raw_Data_17062024.xlsx",index=True)

#4.Dove Cross

Dove_Cross = df[df['Brand'].isin(['Dove'])]
Dove_Cross_1 = Dove_Cross[Dove_Cross['Category'].isin(['Cross-Category'])]
Dove_Cross_1.to_excel("INC17_Dove Cross_Raw_Data_17062024.xlsx",index=True)

#5.Dove MB + Superbowl

Dove_MB_Superbowl = df[df['Brand'].isin(['Dove'])]
Dove_MB_Superbowl.to_excel("INC17_Dove Masterbrand+Superbowl_Raw_Data_17062024.xlsx",index=True)

#6.Degree Deo

Degree_Deo = df[df['Brand'].isin(['Degree','Degree Men','Degree Women'])]
Degree_Deo_1 = Degree_Deo[Degree_Deo['Category'].isin(['Deodorants','Personal Wash'])]
Degree_Deo_1.to_excel("INC13_Degree Deo_Raw_Data_17062024.xlsx",index=True)

#7.Axe Deo

Axe_Deo = df[df['Brand'].isin(['Axe'])]
Axe_Deo_1 = Axe_Deo[Axe_Deo['Category'].isin(['Deodorants','Hair Care','Personal Wash'])]
Axe_Deo_1.to_excel("INC13_Axe Deo_Raw_Data_17062024.xlsx",index=True)

#8.DMC Deo

DMC_Deo = df[df['Brand'].isin(['Dove Men+Care'])]
DMC_Deo_1 = DMC_Deo[DMC_Deo['Category'].isin(['Deodorants'])]
DMC_Deo_1.to_excel("INC15_DMC Deo_Raw_Data_17062024.xlsx",index=True)

#9.DMC PW

DMC_PW = df[df['Brand'].isin(['Dove Men+Care'])]
DMC_PW_1 = DMC_PW[DMC_PW['Category'].isin(['Personal Wash'])]
DMC_PW_1.to_excel("INC15_DMC PW_Raw_Data_17062024.xlsx",index=True)

# #10.Deo Dove

Dove_Deo = df[df['Brand'].isin(['Dove'])]
Dove_Deo_1 = Dove_Deo[Dove_Deo['Category'].isin(['Deodorants'])]
Dove_Deo_1.to_excel("INC17_Dove Deo_Raw_Data_21062024.xlsx",index=True)

#11.PW Dove

Dove_PW = df[df['Brand'].isin(['Dove'])]
Dove_PW_1 = Dove_PW[Dove_PW['Category'].isin(['Personal Wash'])]
Dove_PW_1.to_excel("INC17_Dove PW_Raw_Data_17062024.xlsx",index=True)

# #12.Scale

# Scale = df[df['Brand'].isin(['Scale'])]
# Scale.to_excel("Scale_Raw_Data_17062024.xlsx",index=True)

# #prisma Campaign Name :
# print(df.columns)
# # Selecting columns Prisma_Campaign_Secondary, Category, and Brand
# unique_prisma_campaign_secondary = df[['Prisma_Campaign_Secondary', 'Category', 'Brand']].drop_duplicates()

# # Copying the selected DataFrame to a new DataFrame (if necessary, .copy() is not needed here)
# unique_df = unique_prisma_campaign_secondary.copy()

# # Saving to an Excel file without the index
# unique_df.to_excel('unique_prisma_campaign_secondary_1.xlsx', index=False)