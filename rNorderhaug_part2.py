"""
Author: Renat Norderhaug
Class: CS 457
Project: PA 2
Date: 10/21/2019
"""

import os
from shutil import rmtree
import re

scopeDir = ""
wrkDir = ""

# sample test to run it.
# run the following commands
# CREATE DATABASE DB_1;
# USE DB_1;
# CREATE TABLE TBL_1 (A1 INT, A2 VARCHAR(4));
# INSERT INTO TBL1 values ( 4, HI);
# UPDATE TBL1 SET A2 = "HEY" WHERE A2 = "HI"
# DELETE FROM TBL1 WHERE A2 = "HI"
# DROP TABLE TBL_1;
# ALTER TABLE TBL_1 add A3 float
# SELECT * FROM TBL_1;
# DROP DATABASE DB_1;



#Function createDB creates the user specified database and error checks as necessary
def createDB(qb):
    #creating database dir if not already created
    try:
        #storing string that comes after 'create database'
        dir = qb.split("CREATE DATABASE ")[1]
        # print(dir) Bang bang error check
        #checking if specified database exist
        if os.path.exists(dir):
            print ("!Failed to create database " + dir + " because it already exists.")
        else:
            #creating specified database
            os.makedirs(dir)
            print ("Database " + dir + " created.")
    except IndexError:
            print ("!No database name specified")

#Function dropDB deletes the user specified database and error checks
def dropDB(qb):
    #deleting database dir unless it does not exist
    try:
        #storing string that comes after 'drop database'
        dir = qb.split("DROP DATABASE ")[1]
        #ensure specified database exists
        if os.path.exists(dir):
          #uses rmtree module from shutil to delete the directory
             rmtree(dir)
             print ("Database " + dir + " deleted.")
        else:
             print ("!Failed to delete database " + dir + " because it does not exist.")
    except IndexError:
        print ("!No database name specified")

#Function createTB creates the user specified table and error checks
def createTB(qb):
    try:
        #check if we are in correct dir
        correctDB()
        #getting string after create table
        subDir = qb.split("CREATE TABLE ")[1]
        #parsing for passed, so this takes the actual table name out
        # from the rest of the arguments
        subDir = subDir.split(" (")[0].lower()
        # joins the wrkDir, and subDir path
        psFile = os.path.join(wrkDir, subDir)
        #print [subDir, psFile, wrkDir]
        # checks if table at this directory already exists
        if not os.path.isfile(psFile):
            #to create table this will use files which act as tables
            # opens the psFile at that directory and writes into it
            with open(psFile, "w") as TB:
                print ("Table " + subDir + " created.")
                #start of arg
                if "(" in qb:
                    #creating oList to load & send to file, the variables passed as parameters
                    oList = []
                    #remove the (, which grabs the first variable
                    data = qb.split("(",1)[1]
                    #remove the )
                    data = data[:-1]
                    #in data replace the , with |
                    data = data.replace(", " , " | ")
                    #writing the user specified data about the table into the table
                    TB.write(data)
        else:
            raise ValueError("!Failed to create table " + subDir + " because it already exists.")
    except IndexError:
        print ("Failed to create table because no table name is specified!")
    except ValueError as err:
        print (err.args[0])

#Function dropTB deletes the user specified table and error checks as necessary
def dropTB(qb):
    try:
        #check if we are in correct dir
        correctDB()
        #getting string after DROP TABLE
        subDir = qb.split("DROP TABLE ")[1]
        #finding table in the system
        userTB = os.path.join(wrkDir, subDir)
        #checking if table is correct
        if os.path.isfile(userTB):
            #removing table, use os.remove to remove
            os.remove(userTB)
            print ("Table " + subDir + " deleted.")
        else:
            raise ValueError("!Failed to delete table " + subDir + " because it does not exist.")
    except IndexError:
        print ("!Failed to remove table because no table name specified")
    except ValueError as err:
        print (err.args[0])


