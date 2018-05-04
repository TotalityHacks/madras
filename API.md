# Madras API

## Login
Login to the API and return a token used for authenticating future requests.
- URL: `/login/`
- Method: `POST`
- POST Parameters (JSON format)
    - `username`: The user's username.
    - `password`: The user's password.
- Response
    - On Success: Returns JSON in the format `{'token': '...'}`.
    - On Error: Returns JSON with the error response.

## Registration
Register a user
- URL: `/registration/signup/`
- Method: `POST`
- POST Parameters
    - `email`: The user's email.
    - `password1`: The user's password.
    - `password2`: Confirmation of user's password.
    - `github_user_name`: The user's github username (Optional).- Response
- On Success: Returns JSON in the format `{'success': true}`.
- On Error: Returns JSON with the error response `{'success': false, 'err_field': ...}`.

Activate a user's account
Note: This is sent to the user in an email, should not need to be called directly.
- URL: `/registration/activate/{uidb4}/{token}`
- Method: `GET`
- On Success: Activates the user's account, returns JSON with format `{'message': '...'}`
- On Error: Returns JSON with format `{'error': '...'}`

## Checkin
Return the QR code for the currently authenticated user.
- URL: `/checkin/get_qr_code`
- Method: `GET`
- On Success: Returns HTTPResponse with the generated QR code.
- On error: No errors should occur, except for generic django errors if the user is not logged in.

Return the QR code for any arbitrary user.
- URL: `/checkin/get_qr_code_admin`
- Method: `GET`
- GET parameters
    - email: the email of the user.
- On Success: Returns HTTPResponse with the generated QR code.
- On error: returns JSON with the error response `{'success': false, 'error': {'message': ..., 'title': ...}}`

Check in a user.
- URL: `/checkin/check_in`
- Method: `POST`
- POST parameters
    - uuid: the uuid of the user's check in group, as encoded in the QR code.
- On Success: returns JSON with the response `{'success: True'}`
- On error: returns JSON with the error response: `{'success': false, 'error': {'message': ..., 'title': ...}}`

Check out a user.
- URL: `/checkin/check_out`
- Method: `POST`
- POST parameters
    - uuid: the uuid of the user's check in group, as encoded in the QR code.
- On Success: returns JSON with the response `{'success: True'}`
- On error: returns JSON with the error response: `{'success': false, 'error': {'message': ..., 'title': ...}}`

