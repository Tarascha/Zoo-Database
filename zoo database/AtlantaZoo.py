from tkinter import *
import pymysql
from tkinter import messagebox
from tkinter import ttk
import re
import time
import hashlib

class AtlantaZoo:
    def __init__(self):
        # Invoke createLoginWindow; Invoke buildLoginWindow, Set loginWindow as mainloop
        #Connect to the database
        self.db = self.connect()
        self.cursor = self.db.cursor()
        # Login Window
        self.createLoginWindow()
        self.buildLoginWindow(self.loginWindow)
        self.loginWindow.mainloop()
        self.result_searchForExhibit_Visitor = []
        self.tag = 1
        sys.exit()

##  =======Login Window=======
    def createLoginWindow(self):
        # Create blank Login Window
        self.loginWindow = Tk()
        self.loginWindow.title("Atlanta Zoo System")

        self.loginWindow.withdraw()
        self.loginWindow.update_idletasks()  # Update "requested size" from geometry manager
        x = (self.loginWindow.winfo_screenwidth() - self.loginWindow.winfo_reqwidth()) / 2
        y = (self.loginWindow.winfo_screenheight() - self.loginWindow.winfo_reqheight()) / 2
        self.loginWindow.geometry("+%d+%d" % (x, y))
        self.loginWindow.deiconify()

    def buildLoginWindow(self, loginWindow):
        # Add component for Login Window
        # Login Label
        self.tag = 1
        loginLabel = Label(loginWindow, text="Login",font = "Verdana 13 bold ")
        loginLabel.grid(row=1, column=3, sticky=W+E)

        # Username Label
        usernameLabel = Label(loginWindow, text="Email")
        usernameLabel.grid(row=2, column=2, sticky=W)

        # Password Label
        passwordLabel = Label(loginWindow, text="Password")
        passwordLabel.grid(row=4, column=2, sticky=W)

        # Email Entry

        self.loginemail = StringVar()
        emailAddressEntry = Entry(loginWindow, textvariable=self.loginemail, width=20)
        emailAddressEntry.grid(row=2, column=3, sticky=W + E)


        # Password Entry
        self.loginPassword = StringVar()
        passwordEntry = Entry(loginWindow, textvariable=self.loginPassword, show = '*', width=20)
        passwordEntry.grid(row=4, column=3, sticky=W + E)

        # Login Buttons
        loginButton = Button(loginWindow, text="Login", command=self.loginWindowLoginButtonClicked)
        loginButton.grid(row=6, column=3)

        # Register Button

        registerButton = Button(loginWindow, text="Register", command=self.loginWindowRegisterButtonClicked)
        registerButton.grid(row=6, column=4, sticky=E)

    def loginWindowLoginButtonClicked(self):
        # Click the button on Login Window:
        # Withdraw Login Window;
        self.emailAddress = self.loginemail.get()#loginemail not defined
        self.password = self.loginPassword.get()
        h = hashlib.md5(self.password.encode())
        self.password = h.hexdigest()

        if not self.emailAddress:
            messagebox.showwarning("Email input is empty", "Please enter Email.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        isEmail = self.cursor.execute("SELECT * FROM User WHERE Email = %s", self.emailAddress)
        if not isEmail:
           messagebox.showwarning("Email is not valid.")
           return False
        useremailAndPasswordMatch = self.cursor.execute(
           "SELECT * FROM User WHERE (Email = %s AND Password = %s)", (self.emailAddress, self.password))
        if not useremailAndPasswordMatch:
           messagebox.showwarning("Email and password don\'t match", "Sorry, the Email and password you entered"
                                                                        + " do not match.")
           return False

        isAdminName = self.cursor.execute("SELECT * FROM Admin, User WHERE  Admin.Username = User.Username AND User.Email = %s", (self.emailAddress))
        isVisitorName = self.cursor.execute("SELECT * FROM Visitor, User WHERE  Visitor.Username = User.Username AND User.Email = %s", (self.emailAddress))

        if isAdminName:
            print("Yes Admin")
            self.cursor.execute("SELECT Username FROM User WHERE Email = %s", self.emailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createAdminChooseFunctionalityWindow()
            self.buildChooseAdminFunctionalityWindow(self.chooseAdminFunctionalityWindow)
        elif isVisitorName:
            print("Hello Visitor")
            self.cursor.execute("SELECT Username FROM User WHERE Email = %s", self.emailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createChooseFunctionalityWindow()
            self.buildChooseFunctionalityWindow(self.chooseFunctionalityWindow)
        else:
            print("hey Staff")
            self.cursor.execute("SELECT Username FROM User WHERE Email = %s", self.emailAddress)
            result = self.cursor.fetchall()
            self.username = result[0]
            self.loginWindow.withdraw()
            self.createStaffChooseFunctionalityWindow()
            self.buildStaffChooseFunctionalityWindow(self.chooseStaffFunctionalityWindow)
        return True


    def loginWindowRegisterButtonClicked(self):
        # Click button on Login Window:
        # Invoke createNewUserRegistrationWindow; Invoke buildNewUserRegistrationWindow;
        # Hide Login Window; Set newUserRegistrationWindow on the top
        self.createNewUserRegistrationWindow()
        self.buildNewUserRegistrationWindow(self.newUserRegistrationWindow)
        self.loginWindow.withdraw()

#======New User Registration Window==============


    def createNewUserRegistrationWindow(self):
        # Create blank newUserRegistrationWindow
        self.newUserRegistrationWindow = Toplevel()
        self.newUserRegistrationWindow.title("Atlanta zoo")

    def buildNewUserRegistrationWindow(self,newUserRegistrationWindow):
        # Add components for newUserRegistrationWindow

        # New User Rigestration Label
        newUserRegistrationLabel = Label(newUserRegistrationWindow, text="Atlanta Zoo ",font = "Verdana 13 bold ")
        newUserRegistrationLabel.grid(row=1, column=3, sticky=W)

        # Username Label
        usernameLabel = Label(newUserRegistrationWindow, text="Username")
        usernameLabel.grid(row=2, column=2, sticky=W)

        # Email Address Label
        emailAddressLabel = Label(newUserRegistrationWindow, text="Email Address")
        emailAddressLabel.grid(row=3, column=2, sticky=W)

        # Password Label
        passwordLabel = Label(newUserRegistrationWindow, text="Password")
        passwordLabel.grid(row=4, column=2, sticky=W)

        # Confirm Password Label
        confirmPasswordLabel = Label(newUserRegistrationWindow, text="Confirm Password")
        confirmPasswordLabel.grid(row=5, column=2, sticky=W)

        # Username Entry
        self.registrationUsername = StringVar()
        usernameEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationUsername, width=20)
        usernameEntry.grid(row=2, column=3, sticky=W + E)

        # Email Address Entry
        self.registrationEmailAddress = StringVar()
        emailAddressEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationEmailAddress,width=20)
        emailAddressEntry.grid(row=3, column=3, sticky=W + E)

        # Password Entry
        self.registrationPassword = StringVar()
        passwordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationPassword,show = '*',width=20)
        passwordEntry.grid(row=4, column=3, sticky=W + E)

        # Confirm Password Entry
        self.registrationConfirmPassword = StringVar()
        confirmPasswordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationConfirmPassword,show = '*',width=20)
        confirmPasswordEntry.grid(row=5, column=3, sticky=W + E)

        # Create Staff Button
        createButton = Button(newUserRegistrationWindow, text="Staff", command=self.newStaffCreateButtonClicked)
        createButton.grid(row=6, column=2)

        # Create Visitor Button
        createButton = Button(newUserRegistrationWindow, text="Visitor",
                              command=self.newUserCreateButtonClicked)
        createButton.grid(row=6, column=3)

    def newUserCreateButtonClicked(self):
        # Click the Create Button on New User Registration Window:
        # Invoke createChooseFunctionalityWindow; Invoke buildChooseFunctionalityWindow;
        # Destroy New User Registration Window
        self.username = self.registrationUsername.get()
        self.emailAddress = self.registrationEmailAddress.get()
        self.password = self.registrationPassword.get()
        self.confirmPassword = self.registrationConfirmPassword.get()
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if not self.emailAddress:
            messagebox.showwarning("E-mail input is empty", "Please enter E-mail.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        if len(self.password) < 8:
            messagebox.showwarning("info", "Password must be at least 8 digits")
            return False
        if not self.confirmPassword:
            messagebox.showwarning("Confirm password input is empty", "Please enter confirm password")
            return False

        isUsername = self.cursor.execute("SELECT * FROM User WHERE Username = %s", self.username)
        if isUsername:
           messagebox.showwarning("This username has been used.",
                                  "Please input another username.")
           return False
        isEmail = self.cursor.execute("SELECT * FROM User WHERE Email = %s", self.emailAddress)
        if isEmail:
           messagebox.showwarning("This E-mail address has been used.",
                                  "Please input another E-mail address.")
           return False
        if not (self.password == self.confirmPassword):
           messagebox.showwarning("Password does not match the confirm password.",
                                  "Please reconfirm the password.")
           return False

        h1 = hashlib.md5(self.password.encode())
        h2 = hashlib.md5(self.confirmPassword.encode())
        self.password = h1
        self.confirmPassword = h2
        print(h1.hexdigest())
        print(h2.hexdigest())
        print(self.password.hexdigest())
        print(self.confirmPassword.hexdigest())

        email = self.emailAddress

        def myfunction():
            self.cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s)", (self.username, self.emailAddress,self.password.hexdigest(), "Visitor"))
            self.db.commit()
            self.cursor.execute("INSERT INTO Visitor VALUES (%s)", (self.username))
            self.db.commit()
            messagebox.showinfo("info","Register successfully!")
            self.createChooseFunctionalityWindow()
            self.buildChooseFunctionalityWindow(self.chooseFunctionalityWindow)
            self.newUserRegistrationWindow.destroy()

        if re.match("^[A-Za-z0-9._%\-+!#$&/=?^|~]+@[A-Za-z0-9-]+[.][A-Za-z]+$", email, re.IGNORECASE):
            myfunction()
        else:
            messagebox.showwarning("info", "This is not a valid email address")

    def newStaffCreateButtonClicked(self):
        self.username = self.registrationUsername.get()
        self.emailAddress = self.registrationEmailAddress.get()
        self.password = self.registrationPassword.get()
        self.confirmPassword = self.registrationConfirmPassword.get()
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        if not self.emailAddress:
            messagebox.showwarning("E-mail input is empty", "Please enter E-mail.")
            return False
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        if not self.confirmPassword:
            messagebox.showwarning("Confirm password input is empty", "Please enter confirm password")
            return False
        if len(self.password) < 8:
            messagebox.showwarning("info", "Password must be at least 8 digits")
            return False

        if self.password != self.confirmPassword:
            messagebox.showwarning("info","Password does not match, please enter again")
            return False

        isUsername = self.cursor.execute("SELECT * FROM User WHERE Username = %s", self.username)
        if isUsername:
           messagebox.showwarning("This username has been used.",
                                  "Please input another username.")
           return False
        isEmail = self.cursor.execute("SELECT * FROM User WHERE Email = %s", self.emailAddress)
        if isEmail:
           messagebox.showwarning("This E-mail address has been used.",
                                  "Please input another E-mail address.")
           return False
        if not (self.password == self.confirmPassword):
           messagebox.showwarning("Password does not match the confirm password.",
                                  "Please reconfirm the password.")
           return False

        h3 = hashlib.md5(self.password.encode())
        h4 = hashlib.md5(self.confirmPassword.encode())
        self.password = h3
        self.confirmPassword = h4
        print(h3.hexdigest())
        print(h4.hexdigest())
        print(self.password.hexdigest())
        print(self.confirmPassword.hexdigest())

        email = self.emailAddress

        def myfunction():
            self.cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s)", (self.username, self.emailAddress,self.password.hexdigest(), "Staff"))
            self.db.commit()
            self.cursor.execute("INSERT INTO Staff VALUES (%s)", (self.username))
            self.db.commit()
            messagebox.showinfo("info","Register successfully!")
            self.createStaffChooseFunctionalityWindow()
            self.buildStaffChooseFunctionalityWindow(self.chooseStaffFunctionalityWindow)
            self.newUserRegistrationWindow.destroy()

        if re.match("^[A-Za-z0-9._%\-+!#$&/=?^|~]+@[A-Za-z0-9-]+[.][A-Za-z]+$", email, re.IGNORECASE):
            myfunction()
        else:
            messagebox.showwarning("info", "This is not a valid email address")