#Function alterTB alters the user table specified and error checks as necessary
def alterTB(qb):
    try:
        #check if we are in correct dir
        correctDB()
        #getting string after ALTER TABLE
        userTB = qb.split("ALTER TABLE ")[1]
        userTB = userTB.split(" ")[0]
        myFile = os.path.join(wrkDir, userTB)
        #checking if myFile is file
        if os.path.isfile(myFile):
            #checking for add
            if "ADD" in qb:
                #using a to append to end of file, this allows you to alter
                with open(myFile, "a") as TB:
                    newStr = qb.split("ADD ")[1]
                    #write new data to table
                    TB.write(", " + newStr)
                    print ("Table " + userTB + " modified.")
        else:
            raise ValueError("!Failed to alter table " + userTB + " because it does not exist.")
    except IndexError:
        print ("!Failed to remove table because no table name specified")
    except ValueError as err:
        print (err.args[0])


#Function selectStar will query the user specified table and error check as necessary
def selectStar(qb):
    try:
        #check if we are in correct dir
        correctDB()
        #stringing user specified table
        # make sure to get a space after the query as well.
        findTB = qb.split("FROM ")[1]
        #user table file
        tbFile = os.path.join(wrkDir, findTB)
        #if table file exists
        if os.path.isfile(tbFile):
            #open table file and print out everything
            with open(tbFile,"r+") as TB:
                newOut = TB.read()
                print (newOut)
        else:
            raise ValueError("!Failed to query the table " + findTB + " because it does not exist.")
    except IndexError:
        print ("!Failed to remove table because no table name specified")
    except ValueError as err:
        print (err.args[0])

#Function "useMe" to use the user specified database that was requested
def useMe(qb):
    try:
        # use global to read and write a global variable inside a function,
        global scopeDir
        #placing database in userDB, the value after the USE is the name
        # of the database that we want to use
        scopeDir = qb.split("USE ")[1]
        #as long as database userDB exists we are now using userDB,
        # the scopeDir gets set to the database's dir
        if os.path.exists(scopeDir):
            print ("Using database " + scopeDir + " .")
        else:
            raise ValueError("!Failed to use database because it does not exist.")
    except IndexError:
        print ("!No database name specified")
    except ValueError:
        print (err.args[0])

#Function correctDB ensuring the we are in the correct directory
# working Directory is the scope directory joined with the cwd from the os, so it takes where rNorderhaug_part1.py is located in your filesystem for example.
def correctDB():
    if scopeDir is "":
        raise ValueError("!No database selected")
    else:
        global wrkDir
        wrkDir = os.path.join(os.getcwd(), scopeDir)

def get_column(data):
    column_index = data[0].split(" | ")
    for x in range(len(column_index)):
        column_index[x] = column_index[x].split(" ")[0]
    return column_index


def separate(line):
    line_tester = line.split(" | ")
    for x in range(len(line_tester)):  # Check that each column has an item
        line_tester[x] = line_tester[x].split(" ")[0]
    return line_tester

def insert_into(qb):
    try:
        correctDB()  # Check database is enabled and selected
        table_nm = qb.split(" ")[2].lower()  # Get table name
        file_nm = os.path.join(wrkDir, table_nm)
        if os.path.isfile(file_nm):
            if "values" in qb:  # Check for start of argument section
                with open(file_nm, "a") as table:  # Open the file to insert into
                    out = []  # Create list for output to file
                    data = qb.split("(", 1)[1]  # Remove (
                    data = data[:-1]  # Remove )
                    counter = data.count(",")  # Count argument number
                    for x in range(counter + 1):
                        out.append(data.split(",")[
                                       x].lstrip())  # Import arguments for printing
                        if "\"" == out[x][0] or "\'" == out[x][0]:
                            out[x] = out[x][1:-1]
                    table.write("\n")
                    table.write(" | ".join(out))  # Output the array to a file
                    print ("1 new record inserted.")
            else:
                print ("!Failed to insert into " + table_nm + " because there were no specified arguments")
        else:
            print ("!Failed to alter table " + table_nm + " because it does not exist")
    except IndexError:
        print ("!Failed to insert into table because no table name is specified")
    except ValueError as err:
        print (err.args[0])

  # extremely long function to find where to to delete from, update from, and select in your query.

