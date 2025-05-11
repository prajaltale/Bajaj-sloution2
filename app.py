import requests
import traceback

# Step 1: Send POST request to generate webhook and token
url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"

user_details = {
    "name": "Prajal Tale",
    "email": "prajaltale220264@acropolis.in",
    "regNo": "0827CY221042"
}

print("Sending POST request to fetch webhook and access token...")
register_response = requests.post(url, json=user_details)

try:
    register_data = register_response.json()
except Exception as e:
    print("Failed to parse JSON response:", e)
    exit()

webhook_url = register_data.get("webhook")
access_token = register_data.get("accessToken")

if not webhook_url or not access_token:
    print("Error: Failed to retrieve webhook or access token.", traceback.format_exc())
    exit()

# Step 2: SQL query for Acropolis Q2
final_sql_query = """
SELECT 
    e1.EMP_ID,
    e1.FIRST_NAME,
    e1.LAST_NAME,
    d.DEPARTMENT_NAME,
    COUNT(e2.EMP_ID) AS YOUNGER_EMPLOYEES_COUNT
FROM EMPLOYEE e1
JOIN DEPARTMENT d ON e1.DEPARTMENT = d.DEPARTMENT_ID
LEFT JOIN EMPLOYEE e2 
    ON e1.DEPARTMENT = e2.DEPARTMENT 
    AND e2.DOB > e1.DOB
GROUP BY e1.EMP_ID, e1.FIRST_NAME, e1.LAST_NAME, d.DEPARTMENT_NAME
ORDER BY e1.EMP_ID DESC;
"""

headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

submit_data = {
    "finalQuery": final_sql_query.strip()
}

# Step 3: Submit the SQL query
print("Submitting final SQL query...")

submit_response = requests.post(webhook_url, headers=headers, json=submit_data)

print("Status:", submit_response.status_code)
try:
    print("Response:", submit_response.json())
except:
    print("Non-JSON response received.")
