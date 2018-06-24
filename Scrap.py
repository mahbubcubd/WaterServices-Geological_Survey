# start_date = input("Input the start date: ")
# end_date = input("Input the End date: ")
# url = "https://waterservices.usgs.gov/nwis/dv/?format=json&sites=09519000&startDT=" + start_date + "&endDT=" + end_date + "&siteStatus=all"
# print("The url is ", url)
import requests
import json
import csv
import datetime


def save_csv(json_url, site_location, start_date, end_date,
             site_name, average_first_date, average_per_day,
             average_first_qualifier, average, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['JSON URL', 'Site Location', 'Start Date', 'End Date', 'Site Name',
                      'Date of Average Value', 'Average Value Per Day', 'Qualifier']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'JSON URL': json_url, 'Site Location': site_location, 'Start Date': start_date, 'End Date':
                        end_date, 'Site Name': site_name, 'Date of Average Value': average_first_date,
                         'Average Value Per Day': average_per_day, 'Qualifier': average_first_qualifier[0]})
        for i in range(1, len(average)):
            av = average[i]['value']
            qf = average[i]['qualifiers']
            dt = average[i]['dateTime']
            writer.writerow({'JSON URL': '', 'Site Location': '', 'Start Date': '', 'End Date': '', 'Site Name': '',
                             'Date of Average Value': dt, 'Average Value Per Day': av, 'Qualifier': qf[0]})

        print("Congratulations,\n Your CSV has been successfully saved. Bingo!!! \n")


def instruction(json_url, site_location, start_date, end_date,
                site_name, average_first_date, average_per_day,
                average_first_qualifier, average, filename):
    asking = input("Do you want to save the file now? (Y/N): \n")
    if asking == 'y' or asking == 'Y':
        save_csv(json_url, site_location, start_date, end_date,
                 site_name, average_first_date, average_per_day,
                 average_first_qualifier, average, filename)

    elif asking == 'n' or asking == 'N':
        print("OK, Terminating the script")
    else:
        print("Please select Y or N")
        instruction(json_url, site_location, start_date, end_date,
                    site_name, average_first_date, average_per_day,
                    average_first_qualifier, average, filename)


def try_again():
    one_more = input("Do you want to try again? (Y/N) \n")
    if one_more == 'Y' or one_more == 'y':
        handle_all()
    elif one_more == 'N' or one_more == 'n':
        print("Thank You. Bye")
    else:
        try_again()


def validate_date():
    user_input_start_date = input("Please Input start Date with proper date format (YYYY-MM-DD): \n")
    user_input_end_date = input("Please Input End Date with proper date format (YYYY-MM-DD): \n")
    try:
        datetime.datetime.strptime(user_input_start_date, '%Y-%m-%d')
        datetime.datetime.strptime(user_input_end_date, '%Y-%m-%d')
        url = "https://waterservices.usgs.gov/nwis/dv/?format=json&sites=09519000&startDT=" + user_input_start_date \
              + "&endDT=" + user_input_end_date + "&siteStatus=all"
        return url
    except ValueError:
        print("Incorrect date format, should be YYYY-MM-DD. For example: 2018-05-06 \n")
        validate_date()


def handle_all():
    try:
        url = validate_date()
        data = json.loads((requests.get(url)).content)
        json_url = data['value']['queryInfo']['queryURL']
        site_location = data['value']['queryInfo']['criteria']['locationParam']
        start_date = data['value']['queryInfo']['criteria']['timeParam']['beginDateTime']
        end_date = data['value']['queryInfo']['criteria']['timeParam']['endDateTime']
        site_name = data['value']['timeSeries'][0]['sourceInfo']['siteName']
        average_first_date = data['value']['timeSeries'][0]['values'][0]['value'][0]['dateTime']
        average_per_day = data['value']['timeSeries'][0]['values'][0]['value'][0]['value']
        average_first_qualifier = data['value']['timeSeries'][0]['values'][0]['value'][0]['qualifiers']
        average = data['value']['timeSeries'][0]['values'][0]['value']
        filename = input("Please Insert the csv file name: \n")
        filename = filename + ".csv"
        instruction(json_url, site_location, start_date, end_date,
                    site_name, average_first_date, average_per_day,
                    average_first_qualifier, average, filename)
        try_again()
    except ValueError:
        print("Data Parsing Error. Please check the date you have just input")


handle_all()