def where(search_arg, action, data, up_val=""):
    counter = 0
    column_index = get_column(data)
    attr_name = column_index
    input_data = list(data)
    out = []
    flag = 0
    if "=" in search_arg:  # Evaluate operator
        if "!=" in search_arg:
            r_col = search_arg.split(" !=")[0]
            flag = 1
        else:
            r_col = search_arg.split(" =")[0]

        search_arg = search_arg.split("= ")[1]
        if "\"" in search_arg or "\'" in search_arg:
            search_arg = search_arg[1:-1]
        for line in data:
            line_test = separate(line)
            if search_arg in line_test:
                column_index = attr_name.index(r_col)
                line_index = line_test.index(search_arg)
                if line_index == column_index:  # Check for correct column
                    if action == "delete":
                        del input_data[input_data.index(line)]  # Remove matching field
                        out = input_data
                        counter += 1
                    if action == "select":
                        out.append(input_data[input_data.index(line)])
                    if action == "update":
                        attribute, field = up_val.split(" = ")
                        if attribute in attr_name:
                            sep_line = separate(line)
                            sep_line[attr_name.index(attribute)] = field.strip().strip("'")
                            input_data[input_data.index(line)] = ' | '.join(sep_line)
                            out = input_data
                            counter += 1
    elif ">" in search_arg:  # Evaluate operator
        r_col = search_arg.split(" >")[0]
        search_arg = search_arg.split("> ")[1]
        for line in data:
            line_test = line.split(" | ")
            for x in range(len(line_test)):  # Evaluate each column item
                line_test[x] = line_test[x].split(" ")[0]
                try:
                    line_test[x] = float(line_test[x])  # Check numeric values
                    if line_test[x] > float(search_arg):
                        temp_col = column_index.index(r_col)
                        if x == temp_col:  # Check for column
                            if action == "delete":
                                del input_data[input_data.index(line)]  # Remove matched field
                                out = input_data
                                counter += 1
                            if action == "select":
                                out.append(input_data[input_data.index(line)])
                            if action == "update":
                                print ("hi")
                except ValueError:
                    continue
    if flag:
        out = list(set(data) - set(out))
    return counter, out


def delete_from(input):
    try:
        correctDB()  # Check that a database is selected
        table_name = re.split("DELETE FROM ", input, flags=re.IGNORECASE)[1]  # Get a string to use for the table name
        table_name = table_name.split(" ")[0].lower()
        file_name = os.path.join(wrkDir, table_name)
        if os.path.isfile(file_name):
            with open(file_name, "r+") as table:
                data = table.readlines()
                delete_item = re.split("WHERE ", input, flags=re.IGNORECASE)[1]
                counter, out = where(delete_item, "delete", data)
                table.seek(0)
                table.truncate()
                for line in out:
                    table.write(line)
                if counter > 1:
                    print (counter, " records deleted.")
                elif counter == 1:
                    print (counter, " record deleted.")
                else:
                    print ("No records deleted.")
        else:
            print ("!Failed to delete table " + table_name + " because it does not exist")
    except IndexError:
        print ("!Failed to delete table because no table name is specified")
    except ValueError as err:
        print (err.args[0])

