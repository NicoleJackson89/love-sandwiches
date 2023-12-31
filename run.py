import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated 
    by commas. The loop will repeatedly request data until it is valid.
    """
    # while loop which ends when the correct data is entered, the returned value in the
    # validate_date funtion is used as the condition for the while loop in get_sales_data func
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: \n")

        # converts the string of data from the user into a list of values
        sales_data = data_str.split(",")

        # single if statemnet to call validate_data func passing it the sales_data list
        if validate_data(sales_data):
            print("Data is valid!")
            break  # breaks when returned true

    return sales_data  # returns the users value input


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        # converting each value to int using list comprehension
        [int(value) for value in values]
        if len(values) != 6:  # checking if values list has exactly 6 values
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False  # false if there are errors, the while loop above repeats until true

    return True  # true is returned if there are no errors


# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided.
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated sucessfully.\n")


# def update_surplus_worksheet(data):
#     """
#     Update surplus worksheet, add new row with the surplus data calculated.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated sucessfully.\n")


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_data(sales_row): #sales row list passed to the function
    """
    Compare sales with stock and calculate the surplus fro each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1] # (pulled from the sales worksheet) Accessing the last row in the stock list will slice the final item off the list and return that

    #zip allows us to itirate through 2 or more lists in a for loop
    surplus_data = [] #empty list to store the number from below
    for stock, sales in zip(stock_row, sales_row): #stock_row & sales_row is being unpacked and assigned to a variable stock and sales
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3) #rows and col start at 1 not 0
    # print(column)

    columns = []
    for ind in range(1, 7): #1 is the nr the range starts from and 7 excl the nr is where is ends
        column = sales.col_values(ind)
        columns.append(column[-5:]) #-5 to get the last 5 in each col & : is for multiple alues being sliced
    
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1 #adds 10% to the average
        new_stock_data.append(round(stock_num)) #rounds up the nrs
    
    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to love sandwiches Data Automation")
main()