# Main Code #

# Importing modules #

import PySimpleGUI as sg
import webbrowser
import sys
import sqlite3

# Increasing the recursion limit #

sys.setrecursionlimit(10000)

sg.theme('DarkBlue4')


# Function to check validation of user inputs #
def validate(values):
    # Establishing connection to the sqlite database #

    conn = sqlite3.connect('Student_Database.db')

    cur = conn.cursor()

    # Check if user input exists in the database #

    cur.execute('SELECT * FROM Students WHERE FirstName=? AND LastName=? AND Grade=? AND Email=? AND Staff=?', (values['-FIRSTNAME-'], values['-LASTNAME-'], values['-GRADE-'], values['-EMAIL-'], values['role']))

    result = cur.fetchone()

    # Close the database connection #
    cur.close()
    conn.close()

    return result


# fetch all data from the Events table #
def all_event():
    # Establishing connection to the sqlite database #
    conn = sqlite3.connect('Student_Database.db')

    cur = conn.cursor()

    # Fetch all datas from the Events table #

    cur.execute('SELECT * FROM Events ORDER BY dates ASC')  # Sort it by the date
    data = cur.fetchall()

    data = [row[1:] for row in data]  # Don't want the primary key

    cur.close()
    conn.close()

    return data


# fetch data from database for specific table and record #
def fetch_data(values, table):
    # Establishing connection to the sqlite database #

    conn = sqlite3.connect('Student_Database.db')

    cur = conn.cursor()

    # Fetch data depends on which table needed #

    if table == "Students":
        cur.execute('SELECT * FROM Students WHERE FirstName=? AND LastName=? AND Grade=? AND Email=? AND Staff=?', (values['-FIRSTNAME-'], values['-LASTNAME-'], values['-GRADE-'], values['-EMAIL-'], values['role']))
    else:
        cur.execute('SELECT * FROM Events WHERE EventName=? AND Location=? AND Dates=? AND Points=? AND Description=?', (values['-EVENT-'], values['-LOCATION-'], values['-DATE-'], values['-POINTS-'], values['-DESC-']))
    result = cur.fetchone()

    return result


# Update the database #
def insert_event(event_list):
    # Establishing connection to the sqlite database #

    conn = sqlite3.connect('Student_Database.db')

    cur = conn.cursor()

    # Update the database #

    cur.execute('INSERT INTO Events (EventName, Location, Dates, Points, Description) VALUES (?, ?, ?, ?, ?)', event_list)

    conn.commit()

    cur.close()
    conn.close()


# Inputs for information on the event staff wish to add #
def create_event():
    # Setting up the layout #

    layout = [[sg.Text('Event Name: '), sg.InputText(key='-EVENT-')],
              [sg.Text('Location: '), sg.InputText(key='-LOCATION-')],
              [sg.Text('Date: '), sg.InputText(key='-DATE-')],
              [sg.Text('Points Worth: '), sg.InputText(key='-POINTS-')],
              [sg.Text('Description: '), sg.InputText(key='-DESC-')],
              [sg.Button('Add'), sg.Button('Cancel')]]

    c_window = sg.Window('Add Event', layout)

    event_list = []

    while True:
        event, values = c_window.read()
        if event in (sg.WINDOW_CLOSED, 'Cancel'):
            break
        if event in (sg.Window, 'Add'):
            # Make sure user can't provide uncompleted/invalid input #
            if 0 in [len(values['-EVENT-']), len(values['-LOCATION-']), len(values['-DATE-']), len(values['-POINTS-']), len(values['-DESC-'])] or len(values['-DATE-']) != 10:
                sg.popup("Error: Invalid Event Information")
            else:
                # Append the user inputs into a list #
                event_name = values['-EVENT-']
                location = values['-LOCATION-']
                date = values['-DATE-']
                points = values['-POINTS-']
                description = values['-DESC-']
                event_list.append(event_name)
                event_list.append(location)
                event_list.append(date)
                event_list.append(points)
                event_list.append(description)
                insert_event(event_list)  # update the database according to the list
                break

    c_window.close()

    return event_list


# Current Quarter Stat Configure Page # ** Unfinished **
def sta_stat():
    # Setting up the layout #

    layout = [[]]

    s_window = sg.Window('Configure Quarter Stats', layout, size=(500, 500))