def update_from(input):
    try:
        correctDB()  # Check that a database is selected
        table_nm = re.split("UPDATE ", input, flags=re.IGNORECASE)[1]  # Get string to use for the table name
        table_nm = re.split("SET", table_nm, flags=re.IGNORECASE)[0].lower().strip()
        file_nm = os.path.join(wrkDir, table_nm)
        if os.path.isfile(file_nm):
            with open(file_nm, "r+") as table:
                data = table.readlines()
                update_item = re.split("WHERE ", input, flags=re.IGNORECASE)[1]
                val = re.split("SET ", input, flags=re.IGNORECASE)[1]
                val = re.split("WHERE ", val, flags=re.IGNORECASE)[0]
                counter, out = where(update_item, "update", data, val)
                table.seek(0)
                table.truncate()
                for line in out:
                    if not "\n" in line:
                        line += "\n"
                    table.write(line)
                if counter > 0:
                    print (counter, " records modified.")
                else:
                    print ("No records modified.")
        else:
            print ("!Failed to update table " + table_nm + " because it does not exist")
    except IndexError:
        print ("!Failed to update table because no table name is specified")
    except ValueError as err:
        print (err.args[0])

def select_in(input, inputUp):
    try:
        correctDB()  # Check that a database is selected
        table_nm = re.split("FROM ", input, flags=re.IGNORECASE)[1].lower()  # Gets the  string to use for the table name
        if "WHERE" in inputUp:
            table_nm = re.split("WHERE", table_nm, flags=re.IGNORECASE)[0]
            if " " in table_nm:
                table_nm = table_nm.split(" ")[0]
        file_nm = os.path.join(wrkDir, table_nm)
        output = ""
        if os.path.isfile(file_nm):
            with open(file_nm, "r+") as table:  # Use r+ because the tables are already created
                if "WHERE" in inputUp:  # Using the where to find the matches with all attributes
                    search_item = re.split("WHERE ", input, flags=re.IGNORECASE)[1]
                    data = table.readlines()
                    counter, output = where(search_item, "select", data)
                    for line in output:
                        print(line)
                if "SELECT *" in inputUp:
                    if not output == "":  # Checks if the output is allocated
                        for line in output:
                            print(line)
                    else:
                        output = table.read()
                        print(output)
                else:  # If doesnt want all attributes, trim down output
                    # in the case of a regular select
                    arguments = re.split("SELECT", input, flags=re.IGNORECASE)[1]
                    attributes = re.split("FROM", arguments, flags=re.IGNORECASE)[0]
                    attributes = attributes.split(",")
                    if not output == "":  # Checks if the output is allocated, so its not empty
                        lines = output
                    else:
                        lines = table.readlines()
                        data = lines
                    for line in lines:
                        out = []
                        for attribute in attributes:
                            attribute = attribute.strip()
                            # gets the data at the column
                            column_index = get_column(data)
                            if attribute in column_index:
                                separated_line = separate(line)
                                out.append(separated_line[column_index.index(attribute)].strip())
                        print (" | ".join(out))
        else:
            print ("!Failed to query table " + table_nm + " because it does not exist")
    except IndexError:
        print ("!Failed to select because no table name is specified")
    except ValueError as err:
        print (err.args[0])




# to create a user specified database
def main():
    try:
        while True:
            command = ""
            while not ";" in command and not "--" in command:
                command += input("\n enter a command \n")  # Read input command

            command = command.split(";")[0]  # Remove ; from the command
            command_string = str(command)  # Normalize the command
            command_string = command_string.upper()

            if "--" in command:  # Pass the comments to find command
                pass

            elif "ALTER TABLE" in command_string:
                alterTB(command)

            elif "CREATE DATABASE" in command_string:
                createDB(command)

            elif "CREATE TABLE" in command_string:
                createTB(command)

            elif "DELETE FROM" in command_string:
                delete_from(command)

            elif "DROP DATABASE" in command_string:
                dropDB(command)

            elif "DROP TABLE" in command_string:
                dropTB(command)

            elif "INSERT INTO" in command_string:
                insert_into(command)

            elif "SELECT" in command_string:
                select_in(command, command_string)

            elif "UPDATE" in command_string:
                update_from(command)

            elif "USE" in command_string:
                useMe(command)

            elif ".EXIT" in command:  # Exit database if specified
                print ("All done.")
                exit()

    except (EOFError, KeyboardInterrupt) as e:  # Exit script
        print ("\n All done.")
    except ValueError as err:
        print("oops try again!")


if __name__ == '__main__':
    main()
