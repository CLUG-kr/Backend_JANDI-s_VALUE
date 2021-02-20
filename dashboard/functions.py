import requests
import json

class CommonFunctions :
    
    def username(self, headers) : # token 이용하여 username get api
        print("username함수 호출 굳")
        r = requests.get('https://api.github.com/user', headers=headers)
        username = r.json()
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