# Current Quarter Stat Page # ** Unfinished **
def stu_stat(result):
    # Setting up the layout #

    layout = [[sg.Text("Your score:"), sg.Text(result[1])],
              [sg.Text("Went to an Event?")],
              [sg.Text("Verify here:")],
              [sg.InputText(key="-EVENT-", tooltip="Enter Event Name"), sg.InputText(key="-CODE-", tooltip="Enter Attendance Code")],
              [sg.Push(), sg.Button("Back to Dashboard")]]

    s_window = sg.Window('Quarter Statistic', layout, size=(500, 500))

    # Event loop #
    while True:
        event, values = s_window.read()
        if event in (sg.WINDOW_CLOSED, "Back to Dashboard"):
            break

    s_window.close()


# Staff Profile Page #
def sta_profile(result):
    # Setting up the layout and staff information #

    layout = [[sg.Text("Staff Profile")],
              [sg.Text("First Name:"), sg.Text(result[1])],
              [sg.Text("Last Name:"), sg.Text(result[2])],
              [sg.Text("Staff Email:"), sg.Text(result[5])],
              [sg.Push(), sg.Button("Back to Dashboard")]]

    p_window = sg.Window('Staff Profile', layout, size=(500, 500))

    # Event loop #
    while True:
        event, values = p_window.read()
        if event in (sg.WINDOW_CLOSED, "Back to Dashboard"):
            break

    p_window.close()


# Student Profile Page #
def stu_profile(result):
    # Setting up the layout and student information #

    layout = [[sg.Text("Student Profile")],
              [sg.Text("First Name:"), sg.Text(result[1])],
              [sg.Text("Last Name:"), sg.Text(result[2])],
              [sg.Text("Grade:"), sg.Text(result[3])],
              [sg.Text("Student Email:"), sg.Text(result[5])],
              [sg.Text("Current Quarter Points Earned:"), sg.Text(result[4])],
              [sg.Push(), sg.Button("Back to Dashboard")]]

    p_window = sg.Window('Student Profile', layout, size=(500, 500))

    # Event loop #
    while True:
        event, values = p_window.read()
        if event in (sg.WINDOW_CLOSED, "Back to Dashboard"):
            break

    p_window.close()


# Staff Dashboard Page #
def sta_dashboard(result):
    # Setting up the layout #

    data = all_event()  # Obtain all data in the event table

    layout = [[sg.Text("Staff Dashboard")],
              [sg.Button("Staff Profile"), sg.Button("Quarter Summary")],
              [sg.Text("Configure Events")],
              [sg.Table(values=data, headings=['EventName', 'Location', 'Date', 'Points', 'Description'], key='-EVENT-')],
              [sg.Button("+", tooltip=" Add New Event "), sg.Push(), sg.Button("Back to Login")]]

    d_window = sg.Window('Staff Dashboard', layout, size=(500, 500))

    # Event loop #
    while True:
        refresh_data = all_event()  # Obtain new data in the event table
        event, values = d_window.read()
        if event in (sg.WINDOW_CLOSED, "Back to Login"):
            back = 'back'
            break
        if event in (d_window, "+"):  # Creating new events
            new_event = create_event()
            if new_event:
                refresh_data.append(new_event)
                d_window['-EVENT-'].update(values=refresh_data)
        if event in (d_window, "Staff Profile"):
            sta_profile(result)  # Load Staff Profile Page
        if event in (d_window, "Quarter Summary"):
            sta_stat()  # Load Quarter Summary Page

    d_window.close()

    return back


# Student Dashboard Page #
def stu_dashboard(result):
    # Setting up the layout #

    data = all_event()  # Obtain all data in the event table

    layout = [[sg.Text("Student Dashboard")],
              [sg.Button("Student Profile"), sg.Button("Quarter Summary")],
              [sg.Text("Upcoming Events")],
              [sg.Table(values=data, headings=['EventName', 'Location', 'Date', 'Points'], key='-EVENT-')],
              [sg.Button("Refresh")],
              [sg.Button("Back to Login")]]

    d_window = sg.Window('Student Dashboard', layout, size=(500, 500))

    # Event loop #
    while True:
        event, values = d_window.read()
        if event in (sg.WINDOW_CLOSED, "Back to Login"):
            back = 'back'
            break
        if event in (d_window, "Refresh"):  # Refresh the upcoming event table
            data = all_event()
            d_window['-EVENT-'].update(values=data)
        if event in (d_window, "Student Profile"):
            stu_profile(result)  # Load Student Profile Page #
        if event in (d_window, "Quarter Summary"):
            stu_stat(fetch_data(result, "Students"))  # Load Quarter Summary Page #

    d_window.close()

    return back


