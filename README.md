*Artiselite Technical Assessment*
This project is built using Vue.js (with Vuetify), FastAPI, and PostgreSQL.

*Running the Application*
*Frontend*
1. Navigate to the project root directory.
2. Run the following command: npm run dev  

*Backend (API)*
1. Navigate to the fastApi folder.
2. Start the API server with: uvicorn main:app --reload  

*Initialization*
The application requires user authentication before accessing the frontend. An admin user must first be created manually to initialize the application. The following setup steps are required:

1. Set up roles in the database:
Run the following SQL commands in PGAdmin4 to populate the roles table:

INSERT INTO roles (id, name) VALUES (0, 'Admin');  
INSERT INTO roles (id, name) VALUES (1, 'Manager');  
INSERT INTO roles (id, name) VALUES (2, 'Operator');  

2. Create an initial admin user:
Insert at least one admin user directly into the database.

Once the above steps are complete, the admin user can log in to the application and manage users and roles.

*Features*
*Completed Features*
- Authentication System:
- - User login and registration (managed by the admin).
- - Role-based access control (Admin, Manager, Operator).

- Inventory Management (accessible to Admins and Managers):
- - Add, delete, view, and edit inventory items.

- Team Management:
- - Admins can create and manage users.
- - All roles can view the team interface.

*Partially Completed Features*
- Inbound Interface:
- - Development in progress; not fully implemented
- Outbound Interface:
- - Development in progress; not fully implemented

*Known limitations*
- Operators currently have access to inventory, which is not aligned with the project requirements. This will be restricted given more time
