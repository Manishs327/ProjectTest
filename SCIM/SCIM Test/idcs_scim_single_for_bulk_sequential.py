import requests
import requests.auth
import concurrent.futures
import logging
#######logging####
logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#######Variables for oauth token#######
#CLIENT_ID = "migtenantqa1.idcs_clinicalone-CNE"
#CLIENT_SECRET = "secret=EFFFE515DA37412F905FE8083C43F3A9"
CLIENT_ID = "migtenantqa1.migtrialqa11user1"
CLIENT_SECRET = "MAnager12!@"
#TOKEN_URL = "https://iams-hs-sso-stg.iams.hs.ocs.oraclecloud.com/ms_oauth/oauth2/endpoints/migtenantqa1_oracle/tokens?"
#SCOPE = "migtenantqa1"


#######Define the URL of the SCIM API endpoint#######
#api_url = 'https://migtenantqa1-hs-sso-stg.iams.hs.ocs.oraclecloud.com:443/scimgateway/v1/migtenantqa1/migtenantqa1/Users/'
api_url = 'https://hs-identity-api-stg.oracleindustry.com/scim/v1/migtenantqa1/Bulk'
#api_url = 'https://hs-identity-api-stg.oracleindustry.com/scim/v1/migtenantqa1/Bulk'
# Number of requests to make
#######Total number of users /requests to be called#############
num_requests = 100

#######USER PREFIX#######
username_prefix = 'SCIMIDCSUSER_6'
print('Username Prefix is ', username_prefix)

#######Function to get oauth toke#######
# def get_oauth_token():
#     client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
#     post_data = {"grant_type": "client_credentials",
#                  "scope": SCOPE}
#     response = requests.post(TOKEN_URL,
#                              auth=client_auth,
#                              data=post_data)
#     token_json = response.json()
#     return token_json["access_token"]
# get_oauth_token()


#######function to make a POST request with a dynamic OAuth token and variable body def make_post_request(username)#######
def make_post_request(username):
    #oauth_token = get_oauth_token()
    headers = {
        'Authorization': f'Basic bWlndGVuYW50cWExLm1pZ3RyaWFscWExMXVzZXIxOk1BbmFnZXIxMiFA'
    }
#######Adjust the payload creation as needed, starting username with a prefix#######
    # data = {
    #     "schemas": ["urn:scim:schemas:core:2.0:User"],
    #     "id": f"{username}f2215fb73cb348e5b9ae22794edcca9e",
    #     "userName": username,
    #     "name": {
    #         "familyName": username,
    #         "givenName": username
    #     },
    #     "emails": [
    #         {
    #             "value": f"{username}@oracle.com",
    #             "type": "work"
    #         }
    #     ],
    #     "externalId": f"{username}sb73cb348e5b9ae22794edcca0e"
    # }



    ###data for bulk single user
    data={
  "schemas": ["urn:scim:schemas:core:2.0:BulkRequest"],
  "failOnErrors":1,
  "Operations":[
    {
      "method":"POST",
      "path":"/Users",
      "bulkId":"qwerty",
      "data":{
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
    }]
}
    print(data)
    response = requests.post(api_url, json=data, headers=headers)
    response_code = response.status_code
    result=  response.text
    return response_code, result

#######Generate usernames by incrementing from 1 to num_requests#######
usernames = [f"{username_prefix}{i + 1}" for i in range(num_requests)]
print(usernames)

#######Use concurrent.futures to make parallel POST requests#######
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     results = list(executor.map(make_post_request, usernames))
# created = 0
# error =0
# iam =0
# #######Process the responses as needed#######
# for i, (response_code, result) in enumerate(results):
#     logging.info(f"Request {i+1} Response: {result} ")
#     logging.info(f"Request {i+1} Response Code: {response_code} ")
#     #print(result.description)
#     print(response_code)
#     if(response_code==201):
#         created=created+1
#     else:
#         error=error+1
#         print(type(result))
# print(created)
# print(error)
# print(iam)
for username in usernames:
    count=0
    result = make_post_request(username)
    logging.info(f"Request {count+1} Response: {result[1]} ")
    logging.info(f"Request {count+1} Response Code: {result[0]} ")
    count+=1
    print(result)


#######End of script#######
