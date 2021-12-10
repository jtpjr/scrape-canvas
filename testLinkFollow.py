import argparse
import requests

#This method does not work, authentication needs OAuth2 (seems like);
#Using this?:
#from requests_oauthlib import OAuth2Session

#---------------------------------------------------------------------
#Code:


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Try following canvas link with request lib")
    parser.add_argument("url", help="URL to follow")
    parser.add_argument("token", help="Token generated in the settings page on Canvas")
    args = parser.parse_args()
    
    
    simpleToken = args.token
   
    head = {"Authorization": "Bearer {}".format(simpleToken)}
    
    print(head) 
    
    print("------------------------------------------------------------------------")

    response = requests.get(args.url, headers=head, allow_redirects=True)
 
    
    #token = {
    
    
    if response.history:
        print("Request was redirected:")
        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)
    else:
        print("Request was not redirected.")