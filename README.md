## Library Management Web Application

## Introduction:
This Library Management System is a web application designed to manage library operations efficiently. Built with Flask, it leverages SQLAlchemy for database interactions and Flask-Migrate for easy database migrations. The system allows for comprehensive management of books, members, and transactions, including book issuance and returns, with an intuitive user interface

## Features
Book Management: Add, update, delete, and search for books.
Member Management: Register new members, update member details, and manage member information.
Transaction Management: Issue and return books, with automated rent calculations.
Import Books: Bulk import books using an external API.
Responsive Design: The application is built using Bootstrap, ensuring a responsive design that adapts to different screen sizes.


## Usage:
Navigate through the application using the menu to access different sections. Each section provides forms and tables to manage the corresponding entities (books, members, transactions). Utilize the search functionality to quickly find specific records.


## Functionality:
- CRUD operations on Books and Members.
- Issuing and returning books to/from members.
- Searching for books by name and author.
- Charging rent fees on book returns.
- Debt management for members.

## Technologies Used :
Backend Framework: Flask
Frontend: HTML, CSS, JavaScript (if applicable)
Database:  SQLite as the database management system (DBMS) and SQLAlchemy as an Object-Relational Mapping (ORM) tool
Deployment:pythonanywhere.com

## Screenshots:
Include screenshots of key screens and reports:
open a browser and type poorvi.pythonanywhere.com
1. Home Page
   Home page consists of 6 buttons as shown below.
   ![Homre_Page](https://github.com/Poorvi-R-Bhat/Library/assets/27720465/d5c96024-7a16-40f3-bd00-d427a331d9e2)
   
2. Book Management
   Following are the functionalities under Book Management
   Here the new book can be added
   Book can be searched based on Author and Title
   Select all and Delete all books
   Issue books
  ![Manage_books](https://github.com/Poorvi-R-Bhat/Library/assets/27720465/dbbe248c-192f-4514-863d-a1571e827cdf)

3. Adding a Member
   ![Manage_member](https://github.com/Poorvi-R-Bhat/Library/assets/27720465/4455d0bb-a641-40f4-8733-16a3bd78e232)

4.Updating the existing Member
   By clicking the edit icon in the member page,Member can be updated
   ![Update_Member](https://github.com/Poorvi-R-Bhat/Library/assets/27720465/2826ea87-f3c7-4bf2-ad47-c6dfc87d7732)

5. Issue the book to a member
   Issuing a book to member with the rent fee
   ![Issue_Book](https://github.com/Poorvi-R-Bhat/Library/assets/27720465/5ec98abc-bbe4-4fda-b4f8-ff22dfbdd2eb)

6. Updating the book
   Books can be updated by clicking on the Edit icon from the Book page
   ![Update_book](https://github.com/Poorvi-R-Bhat/Library/assets/27720465/009cec88-6071-4ee3-9572-087f2dc23609)

7. Import Books
   Bulk importing the book using API (at a time 20)
   ![Import_book](https://github.com/Poorvi-R-Bhat/Library/assets/27720465/8db324b8-4113-4d9f-b6c2-03d3ccc86213)

8. Returning the book issued
   Book which was issued can be returned by clicking on Return Book button from the home page
  ![Return_Book](https://github.com/Poorvi-R-Bhat/Library/assets/27720465/23f7e3fa-38dc-431a-841b-a1502902daed)


10. Transaction
   To view the transaction and deleting all the transactions, click on View transaction button from the Home page
   ![View_Transactions](https://github.com/Poorvi-R-Bhat/Library/assets/27720465/9a4cea49-11f5-4fd4-be2d-ac5b1fda70ca)


   
