"""
Project Goals

Using Covid Dataset, create visualizations and information based on user input.
If user enters x state/county, program should only output for that case.
Should be able to compare aspects of different data sets

COMPLETED:
Open csv/xslx file
Parse through the file
Ask the user if they want to make another chart after the visualizations they've requested are done (yes/no). If no, program quits. If yes, the program loops.
Allow users to select one county at a time. When done, only info from that county should be displayed (y=days, x = cases/deaths)
Allow users to create graphs comparing two different counties.
Add fifth and sixth options (one state mortalities and one state cases) onto option variable in get_user_input() function
Update descriptions across functions to make each specific and clear
Find a way to import dictionary from a file to reduce file length

TO-DO:
Allow users to see the list of states and their corresponding numbers so that they can choose which one they want (need to figure out how to organize [ex. by state?])
Make functioning website that runs this code when everything else works
Reconsider which types of plots should be used for different functions (all line? stacked bar?)
Add monthly cases/mortalities for each state

"""
import sys
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pickle, os



def get_user_input():
    option = int(input("There are several options you can choose in our visualizer. They include\n 1.) Comparing the cases and mortalities in a single county\n 2.) Comparing the cases of 2 different counties\n 3.) Comparing the mortalities of 2 different counties\n 4.) Graphing the cases in a single county over time\n 5.) Graphing the mortalities in a single county over time\n 6.) Graphing the monthly cases of a single county\n 7.) Graphing the monthly mortalities of a single county\n 8.) Comparing the monthly cases of two different counties\n 9.) Comparing the monthly cases and mortalities for a sigle county, or\n 10.) Comparing the monthly mortalities of two different counties\nWhich would you like to do? Please select a number from 1 to 10. "))
    
    if option == 1:
        user_response = int(input("Select the county whose cases and mortalities you wish to track. "))
        one_county_cases_and_mortalities_comparison_daily(user_response)

    elif option == 2:
        user_response_1 = int(input("Select the first county whose cases you wish to compare. "))
        user_response_2 = int(input("Select the second county whose cases you wish to compare. "))
        cases_comparison_daily(user_response_1, user_response_2)

    elif option == 3:
        user_response_1 = int(input("Select the first county whose mortalities you wish to compare. "))
        user_response_2 = int(input("Select the second county whose mortalities you wish to compare. "))
        mortality_comparison_daily(user_response_1, user_response_2)

    elif option == 4:
        user_response = int(input("Choose the county whose cases you wish to graph. "))
        one_county_cases_daily(user_response)

    elif option == 5:
        user_response = int(input("Choose the county whose mortalities you wish to graph. "))
        one_county_mortalities_daily(user_response)

    elif option == 6:
        user_response = int(input("Choose the county whose monthly cases you wish to graph. "))
        one_county_cases_monthly(user_response)

    elif option == 7: 
        user_response = int(input("Choose the county whose montlhy mortalities you wish to graph. ")
        one_county_mortalities_monthly(user_response)

    elif option == 8:
        user_response_1 = int(input("Enter the first county whose monthly case numbers you wish to compare. "))
        user_response_2 = int(input("Enter the second county whose monthly case numbers you wish to compare. "))
        cases_comparison_monthly(user_response_1, user_response_2)

    elif option == 9:
        user_response_1 = int(input("Enter the first county whose monthly mortality numbers you wish to compare. "))
        user_response_2 = int(input("Enter the second county whose monthly mortality numbers you wish to compare. "))

    elif option == 10: 
        user_response = int(input("Select the county whose monthly cases and mortalities you wish to track. "))
        one_county_cases_and_mortalities_comparison_monthly(user_response)
    

def loop_program():
    print("Would you like to generate another chart (yes/no)?")
    response = input()
    while True:
        if response.lower() == "yes":
            run_program()
        elif response.lower() == "no":
            print("Thank you for using our COVID-19 tracker!")
            sys.exit()
        else:
            print("Invalid response. Please try again.")
            response = input()


def one_county_cases_daily(user_response):
    county = str(counties[user_response])
    fig = px.line(df2, x="Date", y=county,
                     labels={
                         "Date": "Date",
                         county: "Cases",
                     },
                     title= county+ ' Covid Cases Over Time')
    fig.show()

def one_county_cases_monthly(user_response):
    county = str(counties[user_response])
    fig = px.line(df4, x="Month", y=county,
                     labels={
                         "Month": "Month",
                         county: "Cases",
                     },
                     title= county+ ' Monthly Covid Cases')
    fig.show()


def one_county_mortalities_daily(user_response):
    county = str(counties[user_response])
    fig = px.line(df3, x="Date", y=county,
                  labels={
                      "Date": "Date",
                      county: "Mortalities",
                  },
                  title=county + ' Covid Mortalities Over Time')
    fig.show()

def one_county_mortalities_monthly(user_response):
    county = str(counties[user_response])
    fig = px.line(df5, x="Month", y=county,
                     labels={
                         "Date": "Month",
                         county: "Mortalities",
                     },
                     title= county+ ' Monthly Covid Cases')
    fig.show()

def cases_comparison_daily(user_response_1, user_response_2):
    county1 = str(counties[user_response_1])
    county2 = str(counties[user_response_2])
    fig = go.Figure(data=[
        go.Scatter(name=county1 + " Cases", x=df2['Date'], y=df2[county1]),
        go.Scatter(name=county2 + " Cases", x=df2['Date'], y=df2[county2]),
    ],
        layout=go.Layout(
            title="Cases Comparison: " + county1 + " and " + county2,
            yaxis_title="Cases",
            xaxis_title="Date"
        )
    )
    fig.show()

def cases_comparison_monthly(user_response_1, user_response_2):
    county1 = str(counties[user_response_1])
    county2 = str(counties[user_response_2])
    fig = go.Figure(data=[
        go.Scatter(name=county1 + " Cases", x=df4['Month'], y=df4[county1]),
        go.Scatter(name=county2 + " Cases", x=df4['Month'], y=df4[county2]),
    ],
        layout=go.Layout(
            title="Monthly Cases Comparison: " + county1 + " and " + county2,
            yaxis_title="Cases",
            xaxis_title="Month"
        )
    )
    fig.show()

def mortality_comparison_daily(user_response_1, user_response_2):
    county1 = str(counties[user_response_1])
    county2 = str(counties[user_response_2])
    fig = go.Figure(data=[
        go.Scatter(name=county1 + " Mortalities", x=df3['Date'], y=df3[county1]),
        go.Scatter(name=county2 + " Mortalities", x=df3['Date'], y=df3[county2]),
    ],
        layout=go.Layout(
            title="Mortalities Comparison: " + county1 + " and " + county2,
            yaxis_title="Mortalities",
            xaxis_title="Date"
        )
    )
    fig.show()

def mortality_comparison_monthly(user_response_1, user_response_2):
    county1 = str(counties[user_response_1])
    county2 = str(counties[user_response_2])
    fig = go.Figure(data=[
        go.Scatter(name=county1 + " Mortalities", x=df5['Month'], y=df5[county1]),
        go.Scatter(name=county2 + " Mortalities", x=df5['Month'], y=df5[county2]),
    ],
        layout=go.Layout(
            title="Monthly Mortalities Comparison: " + county1 + " and " + county2,
            yaxis_title="Mortalities",
            xaxis_title="Date"
        )
    )
    fig.show()

def one_county_cases_and_mortalities_comparison_daily(user_response):
    county_name =  str(counties[user_response])

    fig = go.Figure(data=[
        go.Scatter(name=county_name + " Cases", x=df2['Date'], y=df2[county_name]),
        go.Scatter(name=county_name +" Mortalities", x=df3['Date'], y=df3[county_name]),
    ],
        layout=go.Layout(
            title="Cases and Mortalities Comparison: " + county_name,
            yaxis_title="Number of Cases/ Mortalities",
            xaxis_title="Date"
        )
    )
    fig.show()

def one_county_cases_and_mortalities_comparison_monthly(user_response):
    county_name =  str(counties[user_response])

    fig = go.Figure(data=[
        go.Scatter(name=county_name + " Monthly Cases", x=df4['Month'], y=df4[county_name]),
        go.Scatter(name=county_name +" Monthly Mortalities", x=df5['Month'], y=df5[county_name]),
    ],
        layout=go.Layout(
            title="Cases and Mortalities Comparison: " + county_name,
            yaxis_title="Number of Cases/ Mortalities",
            xaxis_title="Date"
        )
    )
    fig.show()

def run_program():
    get_user_input()
    loop_program()

counties = pickle.load(open("counties.p", "rb"))
csv_file_1 = "Coronavirus_by_County_20200715.csv"
csv_file_2 = "Coronavirus_By_County POSITIVE CASES.csv"
csv_file_3 = "Coronavirus_By_County CONFIRMED MORTALITIES.csv"
csv_file_4 = "Coronavirus_By_County_MONTHLY_CASE_NUMBERS.csv"
csv_file_5 = "Coronavirus_By_County_MONTHLY_MORTALITY_NUMBERS.csv"

os.getcwd()
os.chdir(r"C:\Users\steve\PycharmProjects\COVID-19 Project")

df = pd.read_csv(csv_file_1)
df2 = pd.read_csv(csv_file_2)
df3 = pd.read_csv(csv_file_3)
df4 = pd.read_csv(csv_file_4)
df5 = pd.read_csv(csv_file_5)

print("Welcome to our COVID-19 visualizer!")
run_program()

