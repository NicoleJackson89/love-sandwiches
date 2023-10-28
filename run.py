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

        data_str = input("Enter your data here: ")

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


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated sucessfully.\n")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)
