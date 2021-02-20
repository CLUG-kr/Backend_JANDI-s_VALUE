import requests
import json

class CommonFunctions :
    
    def username(self, headers) : # token 이용하여 username get api
        print("headers", headers)
        r = requests.get('https://api.github.com/user', headers=headers)
        print("111", r.json)
        username = r.json()
        print(username)
        return username['login']


    def obtain_repositories(self) :
        r = requests.get('https://api.github.com/user/repos', headers=headers, params=query )
        ctx = r.json()
        repositories = []

        githubUserView =GithubUserView()
        name = githubUserView.username()
        # name = super().username()
        
        for x in ctx : 
            if x['owner']['login'] == name :
                repositories.append(x['name'])
        data = {
            'repositories' : repositories
        } 
        print(type(data))
        json_data = json.dumps(data) 
        print(type(json_data)) 
         
        return data #딕셔너리타입