# Help Page #
def help_center():
    # Setting up the layout #

    layout = [[sg.Text("Help Center")],
              [sg.Text("Diamond Bar High School Events")],
              [sg.Text("DBHS has unlimited amount of thrilling events to offer, \nwhether its sport, games, music, or performance, DBHS has it all!")],
              [sg.Text("DBHS Home Page", text_color="#0000EE", enable_events=True, key="-URL1-")],
              [sg.Text("Feedback", text_color="#0000EE", enable_events=True, key="-URL2-")],
              [sg.Button("Done")]]

    h_window = sg.Window('Help Center', layout, size=(300, 200), finalize=True)
    h_window["-URL1-"].set_cursor("hand2")
    h_window["-URL2-"].set_cursor("hand2")

    # Event loop #
    while True:
        event, values = h_window.read()

        if event == '-URL1-':
            webbrowser.open("https://dbhs.wvusd.k12.ca.us/")  # Takes you to DBHS Home Page
        if event == '-URL2-':
            webbrowser.open(
                "https://docs.google.com/forms/d/e/1FAIpQLSfFeVzJI_K76JbflZy4KPwTD7KWHnlBX8KGToIr99HcjMQu3g/viewform"
                "?usp=pp_url/")  # Takes you to Feedback form
        if event in (sg.WINDOW_CLOSED, "Done"):
            break

    h_window.close()


# Login Page #
def login():
    # Setting up the layout #

    layout = [[sg.Text("Welcome to DBHS Event System!")],
              [sg.Text("Please enter your first and last name:")],
              [sg.Input(key="-FIRSTNAME-", size=10, tooltip=" First Name "), sg.Input(key="-LASTNAME-", size=10, tooltip=" Last Name ")],
              [sg.Radio("Student", 'role', key='-STUDENT-', default=False), sg.Radio("Staff", 'role', key='-STAFF-', default=False)],
              [sg.Text("Grade:"), sg.Combo(["Freshman", "Sophomore", "Junior", "Senior"], key='-GRADE-', tooltip=" Ignore if you are a staff! ")],
              [sg.Text("School Email:"), sg.Input(key="-EMAIL-", tooltip=" Please enter DISTRICT EMAIL!")],
              [sg.Button("Next"), sg.Button("Exit")],
              [sg.Push(), sg.Button("Help")]]
#              [sg.Image(filename='DBHS_Brahma.png')]]

    l_window = sg.Window('DBHS Involvement System', layout, size=(400, 400))

    # Event loop #
    while True:
        event, values = l_window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event in (sg.Window, "Help"):
            help_center()
        # Make sure user can't select both radio button at once #
        if event.startswith('role'):
            if values['role'] == 'Student':
                l_window['Staff 2'].update(False)
            elif values['role'] == 'Staff':
                l_window['Student'].update(False)
        if event in (sg.Window, "Next"):
            # Check if user has left his/her role blank #
            if values['-STUDENT-'] is False and values['-STAFF-'] is False:
                sg.popup("Error: Invalid Login Credentials")
            elif values['-STUDENT-']:  # Check if user is a student
                values['role'] = 'No'
                if validate(values):
                    result = fetch_data(values, "Students")  # Information needed for Profile
                    l_window.disappear()
                    if stu_dashboard(result) == "back":  # Sends user to student dashboard
                        l_window.reappear()
                else:
                    sg.popup("Error: Invalid Student Login Credentials")
            else:  # user is a staff
                values['role'] = 'Yes'
                if len(values['-GRADE-']) == 0:
                    values['-GRADE-'] = "Staff"  # Check if user is a staff
                    if validate(values):
                        result = fetch_data(values, "Students")  # Information needed for Profile
                        l_window.disappear()
                        if sta_dashboard(result) == "back":  # Sends user to staff dashboard
                            l_window.reappear()
                    else:
                        sg.popup("Error: Invalid Staff Login Credentials")
                else:
                    sg.popup("Error: Invalid Staff Login Credentials")

    l_window.close()


if __name__ == "__main__":
    login()