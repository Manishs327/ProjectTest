import requests
import requests.auth
import concurrent.futures
import logging
import datetime

#######logging####
logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#result=$(curl --trace-ascii trace.out -u "tenantb.idcs_scim_001:dummySecret=alksfdkalsjaskljfAAAsjaslkji" -X POST https://hs-iams-loginsvc-dev.iad.icprod.oracleindustry.com:61704/ms_oauth/oauth2/endpoints/tenantb_oracle/tokens -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=client_credentials&scope=tenantb.iamsscim_IdcsBizSvc1.idcs" 2>/dev/null )


#######Variables for oauth token#######
CLIENT_ID = "tenantb.idcs_scim_001"
CLIENT_SECRET = "dummySecret=alksfdkalsjaskljfAAAsjaslkji"
TOKEN_URL = "https://hs-iams-loginsvc-dev.iad.icprod.oracleindustry.com:61704/ms_oauth/oauth2/endpoints/tenantb_oracle/tokens?"
SCOPE = "tenantb.iamsscim_IdcsBizSvc1.idcs"


#######Define the URL of the SCIM API endpoint#######
#api_url = 'https://migtenantqa1-hs-sso-stg.iams.hs.ocs.oraclecloud.com:443/scimgateway/v1/migtenantqa1/migtenantqa1.clinicalone-CNE/Users/'
api_url = 'http://d14ws1dby6.iad.icprod.oracleindustry.com:14000/scimgateway/v1/tenantb/tenantb.IdcsBizSvc1/Users'
# Number of requests to make
#######Total number of users /requests to be called#############
num_requests = 10

#######USER PREFIX#######
username_prefix = 'IDCSUSERSEPT28'

#######Function to get oauth toke#######
def get_oauth_token():
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "client_credentials",
                 "scope": SCOPE}
    response = requests.post(TOKEN_URL,
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    print(token_json)
    return token_json["access_token"]
get_oauth_token()

def onlytoken(username):
    try:
        oauth_token = get_oauth_token()
        return oauth_token
    except Exception as e:
        logging.error(f"Error for username {username}: {str(e)}")

#######function to make a POST request with a dynamic OAuth token and variable body def make_post_request(username)#######
def make_post_request(username):
    try:

        oauth_token = get_oauth_token()
        headers = {
            'Authorization': f'Bearer {oauth_token}',
        }
#######Adjust the payload creation as needed, starting username with a prefix#######
        data = {
            "schemas": ["urn:scim:schemas:core:2.0:User"],
            "id": f"{username}f2215fb73cb348e5b9ae22794edcca9e",
            "userName": username,
            "name": {
                "familyName": username,
                "givenName": username
            },
            "emails": [
                {
                    "value": f"{username}@oracle.com",
                    "type": "work"
                }
            ],
            "externalId": f"{username}sb73cb348e5b9ae22794edcca0e"
        }
        response = requests.post(api_url, json=data, headers=headers)
        response_code = response.status_code
        result=  response.text
        return response_code, result
    except Exception as e:
        #logging.error(f"Error for username {username}: {str(e)}")
        return (f"Error for username {username}", {str(e)})
        # Return None or an error code to indicate failure
#######Generate usernames by incrementing from 1 to num_requests#######
usernames = [f"{username_prefix}{i + 1}" for i in range(num_requests)]

#######Use concurrent.futures to make parallel POST requests#######


start_time = datetime.datetime.now()
# t1 = datetime.strptime(start_time, "%H:%M:%S")
# print('Start time:', t1.time())

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     results = list(executor.map(make_post_request, usernames))

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    results = list(executor.map(make_post_request, usernames))
    #tokens = list(executor.map(onlytoken, usernames))

end_time = datetime.datetime.now()
# t2 = datetime.strptime(end_time, "%H:%M:%S")
# print('End time:', t2.time())
# print(start_time)
print(end_time - start_time)
#######Process the responses as needed#######
#logging.info(results)
# for i, (response_code, result) in enumerate(results):
#     logging.info(f"Request {i+1} Response: {result} ")
#     logging.info(f"Request {i+1} Response Code: {response_code} ")
count=0
for i in results:
    if "Error for" in str(i[0]):
        print(count)
        logging.info(f"Request {count+1} Response: {i[1]} ")
    else:
        print(count)
        logging.info(f"Request {count+1} Response: {i[1]} ")
        logging.info(f"Request {count+1} Response Code: {i[0]} ")
    count+=1



# for i in tokens:
#     count=1
#     logging.info(f"Resquest Number: {count}")
#     logging.info(f"Token: {i} ")
#     count+=1
#######End of script#######
