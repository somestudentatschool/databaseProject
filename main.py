# Requires PySimpleGUI package to be installed.

# Note: Intentionally doesn't save the database changes between program runs!
#       This is so you can test your database against our program without making you change everything in the database
#       back for the next group. Everything still works locally as normal.

import datetime

import PySimpleGUI as gui
import os
import sqlite3 as sql


CAR_TYPE = {
    "compact": 1,
    "medium": 2,
    "large": 3,
    "suv": 4,
    "truck": 5,
    "van": 6,
}

CATEGORY = {
    "basic": 0,
    "luxury": 1,
}

RENTAL_TYPE = {
    "daily": 1,
    "weekly": 7,
}


connection = sql.connect("car.db")


def main():
    layout = [
        [gui.Text("Main", key="MAIN_MENU_TEXT")],
        [gui.Button("Add New Customer", key="ADD_CUSTOMER_BUTTON")],
        [gui.Button("Add New Vehicle", key="ADD_VEHICLE_BUTTON")],
        [gui.Button("Rent Car", key="RENT_CAR_BUTTON")],
        [gui.Button("Return Car", key="RETURN_CAR_BUTTON")],
        [gui.Button("View Customers", key="VIEW_CUSTOMERS_BUTTON")],
        [gui.Button("View Vehicles", key="VIEW_VEHICLES_BUTTON")],
    ]

    window = gui.Window("Main Menu", layout)
    while True:
        event, values = window.read()
        if event == "EXIT" or event == gui.WIN_CLOSED:
            break

        if event == "ADD_CUSTOMER_BUTTON":
            window_add_customer()
        elif event == "ADD_VEHICLE_BUTTON":
            window_add_vehicle()
        elif event == "RENT_CAR_BUTTON":
            window_rent_car()
        elif event == "RETURN_CAR_BUTTON":
            window_return_car()
        elif event == "VIEW_CUSTOMERS_BUTTON":
            window_view_customers()
        elif event == "VIEW_VEHICLES_BUTTON":
            window_view_vehicles()

    # return_car(window, "G. Clarkson", "WDCGG0EB0EG188709", "2019-11-15")

    window.close()
    pass


def window_add_customer():
    instructions = "Input customer info:"

    layout = [
        [gui.Text(instructions)],
        [gui.Text("Name"), gui.InputText(key="NAME")],
        [gui.Text("Phone"), gui.InputText(key="PHONE")],
        [gui.Submit(key="SUBMIT")]
    ]

    window = gui.Window("Add New Customer", layout)
    while True:
        event, values = window.read()
        if event == "EXIT" or event == gui.WIN_CLOSED:
            break

        if event == "SUBMIT":
            name = values["NAME"]
            phone = values["PHONE"]
            add_new_customer(name, phone)

        pass
    window.close()
    pass


def window_add_vehicle():
    instructions = "Input vehicle info:"

    layout = [
        [gui.Text(instructions)],
        [gui.Text("Description"), gui.InputText(key="DESCRIPTION")],
        [gui.Text("Year"), gui.InputText(key="YEAR")],
        [gui.Text("Type"), gui.InputText(key="TYPE")],
        [gui.Text("Category"), gui.InputText(key="CATEGORY")],
        [gui.Submit(key="SUBMIT")]
    ]

    window = gui.Window("Add New Vehicle", layout)
    while True:
        event, values = window.read()
        if event == "EXIT" or event == gui.WIN_CLOSED:
            break

        if event == "SUBMIT":
            description = values["DESCRIPTION"]
            year = int(values["YEAR"])
            try:
                type = int(values["TYPE"])
            except:
                type = CAR_TYPE[values["TYPE"].lower()]
            try:
                category = int(values["CATEGORY"])
            except:
                category = CATEGORY[values["CATEGORY"].lower()]

            add_new_vehicle(description, year, type, category)

        pass
    window.close()
    pass


