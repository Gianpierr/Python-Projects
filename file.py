from tabulate import tabulate
""" 
    - Improvements to make to program: add a loop to reprompt the user to the main menu again
    - Write to a different file instead of overwriting the same file consistently     
"""

def print_menu(): # function that prints the main menu at the beginning of the program
    print(15 * '*' + ' FILE OPERATIONS ' + 15 * '*' + '\n')
    print("[1] Print the data")
    print("[2] Delete a row or column")
    print("[3] Insert a row or column")
    print("[4] Change a value in a cell")
    print("[5] Output the file in csv format")
    print()
    print(15 * '*' + ' FILE OPERATIONS ' + 15 * '*' + '\n')


def file_operations(file):  # function that performs all the operations showcased in menu
    try:
        with (open(file, "r+") as csvfile): # open the file that you want to manipulate
            print_menu()  # print menu
            choice = input("Enter a number for a specific operation: ") # store user choice in variable
            rows = csvfile.readlines()  # read the data for subsequent operations
            if choice == '1':  # user selected to output the data
                headers = rows[0].split(',')   # split the first row from the list rows to create headers for table
                table = []       # initialize list for the data
                for line in rows[1:]:
                    print(line.split(','))
                    table.append(line.split(','))  # append each line of data to a table list
                print()
                print(tabulate(table, headers = headers, tablefmt= "grid"))  # output the data neatly

            elif choice == '2':  # user selected option 2
                print("[1] Delete a row")  # prompt the user if they would like to delete a row or column
                print("[2] Delete a column")

                del_choice = input("Select an option: ")  # store user input into a choice variable

                if del_choice == '1':  # user chose to delete a row
                    print(f"Valid choices for deletion are in the range (0 - {len(rows) - 1})") # print valid inputs
                    row_choice = int(input("Enter row to be deleted: "))  # store row index to be deleted in variable
                    del rows[row_choice]  # delete the row
                    with open(file, "w+") as csvfile: # write the modified list to the existing file
                        for line in rows:
                            csvfile.write(line)

                elif del_choice == '2': # user decided to delete a column
                    print(f"Valid choices for deletion are in the range (0 - {len(rows[0].split(',')) - 1})") # print the valid inputs
                    col_choice = int(input("Enter column to be deleted: ")) # store user column choice
                    with open(file, "w+") as csvfile:
                        for line in rows:       # to delete a column, we have to split each line into a list
                            line = line.split(',') # delete the index given by the user, and join it back into a string
                            del line[col_choice]
                            csvfile.write(','.join(line)) # once the modified rows are produced, they can be written to
                                                          # the file
                else:
                    print("Incorrect input! Please enter a valid option.") # if user provides invalid indices


            elif choice == '3':  # user wants to insert a column or row
               print("[1] Insert a row")
               print("[2] Insert a column")        # prompt user for option and store into a variable
               choice = input("Select an option: ")

               if choice == '1':  # user chose to delete a row
                   cols = rows[0].split(',')  # headers column, will also be used to count the number of columns
                   row_values = input(f"Enter {len(cols)} row values (comma-separated): ") # row-values to be inserted
                   row_location = int(input(f"Index of insertion? Valid input: (0, {len(cols) - 1}): ")) # index where insertion occurs
                   with open(file, "w") as csvfile:
                       temp = []
                       for value in row_values.split(','):  # append row values to a list
                           temp.append(value.strip())
                       clean_row_values = ','.join(temp)    # cleans the input and formats the string for csv
                       rows.insert(row_location, clean_row_values + '\n') # inserts clean row into rows list
                       for line in rows:  # now write the rows list to the file
                           csvfile.write(line)

               elif choice == '2': # user wants to insert a column
                   rows = rows[:len(rows)] # only want the data because we prompt user for the header
                   col_title = input("Enter the title for new column: ") # so we do not need to include in processing
                   # input location for column to be inserted
                   col_location = int(input(f"Index of insertion? (Valid input: (0, {len(rows) - 1}): "))
                   # prompt user to enter the location of column insertion
                   column = input(f"Enter {len(rows) - 1} column values (comma-separated): ")

                   col_list = column.split(',') # split comma-separated data into a list for easier file writing
                   header_row = rows[0].split(',') # define the header list (which is the first row of the data file)
                   header_row.insert(col_location, col_title) # insert the new header in header list

                   if len(col_list)  != len(rows) - 1: # make sure the number of column values matches number of row val
                       print("Number of columns and rows do not match.") # if they don't print an error
                   else:
                       with open(file, "w+") as csvfile:
                           csvfile.write(','.join(header_row)) # write the header row list to the file
                           i = 0
                           col_list = column.split(',')  # define the column list to later write to the file
                           for line in rows[1:]:  # iterate through the data without the header row
                               if i > len(col_list) - 1:  # if i is greater than the length of column list, break
                                   break          # i is a pointer to the column values to be inserted
                                                  # so we do not want an index error where the pointer is out of range
                               line = line.split(',') # make every line into a list to easily insert a new column value
                               line.insert(col_location, col_list[i]) #insert the column value
                               line = ','.join(line)  # convert the modified (column added) list to a csv string
                               csvfile.write(line)  # write that string to the file
                               i += 1    # point to the next column value to be inserted
               else:
                   print("Incorrect input! Please enter a valid option.")
                   # if user inputs anything other than a 1 or a 2, then print error message

            elif choice == '4': # user wants to change a value in a cell
                # prompt user to insert the column they want to insert at (give valid inputs to guide user)
                col = int(input(f"Enter the column (Valid column index: 0 - {len(rows[0].split(',')) - 1}): "))
                # prompt user to input the row they want to insert at (give valid inputs to guide user)
                row = int(input(f"Enter the row (Valid row index: 0 - {len(rows) - 1}): "))
                # prompt the user for the value to be inserted at the cell specified previously
                new_value = input("Enter the value to be inserted: ")

                if 0 <= col < len(rows[0].split(','))  and 0 <= row < len(rows): # check if the inputted indices are valid
                    with open(file, "w+") as csvfile:
                        for index, line in enumerate(rows):
                            if index == row:  # if were at the row that was given by the user, we will modify
                                line = line.split(',') # split string into a list
                                line[col] = str(new_value)  # modify the old value to the new specified value
                                line = ','.join(line)    # convert list to a csv string (row)
                                csvfile.write(line)      # write that row to the file
                            else:
                                csvfile.write(line)  # if not at the specified index, just write the row as is.


                else:
                    print("Error: Index is out of range. Please try again!")
                    # error handling: if index provided is out of range, print so

                print("Changes made!")
                # success message. When the value was changed.

            elif choice == '5': # user wants to output the data in csv format
                for line in rows:
                    print(line.strip()) # strip of white space and print each line

    except FileNotFoundError:  # error handling if user provides a faulty or non-existent file name
        print("File does not exist! ")
    except ValueError: # error handling for any invalid type conversion done above
        print("Incorrect input! Please enter a valid option.")


file_operations("data.txt")
