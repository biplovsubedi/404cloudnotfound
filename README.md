# 404cloudnotfound
Sample Code for 404 Cloud Not Found Team

Lambda handler available in main.py in lib folder.

Google Maps data is  retrieved using Google Maps API key. Since this is a private key, and uploading it in github public repo raises an alert, it has been removed from the file.

Please supply your personal Google Maps API key in lib.googleroutes.py (variable -- GMAPS_API_KEY)

Leaving it blank raises an error.

Usage:
1. Update GMAPS_API_KEY.
2. Create a DynamoDB table 'employees' or Update TableName in  main.query_dynamodb() function.
3. Add items with following keys: emp_id, emp_name, home_loc, office_loc, contact, email, shift_start, shift_end.
4. Zip the lib folder. Required to package all python dependencies.
5. Create a new lambda function, and upload the zipped file.
6. Provide main.lambda_handler as entry point.
7. To mitigate timeout issues, it is recommended to increase the max timeout to 10+ seconds.