def window_rent_car():
    instructions = "Input rental info:"
    footnote = "* are required fields."

    layout = [
        [gui.Text(instructions)],
        [gui.Text("Customer ID"), gui.InputText(key="CUSTOMER_ID")],
        [gui.Text("Car Type"), gui.InputText(key="TYPE")],
        [gui.Text("Car Category"), gui.InputText(key="CATEGORY")],
        [gui.Text("Start Date"), gui.InputText(key="CATEGORY")],
        [gui.Text("Rental Type"), gui.InputText(key="RENTAL_TYPE")],
        [gui.Text("Rental Periods"), gui.InputText(key="QTY")],
        [gui.Checkbox("Pay Now", key="PAY_NOW", default=False)],
        [gui.Submit(key="SUBMIT")],
        # [gui.Text(footnote)],
    ]

    window = gui.Window("Rent Car", layout)
    while True:
        event, values = window.read()
        if event == "EXIT" or event == gui.WIN_CLOSED:
            break

        if event == "SUBMIT":
            cid = int(values["CUSTOMER_ID"])
            try:
                car_type = int(values["TYPE"])
            except:
                car_type = CAR_TYPE[values["TYPE"].lower()]
            try:
                category = int(values["CATEGORY"])
            except:
                category = CATEGORY[values["CATEGORY"].lower()]
            start_date = values["START_DATE"]
            try:
                rental_type = int(values["RENTAL_TYPE"])
            except:
                rental_type = RENTAL_TYPE[values["RENTAL_TYPE"].lower()]
            qty = int(values["QTY"])
            payment_date = None
            if values["PAY_NOW"] is True:
                payment_date = datetime.datetime.today().date().strftime("%y-%m-%d")

            rent_car(cid, car_type, category, start_date, rental_type, qty, payment_date)
            pass

        pass
    window.close()
    pass


def window_return_car():
    instructions = "Input rental info:"
    footnote = "Note: Vehicle Info can be the Vehicle ID or the Description.\n" \
               "Partial matching is enabled for Customer Name and Vehicle Info."

    layout = [
        [gui.Text(instructions)],
        [gui.Text("Customer Name"), gui.InputText(key="CUSTOMER_NAME")],
        [gui.Text("Vehicle Info"), gui.InputText(key="VEHICLE_INFO")],
        [gui.Text("Return Date"), gui.InputText(key="RETURN_DATE")],
        [gui.Submit(key="SUBMIT")],
        [gui.Text(footnote)],
    ]

    window = gui.Window("Rent Car", layout)
    while True:
        event, values = window.read()
        if event == "EXIT" or event == gui.WIN_CLOSED:
            break

        if event == "SUBMIT":
            customer_name = values["CUSTOMER_NAME"]
            vehicle_info = values["VEHICLE_INFO"].upper()
            return_date = values["RETURN_DATE"]

            return_car(customer_name, vehicle_info, return_date)
            pass

        pass
    window.close()
    pass


def window_view_customers():
    instructions_text = "Enter a filter, or leave blank, and press submit.\n" \
                        "The filter should be formatted like a Where\n" \
                        "statement (without the \"WHERE\" keyword)."
    footnote = "Note: to do partial matching, you should use\n" \
               "the LIKE keyword in the filter.\n" \
               "Ex. Name LIKE \"G. Cl%\" (gets G. Clarkson)"

    left_layout = [
        [gui.Text(instructions_text)],
        [gui.Text("Filter"), gui.InputText(key="FILTER")],
        [gui.Submit(key="SUBMIT"), gui.Cancel("Clear", key="CLEAR")],
        [gui.Text(footnote)],
    ]
    right_layout = [
        [gui.Table([], headings=["Customer ID (CustID)", "Customer Name (Name)", "Total Balance"], key="TABLE")]
    ]
    layout = [
        [
            gui.Column(left_layout),
            gui.VSeparator(),
            gui.Column(right_layout),
        ]
    ]

    window = gui.Window("View Customers", layout)
    while True:
        event, values = window.read()
        if event == "EXIT" or event == gui.WIN_CLOSED:
            break

        if event == "SUBMIT":
            customers = get_customers(values["FILTER"])
            window["TABLE"].update(customers)
        elif event == "CLEAR":
            window["TABLE"].update([])

        pass
    window.close()
    pass


def window_view_vehicles():
    instructions_text = "Enter a filter, or leave blank, and press submit.\n" \
                        "The filter should be formatted like a Where\n" \
                        "statement (without the \"WHERE\" keyword)."
    footnote = "Note: to do partial matching, you should use\n" \
               "the LIKE keyword in the filter.\n" \
               "Ex. Description LIKE \"%BMW%\" (gets all BMWs)"

    left_layout = [
        [gui.Text(instructions_text)],
        [gui.Text("Filter"), gui.InputText(key="FILTER")],
        [gui.Submit(key="SUBMIT"), gui.Cancel("Clear", key="CLEAR")],
        [gui.Text(footnote)],
    ]
    right_layout = [
        [gui.Table([], headings=["Vehicle ID", "Description", "Daily Average"], key="TABLE")]
    ]
    layout = [
        [
            gui.Column(left_layout),
            gui.VSeparator(),
            gui.Column(right_layout),
        ]
    ]

    window = gui.Window("View Vehicles", layout)
    while True:
        event, values = window.read()
        if event == "EXIT" or event == gui.WIN_CLOSED:
            break

        if event == "SUBMIT":
            vehicles = get_vehicles(values["FILTER"])
            window["TABLE"].update(vehicles)
        elif event == "CLEAR":
            window["TABLE"].update([])

        pass
    window.close()
    pass


