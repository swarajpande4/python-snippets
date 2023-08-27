## Flask JWT Auth Sample Application
Flask JWT Auth sample application based on the application factory design. 


## API Reference

1. **Signup API**
    ```bash
    curl -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=<USERNAME>&password=<PASSWORD>" \
    http://localhost:5000/signup
    ```

2. **Login API (Accepting Form Data)**:

    ```bash
    curl -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=<USERNAME>&password=<PASSWORD>" \
    http://localhost:5000/login
    ```

3. **Get All Users API**:


    ```bash
    curl -X GET \
    -H "Authorization: Bearer <YOUR ACCESS TOKEN>" \
    http://localhost:5000/users
    ```

4. **Get User API**:

    ```bash
    curl -X GET \
    -H "Authorization: Bearer <YOUR ACCESS TOKEN>" \
    http://localhost:5000/user/<userid>
    ```

5. **Add User API (Accepting Form Data)**:

    ```bash
    curl -X POST \
    -H "Authorization: Bearer <YOUR ACCESS TOKEN>" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=<NAME>&username=<USERNAME>" \
    http://localhost:5000/user
    ```

6. **Edit User API (Accepting Form Data)**:

    ```bash
    curl -X PUT \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=<NAME>&username=<USERNAME>" \
    http://localhost:5000/user/<userid>
    ```

7. **Delete User API**:

    ```bash
    curl -X DELETE \
    -H "Authorization: Bearer <YOUR ACCESS TOKEN>" \
    http://localhost:5000/user/<userid>
    ```