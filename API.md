# Madras API

## Login
Login to the API and return a token used for authenticating future requests.
- URL: `/login`
- Method: `POST`
- POST Parameters (JSON format)
    - `username`: The user's username.
    - `password`: The user's password.
- Response
    - On Success: Returns JSON in the format `{'token': '...'}`.
    - On Error: Returns JSON with the error response.

## Registration
Register a user
- URL: `/signup`
- Method: `POST`
- POST Parameters (JSON Format)
    - `email`: The user's email.
    - `password1`: The user's password.
    - `password2`: Confirmation of user's password.
    - `github_user_name`: The user's github username (Optional).- Response
- On Success: Returns JSON in the format `{'success': true}`.
- On Error: Returns JSON with the error response `{'success': false, 'err_field': ...}`.

Activate a user's account
- URL: `/activate/{uidb4}/{token}`
- Method: `GET`
- On Success: Activates the user's account, returns JSON with format `{'message': '...'}`
- On Error: Returns JSON with format `{'error': '...'}`