def add_new_customer(name: str, phone: str):
    command = "INSERT INTO CUSTOMER (Name, Phone) " \
              "VALUES (\"" + name + "\", \"" + phone + "\")"

    cursor = connection.cursor()
    try:
        cursor.execute(command)
        gui.popup("Customer " + name + " added.")
    except:
        gui.popup("SQL Query Failed: please make sure Name and Phone are valid.")

    cursor.close()
    pass


def add_new_vehicle(description: str, year: int, type: int, category: int):
    command = "INSERT INTO VEHICLE (Description, Year, Type, Category) " \
              "VALUES (\"" + description + "\", " + str(year) + ", " + str(type) + ", " + str(category) + ")"

    cursor = connection.cursor()
    try:
        cursor.execute(command)
        gui.popup("Vehicle " + description + " added.")
    except:
        gui.popup("SQL Query Failed: please make sure the Description is valid.")

    cursor.close()
    pass


def rent_car(cid: int, v_type: int, v_category: int, start_date: str, rental_type: int, qty: int, payment_date: str = None):
    cursor = connection.cursor()

    # Order Date:
    order_date = datetime.datetime.today().date().strftime("%y-%m-%d")

    # Return Date
    s_date = datetime.datetime.strptime(start_date, "%y-%m-%d").date()
    r_date = s_date + datetime.timedelta(days=(rental_type * qty))
    return_date = r_date.strftime("%y-%m-%d")

    # Vehicle ID
    vt_command = "SELECT VehicleID " \
                 "FROM VEHICLE " \
                 "WHERE Type=" + str(v_type) + " AND Catagory=" + str(v_category)
    rv_command = "SELECT VehicleID " \
                 "FROM RENTAL " \
                 "WHERE date(StartDate) < date(\"" + return_date + "\") AND date(ReturnDate) > date(\"" + start_date + "\")"

    vehicle_table = cursor.execute(vt_command).fetchall()
    try:
        rented_table = cursor.execute(rv_command).fetchall()
    except:
        gui.popup("SQL Query Failed: make sure the start date is a valid date.")
        cursor.close()
        return
    vid = None
    for record in vehicle_table:
        if record not in rented_table:
            vid = record[0]
            break
    if vid is None:
        gui.Popup("No free vehicle of that type and category could be found.")
        return

    # Total Amount
    rate_command = "SELECT Weekly, Daily " \
                   "FROM RATE " \
                   "WHERE Type=" + str(v_type) + " AND Category=" + str(v_category)

    rate_table = cursor.execute(rate_command).fetchall()
    if len(rate_table) == 0:
        gui.Popup("No rate for vehicle of that type and category could be found.")
        return
    if rental_type == 7:
        total_amount = rate_table[0][0] * qty
    else:
        total_amount = rate_table[0][1] * qty

    # INSERT
    if payment_date is not None:
        command = "INSERT INTO RENTAL (CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate) " \
                  "VALUES (" + str(cid) + ", \"" + vid + "\", \"" + start_date + "\", \"" + order_date + "\", " + str(rental_type) + ", " + str(qty) + ", \"" + return_date + "\", " + str(total_amount) + ", \"" + payment_date + "\")"
    else:
        command = "INSERT INTO RENTAL (CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount) " \
                  "VALUES (" + str(cid) + ", \"" + vid + "\", \"" + start_date + "\", \"" + order_date + "\", " + str(rental_type) + ", " + str(qty) + ", \"" + return_date + "\", " + str(total_amount) + ")"

    try:
        cursor.execute(command)
        gui.popup("Car " + vid + " rented.")
    except:
        gui.popup("SQL Query Failed: please make sure all inputs are valid.")

    cursor.close()

    return


