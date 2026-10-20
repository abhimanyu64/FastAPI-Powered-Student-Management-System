# FastAPI-Powered-Student-Management-System

## Project Documentation and Final Report

---

## 1. Abstract

The Student Database Management System is a full-stack application designed to organize and manage student records efficiently. It provides a web-based interface for creating, viewing, searching, updating, and deleting student information.

The backend is developed using Python and FastAPI, while SQLite provides persistent data storage. The frontend uses HTML, CSS, and JavaScript to provide an interactive dashboard. Pandas and NumPy support CSV dataset processing, data validation, and statistical analysis.

The system also supports importing student records from a CSV dataset and automatically generating student IDs through SQLite.

## 2. Objectives

The primary objectives of this project are:

1. To develop a user-friendly student record management application.
2. To implement Create, Read, Update, and Delete (CRUD) operations.
3. To store and retrieve records using an SQLite database.
4. To generate unique student IDs automatically.
5. To validate user inputs and handle duplicate records.
6. To import student datasets from CSV files.
7. To apply Pandas and NumPy for data processing and analysis.
8. To document the implementation, testing procedures, and final outcome.
9. To maintain project code and documentation in a GitHub repository.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming and data processing |
| FastAPI | REST API development |
| SQLite | Persistent relational database |
| HTML | Dashboard structure |
| CSS | Dashboard styling and responsive layout |
| JavaScript | Frontend interaction and API communication |
| Pandas | CSV reading, data cleaning, and tabular analysis |
| NumPy | Numeric validation and statistical calculations |
| Git and GitHub | Version control and project hosting |

## 4. System Architecture

The application consists of three main layers.

### 4.1 Frontend

The frontend provides a dashboard for managing student information. Users can add new records, view existing records, search for students, edit details, and delete records.

### 4.2 Backend

The FastAPI backend receives frontend requests, validates input, executes database operations, and returns JSON responses.

### 4.3 Database

SQLite stores student records persistently. Each record contains a unique student ID, name, email, course, and academic year.

The intended data flow is:

**User → Web Dashboard → FastAPI Backend → SQLite Database → API Response → Dashboard**

## 5. Implementation

### 5.1 Student Record Management

The application implements CRUD functionality:

- **Create:** Adds a student record.
- **Read:** Retrieves all students or an individual student.
- **Update:** Modifies an existing record.
- **Delete:** Removes a selected record.

### 5.2 Automatic Student ID Generation

The student ID is generated automatically by SQLite using an auto-incrementing primary key. The project is configured to start IDs at 501 for a fresh database. Existing database records retain their IDs.

### 5.3 Input Validation and Error Handling

The backend validates required fields and academic year values. Duplicate email addresses are rejected, and requests for nonexistent student IDs return an appropriate error response.

### 5.4 CSV Dataset Import

The project includes a sample CSV dataset with the columns `name`, `email`, `course`, and `year`.

The CSV import script reads the dataset, checks required fields, validates numeric year values, and sends valid records to the backend API. Duplicate email addresses are skipped and other failures are reported.

### 5.5 Pandas and NumPy

Pandas is used to read and process CSV records, normalize column names, clean text fields, and summarize student data.

NumPy is used for numeric validation and calculating statistics such as minimum, maximum, mean, and median academic year.

## 6. Testing and Verification

The following tests should be performed and the actual results recorded before submission.

| Test case | Expected result | Actual result |
|---|---|---|
| **Create student** | Record created successfully | <img width="400" alt="create_student" src="https://github.com/user-attachments/assets/1c0cbf73-7717-4dec-bfd1-d375437e21ec"> |
| **Read students** | Student records displayed | <img width="400" alt="student_dashboard" src="https://github.com/user-attachments/assets/d35cdc3d-e9c8-40df-bd6d-8afb9c22e374"> |
| **Update student** | Changes saved successfully | <img width="400" alt="update_student" src="https://github.com/user-attachments/assets/c5f37b4d-f148-4e07-bd00-3416ed62cc09"> |
| **Delete student** | Selected record removed | <img width="400" alt="delete_student" src="https://github.com/user-attachments/assets/2fe842c5-53a0-41fa-a7a7-7e630858cc41"> |
| **Database persistence** | Records remain after backend restart | <img width="400" alt="database" src="https://github.com/user-attachments/assets/d4be4ea0-918d-4fff-86a4-4b8121c9ded9"> |
| **CSV import** | Valid rows imported and counts reported | <img width="400" alt="student_csv" src="https://github.com/user-attachments/assets/48ca3b73-1dbc-444f-a1ba-7f08ea0929df"> |
| **Dataset analysis** | Dataset statistics displayed | <img width="400" alt="pandas and numpy analysis" src="https://github.com/user-attachments/assets/28eadbcf-a4de-4cd9-bf8d-d0c091074103"> |

## 7. Results and Discussion

After successful execution and verification, the project demonstrates a web-based approach to student record management. The dashboard provides access to student information, while the backend API performs database operations and the SQLite database preserves records between application restarts.

The CSV import and analysis scripts extend the application by allowing batch data entry and dataset-level analysis.

Insert the actual observations and screenshots obtained during testing before final submission.

## 8. Limitations and Future Enhancements

Possible future improvements include:

- Authentication and role-based access control.
- Direct CSV upload through the web dashboard.
- Exporting filtered student records to CSV.
- More advanced data visualization and reporting.
- Improved audit logging and database backup facilities.
- Automated unit and integration tests.
- Deployment to a hosted server.

## 9. Final Outcome

The project is designed to provide an integrated student database management solution combining a web interface, REST API, persistent database, and dataset analysis tools.

The final submission should include the complete source code, sample CSV dataset, README instructions, project documentation, and genuine screenshots demonstrating the application's behavior.

The project should be considered complete only after the implementation has been executed, the verification tests have been performed, and the resulting evidence has been reviewed.