## Visitor
##==========Visitor Choose Functionality Window================

    def createChooseFunctionalityWindow(self):
        # Create blank chooseFunctionalityWindow
        self.chooseFunctionalityWindow = Toplevel()
        self.chooseFunctionalityWindow.title("Atlanta Zoo : User")

    def buildChooseFunctionalityWindow(self,chooseFunctionalityWindow):
        # Add component to chooseFunctionalityWindow

        #Choose Functionality Label

        chooseFunctionalityLabel = Label(chooseFunctionalityWindow, text="Atlanta Zoo",font = "Verdana 10 bold ")
        chooseFunctionalityLabel.grid(row=1, column=2, sticky=W+E)

        # Search Exhibit
        searchExhibitWindow = Button(chooseFunctionalityWindow, text="search Exhibit",
                              command=self.searchExhibit)
        searchExhibitWindow.grid(row=3, column=1)

        # search shows
        searchShowsWindow = Button(chooseFunctionalityWindow, text="Search Shows",
                              command=self.searchShows)
        searchShowsWindow.grid(row=5, column=1)

        # view exhibit history
        # Search Exhibit
        exhibitHistory = Button(chooseFunctionalityWindow, text="view exhibit history",
                              command=self.exhibitHistory)
        exhibitHistory.grid(row=3, column=3)

        # view show history

        showHistory = Button(chooseFunctionalityWindow, text="view show history",
                              command=self.showHistory)
        showHistory.grid(row=5, column=3)


        # Search for animals
        searchAnimals = Button(chooseFunctionalityWindow, text="search for animals",
                              command=self.searchAnimals)
        searchAnimals.grid(row=7, column=1)

        # Log Out Buttons

        logOutButton = Button(chooseFunctionalityWindow, text="Log out", command=self.chooseFunctionalityWindowLogOutButtonClicked)
        logOutButton.grid(row=9, column=2,sticky=E)

    def searchExhibit(self):

        self.createSearchExhibitWindow()
        self.buildSearchExhibitWindow(self.searchExhibitWindow)
        self.chooseFunctionalityWindow.withdraw()

    def searchAnimals(self):
        self.createSearchAnimalWindow()
        self.buildSearchAnimalWinodw(self.searchAnimalWindow)
        self.chooseFunctionalityWindow.withdraw()

    def searchShows(self):
        self.createSearchShowWindow()
        self.buildSearchShowWindow(self.searchShowWindow)
        self.chooseFunctionalityWindow.withdraw()

    def exhibitHistory(self):
        self.createExhibitHistory()
        self.buildExhibitHistory(self.exhibitHistoryWindow)
        self.chooseFunctionalityWindow.withdraw()

    def showHistory(self):
        self.createShowHistory()
        self.buildShowHistory(self.showHistoryWindow)
        self.chooseFunctionalityWindow.withdraw()

    def chooseFunctionalityWindowLogOutButtonClicked(self):
        # Click Log Out Buttion on Choose Functionality Window:
        # Destroy Choose Functionality Window
        # Display Login Window
        self.chooseFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

#=========search Exhibit Window============

    def createSearchExhibitWindow(self):
        self.searchExhibitWindow = Toplevel()
        self.searchExhibitWindow.title("Search for Exhibit")

    def buildSearchExhibitWindow(self,searchExhibitWindow):
        self.result_searchForExhibit_Visitor = []
        # Title Label
        viewExhibitLabel = Label(searchExhibitWindow, text="Exhibits", font="Verdana 10 bold ")
        viewExhibitLabel.grid(row=1, column=3, sticky=W + E)

        # Title Label 2
        viewZooLabel = Label(searchExhibitWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=2, column=1, )

        # Search Button
        searchButton = Button(searchExhibitWindow, text="Search", command=self.searchForExhibit_Visitor)
        searchButton.grid(row=2, column=5)

        #Return Button
        returnButton = Button(searchExhibitWindow, text="Return", command=self.SearchExhibitWindowReturnButtonClicked)
        returnButton.grid(row=2, column=6)

        # min label
        minLabel = Label(searchExhibitWindow, text = "Min", font = "Verdana 10 bold")
        minLabel.grid(row=3, column = 6)

        # max label
        maxLabel = Label(searchExhibitWindow, text = "Max", font = "Verdana 10 bold")
        maxLabel.grid(row=3, column = 7)

        #name label
        nameLabel = Label(searchExhibitWindow, text = "Name", font = "Verdana 10 bold")
        nameLabel.grid(row=4, column = 1)

        # name entry
        self.nameEntry = StringVar()
        name = Entry(searchExhibitWindow, textvariable=self.nameEntry, width=10)
        name.grid(row=4, column=2, sticky=W + E)

        # num animals label
        numAnimalsLabel = Label(searchExhibitWindow, text="Num Animals", font="Verdana 10 bold")
        numAnimalsLabel.grid(row=4, column=5)

        # min num animal
        self.minanimal = IntVar()
        self.minanimal = Spinbox(searchExhibitWindow, from_=0, to_=100, width=5)
        self.minanimal.grid(row=4, column=6)

        # max num animal
        self.maxanimal = IntVar()
        self.maxanimal = Spinbox(searchExhibitWindow, from_=0, to_=100, width=5)
        self.maxanimal.grid(row=4, column=7)

        # size label
        sizelabel = Label(searchExhibitWindow, text = "Size", font="Verdana 10 bold")
        sizelabel.grid(row=6, column =1)

        # max size label
        maxsizeLabel = Label(searchExhibitWindow, text = "Max", font = "Verdana 10 bold")
        maxsizeLabel.grid(row=5, column=3)

        # min size label
        minsizeLabel = Label(searchExhibitWindow, text = "Min", font = "Verdana 10 bold")
        minsizeLabel.grid(row=5, column=2)

        # min size
        self.minsize_exhibit = IntVar()
        self.minsize_exhibit = Spinbox(searchExhibitWindow, from_=0, to_=1000, width=5)
        self.minsize_exhibit.grid(row=6, column=2)

        # max size
        self.maxsize_exhibit = IntVar()
        self.maxsize_exhibit = Spinbox(searchExhibitWindow, from_=0, to_=1000, width=5)
        self.maxsize_exhibit.grid(row=6, column=3)

        # water feature label
        waterLabel = Label(searchExhibitWindow, text = "Water Feature", font = "Verdana 10 bold")
        waterLabel.grid(row=6, column=5)

        # water feature drop down menu
        self.waterFeature_searchExhibit = StringVar()
        self.waterFeature_searchExhibit.set("Yes")
        lst = ["Yes", "No"]
        optionbutton = OptionMenu(searchExhibitWindow, self.waterFeature_searchExhibit, *lst)
        optionbutton.grid(row=6, column=6)

        # search table
        self.tv = ttk.Treeview(searchExhibitWindow)
        self.tv['columns'] = ("Name", "Size", "NumAnimals", "Water")

        self.tv.heading("Name", text='                     Name                             ▼', anchor='w')
        self.tv.column("Name", minwidth=2)

        self.tv.heading("Size", text="                     Size                             ▼", anchor='w')
        self.tv.column("Size",  minwidth=2)

        self.tv.heading("NumAnimals", text="               NumAnimals               ▼")
        self.tv.column("NumAnimals", minwidth=2)

        self.tv.heading("Water", text=" Water")
        self.tv.column("Water",  minwidth=2)

        self.tv['show'] = 'headings'
        self.tv.grid(row=7, column=3, columnspan = 3  )

        self.tv.bind("<Double-1>",self.onClick)

    def SearchExhibitWindowReturnButtonClicked(self):
        # Click Return Buttion on Search Exhibit Window:
        # Destroy Search Exhibit Window
        # Display Choose Functionality Window
        self.searchExhibitWindow.destroy()
        self.chooseFunctionalityWindow.deiconify()

    def onClick(self,event):
        region = self.tv.identify_region( event.x, event.y)
        if region=="heading":
            meo = {1: "E.Name", 2: "E.Size", 3: "NumAnimals", 4: "Water"}
            column = self.tv.identify_column(event.x)
            c_num = int(column.split("#")[-1])
            c_name = meo[c_num]
            name =self.sort_exhibit_name_visitor
            size = self.sort_exhibit_size_visitor
            water_feature = self.sort_exhibit_water_visitor
            num_animal= self.sort_exhibit_AnimalNum_visitor
            condition = " WHERE A.Exhibit = E.Name "

            if self.sort_exhibit_water_visitor == "Yes": condition+=" AND E.Water_Feature = true"
            elif self.sort_exhibit_water_visitor == "No": condition+=" AND E.Water_Feature = false"
            else: condition+=" AND E.Water_Feature = false OR E.Water_Feature = true"

            if size: condition+=" AND E.size >=" +str(size[0]) + " and E.Size <=" + str(size[1])

            if name: condition+=" AND A.Exhibit= '" + name +"'"

            if num_animal: condition2= " HAVING count(*) >=" + str(num_animal[0]) +" and count(*) <="+ str(num_animal[1])

            pre_sql = "SELECT E.Name, E.Size, count(*) as NumAnimals, E.Water_Feature as Water \
            FROM Exhibit as E, Animal As A " + condition + " GROUP BY A.Exhibit" + condition2

            pre_sql +=" ORDER BY " + str(c_name) + " "

            print(pre_sql)
            sql = ""
            if self.tag == 1:
                self.tag = 0
                sql = pre_sql+ "DESC ;"
                self.sorting_column(self.tv, sql)
            else:
                sql = pre_sql+ "ASC ;"
                self.tag = 1
                self.sorting_column(self.tv, sql)

        elif region=="cell":
            # row = self.tv.identify_row(event.y)
            # print(row)
            # name = self.tv.identify_element(row,"Name")
            # print(name)
            curItem = self.tv.item(self.tv.focus())
            name = curItem['values'][0]
            size = curItem['values'][1]
            NumAnimals = curItem['values'][2]
            WaterFeature = curItem['values'][3]
            print(curItem)
            self.createExhibitDetailWindow()
            self.buildExhibitDetailWindow(self.ExhibitDetailWindow, name, size, NumAnimals, WaterFeature)

    def sorting_column(self, tv_table, sql):
        # tv_table is like self.tv
        # sql is string of sql lanugage
        # order is string of either "DESC" or "ASC"
        self.cursor.execute(sql)
        result_tuple = self.cursor.fetchall()
        tv_table.delete(*tv_table.get_children())
        for i, result in enumerate(result_tuple):
            ans = []
            for k in result:
                ans.append(str(k))
            tv_table.insert("",i, value=tuple(ans))

    def treeview_sort_column(self,tv,col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: \
           self.treeview_sort_column(tv, col, not reverse))