def return_car(customer_name: str, vehicle_info: str, return_date: str):
    cursor = connection.cursor()

    # Find rental record to change
    rental_command = "SELECT CustID, VehicleID, TotalAmount, PaymentDate " \
                     "FROM CUSTOMER " \
                     "    NATURAL JOIN RENTAL " \
                     "    NATURAL JOIN (SELECT VehicleID " \
                     "        FROM VEHICLE " \
                     "        WHERE Description LIKE \"%" + vehicle_info + "%\" " \
                     "            OR VehicleID LIKE \"" + vehicle_info + "%\") " \
                     "WHERE Name Like \"%" + customer_name + "%\" AND date(ReturnDate) = date(\"" + return_date + "\")"

    try:
        rental_table = cursor.execute(rental_command).fetchall()
    except:
        gui.popup("SQL Query Failed: please check that Customer Name and Vehicle Info has only valid characters.")
        cursor.close()
        return
    if len(rental_table) == 0:
        gui.popup("Return failed: no rental record matches the given criteria.")
        return
    elif len(rental_table) > 1:
        gui.Popup("Return failed: multiple rental records match the given criteria. Using VehicleID for vehicle info may solve the problem.")
        return
    elif rental_table[0][3] is not None and rental_table[0][3] != "NULL":
        gui.Popup("Return failed: car has already been returned.")
        return
    cid = rental_table[0][0]
    vid = rental_table[0][1]
    total_amount = rental_table[0][2]

    # Print amount due and ask for user confirmation
    answer = gui.popup_yes_no("The total amount due is " + '${:,.2f}'.format(total_amount) + ", do you accept?")

    # Apply the change
    payment_date = datetime.date.today().strftime("%y-%m-%d")
    if answer == "Yes":
        command = "UPDATE RENTAL " \
                  "SET PaymentDate=\"" + payment_date + "\" " \
                  "WHERE CustID=" + str(cid) + " AND VehicleID=\"" + vid + "\" AND date(ReturnDate)=date(\"" + return_date + "\")"
        try:
            cursor.execute(command)
            gui.popup("Car " + vid + " returned.")
        except:
            gui.popup("SQL Query Failed: please make sure the customer name and return date is valid.")
        pass

    cursor.close()

    pass


def get_customers(filter: str = ""):
    if filter == "":
        filter = "0=0"

    command = "SELECT CustID, Name, IFNULL(TotalBalance, 0) as TotalBalance " \
              "FROM CUSTOMER " \
              "    LEFT JOIN (SELECT CustID as _CustID, Name as _Name, SUM(TotalAmount) as TotalBalance " \
              "        FROM CUSTOMER " \
              "            NATURAL JOIN RENTAL " \
              "        WHERE PaymentDate IS NULL " \
              "            OR PaymentDate=\"NULL\" " \
              "        GROUP BY _CustID) ON CustID=_CustID " \
              "WHERE " + filter + " " \
              "ORDER BY TotalBalance DESC"

    cursor = connection.cursor()
    results_table = []
    try:
        results_table = cursor.execute(command).fetchall()
    except:
        gui.popup("SQL Query Failed: please check that the Filter is a valid WHERE clause.")

    for i in range(len(results_table)):
        results_table[i] = (results_table[i][0], results_table[i][1], '${:,.2f}'.format(float(results_table[i][2])))

    cursor.close()

    return results_table


def get_vehicles(filter: str = ""):
    if filter == "":
        filter = "0=0"

    command = "SELECT VehicleID as VIN, Description, IFNULL(DailyAverage, \"Non-Applicable\") as DailyAverage " \
              "FROM VEHICLE " \
              "    LEFT JOIN (SELECT VehicleID as _VIN, Description as _Description, TotalAmount / AVG(RentalType * Qty) as DailyAverage " \
              "        FROM Vehicle " \
              "            NATURAL JOIN RENTAL " \
              "        GROUP BY _VIN) ON VehicleID=_VIN " \
              "WHERE " + filter + " " \
              "ORDER BY DailyAverage ASC"

    cursor = connection.cursor()
    try:
        results_table = cursor.execute(command).fetchall()
    except:
        gui.popup("SQL Query Failed: please check that the Filter is a valid WHERE clause.")

    for i in range(len(results_table)):
        if results_table[i][2] != "Non-Applicable":
            results_table[i] = (results_table[i][0], results_table[i][1], '${:,.2f}'.format(float(results_table[i][2])))

    cursor.close()

    return results_table


if __name__ == '__main__':
    main()
    connection.close()


