# _**MGNREGA**_

MGNREGA is a Console Python Application used for User Management using SQLite Database.

##Download
```
git clone <URL to download the project>
```
## Installation
Activate your Python virtual environment, and download the required libraries.
```
virtualenv -p python3 env
source env/bin/activate
```
Install sqllite3 .

```bash
pip install db-sqlite3
```
Install Pandas .

```bash
pip install pandas
```
Install Pandas .

```bash
pip install pandas
```


How to run the project
```
python main.py
```
Create an admin using sql query so that you can create GPMs and Members
```
INSERT INTO Users(username, password, name, role) VALUES(?, ?, ? ,?);
```
## User scenarios

This project contains three different User Scenarios:
1)Block Development Officer
2)Gram Panchayat Member
3)Members

Block Development Officer has following options
```
(1)Create GPM accounts
(2)Delete GPM accounts
(3)Update GPM
(4)Create Project
(5)Update Project
(6)Delete Project
(7)Show GPM accounts
(8)Show Projects
(9)Show member accounts
(10)See the complaints
(11)Approve Pending Requests
(12)Previous Menu

```

Grama Panchayat Member has following options

```
(1)Add Members
(2)Show Members
(3)Assign the members to projects
(4)Pending approvals
(5)Previous Menu

```

Members have following options
```
(1)View Details
(2)File complaints
(3)Previous Menu

```
