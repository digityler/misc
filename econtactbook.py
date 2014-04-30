#econtactbook.py
#
#Tyler Clark
#23 Dec 2012
#
#a text based contact book that can store, update, and retrieve a
#contact's name, address, phone number, and email by using an xml file
#
#


import xml.etree.ElementTree as ET
#xml parser


class Tree:
    #returns root of existing ebook xml file or creates new one

    def getBook(self):
        try:
            tree = ET.parse('ebook.xml')
            book = tree.getroot()
        except:
            book = ET.Element('book')
            tree = ET.ElementTree(book)
            tree.write('ebook.xml')
            tree = ET.parse('ebook.xml')
            book = tree.getroot()
        return book

  
class TextUI:
    #provides functions for text based user interface
    
    aTree = Tree()
    #common Tree instance referred to by Contact and CommandExec classes
    
    def __init__(self):
        #intro printed only when program is first run
        print("Welcome to your electronic contact book!")
        print("Here is the list of commands for your ebook.")
        print("Enter one of the following letters to proceed.")
    
    def commandList(self):
        #main directory, referred to after each command entry
        print()
        print("N - New: creates a contact")
        print("D - Delete: removes a contact")
        print("U - Update: changes a contact's information")
        print("S - Search: looks for an existing contact")
        print("A - All: displays all contacts")
        print("Q - Quit: exits the application")
        return self.commandEntry()

    def commandEntry(self):
        #based on input, directs to contact creation or executes a command on an existing contact
        print()
        c = input("Please enter a command: ").upper()
        
        if c == 'N':
            name, address, phone, email = self.getInputs()
            aContact = Contact(name, address, phone, email)
            return True
        elif c == 'D':
            comDel = CommandExec()
            comDel.delContact()
            return True
        elif c == 'U':
            comUpdate = CommandExec()
            comUpdate.updateContact()
            return True
        elif c == 'S':
            print()
            name = input("Enter the name of the contact you would like to look up: ")
            comSearch = CommandExec()
            comSearch.searchContact(name)
            return True
        elif c == 'A':
            comAll = CommandExec()
            comAll.displayAll()
            return True
        elif c == 'Q':
            return False
        else:
            print()
            print("Invalid entry.")
            return True
    
    def getInputs(self):
        #gets and then returns 4 pieces of info about a new contact from the user
        print()
        self.name = input("Enter name: ")
        self.address = input("Enter address: ")
        self.phone = input("Enter phone number: ")
        self.email = input("Enter email: ")
        return self.name, self.address, self.phone, self.email


class Contact:
    #creates a contact with name, address, phone, email and writes to an xml file

    def __init__(self, name, address, phone, email):
        #sets all tags with the contact's name as an attribute
        
        aTree = TextUI.aTree
        book = aTree.getBook()
        #creates instance of Tree and sets book as root
        
        #appends contact tag to root, book
        contact = ET.SubElement(book, 'contact', key = name)
        
        #appends each piece of information to its contact tag
        nameTag = ET.SubElement(contact, 'name', key = name)
        nameTag.text = name

        addressTag = ET.SubElement(contact, 'address', key = name)
        addressTag.text = address

        phoneTag = ET.SubElement(contact, 'phone', key = name)
        phoneTag.text = phone

        emailTag = ET.SubElement(contact, 'email', key = name)
        emailTag.text = email
         
        tree = ET.ElementTree(book)
        tree.write('ebook.xml')

        print()
        print("The contact has been saved in your ebook as shown.")


class CommandExec:
    #contains all functions for acting on a contact
    #includes getBook within class for up to date contact info

    def __init__(self):
        #creates instance of Tree and sets book as root
        aTree = TextUI.aTree
        self.book = aTree.getBook()

    def displayAll(self):
        #displays all information for all contacts
        for node in self.book.iter():
            if (node.tag != 'book') and (node.tag != 'contact'):
                print(node.text)
            else:
                print()

    def searchContact(self, name):
        #searches for a specific contact by name and displays all info
        print()
        i = 0
        for node in self.book.iter():
            if (node.get('key') == name) and (node.tag != 'contact'):
                print(node.text)
                i = i + 1
        if i == 0:
            print("There is no contact by that name.")
            return False
        else:
            return True
                
    def delContact(self):
        #removes a contact from the book
        print()
        name = input("Enter the name of the contact you would like to delete: ")
        
        #confirms decision and then loops thru and deletes each tag matching the name attribute
        deleteProceed = self.searchContact(name)
        print()
        while deleteProceed == True:
            decision = input("Are you sure you want to delete this contact? (Y/N) ").upper()
            print()
            if decision == 'Y':
                for parentnode in self.book.iter():
                    for childnode in parentnode:
                        if childnode.get('key') == name:
                            parentnode.remove(childnode)
                            tree = ET.ElementTree(self.book)
                            tree.write('ebook.xml')
                print(name, "has been deleted.")
                return False
            elif decision == 'N':
                return False
            else:
                print("Please type either Y or N.")
                print()

    def updateContact(self):
        #updates a contact's information, one piece at a time
        print()
        name = input("Enter the name of the contact you would like to update: ")
        
        #waits on user input and then writes over the selected value with new info
        updateProceed = self.searchContact(name)
        print()
        while updateProceed == True:
            print("N - name")
            print("A - address")
            print("P - phone")
            print("E - email")
            print("C - cancel")
            print()
            infoType = input("Type one of the above letters to update a field, or C to cancel: ").upper()
            print()
            if infoType == 'N':
                infoType = 'name'
                newInfo = input("Enter the new name: ")
                self.updateInfo(name, infoType, newInfo)
                
                #resets all tag attributes to the new name
                for node in self.book.iter():
                    if node.get('key') == name:
                        node.set('key', newInfo)
                        tree = ET.ElementTree(self.book)
                        tree.write('ebook.xml')
                self.searchContact(newInfo)
                return False
            elif infoType == 'A':
                infoType = 'address'
                newInfo = input("Enter the new address information: ")
                self.updateInfo(name, infoType, newInfo)
                self.searchContact(name)
            elif infoType == 'P':
                infoType = 'phone'
                newInfo = input("Enter the new phone number: ")
                self.updateInfo(name, infoType, newInfo)
                self.searchContact(name)
            elif infoType == 'E':
                infoType = 'email'
                newInfo = input("Enter the new email: ")
                self.updateInfo(name, infoType, newInfo)
                self.searchContact(name)
            elif infoType == 'C':
                return False
            else:
                print("Please type one of the above letters to update, or C to cancel.")
            print()

    def updateInfo(self, name, infoType, newInfo):
        #called by all update selections, loops thru and changes info based on selection and name attribute
        for node in self.book.iter():
            if (node.get('key') == name) and (node.tag == infoType):
                node.text = newInfo
                tree = ET.ElementTree(self.book)
                tree.write('ebook.xml')
                print()
                print("Update made.")


def main():
    #main loop, waits for user input and keeps redirecting to command list
    stillRunning = True
    starter = TextUI()
    while stillRunning == True:
        stillRunning = starter.commandList()

main()