# ==========Exhibit Detail================

    def createExhibitDetailWindow(self):
        self.ExhibitDetailWindow = Toplevel()
        self.ExhibitDetailWindow.title("Exhibit Detail")

    def buildExhibitDetailWindow(self, ExhibitDetailWindow, name, size, numAnimals, waterFeature):
        # title label
        name = str(name)
        self.Exhibit_Detail_Page_ExhibitName = name
        size = str(size)
        numAnimals = str(numAnimals)
        waterFeature = str(waterFeature)
        waterFeature ="Yes" if waterFeature=="1" else "No"

        label = Label(ExhibitDetailWindow, text="Exhibit Detail", font="Verdana 10 bold")
        label.grid(row=1, column=2)

        # zoo label
        label = Label(ExhibitDetailWindow, text="Atlanta Zoo", font="Verdana 10 bold")
        label.grid(row=2, column=1)

        # Name Label
        label = Label(ExhibitDetailWindow, text="Name: " + name, font="Verdana 10 bold")
        label.grid(row=3, column=1)

        # size label
        label = Label(ExhibitDetailWindow, text="Size: " + size, font="Verdana 10 bold")
        label.grid(row=3, column=2)

        # num animals label
        label = Label(ExhibitDetailWindow, text="Num Animals: " + numAnimals, font="Verdana 10 bold")
        label.grid(row=3, column=3)

        # water feature
        label = Label(ExhibitDetailWindow, text="Water Feature: " + waterFeature, font="Verdana 10 bold")
        label.grid(row=4, column=1)

        # Search Button
        logVisitButton = Button(ExhibitDetailWindow, text="Log Visit", command=self.logVisit_toExhibit_Clicked)
        logVisitButton.grid(row=4, column=2)

        # search table
        self.tv_exhibit_detail = ttk.Treeview(self.ExhibitDetailWindow)
        self.tv_exhibit_detail['columns'] = ("Name", "Species")

        self.tv_exhibit_detail.heading("Name", text='                     Name                             ▼', anchor='w')
        self.tv_exhibit_detail.column("Name", minwidth=1)

        self.tv_exhibit_detail.heading("Species", text="                     Species                          ▼", anchor='w')
        self.tv_exhibit_detail.column("Species", minwidth=1)

        self.tv_exhibit_detail['show'] = 'headings'
        self.tv_exhibit_detail.grid(row=7, column=2, columnspan=1)

        # get data from server
        self.exhibitDetail(name)

        # click
        self.tv_exhibit_detail.bind("<Double-1>", self.animalDetailOnClicked)

    def animalDetailOnClicked(self, event):
        region = self.tv_exhibit_detail.identify_region(event.x, event.y)
        if region == "cell":
            curItem = self.tv_exhibit_detail.item(self.tv_exhibit_detail.focus())
            name = curItem['values'][0]
            species = curItem['values'][1]
            self.createAnimalDetailWindow()
            self.buildAnimalDetailWindow(self.AnimalDetailWindow, name, species)

    def logVisit_toExhibit_Clicked(self):
        tran = {"Nov": "11", "Dec":"12", "Oct":"10", "Sep":"09", "Feb":"02",
        "Jan":"01", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07", "Aug":"08"}
        name = self.username[0]
        exhibit = self.Exhibit_Detail_Page_ExhibitName
        date = time.ctime()
        dateList = date.split()
        date = dateList[-1]+"-"+tran[dateList[1]]+"-"+dateList[2]+" "+dateList[3]
        # ctime = 'Mon Nov 26 13:37:28 2018'
        # date = "2018-11-13 12:01:00"
        print(date)
        print(exhibit)
        print(name)
        sql = "INSERT INTO Visit_Exhibit(Exhibit, Visitor, Datetime) VALUES ('"+exhibit+ \
        "', '"+name+"', '"+date+"');"
        self.cursor.execute(sql)
        self.db.commit()


#==========Animals Detail================
    def createAnimalDetailWindow(self):
        self.AnimalDetailWindow = Toplevel()
        self.AnimalDetailWindow.title("Animal Detail")

    def buildAnimalDetailWindow(self, AnimalDetailWindow, name, species):
        #title label

        name, species, types, age, exhibit =  self.animalDetail(name, species)

        label = Label(AnimalDetailWindow, text= "Animal Detail", font="Verdana 10 bold")
        label.grid(row=1, column=2)

        # zoo label
        label = Label(AnimalDetailWindow, text="Atlanta Zoo", font="Verdana 10 bold")
        label.grid(row=2, column=1)

        # Name Label
        label = Label(AnimalDetailWindow, text="Name: " + name, font="Verdana 10 bold")
        label.grid(row=3, column=1)

        # species label
        label = Label(AnimalDetailWindow, text="Species: "+species, font="Verdana 10 bold")
        label.grid(row=3, column=2)

        # age label
        label = Label(AnimalDetailWindow, text="Age:  " + age, font="Verdana 10 bold")
        label.grid(row=3, column=3)

        # Exhibit label
        label = Label(AnimalDetailWindow, text="Exhibit: " + exhibit, font="Verdana 10 bold")
        label.grid(row=4, column=1)

        # type label
        label = Label(AnimalDetailWindow, text="Type: " + types, font="Verdana 10 bold")
        label.grid(row=4, column=2)


#==========search Animals Window================

    def createSearchAnimalWindow(self):
        self.searchAnimalWindow = Toplevel()
        self.searchAnimalWindow.title("Search for Animal")

    def buildSearchAnimalWinodw(self,searchAnimalWindow):

        # viewZoo label
        viewZooLabel = Label(searchAnimalWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=1, )

        # viewAnimal label
        viewAnimalLabel = Label(searchAnimalWindow, text="Animals", font="Verdana 10 bold ")
        viewAnimalLabel.grid(row=1, column=3, sticky=W + E)

        # Exhibit label
        viewZooLabel = Label(searchAnimalWindow, text="Exhibit", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=5, )

        # Exhibit Drop Down Button
        sql = "SELECT Name FROM Exhibit;"
        self.cursor.execute(sql)
        ExhibitTuple = self.cursor.fetchall()
        ExhibitList = []
        ExhibitList.append("")
        for i in ExhibitTuple:
            ExhibitList.append(i[0])

        Exhibit = StringVar()
        Exhibit.set(ExhibitList[0])

        AtZooFromOptionMenu = OptionMenu(searchAnimalWindow, Exhibit, *ExhibitList)
        AtZooFromOptionMenu.config(width= 10)

        AtZooFromOptionMenu.grid(row=1, column=7)

        # Animal Name Label
        viewZooLabel = Label(searchAnimalWindow, text="Name", font="Verdana 10 bold ")
        viewZooLabel.grid(row=3, column=1)

        # Animal Name Entry
        animalName = StringVar()
        nameEntry = Entry(searchAnimalWindow, textvariable=animalName, width=10)
        nameEntry.grid(row=3, column=3, sticky=W + E)

        # Animal Age Label
        viewAge = Label(searchAnimalWindow, text="Age", font="Verdana 10 bold ")
        viewAge.grid(row=3, column=5 )

        # Animal Age Select
        # Don't know
        #
        # Animal Min Max Label
        minLabel = Label(searchAnimalWindow, text="MIN", font="Verdana 10 bold ")
        minLabel.grid(row=2, column=7)

        maxLabel = Label(searchAnimalWindow, text="MAX", font="Verdana 10 bold ")
        maxLabel.grid(row=2, column=8)

        selectMinAge = IntVar()
        selectMinAge = Spinbox(searchAnimalWindow, from_=0, to=100, width=5)
        selectMinAge.grid(row=3, column=7)

        selectMaxAge = IntVar()
        selectMaxAge = Spinbox(searchAnimalWindow, from_=0, to=100, width=5)
        selectMaxAge.grid(row=3, column=8)

        # Animal Species label
        viewZooLabel = Label(searchAnimalWindow, text="Species", font="Verdana 10 bold ")
        viewZooLabel.grid(row=5, column=1)

        # Animal species Entry
        species = StringVar()
        speciesEntry = Entry(searchAnimalWindow, textvariable=species,  width=10)
        speciesEntry.grid(row=5, column=3, sticky=W + E)

        # Animal Type label
        viewAnimalType = Label(searchAnimalWindow, text="Type", font="Verdana 10 bold ")
        viewAnimalType.grid(row=5, column=5)

        sql = "SELECT DISTINCT Type FROM Animal;"
        self.cursor.execute(sql)
        typeTuple = self.cursor.fetchall()
        typeList = []
        typeList.append("")
        for i in typeTuple:
            typeList.append(i[0])

        Type = StringVar()
        Type.set(typeList[0])

        typeMenu = OptionMenu(searchAnimalWindow, Type, *typeList)
        typeMenu.grid(row=5, column=7)


        self.tv_animal_detail = ttk.Treeview(searchAnimalWindow)
        self.tv_animal_detail['columns'] = ("Name", "Species", "Exhibit", "Age", "Type")

        self.tv_animal_detail.heading("Name", text='                     Name                         ▼', anchor='w')
        self.tv_animal_detail.column("Name", minwidth=2)

        self.tv_animal_detail.heading("Species", text="                     Species                    ▼", anchor='w')
        self.tv_animal_detail.column("Species",  minwidth=2)

        self.tv_animal_detail.heading("Exhibit", text="                  Exhibit                      ▼")
        self.tv_animal_detail.column("Exhibit", minwidth=2)

        self.tv_animal_detail.heading("Age", text="                     Age                            ▼")
        self.tv_animal_detail.column("Age",  minwidth=2)

        self.tv_animal_detail.heading("Type", text="                     Type                          ▼")
        self.tv_animal_detail.column("Type",  minwidth=2)

        self.tv_animal_detail['show'] = 'headings'
        self.tv_animal_detail.grid(row=7, column=3, columnspan = 3  )
        # Search Button

        def searchBottonFun():
            self.searchAnimal_Visitor(Exhibit.get(), animalName.get(), selectMinAge.get(),
                selectMaxAge.get(), species.get(), Type.get())


        searchButton = Button(searchAnimalWindow, text="Search", command=searchBottonFun)
        searchButton.grid(row=1, column=4)

        #Return Button
        returnButton = Button(searchAnimalWindow, text="Return", command=self.searchAnimalWindowReturnButtonClicked)
        returnButton.grid(row=1, column=9)

        self.tv_animal_detail.bind("<Double-1>", self.animalDetailOnClicked2)

    def animalDetailOnClicked2(self, event):
        region = self.tv_animal_detail.identify_region(event.x, event.y)
        if region == "heading":
            column = self.tv_animal_detail.identify_column(event.x)

            meo = {1: "Name", 2: "Species", 3: "Exhibit", 4: "Age", 5:"Type"}
            c_num = int(column.split("#")[-1])
            c_name = meo[c_num]

            animalName =self.sort_animal_name_visitor
            species = self.sort_animal_species_visitor
            Exhibit = self.sort_animal_exhibit_visitor
            minLabel = self.sort_animal_min_visitor
            maxLabel = self.sort_animal_max_visitor
            Type = self.sort_animal_type_visitor

            condition = " WHERE Age>=" +str(minLabel)+ " and Age<=" +str(maxLabel)
            if Exhibit:
                condition+=" AND Exhibit = '"+Exhibit+"'"
            if animalName:
                condition+=" AND  Name = '" +animalName + "'"
            if species:
                condition+="  AND Species= '" + species + "'"
            if Type:
                condition+="  AND Type= '" + Type + "'"

            sql_searchShows = "SELECT Name, Species, Exhibit, Age, Type FROM Animal "+condition

            if self.tag == 1:
                self.tag=0
                sql = sql_searchShows + " ORDER BY "+c_name+" DESC ;"
            else:
                self.tag=1
                sql = sql_searchShows + " ORDER BY "+c_name+" ASC ;"
            self.sorting_column(self.tv_animal_detail, sql)
        if region == "cell":
            curItem = self.tv_animal_detail.item(self.tv_animal_detail.focus())
            name = curItem['values'][0]
            species = curItem['values'][1]
            self.createAnimalDetailWindow()
            self.buildAnimalDetailWindow(self.AnimalDetailWindow, name, species)

    def searchAnimalWindowReturnButtonClicked(self):
        # Click Return Button on Search Animal Window:
        # Destroy Search Animal Window
        # Display Choose Functionality Window
        self.searchAnimalWindow.destroy()
        self.chooseFunctionalityWindow.deiconify()


#============== search Show Window ==============

    def createSearchShowWindow(self):
        self.searchShowWindow = Toplevel()
        self.searchShowWindow.title("Search for Show")

    def buildSearchShowWindow(self, searchShowWindow):
        # viewZoo label
        viewZooLabel = Label(searchShowWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=1, )

        # viewShow label
        viewShowLabel = Label(searchShowWindow, text="Shows", font="Verdana 10 bold ")
        viewShowLabel.grid(row=1, column=3, sticky=W + E)

        # Show Name label
        ShowNameLabel = Label(searchShowWindow, text="Name", font="Verdana 10 bold ")
        ShowNameLabel.grid(row=5, column=1)

        showName = StringVar()
        nameEntry = Entry(searchShowWindow, textvariable=showName, width=10)
        nameEntry.grid(row=5, column=3, sticky=W + E)

        # Show Date Label
        showDateLabel = Label(searchShowWindow, text="Date", font="Verdana 10 bold ")
        showDateLabel.grid(row=5, column=7)

         # Show Date Entry
        showDatetime = StringVar()
        showDateLabel = Entry(searchShowWindow, textvariable=showDatetime, width=10)
        showDateLabel.grid(row=5, column=9)

        # Date Format
        DateFormat = Label(searchShowWindow, text="YYYY-MM-DD", font="Verdana 10 bold ")
        DateFormat.grid(row=5, column=11, sticky=W + E)

        logVisitButton = Button(searchShowWindow, text="Log Visit", command=self.logVisit_toShow_Clicked)
        logVisitButton.grid(row=4, column=2)

        self.tv_Shows = ttk.Treeview(self.searchShowWindow)
        self.tv_Shows['columns'] = ("Name", "Exhibit", "Datetime")

        self.tv_Shows.heading("Name", text='                     Name                           ▼', anchor='w')
        self.tv_Shows.column("Name", minwidth=2)

        self.tv_Shows.heading("Exhibit", text="                     Exhibit                        ▼", anchor='w')
        self.tv_Shows.column("Exhibit", minwidth=2)

        self.tv_Shows.heading("Datetime", text="                     Datetime                       ▼")
        self.tv_Shows.column("Datetime", minwidth=2)

        self.tv_Shows['show'] = 'headings'
        self.tv_Shows.grid(row=9, column=3, columnspan=3)

        sql = "SELECT DISTINCT Exhibit FROM Shows;"
        self.cursor.execute(sql)
        ExhibitTuple = self.cursor.fetchall()
        ExhibitList = []
        ExhibitList.append("")
        for i in ExhibitTuple:
            ExhibitList.append(i[0])

        # Show Date Label
        showDateLabel = Label(searchShowWindow, text="Exhibit", font="Verdana 10 bold ")
        showDateLabel.grid(row=7, column=1)

        Exhibit = StringVar()
        Exhibit.set(ExhibitList[0])
        AtZooFromOptionMenu = OptionMenu(searchShowWindow, Exhibit, *ExhibitList)
        AtZooFromOptionMenu.config(width= 10)

        AtZooFromOptionMenu.grid(row=7, column=3)
        # Search Button
        def searchShooows():
            self.searchShows_Visitor(self.tv_Shows, showName.get(), showDatetime.get(), Exhibit.get())
        searchButton = Button(searchShowWindow, text="Search",
            command=searchShooows)
        searchButton.grid(row=7, column=4)

        def bindData(event):
            region = self.tv_Shows.identify_region( event.x, event.y)
            if region=="cell":
                print("You have a single click.")
                curItem = self.tv_Shows.item(self.tv_Shows.focus())
                self.logVisit_toShow_ShowName = str(curItem["values"][0])
                self.logVisit_toShow_DataTime = str(curItem["values"][2])
                self.logVisit_toShow_exhibitName = str(curItem["values"][1])


        self.tv_Shows.bind("<Double-1>",self.onClick_show)
        self.tv_Shows.bind("<Button-1>",bindData)

        #Return Button
        returnButton = Button(searchShowWindow, text="Return", command=self.SearchShowWindowReturnButtonClicked)
        returnButton.grid(row=7, column=5)

    def onClick_show(self,event):
        region = self.tv_Shows.identify_region( event.x, event.y)
        if region=="heading":
            column = self.tv_Shows.identify_column(event.x)
            self.treeview_sort_column(self.tv_Shows, column, False)
        elif region=="cell":
            # row = self.tv.identify_row(event.y)
            # print(row)
            # name = self.tv.identify_element(row,"Name")
            # print(name)
            curItem = self.tv_Shows.item(self.tv_Shows.focus())
            exhibitName = curItem['values'][1]
            condition = " WHERE A.Exhibit = E.Name "
            condition+=" AND A.Exhibit= '" + exhibitName +"'"



            sql = "SELECT E.Name, E.Size, count(*) as NumAnimals, E.Water_Feature as Water \
            FROM Exhibit as E, Animal As A " + condition + " GROUP BY A.Exhibit;"

            print(sql)

            self.cursor.execute(sql)
            result_Exhibit_detail = self.cursor.fetchall()

            name = str(result_Exhibit_detail[0][0])
            size = str(result_Exhibit_detail[0][1])
            NumAnimals=str(result_Exhibit_detail[0][2])
            WaterFeature=str(result_Exhibit_detail[0][3])

            self.createExhibitDetailWindow()
            self.buildExhibitDetailWindow(self.ExhibitDetailWindow,name,size,NumAnimals,WaterFeature)

    def logVisit_toShow_Clicked(self):
        name = self.username[0]
        showName = self.logVisit_toShow_ShowName
        date = self.logVisit_toShow_DataTime
        exhibit = self.logVisit_toShow_exhibitName

        tran = {"Nov": "11", "Dec":"12", "Oct":"10", "Sep":"09", "Feb":"02",
        "Jan":"01", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07", "Aug":"08"}
        date_cur = time.ctime()
        dateList = date_cur.split()
        for i in range(len(dateList)):
            if len(dateList[i])<=1:
                dateList[i]= "0"+dateList[i]
        date_cur = dateList[-1]+"-"+tran[dateList[1]]+"-"+dateList[2]+" "+dateList[3]

        print(date)
        print(date_cur)
        if date_cur>date:
            sql = "INSERT INTO Visit_Exhibit(Exhibit, Visitor, Datetime) VALUES ('"+exhibit+ \
            "', '"+name+"', '"+date+"');"
            self.cursor.execute(sql)
            self.db.commit()
            sql2 = "INSERT INTO Visit_Show(ShowName, Datetime, Visitor) VALUES ('"+showName+ \
            "', '"+date+"', '"+name+"');"
            self.cursor.execute(sql2)
            self.db.commit()
            messagebox.showinfo("info","Congraudations! You have log a visit to this show.")
        else:
            messagebox.showwarning("You cannot log a visit to the finished show!")

    def SearchShowWindowReturnButtonClicked(self):
        # Click Return Button on Search Show Window:
        # Destroy Search Show Window
        # Display Choose Functionality Window
        self.searchShowWindow.destroy()
        self.chooseFunctionalityWindow.deiconify()
    #===========Show Result===============


#==========exhibit History=============

    def createExhibitHistory(self):
        self.exhibitHistoryWindow = Toplevel()
        self.exhibitHistoryWindow.title("exhibit History")

    def buildExhibitHistory(self,exhibitHistoryWindow):

        # Title Label
        viewExhibitLabel = Label(exhibitHistoryWindow, text = "Exhibits History", font = "Verdana 10 bold ")
        viewExhibitLabel.grid(row=1, column=3, sticky=W + E)

        # Title Label 2
        viewZooLabel = Label(exhibitHistoryWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=2, column=1, )

        # name lable
        nameLabel = Label(exhibitHistoryWindow, text="Name", font="Verdana 10 bold")
        nameLabel.grid(row=3, column=1)

        # name entry
        ExhibitName = StringVar()
        name = Entry(exhibitHistoryWindow, textvariable=ExhibitName, width=20)
        name.grid(row=3, column=2, sticky=W + E)

        # num Visits label
        numVisitsLabel = Label(exhibitHistoryWindow, text="Number of Visits", font="Verdana 10 bold")
        numVisitsLabel.grid(row=3, column=3)

        # min num visits
        # max num visits
        minLabel = Label(exhibitHistoryWindow, text="MIN", font="Verdana 10 bold ")
        minLabel.grid(row=2, column=4)

        maxLabel = Label(exhibitHistoryWindow, text="MAX", font="Verdana 10 bold ")
        maxLabel.grid(row=2, column=5)

        selectMinVisit = IntVar()
        selectMinVisit = Spinbox(exhibitHistoryWindow, from_=1, to=100, width=5)
        selectMinVisit.grid(row=3, column=4)

        selectMaxVisit = IntVar()
        selectMaxVisit = Spinbox(exhibitHistoryWindow, from_=1, to=100, width=5)
        selectMaxVisit.grid(row=3, column=5)

        # Time label
        TimeLabel = Label(exhibitHistoryWindow, text="Time", font="Verdana 10 bold")
        TimeLabel.grid(row=4, column=1)

        # Time Entry
        TimeEntry = StringVar()
        name = Entry(exhibitHistoryWindow, textvariable=TimeEntry, width=20)
        name.grid(row=4, column=2, sticky=W + E)

        self.tv_exhibit_history = ttk.Treeview(exhibitHistoryWindow)
        self.tv_exhibit_history['columns'] = ("Name", "Time", "Number of Visits")


        self.tv_exhibit_history.heading("Name", text='                     Name                             ▼', anchor='w')
        self.tv_exhibit_history.column("Name", minwidth=2)

        self.tv_exhibit_history.heading("Time", text="                     Time                             ▼", anchor='w')
        self.tv_exhibit_history.column("Time",  minwidth=2)

        self.tv_exhibit_history.heading("Number of Visits", text="                     Number of Visits              ▼")
        self.tv_exhibit_history.column("Number of Visits", minwidth=2)

        self.tv_exhibit_history['show'] = 'headings'
        self.tv_exhibit_history.grid(row=7, column=3, columnspan = 3  )

        def searchBottonFun():
            print(str(ExhibitName.get()), (str(selectMinVisit.get()),
                  str(selectMaxVisit.get())), str(TimeEntry.get()))
            self.searchExhibit_Hisotory(ExhibitName.get(), (selectMinVisit.get(),
                selectMaxVisit.get()), TimeEntry.get())


        searchButton = Button(exhibitHistoryWindow, text="Search", command=searchBottonFun)
        searchButton.grid(row=1, column=4)

        #Return Button
        returnButton = Button(exhibitHistoryWindow, text="Return", command=self.exhibitHistoryWindowReturnButtonClicked)
        returnButton.grid(row=1, column=5)

        self.tv_exhibit_history.bind("<Double-1>", self.exhibit_historyOnClicked2)

    def exhibit_historyOnClicked2(self, event):
        region = self.tv_exhibit_history.identify_region(event.x, event.y)
        if region == "heading":
            column = self.tv_exhibit_history.identify_column(event.x)
            self.treeview_sort_column(self.tv_exhibit_history, column, False)
        if region == "cell":
            curItem = self.tv_exhibit_history.item(self.tv_exhibit_history.focus())
            exhibitName = curItem['values'][0]
            condition = " WHERE A.Exhibit = E.Name "
            condition+=" AND A.Exhibit= '" + exhibitName +"'"
            sql = "SELECT E.Name, E.Size, count(*) as NumAnimals, E.Water_Feature as Water \
            FROM Exhibit as E, Animal As A " + condition + " GROUP BY A.Exhibit;"

            self.cursor.execute(sql)
            result_Exhibit_detail = self.cursor.fetchall()

            name = str(result_Exhibit_detail[0][0])
            size = str(result_Exhibit_detail[0][1])
            NumAnimals=str(result_Exhibit_detail[0][2])
            WaterFeature=str(result_Exhibit_detail[0][3])

            self.createExhibitDetailWindow()
            self.buildExhibitDetailWindow(self.ExhibitDetailWindow, name, size, NumAnimals, WaterFeature)

    def exhibitHistoryWindowReturnButtonClicked(self):
        # Click Return Button on Exhibit History Window:
        # Destroy Exhibit History Window
        # Display Choose Functionality Window
        self.exhibitHistoryWindow.destroy()
        self.chooseFunctionalityWindow.deiconify()

    #===========show History=========================
    def createShowHistory(self):
        self.showHistoryWindow = Toplevel()
        self.showHistoryWindow.title("Show History")

    def buildShowHistory(self, showHistoryWindow):
        # Title Label
        viewExhibitLabel = Label(showHistoryWindow, text="Show History", font="Verdana 10 bold ")
        viewExhibitLabel.grid(row=1, column=3, sticky=W + E)

        # Title Label 2
        viewZooLabel = Label(showHistoryWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=2, column=1, )

        # name lable
        nameLabel = Label(showHistoryWindow, text="Name", font="Verdana 10 bold")
        nameLabel.grid(row=3, column=1)

        # name entry
        ShowName = StringVar()
        name = Entry(showHistoryWindow, textvariable=ShowName, width=20)
        name.grid(row=3, column=2, sticky=W + E)

        # name lable
        nameLabel = Label(showHistoryWindow, text="Exhibit", font="Verdana 10 bold")
        nameLabel.grid(row=3, column=3)

        sql = "SELECT DISTINCT Exhibit FROM Shows;"
        self.cursor.execute(sql)
        ExhibitTuple = self.cursor.fetchall()
        ExhibitList = []
        ExhibitList.append("")
        for i in ExhibitTuple:
            ExhibitList.append(i[0])

        Exhibit = StringVar()
        Exhibit.set(ExhibitList[0])

        AtZooFromOptionMenu = OptionMenu(showHistoryWindow, Exhibit, *ExhibitList)
        AtZooFromOptionMenu.config(width= 10)

        AtZooFromOptionMenu.grid(row=3, column=4)

        # Time label
        sizeLabel = Label(showHistoryWindow, text="Time", font="Verdana 10 bold")
        sizeLabel.grid(row=4, column=1)

        # Time Entry
        TimeEntry = StringVar()
        name = Entry(showHistoryWindow, textvariable=TimeEntry, width=20)
        name.grid(row=4, column=2, sticky=W + E)

        #Time Format
        timeFormat = Label(showHistoryWindow, text="（HH:MM:SS）", font="Verdana 10 bold")
        timeFormat.grid(row=4, column=3)

        self.tv_show_history = ttk.Treeview(showHistoryWindow)
        self.tv_show_history['columns'] = ("Name", "Time", "Exhibit")

        self.tv_show_history.heading("Name", text='                     Name                             ▼', anchor='w')
        self.tv_show_history.column("Name", minwidth=2)

        self.tv_show_history.heading("Time", text="                     Time                             ▼", anchor='w')
        self.tv_show_history.column("Time",  minwidth=2)

        self.tv_show_history.heading("Exhibit", text="                     Exhibit                             ▼")
        self.tv_show_history.column("Exhibit", minwidth=2)

        self.tv_show_history['show'] = 'headings'
        self.tv_show_history.grid(row=7, column=3, columnspan = 3  )

        # Search Button
        def searchBottonFun():
            print(ShowName.get(), Exhibit.get(), TimeEntry.get())
            self.ShowHistory_Visitor(ShowName.get(), TimeEntry.get(), Exhibit.get())

        searchButton = Button(showHistoryWindow, text="Search", command=searchBottonFun)
        searchButton.grid(row=4, column=4)

        #Return Button
        returnButton = Button(showHistoryWindow, text="Return", command=self.showHistoryWindowReturnButtonClicked)
        returnButton.grid(row=4, column=5)

        self.tv_show_history.bind("<Double-1>", self.ShowHistDetailOnClicked2)

    def ShowHistDetailOnClicked2(self, event):
        region = self.tv_show_history.identify_region(event.x, event.y)
        if region == "heading":
            column = self.tv_show_history.identify_column(event.x)
            self.treeview_sort_column(self.tv_show_history, column, False)

    def showHistoryWindowReturnButtonClicked(self):
        # Click Return Button on Show History Window:
        # Destroy Show History Window
        # Display Choose Functionality Window
        self.showHistoryWindow.destroy()
        self.chooseFunctionalityWindow.deiconify()

## Staff
#==================StaffChoseFunctionalityTable =========================

    def createStaffChooseFunctionalityWindow(self):

        # Create blank chooseFunctionalityWindow
        self.chooseStaffFunctionalityWindow = Toplevel()
        self.chooseStaffFunctionalityWindow.title("Atlanta Zoo : Staff")

    def buildStaffChooseFunctionalityWindow(self,chooseStaffFunctionalityWindow):

        chooseStaffFunctionalityLabel = Label(chooseStaffFunctionalityWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        chooseStaffFunctionalityLabel.grid(row=1, column=2, sticky=W + E)

        # Search Animal
        searchStaffExhibitWindow = Button(chooseStaffFunctionalityWindow, text="search Animals",
                                     command=self.searchStaffAnimal)
        searchStaffExhibitWindow.grid(row=2, column=1)

        # view shows
        searchStaffShowsWindow = Button(chooseStaffFunctionalityWindow, text="View Shows",
                                   command=self.searchStaffShows)
        searchStaffShowsWindow.grid(row=2, column=2)

        logOutButton = Button(chooseStaffFunctionalityWindow, text="Log out",
                              command=self.chooseStaffFunctionalityWindowLogOutButtonClicked)
        logOutButton.grid(row=2, column=3, sticky=E)

    def chooseStaffFunctionalityWindowLogOutButtonClicked(self):
        self.chooseStaffFunctionalityWindow.withdraw()
        self.chooseStaffFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

    def searchStaffAnimal(self):
        self.createSearchStaffAnimalWindow()
        self.buildSearchStaffAnimalWinodw(self.searchStaffAnimalWindow)
        self.chooseStaffFunctionalityWindow.withdraw()

    def searchStaffShows(self):
        self.createSearchStaffShowsWindow()
        self.buildSearchStaffShowsWinodw(self.searchStaffShowsWindow)
        self.chooseStaffFunctionalityWindow.withdraw()

    # ==================  searchStaffAnimals ========================
    def createSearchStaffAnimalWindow(self):
        self.searchStaffAnimalWindow = Toplevel()
        self.searchStaffAnimalWindow.title("Search for Animal")


    def buildSearchStaffAnimalWinodw(self,searchStaffAnimalWindow):

        # viewZoo label
        viewZooLabel = Label(searchStaffAnimalWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=1, )

        # viewAnimal label
        viewAnimalLabel = Label(searchStaffAnimalWindow, text="Animals", font="Verdana 10 bold ")
        viewAnimalLabel.grid(row=1, column=3, sticky=W + E)

        # Exhibit label
        viewZooLabel = Label(searchStaffAnimalWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=5, )

        # Exhibit Drop Down Button
        # ExhibitTuple = self.cursor.fetchall()
        sql = "SELECT Name FROM Exhibit;"
        self.cursor.execute(sql)
        ExhibitTuple = self.cursor.fetchall()
        ExhibitList = []
        ExhibitList.append("")
        for i in ExhibitTuple:
            ExhibitList.append(i[0])
        # ExhibitList = []
        # for i in ExhibitTuple:
        #     ExhibitList.append(i[0])

        Exhibit = StringVar()
        Exhibit.set(ExhibitList[0])

        AtZooFromOptionMenu = OptionMenu(searchStaffAnimalWindow, Exhibit, *ExhibitList)
        AtZooFromOptionMenu.config(width= 10)

        AtZooFromOptionMenu.grid(row=1, column=7)

        # Animal Name Label
        viewZooLabel = Label(searchStaffAnimalWindow, text="Name", font="Verdana 10 bold ")
        viewZooLabel.grid(row=3, column=1, )

        # Animal Name Entry
        animalName = StringVar()
        nameEntry = Entry(searchStaffAnimalWindow, textvariable=animalName, width=10)
        nameEntry.grid(row=3, column=3, sticky=W + E)

        # Animal Age Label
        viewAge = Label(searchStaffAnimalWindow, text="Age", font="Verdana 10 bold ")
        viewAge.grid(row=3, column=5)

        # Animal Age Select
        # Don't know
        #
        # Animal Min Max Label
        minLabel = Label(searchStaffAnimalWindow, text="MIN", font="Verdana 10 bold ")
        minLabel.grid(row=2, column=7)

        maxLabel = Label(searchStaffAnimalWindow, text="MAX", font="Verdana 10 bold ")
        maxLabel.grid(row=2, column=8)

        selectMinAge = IntVar()
        selectMinAge = Spinbox(searchStaffAnimalWindow, from_=0, to=100, width=5)
        selectMinAge.grid(row=3, column=7)

        selectMaxAge = IntVar()
        selectMaxAge = Spinbox(searchStaffAnimalWindow, from_=0, to=100, width=5)
        selectMaxAge.grid(row=3, column=8)

        # Animal Species label
        viewZooLabel = Label(searchStaffAnimalWindow, text="Species", font="Verdana 10 bold ")
        viewZooLabel.grid(row=5, column=1)

        # Animal species Entry
        species = StringVar()
        speciesEntry = Entry(searchStaffAnimalWindow, textvariable=species, width=10)
        speciesEntry.grid(row=5, column=3, sticky=W + E)

        # Animal Type label
        viewAnimalType = Label(searchStaffAnimalWindow, text="Type", font="Verdana 10 bold ")
        viewAnimalType.grid(row=5, column=5, )

        # Animal Type  Drop Down Box
        # ExhibitTuple = self.cursor.fetchall()
        sql = "SELECT DISTINCT Type FROM Animal;"
        self.cursor.execute(sql)
        typeTuple = self.cursor.fetchall()
        typeList = []
        typeList.append("");
        for i in typeTuple:
            typeList.append(i[0])
        # ExhibitList = []
        # for i in ExhibitTuple:
        #     ExhibitList.append(i[0])


        Type = StringVar()
        Type.set(typeList[0])

        typeMenu = OptionMenu(searchStaffAnimalWindow, Type, *typeList)
        typeMenu.grid(row=5, column=7)

        self.tv_animal_detail = ttk.Treeview(searchStaffAnimalWindow)
        self.tv_animal_detail['columns'] = ("Name", "Species", "Exhibit", "Age", "Type")

        self.tv_animal_detail.heading("Name", text='                     Name                             ▼', anchor='w')
        self.tv_animal_detail.column("Name", minwidth=2)

        self.tv_animal_detail.heading("Species", text="                     Species                         ▼", anchor='w')
        self.tv_animal_detail.column("Species",  minwidth=2)

        self.tv_animal_detail.heading("Exhibit", text="                     Exhibit                          ▼")
        self.tv_animal_detail.column("Exhibit", minwidth=2)

        self.tv_animal_detail.heading("Age", text="                     Age                             ▼")
        self.tv_animal_detail.column("Age",  minwidth=2)

        self.tv_animal_detail.heading("Type", text="                     Type                             ▼")
        self.tv_animal_detail.column("Type",  minwidth=2)

        self.tv_animal_detail['show'] = 'headings'
        self.tv_animal_detail.grid(row=7, column=3, columnspan = 3  )

        def searchBottonFun():
            self.searchAnimal_Visitor(Exhibit.get(), animalName.get(), selectMinAge.get(),
                selectMaxAge.get(), species.get(), Type.get())
        # Search Button
        searchButton = Button(searchStaffAnimalWindow, text="Search", command=searchBottonFun)
        searchButton.grid(row=1, column=4)

        # Return Button
        returnButton = Button(searchStaffAnimalWindow, text="Return", command=self.searchStaffAnimalWindowReturnButtonClicked)
        returnButton.grid(row=1, column=5)

        self.tv_animal_detail.bind("<Double-1>", self.staffAnimalCare)

    def staffAnimalCare(self, event):
        region = self.tv_animal_detail.identify_region(event.x, event.y)
        if region == "heading":
            column = self.tv_animal_detail.identify_column(event.x)
            self.treeview_sort_column(self.tv_animal_detail, column, False)
        if region == "cell":
            curItem = self.tv_animal_detail.item(self.tv_animal_detail.focus())
            name = curItem['values'][0]
            species = curItem['values'][1]
            self.createStaffAnimalCare()
            self.buildStaffAnimalCare(self.StaffAnimalCareWindow, name, species)

    def searchStaffAnimalWindowReturnButtonClicked(self):
        # Click Return Button on Search Staff Animal Window:
        # Destroy Search Staff Animal Window
        # Display Choose Staff Functionality Window
        self.searchStaffAnimalWindow.destroy()
        self.chooseStaffFunctionalityWindow.deiconify()

    #================ Animal Care =================================
    def createStaffAnimalCare(self):
        self.StaffAnimalCareWindow = Toplevel()
        self.StaffAnimalCareWindow.title("Animal Detail")

    def buildStaffAnimalCare(self, staffAnimalCareWindow, name, species):
        #title label

        name, species, types, age, exhibit = self.animalDetail(name, species)

        label = Label(staffAnimalCareWindow, text= "Animal Detail", font="Verdana 10 bold")
        label.grid(row=1, column=2)

        # zoo label
        label = Label(staffAnimalCareWindow, text="Atlanta Zoo", font="Verdana 10 bold")
        label.grid(row=2, column=1)

        # Name Label
        label = Label(staffAnimalCareWindow, text="Name: " + name, font="Verdana 10 bold")
        label.grid(row=3, column=1)

        # species label
        label = Label(staffAnimalCareWindow, text="Species: "+species, font="Verdana 10 bold")
        label.grid(row=3, column=2)

        # age label
        label = Label(staffAnimalCareWindow, text="Age:  " + age, font="Verdana 10 bold")
        label.grid(row=3, column=3)

        # Exhibit label
        label = Label(staffAnimalCareWindow, text="Exhibit: " + exhibit, font="Verdana 10 bold")
        label.grid(row=4, column=1)

        # type label
        label = Label(staffAnimalCareWindow, text="Type: " + types, font="Verdana 10 bold")
        label.grid(row=4, column=2)

        # CareNote entry
        self.noteEntry = StringVar()
        note = Entry(staffAnimalCareWindow, textvariable=self.noteEntry, width=20)
        note.grid(row=5, column=1, sticky=W + E)

        # CareNote label
        noteLabel = Label(staffAnimalCareWindow, text="Note", font="Verdana 10 bold")
        noteLabel.grid(row=5, column=2)

        #time
        tran = {"Nov": "11", "Dec":"12", "Oct":"10", "Sep":"09", "Feb":"02",
        "Jan":"01", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07", "Aug":"08"}
        date = time.ctime()
        dateList = date.split()
        date = dateList[-1]+"-"+tran[dateList[1]]+"-"+dateList[2]+" "+dateList[3]

        # LogNote Button
        def steps():

            self.LogNote(name, species, date)


        LogNoteButton = Button(staffAnimalCareWindow, text="Log Note", command=steps)
        LogNoteButton.grid(row=5, column=3)


        # Table
        self.tv_Animal_Care = ttk.Treeview(staffAnimalCareWindow)
        self.tv_Animal_Care['columns'] = ("Staff Member", "Note", "Time")

        self.tv_Animal_Care.heading("Staff Member", text='                     Staff Member                             ▼', anchor='w')
        self.tv_Animal_Care.column("Staff Member", minwidth=2)

        self.tv_Animal_Care.heading("Note", text="                     Note                             ▼", anchor='w')
        self.tv_Animal_Care.column("Note", minwidth=2)

        self.tv_Animal_Care.heading("Time", text="                     Time                             ▼")
        self.tv_Animal_Care.column("Time", minwidth=2)

        self.tv_Animal_Care.grid(row=6, column=4, columnspan=3)

        sql = "SELECT Staff_member, Text, Datetime FROM Animal_Care WHERE Animal = '" + name + "' and Species = '"+ species +"' ;"
        print(sql)
        print(name)
        isshows = self.cursor.execute(sql)
        result_s = self.cursor.fetchall()
        print(result_s)
        self.tv_Animal_Care.delete(*self.tv_Animal_Care.get_children())
        for i, result in enumerate(result_s):
            self.tv_Animal_Care.insert("",i, value=(str(result[0]),str(result[1]),str(result[2])))

    # StaffLogNote
    #================Search  Staff Show ===========================

    def createSearchStaffShowsWindow(self):
        self.searchStaffShowsWindow = Toplevel()
        self.searchStaffShowsWindow.title("Search for Shows")

    def buildSearchStaffShowsWinodw(self,searchStaffShowsWindow):
        # viewZoo label
        viewZooLabel = Label(searchStaffShowsWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=1, )

        # viewAnimal label
        viewAnimalLabel = Label(searchStaffShowsWindow, text="   Staff- Show Historry", font="Verdana 10 bold ")
        viewAnimalLabel.grid(row=1, column=3, sticky=W + E)


        self.tv_staff_show = ttk.Treeview(searchStaffShowsWindow)
        self.tv_staff_show['columns'] = ("Name", "Time", "Exhibit")

        self.tv_staff_show.heading("Name", text='                     Name                             ▼', anchor='w')
        self.tv_staff_show.column("Name", minwidth=2)

        self.tv_staff_show.heading("Time", text="                     Time                             ▼", anchor='w')
        self.tv_staff_show.column("Time",  minwidth=2)

        self.tv_staff_show.heading("Exhibit", text="                     Exhibit                          ▼")
        self.tv_staff_show.column("Exhibit", minwidth=2)

        self.tv_staff_show.grid(row=9, column=3, columnspan = 3 )

        #self.searchShows_Staff(self.username[0])
        sql = "SELECT Name, Datetime, Exhibit FROM Shows WHERE Host = '" + self.username[0] + "';"


        isshows = self.cursor.execute(sql)
        result_s = self.cursor.fetchall()
        print(result_s)
        self.tv_staff_show.delete(*self.tv_staff_show.get_children())
        for i, result in enumerate(result_s):
            self.tv_staff_show.insert("",i, value=(str(result[0]),str(result[1]),str(result[2])))

        # Return Button
        returnButton = Button(searchStaffShowsWindow, text="Return",command=self.searchStaffShowsWindowReturnButtonClicked)
        returnButton.grid(row=1, column=5)

        self.tv_staff_show.bind("<Double-1>", self.Staff_ShowOnClicked)

    def Staff_ShowOnClicked(self, event):
        region = self.tv_staff_show.identify_region(event.x, event.y)
        if region == "heading":
            column = self.tv_staff_show.identify_column(event.x)
            self.treeview_sort_column(self.tv_staff_show, column, False)

    def searchStaffShowsWindowReturnButtonClicked(self):
        # Click Return Button on Search Staff Show Window:
        # Destroy Search Search Staff Show Window
        # Display Choose Staff Functionality Window
        self.searchStaffShowsWindow.destroy()
        self.chooseStaffFunctionalityWindow.deiconify()

    #==================------------------------------------------------

    #====== Admin Functionality Window

    def createAdminChooseFunctionalityWindow(self):
        # Create blank chooseFunctionalityWindow
        self.chooseAdminFunctionalityWindow = Toplevel()
        self.chooseAdminFunctionalityWindow.title("Atlanta Zoo : Admin")

    def buildChooseAdminFunctionalityWindow(self, chooseAdminFunctionalityWindow):
        chooseAdminFunctionalityLabel = Label(chooseAdminFunctionalityWindow, text="Atlanta Zoo",
                                              font="Verdana 10 bold ")
        chooseAdminFunctionalityLabel.grid(row=1, column=2, sticky=W + E)

        # view Visitor
        viewVisitorWindowAdmin = Button(chooseAdminFunctionalityWindow, text="view Visitor",
                                          command=self.adminViewVisitor)
        viewVisitorWindowAdmin.grid(row=2, column=1)

        # view Staff
        viewStaffWindow = Button(chooseAdminFunctionalityWindow, text="View staff",
                                        command=self.adminViewStaff)
        viewStaffWindow.grid(row=2, column=2)

        #view Shows
        viewShowsWindow = Button(chooseAdminFunctionalityWindow, text="View Shows",
                                 command=self.adminViewShows)
        viewShowsWindow.grid(row=3, column=1)

        # view Animals
        viewAnimalsWindow = Button(chooseAdminFunctionalityWindow, text="View Animals",
                                 command=self.adminViewAnimals)
        viewAnimalsWindow.grid(row=3, column=2)
        # Add Animals

        addAnimalsWindow = Button(chooseAdminFunctionalityWindow, text="Add Animals",
                                   command=self.adminAddAnimals)
        addAnimalsWindow.grid(row=3, column=3)

        # Add Shows
        addShowsWindow = Button(chooseAdminFunctionalityWindow, text="Add Shows",
                                command=self.adminAddShows)
        addShowsWindow.grid(row=4, column=1)

        logOutButton = Button(chooseAdminFunctionalityWindow, text="Log out",
                              command=self.chooseAdminFunctionalityWindowLogOutButtonClicked)
        logOutButton.grid(row=4, column=3, sticky=E)

    def chooseAdminFunctionalityWindowLogOutButtonClicked(self):
        self.chooseAdminFunctionalityWindow.destroy()
        self.loginWindow.deiconify()

    def adminViewVisitor(self):
        self.createAdminViewVistorWindow()
        self.buildAdminViewVisitorWindow(self.adminViewVisitorWindow)

    def adminViewStaff(self):
        self.createAdminViewStaffWindow()
        self.buildAdminViewStaffWindow(self.adminViewStaffWindow)

    def adminViewShows(self):
        self.createAdminViewShowsWindow()
        self.buildAdminViewShowsWindow(self.adminViewShowsWindow)

    def adminViewAnimals(self):
        self.createAdminViewAnimalsWindow()
        self.buildAdminViewAnimalsWindow(self.adminViewAnimalsWindow)

    def adminAddAnimals(self):
        self.createAdminAddAnimals()
        self.buildAdminAddAnimals(self.adminAddAnimalsWindow)

    def adminAddShows(self):
        self.createAdminAddShows()
        self.buildAdminAddShows(self.adminAddShowsWindow)

    # ====== Admin view Visitor ==========================
    def createAdminViewVistorWindow(self):
        self.adminViewVisitorWindow = Toplevel()
        self.adminViewVisitorWindow.title("Atlanta zoo")

    def buildAdminViewVisitorWindow(self,adminViewVisitorWindow):
        a = Label(adminViewVisitorWindow, text="Atlanta Zoo",font="Verdana 10 bold ")
        a.grid(row=1, column=1, sticky=W + E)

        b = Label(adminViewVisitorWindow, text="View Visitor", font="Verdana 10 bold ")
        b.grid(row=1, column=3, sticky=W + E)

        # Admin View Staff table
        self.tv_Admin_Visitor = ttk.Treeview(adminViewVisitorWindow)
        self.tv_Admin_Visitor['columns'] = ("UserName", "Email")

        self.tv_Admin_Visitor.heading("UserName", text='                     Username                         ▼', anchor='w')
        self.tv_Admin_Visitor.column("UserName", minwidth=2)

        self.tv_Admin_Visitor.heading("Email", text="                     Email                             ▼", anchor='w')
        self.tv_Admin_Visitor.column("Email", minwidth=2)

        self.tv_Admin_Visitor['show'] = 'headings'
        self.tv_Admin_Visitor.grid(row=3, column=1, columnspan=3)

        def show():
            sql = "SELECT U.Username, U.Email FROM Visitor as V, User as U WHERE V.Username = U.Username;"

            self.cursor.execute(sql)
            view_visitor_Admin = self.cursor.fetchall()
            print(view_visitor_Admin)
            self.tv_Admin_Visitor.delete(*self.tv_Admin_Visitor.get_children())
            for i, result in enumerate(view_visitor_Admin):
                print(result)
                self.tv_Admin_Visitor.insert("", i, value=(str(result[0]), str(result[1])))

        def steps():
            self.Admin_Delete_Visitor()
            show()

        show()
        c = Button(adminViewVisitorWindow, text="Delete Visitor", command=steps)
        c.grid(row=4, column=2)

        def bindData(event):
            region = self.tv_Admin_Visitor.identify_region( event.x, event.y)
            if region=="cell":
                curItem = self.tv_Admin_Visitor.item(self.tv_Admin_Visitor.focus())
                self.Admin_Delete_Visitor_UserName = str(curItem["values"][0])
                self.Admin_Delete_Visitor_Email = str(curItem["values"][1])

        def sortting(event):
            region = self.tv_Admin_Visitor.identify_region( event.x, event.y)
            if region=="heading":
                column = self.tv_Admin_Visitor.identify_column(event.x)
                self.treeview_sort_column(self.tv_Admin_Visitor, column, False)

        self.tv_Admin_Visitor.bind("<Button-1>", bindData)
        self.tv_Admin_Visitor.bind("<Double-1>", sortting)

    def Admin_Delete_Visitor(self):
        name = str(self.Admin_Delete_Visitor_UserName)
        sql1 = "DELETE FROM User WHERE Username = '" + name + "'; "
        sql2 = "DELETE FROM Visitor WHERE Username = '" + name + "'; "
        isVisitors1 = self.cursor.execute(sql2)
        self.db.commit();
        isVisitors2 = self.cursor.execute(sql1)
        self.db.commit();
        messagebox.showinfo("info","Deletion Succeed!")


# ====== Admin view Staff==========================

    def createAdminViewStaffWindow(self):
        self.adminViewStaffWindow = Toplevel()
        self.adminViewStaffWindow.title("Atlanta zoo")

    def buildAdminViewStaffWindow(self,adminViewStaffWindow):
        a = Label(adminViewStaffWindow, text="Atlanta Zoo",font="Verdana 10 bold ")
        a.grid(row=1, column=1, sticky=W + E)

        b = Label(adminViewStaffWindow, text="View Staff", font="Verdana 10 bold ")
        b.grid(row=1, column=3, sticky=W + E)

        # Admin View Staff table
        self.tv_Admin_Staff = ttk.Treeview(adminViewStaffWindow)
        self.tv_Admin_Staff['columns'] = ("UserName", "Email")

        self.tv_Admin_Staff.heading("UserName", text='                     Username                       ▼', anchor='w')
        self.tv_Admin_Staff.column("UserName", minwidth=2)

        self.tv_Admin_Staff.heading("Email", text="                     Email                             ▼", anchor='w')
        self.tv_Admin_Staff.column("Email", minwidth=2)

        self.tv_Admin_Staff['show'] = 'headings'
        self.tv_Admin_Staff.grid(row=3, column=1, columnspan=3)

        def show():
            sql = "SELECT U.Username, U.Email FROM Staff as V, User as U WHERE V.Username = U.Username;"

            self.cursor.execute(sql)
            view_visitor_Admin = self.cursor.fetchall()
            print(view_visitor_Admin)
            self.tv_Admin_Staff.delete(*self.tv_Admin_Staff.get_children())
            for i, result in enumerate(view_visitor_Admin):
                print(result)
                self.tv_Admin_Staff.insert("", i, value=(str(result[0]), str(result[1])))

        def steps():
            self.Admin_Delete_Staff()
            show()

        show()
        c = Button(adminViewStaffWindow, text="Delete Staff", command=steps)
        c.grid(row=4, column=2)

        def bindData(event):
            region = self.tv_Admin_Staff.identify_region( event.x, event.y)
            if region=="cell":
                curItem = self.tv_Admin_Staff.item(self.tv_Admin_Staff.focus())
                self.Admin_Delete_Staff_UserName = str(curItem["values"][0])
                self.Admin_Delete_Staff_Email = str(curItem["values"][1])
        def sortting(event):
            region = self.tv_Admin_Staff.identify_region( event.x, event.y)
            if region=="heading":
                column = self.tv_Admin_Staff.identify_column(event.x)
                self.treeview_sort_column(self.tv_Admin_Staff, column, False)


        self.tv_Admin_Staff.bind("<Button-1>", bindData)
        self.tv_Admin_Staff.bind("<Double-1>",sortting)

    def Admin_Delete_Staff(self):
        name = str(self.Admin_Delete_Staff_UserName)
        sql1 = "DELETE FROM Staff WHERE Username = '" + name + "'; "
        sql2 = "DELETE FROM Visitor WHERE Username = '" + name + "'; "
        isVisitors1 = self.cursor.execute(sql2)
        self.db.commit();
        isVisitors2 = self.cursor.execute(sql1)
        self.db.commit();
        messagebox.showinfo("info","Congraudations! You have log a visit to this show.")

    #======== view Show Admin============================
    def createAdminViewShowsWindow(self):
        self.adminViewShowsWindow = Toplevel()
        self.adminViewShowsWindow.title("Atlanta zoo")

    def buildAdminViewShowsWindow(self, adminViewShowsWindow):
         # Title Label
        viewZooLabel = Label(adminViewShowsWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=1, )

        # viewShow label
        viewShowLabel = Label(adminViewShowsWindow, text="Shows", font="Verdana 10 bold ")
        viewShowLabel.grid(row=1, column=3, sticky=W + E)

        # Show Name label
        ShowNameLabel = Label(adminViewShowsWindow, text="Name", font="Verdana 10 bold ")
        ShowNameLabel.grid(row=5, column=1)

        showName = StringVar()
        nameEntry = Entry(adminViewShowsWindow, textvariable=showName, width=10)
        nameEntry.grid(row=5, column=3, sticky=W + E)

        # Show Date Label
        showDateLabel = Label(adminViewShowsWindow, text="Date", font="Verdana 10 bold ")
        showDateLabel.grid(row=5, column=7)

         # Show Date label
        showDatetime = StringVar()
        showDateLabel = Entry(adminViewShowsWindow, textvariable=showDatetime, width=10)
        showDateLabel.grid(row=5, column=9)

        # Date Format
        DateFormat = Label(adminViewShowsWindow, text="YYYY-MM-DD", font="Verdana 10 bold ")
        DateFormat.grid(row=5, column=11, sticky=W + E)

        logVisitButton = Button(adminViewShowsWindow, text="Delete Show", command=self.Admin_Remove_Shows)
        logVisitButton.grid(row=4, column=2)

        self.tv_Shows_Admin = ttk.Treeview(adminViewShowsWindow)
        self.tv_Shows_Admin['columns'] = ("Name", "Exhibit", "Datetime")

        self.tv_Shows_Admin.heading("Name", text='                     Name                             ▼', anchor='w')
        self.tv_Shows_Admin.column("Name", minwidth=2)

        self.tv_Shows_Admin.heading("Exhibit", text="                     Exhibit                         ▼", anchor='w')
        self.tv_Shows_Admin.column("Exhibit", minwidth=2)

        self.tv_Shows_Admin.heading("Datetime", text="                     Datetime                         ▼")
        self.tv_Shows_Admin.column("Datetime", minwidth=2)

        self.tv_Shows_Admin['show'] = 'headings'
        self.tv_Shows_Admin.grid(row=9, column=3, columnspan=3)

        sql = "SELECT DISTINCT Exhibit FROM Shows;"
        self.cursor.execute(sql)
        ExhibitTuple = self.cursor.fetchall()
        ExhibitList = []
        ExhibitList.append("")
        for i in ExhibitTuple:
            ExhibitList.append(i[0])

        ShowNameLabel = Label(adminViewShowsWindow, text="Exhibit", font="Verdana 10 bold ")
        ShowNameLabel.grid(row=7, column=2)
        Exhibit = StringVar()
        Exhibit.set(ExhibitList[0])
        AtZooFromOptionMenu = OptionMenu(adminViewShowsWindow, Exhibit, *ExhibitList)
        AtZooFromOptionMenu.config(width= 10)
        AtZooFromOptionMenu.grid(row=7, column=3,columnspan=1)
        # Search Button
        def searchShooows():
            self.searchShows_Visitor(self.tv_Shows_Admin,showName.get(), showDatetime.get(), Exhibit.get())

        searchButton = Button(adminViewShowsWindow, text="Search", command=searchShooows)
        searchButton.grid(row=7, column=4)

        def bindData(event):
            region = self.tv_Shows_Admin.identify_region( event.x, event.y)
            if region=="cell":
                print("You have a single click.")
                curItem = self.tv_Shows_Admin.item(self.tv_Shows_Admin.focus())
                self.deleteShow_ShowName = str(curItem["values"][0])
                self.deleteShow_DataTime = str(curItem["values"][2])
                self.deleteShow_exhibitName = str(curItem["values"][1])
        def sortting(event):
            region = self.tv_Shows_Admin.identify_region( event.x, event.y)
            if region=="heading":
                column = self.tv_Shows_Admin.identify_column(event.x)
                self.treeview_sort_column(self.tv_Shows_Admin, column, False)


        self.tv_Shows_Admin.bind("<Double-1>",sortting)
        self.tv_Shows_Admin.bind("<Button-1>",bindData)

    def onClick_show_Admin(self,event):
        region = self.tv_Shows_Admin.identify_region( event.x, event.y)
        if region=="heading":
            column = self.tv_Shows_Admin.identify_column(event.x)
            self.treeview_sort_column(self.tv_Shows_Admin, column, False)

    def Admin_Remove_Shows(self):
        showName = self.deleteShow_ShowName
        date = self.deleteShow_DataTime
        sql1 = "DELETE FROM Shows WHERE Name = '" + showName + "' and Datetime ='"+date+"' ; "
        self.cursor.execute(sql1)
        self.db.commit();
        messagebox.showinfo("info","Deletion Succeed!")

    #===Admin view Animals =====================

    def createAdminViewAnimalsWindow(self):
        self.adminViewAnimalsWindow = Toplevel()
        self.adminViewAnimalsWindow.title("Atlanta zoo")

    def buildAdminViewAnimalsWindow(self,adminViewAnimalsWindow):

        # viewZoo label
        viewZooLabel = Label(adminViewAnimalsWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=1, )

        # viewAnimal label
        viewAnimalLabel = Label(adminViewAnimalsWindow, text="Animals", font="Verdana 10 bold ")
        viewAnimalLabel.grid(row=1, column=3, sticky=W + E)

        # Exhibit label
        viewZooLabel = Label(adminViewAnimalsWindow, text="Exhibit", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=5, )

        # Exhibit Drop Down Button
        sql = "SELECT Name FROM Exhibit;"
        self.cursor.execute(sql)
        ExhibitTuple = self.cursor.fetchall()
        ExhibitList = []
        ExhibitList.append("")
        for i in ExhibitTuple:
            ExhibitList.append(i[0])

        Exhibit = StringVar()
        Exhibit.set(ExhibitList[0])

        AtZooFromOptionMenu = OptionMenu(adminViewAnimalsWindow, Exhibit, *ExhibitList)
        AtZooFromOptionMenu.config(width= 10)
        AtZooFromOptionMenu.grid(row=1, column=7)

        # Animal Name Label
        viewZooLabel = Label(adminViewAnimalsWindow, text="Name", font="Verdana 10 bold ")
        viewZooLabel.grid(row=3, column=1, )

        # Animal Name Entry
        animalName = StringVar()
        nameEntry = Entry(adminViewAnimalsWindow, textvariable=animalName, width=10)
        nameEntry.grid(row=3, column=3, sticky=W + E)

        # Animal Age Label
        viewAge = Label(adminViewAnimalsWindow, text="Age", font="Verdana 10 bold ")
        viewAge.grid(row=3, column=5)

        # Animal Age Select
        # Don't know
        #
        # Animal Min Max Label
        minLabel = Label(adminViewAnimalsWindow, text="MIN", font="Verdana 10 bold ")
        minLabel.grid(row=2, column=7)

        maxLabel = Label(adminViewAnimalsWindow, text="MAX", font="Verdana 10 bold ")
        maxLabel.grid(row=2, column=8)

        selectMinAge = Spinbox(adminViewAnimalsWindow, from_=0, to=100, width=5)
        selectMinAge.grid(row=3, column=7)

        selectMaxAge = Spinbox(adminViewAnimalsWindow, from_=0, to=100, width=5)
        selectMaxAge.grid(row=3, column=8)

        # Animal Species label
        viewZooLabel = Label(adminViewAnimalsWindow, text="Species", font="Verdana 10 bold ")
        viewZooLabel.grid(row=5, column=1)

        # Animal species Entry
        species = StringVar()
        speciesEntry = Entry(adminViewAnimalsWindow, textvariable=species, width=10)
        speciesEntry.grid(row=5, column=3, sticky=W + E)

        # Animal Type label
        viewAnimalType = Label(adminViewAnimalsWindow, text="Type", font="Verdana 10 bold ")
        viewAnimalType.grid(row=5, column=5, )

        sql = "SELECT DISTINCT Type FROM Animal;"
        self.cursor.execute(sql)
        typeTuple = self.cursor.fetchall()
        typeList = []
        typeList.append("")
        for i in typeTuple:
            typeList.append(i[0])

        Type = StringVar()
        Type.set(typeList[0])

        typeMenu = OptionMenu(adminViewAnimalsWindow, Type, *typeList)
        typeMenu.grid(row=5, column=7)


        # # # Search Button
        # searchButton = Button(adminViewAnimalsWindow, text="Search", command=self.searchResultTable)
        # searchButton.grid(row=7, column=1)
        self.tv_animal_Admin = ttk.Treeview(adminViewAnimalsWindow)
        self.tv_animal_Admin['columns'] = ("Name", "Species", "Exhibit", "Age", "Type")

        self.tv_animal_Admin.heading("Name", text='                     Name                         ▼', anchor='w')
        self.tv_animal_Admin.column("Name", minwidth=2)

        self.tv_animal_Admin.heading("Species", text="                     Species                   ▼", anchor='w')
        self.tv_animal_Admin.column("Species",  minwidth=2)

        self.tv_animal_Admin.heading("Exhibit", text="                     Exhibit                 ▼")
        self.tv_animal_Admin.column("Exhibit", minwidth=2)

        self.tv_animal_Admin.heading("Age", text="                     Age                             ▼")
        self.tv_animal_Admin.column("Age",  minwidth=2)

        self.tv_animal_Admin.heading("Type", text="                     Type                             ▼")
        self.tv_animal_Admin.column("Type",  minwidth=2)

        self.tv_animal_Admin['show'] = 'headings'
        self.tv_animal_Admin.grid(row=7, column=3, columnspan = 3  )

        def searchBottonFun():
            self.searchAnimal_Admin(Exhibit.get(), animalName.get(), selectMinAge.get(),
                selectMaxAge.get(), species.get(), Type.get())


        searchButton = Button(adminViewAnimalsWindow, text="Search", command=searchBottonFun)
        searchButton.grid(row=1, column=4)

        c = Button(adminViewAnimalsWindow, text="Remove Animals", command=self.deleteAnimal_Admin)
        c.grid(row=8, column=3)

        def bindData(event):
            region = self.tv_animal_Admin.identify_region( event.x, event.y)
            if region=="cell":
                curItem = self.tv_animal_Admin.item(self.tv_animal_Admin.focus())
                self.delete_animal_name_admin = str(curItem["values"][0])
                self.delete_animal_species_admin = str(curItem["values"][1])

        def sortting(event):
            region = self.tv_animal_Admin.identify_region( event.x, event.y)
            if region=="heading":
                column = self.tv_animal_Admin.identify_column(event.x)
                self.treeview_sort_column(self.tv_animal_Admin, column, False)

        self.tv_animal_Admin.bind("<Button-1>",bindData)
        self.tv_animal_Admin.bind("<Double-1>",sortting)

    #remove anmial
    def deleteAnimal_Admin(self):
        sql1 = "DELETE FROM Animal WHERE Name = '" +self.delete_animal_name_admin+ "' AND Species = '" + self.delete_animal_species_admin + "';"
        self.cursor.execute(sql1)
        self.db.commit();
        messagebox.showinfo("info","Congraudations! You have delete a animal.")

    # ===Admin Add Animals =========================

    def createAdminAddAnimals(self):
        self.adminAddAnimalsWindow = Toplevel()
        self.adminAddAnimalsWindow.title("Atlanta zoo")

    def buildAdminAddAnimals(self, adminAddAnimalsWindow):
        # viewZoo label
        viewZooLabel = Label(adminAddAnimalsWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=1, )

        # viewZoo label
        viewZooLabel = Label(adminAddAnimalsWindow, text="AddAnimals", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=3, )

        # Animal Name Label
        viewZooLabel = Label(adminAddAnimalsWindow, text="Name", font="Verdana 10 bold ")
        viewZooLabel.grid(row=2, column=1, )

        # Animal Name Entry
        animalName = StringVar()
        nameEntry = Entry(adminAddAnimalsWindow, textvariable=animalName, width=10)
        nameEntry.grid(row=2, column=3, sticky=W + E)

        # Exhibit label
        viewZooLabel = Label(adminAddAnimalsWindow, text="Exhibit", font="Verdana 10 bold ")
        viewZooLabel.grid(row=4, column=1, )

        sql1 = "SELECT Name FROM Exhibit;"
        self.cursor.execute(sql1)
        ExhibitTuple = self.cursor.fetchall()
        ExhibitList = []
        for i in ExhibitTuple:
            ExhibitList.append(i[0])

        Admin_addAnimal_Exhibit = StringVar()
        Admin_addAnimal_Exhibit.set(ExhibitList[0])

        AtZooFromOptionMenu = OptionMenu(adminAddAnimalsWindow, Admin_addAnimal_Exhibit, *ExhibitList)
        AtZooFromOptionMenu.config(width= 10)

        AtZooFromOptionMenu.grid(row=4, column=3)

        # Type label
        viewZooLabel = Label(adminAddAnimalsWindow, text="Type", font="Verdana 10 bold ")
        viewZooLabel.grid(row=5, column=1, )


        TypeList = ["mammal", "bird", "amphibian", "reptile", "fish", "invertebrate"]

        Admin_addAnimal_Type = StringVar()
        Admin_addAnimal_Type.set(TypeList[0])

        AtZooFromOptionMenu = OptionMenu(adminAddAnimalsWindow, Admin_addAnimal_Type, *TypeList)
        AtZooFromOptionMenu.config(width= 10)

        AtZooFromOptionMenu.grid(row=5, column=3)

        # Species Name Label
        viewZooLabel = Label(adminAddAnimalsWindow, text="Species", font="Verdana 10 bold ")
        viewZooLabel.grid(row=7, column=1, )

        # Species Name Entry
        animalSpecies = StringVar()
        nameEntry = Entry(adminAddAnimalsWindow, textvariable=animalSpecies, width=10)
        nameEntry.grid(row=7, column=3, sticky=W + E)
        # Age

        minLabel = Label(adminAddAnimalsWindow, text="Age", font="Verdana 10 bold ")
        minLabel.grid(row=9, column=1)

        selectAge = IntVar()
        selectAge = Spinbox(adminAddAnimalsWindow, from_=0, to=100, width=5)
        selectAge.grid(row=9, column=3)

        def step():
            self.addAnimal_Admin(str(animalName.get()),
             str(animalSpecies.get()), str(Admin_addAnimal_Type.get()), str(selectAge.get()),str(Admin_addAnimal_Exhibit.get()))
        # Add Button
        addButton = Button(adminAddAnimalsWindow, text="Add Animal", command=step)
        addButton.grid(row=5, column=9)

    def addAnimal_Admin(self,Name, Species, Type, Age, Exhibit):
        sql = "INSERT INTO Animal(Name, Species, Type, Age, Exhibit) VALUES ('" + Name + "', '" + Species+ "', '" + Type+ "', " + Age + ", '" + Exhibit+"' );"
        self.cursor.execute(sql)
        self.db.commit();
        messagebox.showinfo("info","Congraudations! You have insert a animal.")

    #===Admin Add Shows =========================

    def createAdminAddShows(self):
        self.adminAddShowsWindow = Toplevel()
        self.adminAddShowsWindow.title("Atlanta zoo")

    def buildAdminAddShows(self,adminAddShowsWindow):

        # viewZoo label
        viewZooLabel = Label(adminAddShowsWindow, text="Atlanta Zoo", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=1)

        # viewZoo label
        viewZooLabel = Label(adminAddShowsWindow, text="AddShows", font="Verdana 10 bold ")
        viewZooLabel.grid(row=1, column=3)

        # Animal Name Label
        viewZooLabel = Label(adminAddShowsWindow, text="Name", font="Verdana 10 bold ")
        viewZooLabel.grid(row=2, column=1)

        # Animal Name Entry
        animalName = StringVar()
        nameEntry = Entry(adminAddShowsWindow, textvariable=animalName, width=10)
        nameEntry.grid(row=2, column=3, sticky=W + E)


        # Exhibit label
        viewZooLabel = Label(adminAddShowsWindow, text="Exhibit", font="Verdana 10 bold ")
        viewZooLabel.grid(row=4, column=1)


        sql1 = "SELECT Name FROM Exhibit;"
        self.cursor.execute(sql1)
        ExhibitTuple = self.cursor.fetchall()
        ExhibitList = []
        ExhibitList.append("")
        for i in ExhibitTuple:
            ExhibitList.append(i[0])

        Addmin_addShow_Exhibit = StringVar()
        Addmin_addShow_Exhibit.set(ExhibitList[0])

        AtZooFromOptionMenu_Exhibit = OptionMenu(adminAddShowsWindow, Addmin_addShow_Exhibit, *ExhibitList)
        AtZooFromOptionMenu_Exhibit.config(width= 10)

        AtZooFromOptionMenu_Exhibit.grid(row=4, column=3)

        # Staff label
        viewZooLabel_Staff = Label(adminAddShowsWindow, text="Staff", font="Verdana 10 bold ")
        viewZooLabel_Staff.grid(row=5, column=1)

        sql2 = "SELECT Username FROM Staff;"
        self.cursor.execute(sql2)
        StaffTuple = self.cursor.fetchall()
        StaffList = []
        StaffList.append("")
        for i in StaffTuple:
            StaffList.append(i[0])

        addShow_Staff = StringVar()
        addShow_Staff.set(StaffList[0])

        AtZooFromOptionMenu_Staff = OptionMenu(adminAddShowsWindow, addShow_Staff, *StaffList)
        AtZooFromOptionMenu_Staff.config(width= 10)

        AtZooFromOptionMenu_Staff.grid(row=5, column=3)

        # Date Label
        viewZooLabel = Label(adminAddShowsWindow, text="Date", font="Verdana 10 bold ")
        viewZooLabel.grid(row=6, column=1)

        # Date Entry
        addShow_Date = StringVar()
        nameEntry = Entry(adminAddShowsWindow, textvariable=addShow_Date, width=10)
        nameEntry.grid(row=6, column=3, sticky=W + E)

        # Date Format
        DateFormat = Label(adminAddShowsWindow, text="YYYY-MM-DD", font="Verdana 10 bold ")
        DateFormat.grid(row=6, column=5, sticky=W + E)
        # Time Label
        viewZooLabel_date = Label(adminAddShowsWindow, text="Time", font="Verdana 10 bold ")
        viewZooLabel_date.grid(row=7, column=1)

        # Time Entry
        addShow_time = StringVar()
        nameEntry = Entry(adminAddShowsWindow, textvariable=addShow_time, width=10)
        nameEntry.grid(row=7, column=3, sticky=W + E)

        # Time Format
        timeFormat = Label(adminAddShowsWindow, text="HH:MM:SS", font="Verdana 10 bold ")
        timeFormat.grid(row=7, column=5, sticky=W + E)

        def steps():
            Datetime = str(addShow_Date.get()) + " " + str(addShow_time.get())
            print(Datetime)
            self.addShows_Admin(str(animalName.get()),Datetime,str(addShow_Staff.get()),str(Addmin_addShow_Exhibit.get()))
        # Add Button
        addButton = Button(adminAddShowsWindow, text="Add Show", command=steps)
        addButton.grid(row=5, column=9)

    def addShows_Admin(self, Name, Datetime, Staff, Exhibit):
        sql1 = "SELECT * from Shows where Host = '"+Staff+ "' and Datetime = '" +Datetime+ "' ;"
        isThere = self.cursor.execute(sql1)
        if isThere:
            messagebox.showinfo("info","Sorry, this staff already host a show at this time.")
        else:
            sql = "INSERT INTO Shows(Name, Datetime, Host, Exhibit) VALUES ('" + Name + "', '" + Datetime + "', '" + Staff+ "', '" + Exhibit + "' );"
            self.cursor.execute(sql)
            self.db.commit();
            messagebox.showinfo("info","Congraudations! You have insert a show.")

    # ==================------------------------------------------------
    # ==================------------------------------------------------
    # ==================------------------------------------------------
    # ==================------------------------------------------------
    # ==================------------------------------------------------
    # ==================---------------- --------------------------------
    # ==================------------------------------------------------
    # ==================------------------------------------------------
    # ==================------------------------------------------------

#--------------------Database Connection-----------------
    def connect(self):
        try:
            db = pymysql.connect(host = 'academic-mysql.cc.gatech.edu',
                                 db = 'cs4400_group1', user = 'cs4400_group1', passwd = 'ehiHGsY7', autocommit=True)
            return db
        except:
            messagebox.showwarning('Error!','Cannot connect. Please check your internet connection.')
            return False

    def searchForExhibit_Visitor(self):
        name = str(self.nameEntry.get())
        size = [str(self.minsize_exhibit.get()), str(self.maxsize_exhibit.get())]
        water_feature = str(self.waterFeature_searchExhibit.get())
        num_animal = [str(self.minanimal.get()), str(self.maxanimal.get())]

        self.sort_exhibit_name_visitor = name
        self.sort_exhibit_size_visitor = size
        self.sort_exhibit_water_visitor = water_feature
        self.sort_exhibit_AnimalNum_visitor = num_animal

        print(name)
        print(size)
        print(water_feature)
        print(num_animal)

        condition = " WHERE A.Exhibit = E.Name "

        if water_feature == "Yes": condition+=" AND E.Water_Feature = true"
        elif water_feature == "No": condition+=" AND E.Water_Feature = false"
        else: condition+=" AND E.Water_Feature = false OR E.Water_Feature = true"

        if size: condition+=" AND E.size >=" +str(size[0]) + " and E.Size <=" + str(size[1])

        if name: condition+=" AND A.Exhibit= '" + name +"'"

        if num_animal: condition2= " HAVING count(*) >=" + str(num_animal[0]) +" and count(*) <="+ str(num_animal[1])+";"
        else: condition2 = ";"


        sql = "SELECT E.Name, E.Size, count(*) as NumAnimals, E.Water_Feature as Water \
        FROM Exhibit as E, Animal As A " + condition + " GROUP BY A.Exhibit" + condition2

        print(sql)

        self.cursor.execute(sql)
        self.result_searchForExhibit_Visitor = self.cursor.fetchall()

        self.tv.delete(*self.tv.get_children())
        for i, result in enumerate(self.result_searchForExhibit_Visitor):
            if result[3]==1 or result[3]=="1":
                water = "Yes"
            else:
                water = "No"
            self.tv.insert("",i, value=(str(result[0]),str(result[1]),str(result[2]),water))

        print(self.result_searchForExhibit_Visitor)

    def exhibitDetail(self, name):
        sql_exhibit_detail = "SELECT E.Name, E.Size, COUNT(*) as Num_Animals, E.Water_Feature \
        FROM Exhibit as E, Animal as A \
        WHERE A.Exhibit = E.Name and E.Name = '"+name+"' \
        GROUP BY E.Name;"

        print(sql_exhibit_detail)
        self.cursor.execute(sql_exhibit_detail)
        result = self.cursor.fetchall()
        print(result)

        sql_exhibit_animal = "SELECT A.Name, A.Species \
        FROM Animal as A, Exhibit as E WHERE E.Name = '" +name+ "' and A.Exhibit = E.Name;"

        print(sql_exhibit_animal)
        self.cursor.execute(sql_exhibit_animal)
        result_animal = self.cursor.fetchall()

        self.tv_exhibit_detail.delete(*self.tv_exhibit_detail.get_children())
        for i, result in enumerate(result_animal):
            self.tv_exhibit_detail.insert("",i, value=(str(result[0]),str(result[1])))
        print(result_animal)

    def animalDetail(self, name, species):
        #name = self.animal_detail
        sql = "SELECT * FROM Animal WHERE Name = '"+name+"' And Species = '"+species+"';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)
        result = result[0]
        return result[0], result[1], result[2], str(result[3]), result[4]

    def searchAnimal_Visitor(self, Exhibit, animalName, minLabel, maxLabel, species, Type):

        self.sort_animal_name_visitor = animalName
        self.sort_animal_species_visitor = species
        self.sort_animal_exhibit_visitor = Exhibit
        self.sort_animal_type_visitor = Type
        self.sort_animal_min_visitor = minLabel
        self.sort_animal_max_visitor = maxLabel

        condition = " WHERE Age>=" +str(minLabel)+ " and Age<=" +str(maxLabel)
        if Exhibit:
            condition+=" AND Exhibit = '"+Exhibit+"'"
        if animalName:
            condition+=" AND  Name = '" +animalName + "'"
        if species:
            condition+="  AND Species= '" + species + "'"
        if Type:
            condition+="  AND Type= '" + Type + "'"

        sql_searchShows = "SELECT Name, Species, Exhibit, Age, Type FROM Animal "+condition+";"
        print(sql_searchShows)
        self.cursor.execute(sql_searchShows)
        result_ani = self.cursor.fetchall()
        self.tv_animal_detail.delete(*self.tv_animal_detail.get_children())
        print(result_ani)
        for i, result in enumerate(result_ani):
            self.tv_animal_detail.insert("",i, value=(str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])))

    def searchShows_Visitor(self, tv_table, name, date, exhibit):


        if name or exhibit or date:
            condition = " WHERE "
        else: condition = ""
        tag = 1
        if name:
            condition+=" Name = '"+name+"'"
            tag = 0
        if date:
            if tag == 0:
                condition += " AND"
            condition+=" Datetime LIKE '" +date + "%'"
            tag = 0
        if exhibit:
            if tag == 0:
                condition += " AND"
            condition+=" Exhibit= '" + exhibit + "'"

        sql_searchShows = "SELECT Name, Exhibit, Datetime FROM Shows "+condition+";"
        print(sql_searchShows)
        self.cursor.execute(sql_searchShows)
        result_Shows = self.cursor.fetchall()
        tv_table.delete(*tv_table.get_children())
        for i, result in enumerate(result_Shows):
            tv_table.insert("",i, value=(str(result[0]),str(result[1]),str(result[2])))
        print(result_Shows)

    def searchExhibit_Hisotory(self, ExhibitName, Number_of_Visits, TimeEntry):

        if ExhibitName or TimeEntry or Number_of_Visits:
            condition = " WHERE "
            tag = 1
            if ExhibitName:
                condition += " Exhibit ='" + ExhibitName + "' "
                tag = 0
            if TimeEntry:
                if tag == 0:
                    condition += " AND"
                condition += " Datetime LIKE'" + TimeEntry + "%' "
                tag = 0
            if Number_of_Visits:
                if tag == 0:
                    condition += " AND"
                condition += " count >=" + str(Number_of_Visits[0]) + " and count <=" + str(Number_of_Visits[1]) + " "
            condition += ";"
        else:
            condition = " ;"

        sql_searchExhibitHist = "SELECT Exhibit as Name, Datetime as Time, count as Number_of_Visits FROM \
            ((SELECT VE.Exhibit, VE.Datetime  \
            FROM Visit_Exhibit as VE \
            WHERE VE.Visitor = '"+self.username[0]+"') as n1 \
            NATURAL JOIN  \
            (SELECT VE2.Exhibit, COUNT(*) as count \
            FROM Visit_Exhibit as VE2 \
            WHERE VE2.Visitor = '"+self.username[0]+"' \
            GROUP BY VE2.Exhibit, VE2.Visitor)as n2) " + condition +";"

        print(sql_searchExhibitHist)
        self.cursor.execute(sql_searchExhibitHist)
        result_exh = self.cursor.fetchall()
        self.tv_exhibit_history.delete(*self.tv_exhibit_history.get_children())
        print(result_exh)
        for i, result in enumerate(result_exh):
            self.tv_exhibit_history.insert("",i, value=(str(result[0]),str(result[1]),str(result[2])))
        self.db.commit()

    def ShowHistory_Visitor(self, ShowName, TimeEntry, Exhibit):

        condition = " WHERE V.ShowName = S.Name AND V.Datetime = S.Datetime AND V.Visitor = '" +self.username[0]+ "' "

        if ShowName: condition += " AND S.Name = '" + ShowName + "' "

        if Exhibit: condition += " AND S.Exhibit = '" + Exhibit + "' "

        if TimeEntry:
            condition2 = " AND V.Datetime LIKE '" + TimeEntry + "%' ;"
        else:
            condition2 = ";"

        sql_searchShowHist = "SELECT V.ShowName as Name, V.Datetime as Time, S.Exhibit \
        FROM Visit_Show as V, Shows As S " + condition + condition2

        print(sql_searchShowHist)
        self.cursor.execute(sql_searchShowHist)
        result_his = self.cursor.fetchall()
        self.tv_show_history.delete(*self.tv_show_history.get_children())
        print(result_his)
        for i, result in enumerate(result_his):
            self.tv_show_history.insert("",i, value=(str(result[0]),str(result[1]),str(result[2])))
        self.db.commit()

    def LogNote(self, name, Species, Datetime):

    # self.emailAddress = self.loginemail.get()
    # self.password = self.loginPassword.get()
        if self.noteEntry.get()!="":
            Text = self.noteEntry.get();
            StaffMember = self.username[0];

            sql = "INSERT INTO Animal_Care(Animal, Species, Staff_member, Datetime, Text)VALUES('" + name +"', '" + Species + "', '" + StaffMember + "', '" + Datetime + "', '" + Text + "');"

            print(sql)
            isAnmialCare = self.cursor.execute(sql)
            self.db.commit()
            result = self.cursor.fetchall()
            print(isAnmialCare)
            print(result)
        return True

    def searchAnimal_Admin(self, Exhibit, animalName, minLabel, maxLabel, species, Type):

        condition = " WHERE Age>=" +str(minLabel)+ " and Age<=" +str(maxLabel)
        if Exhibit:
            condition+=" AND Exhibit = '"+Exhibit+"'"
        if animalName:
            condition+=" AND  Name = '" +animalName + "'"
        if species:
            condition+="  AND Species= '" + species + "'"
        if Type:
            condition+="  AND Type= '" + Type + "'"

        sql_searchShows = "SELECT Name, Species, Exhibit, Age, Type FROM Animal "+condition+";"
        # print(sql_searchShows)
        self.cursor.execute(sql_searchShows)
        result_ani = self.cursor.fetchall()
        self.tv_animal_Admin.delete(*self.tv_animal_Admin.get_children())
        # print(result_ani)
        for i, result in enumerate(result_ani):
            self.tv_animal_Admin.insert("",i, value=(str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])))


a=AtlantaZoo()
a.db.close()
