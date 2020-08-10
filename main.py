import sys
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pickle

def get_user_input():
    option = int(input("There are several options you can choose in our tracker. They include\n 1.) Showing the number of cases and deaths across the U.S. counties in a single day\n 2.) Comparing the cases and mortalities in a single county\n 3.) Comparing the cases of 2 different counties\n 4.) Comparing the mortalities of 2 different counties\n 5.) Graphing the cases in a single county over time, or\n 6.) Graphing the mortalities in a single county over time\n Which would you like to do? Please select a number from 1 to 6. "))

    if option == 1:
        date = input("Which day's data do you wish to select? Enter in the following numeric form: month/day/year, where months and days less than ten are represented with a zero before them. ")
        user_response = str(date).replace("/", "")
        all_counties(user_response)

    elif option == 2:
        user_response = int(input("Select the county whose cases and mortalities you wish to track. "))
        one_state_cases_and_mortalities_comparison(user_response)

    elif option == 3:
        user_response_1 = int(input("Select the first county whose cases you wish to compare. "))
        user_response_2 = int(input("Select the second county whose cases you wish to compare. "))
        cases_comparison(user_response_1, user_response_2)

    elif option == 4:
        user_response_1 = int(input("Select the first county whose mortalities you wish to compare. "))
        user_response_2 = int(input("Select the second county whose mortalities you wish to compare. "))
        mortality_comparison(user_response_1, user_response_2)

    elif option ==5:
        user_response = int(input("Choose the county whose cases you wish to graph. "))
        one_county_cases(user_response)
    
    elif option == 6:
        user_response = int(input("Choose the county whose mortalities you wish to graph. "))
        one_county_mortalities(user_response)
        

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


def all_counties(user_response):
    # Gets user input (what to look at, what types of charts to make).
    # Asks the user if they wish to continue using the program (exits if no, loops if yes)
    # Implement loop using if/else structure.


    fig = go.Figure(data=[
        go.Bar(name="Positive Covid Cases", x=df['county'], y=df['tstpos_' + str(user_response)]),
        go.Bar(name="Confirmed Covid Deaths", x=df['county'], y=df['mort_'+str(user_response)])
     ],
        layout=go.Layout(
            title = "Covid Data U.S.",
            yaxis_title = "Number of Covid Cases/Deaths",
            xaxis_title = "Counties"
        )
    )

    fig.update_layout(barmode='stack')
    fig.show()


def one_county_cases(user_response):
    county = str(counties[user_response])
    fig = px.line(df2, x="Date", y=county,
                     labels={
                         "Date": "Dates",
                         county: "Cases",
                     },
                     title= county+ ' Covid Cases Over Time')
    fig.show()


def one_county_mortalities(user_response):
    county = str(counties[user_response])
    fig = px.line(df3, x="Date", y=county,
                  labels={
                      "Date": "Dates",
                      county: "Mortalities",
                  },
                  title=county + ' Covid Mortalities Over Time')
    fig.show()

def cases_comparison(user_response_1, user_response_2):
    county1 = str(counties[user_response_1])
    county2 = str(counties[user_response_2])
    fig = go.Figure(data=[
        go.Scatter(name=county1 + " Cases", x=df2['Date'], y=df2[county1]),
        go.Scatter(name=county2 + " Cases", x=df2['Date'], y=df2[county2]),
    ],
        layout=go.Layout(
            title="Cases Comparison: " + county1 + " and " + county2,
            yaxis_title="Cases",
            xaxis_title="Dates"
        )
    )
    fig.show()

def mortality_comparison(user_response_1, user_response_2):
    county1 = str(counties[user_response_1])
    county2 = str(counties[user_response_2])
    fig = go.Figure(data=[
        go.Scatter(name=county1 + " Mortalities", x=df3['Date'], y=df3[county1]),
        go.Scatter(name=county2 + " Mortalities", x=df3['Date'], y=df3[county2]),
    ],
        layout=go.Layout(
            title="Mortalities Comparison: " + county1 + " and " + county2,
            yaxis_title="Mortalities",
            xaxis_title="Dates"
        )
    )
    fig.show()

def one_state_cases_and_mortalities_comparison(user_response):
    county_name =  str(counties[user_response])

    fig = go.Figure(data=[
        go.Scatter(name=county_name + " Cases", x=df2['Date'], y=df2[county_name]),
        go.Scatter(name=county_name +" Mortalities", x=df3['Date'], y=df3[county_name]),
    ],
        layout=go.Layout(
            title="Cases and Mortalities Comparison: " + county_name,
            yaxis_title="Number of Cases/ Mortalities",
            xaxis_title="Dates"
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

df = pd.read_csv(csv_file_1)
df2 = pd.read_csv(csv_file_2)
df3 = pd.read_csv(csv_file_3)


run_program()
