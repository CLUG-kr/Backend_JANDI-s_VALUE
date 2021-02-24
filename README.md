# 잔디의 같이
#### Django REST API, GitHub Oauth2.0 ➡ React Client Web Application


## *Introduction*

### Link
> https://www.jandevelop.com/

### Summary

> - Introduce about PROJECT
>   - Commit Dahs-board Web Application
>   - Github Social Login
>   - If the token is valid, it can be serviced through a web browser
>   - The server is RESTful-designed, enabling dashboard service using HTTP's ruequst 
>   - After 10 minutes, the token automatically expires and logs out. 
>   - Authentication Server_based on the OAuth 2.0 Auth protocol using JWT
>   - Automatically sign in to the server when you log in with your GitHub
>  <br/>
> 
> - BACKEND (Djagno Authentication Server)
>   - 회원(User), 랭킹(Ranking) REST API for Storing Information
>   - 대시보드(Dashboard) REST API for Information Transmission
>   - Authentication and Authorization based on OAuth 2.0 Auth protocol using JWT
>  <br/>
> 


### Requirements

> - BACKEND (Djagno Authentication Server)
>   - [Python 3.6](https://www.python.org/downloads/release/python-360/)
>   - [Django 3.1.6](https://docs.djangoproject.com/en/3.1/)
>   - [Django REST Framework 3.12.2](https://www.django-rest-framework.org/)
>   - [Django REST Framework JWT 1.11.0](https://github.com/jpadilla/django-rest-framework-jwt) 
>   - Details are in "requirements.txt"
>  <br/>
> 
> - Database
>   - [SQLite 3.34](https://www.sqlite.org/releaselog/3_34_1.html)
>   - 향후 [MySQL 5.6](https://dev.mysql.com/downloads/mysql/5.6.html) 로 upgrade 예정

### Backend End-points

> **Resource modeling**
> 
> - Authentication (Token Issuance and Renewal) API 
> 
>   |  HTTP |  Path |  Method |  Request |  Purpose |
>   | --- | --- | --- | --- | --- |
>   |**POST** |/login/|CREATE| None |GitHub ID token to return JWT|
>   |**GET** |/validate/|READ| Access Token |Receive JWT to validate token and return to status code|
>   |**POST** |/refresh/|CREATE| Access Token |Receive JWT to validate tokens and return new tokens|
> 
> - User resource API
> 
>   |  HTTP |  Path |  Method |  Request |  Purpose |
>   | --- | --- | --- | --- | --- |
>   |**GET** |/user/|LIST| Access Token |List All user|
>   |**POST** |/user/|CREATE| Access Token |Create a user|
>   |**GET** |/user/current/|READ| Access Token |Read user currently connected|
> 
> - Repository resource API
> 
>   |  HTTP |  Path |  Method |  Request |  Purpose |
>   | --- | --- | --- | --- | --- |
>   |**GET** |/repolist/|LIST| Access Token |List Repositories|
>
> - Dash-Board resource API
> 
>   |  HTTP |  Path |  Method |  Request |  Purpose |
>   | --- | --- | --- | --- | --- |
>   |**GET** |/dashboard/|READ| Access Token |Return User name, image|
>   |**GET** |/dashboard/commit/|READ| Access Token & Repository Name |Return Commit value|
>   |**GET** |/dashboard/tendency/|READ| Access Token & Repository Name |Return DevTendency|
>   |**GET** |/dashboard/contribution/|READ| Access Token & Repository Name |Graph - Return Contributor value|
>   |**GET** |/dashboard/day/|READ| Access Token & Repository Name |Graph - Return DayTendency value|
>   |**GET** |/dashboard/language/|READ| Access Token & Repository Name |Graph - Return Language value|
>   |**GET** |/dashboard/time/|READ| Access Token & Repository Name |Graph - Return TimeTendency value|
> 
> **Urls**
> 
> - `backend/api/urls.py`
> ```python
> from django.contrib import admin
> from django.urls import path, include, url
> from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
> 
> urlpatterns = [
> 
>     path('admin/', admin.site.urls),
>     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
>     
>     path('oauth/', include('oauth.urls')),
>     path('', include('dashboard.urls')),
>     
> 
> ]
> ```
> 
> 
> - `backend/dashboard/urls.py`
> ```python
> from django.urls import path
> from .views import *
> 
> urlpatterns = [
>     path('repolist/', ObtainRepositories.as_view(), name='ObtainRepositories'),
>     
>     path('dashboard/', GithubUserView.as_view(), name = 'GithubUserView'),
>     
>     path('dashboard/commit/',CommitView.as_view(), name='CommitView'),
>     
>     path('dashboard/tendency/', DevTendencyView.as_view(), name='DevTendencyView'),
>     
>     # graph
>     path('dashboard/language/', LanguageView.as_view(), name='LanguageView'),
>     path('dashboard/contribution/', ContributionView.as_view(), name='ContributionView'),
>     path('dashboard/day/',DayTendencyView.as_view(),name='DayTendencyView'),
>     path('dashboard/time/', TimeTendencyView.as_view(), name='TimeTendencyView')
> ]
> ```

### System configuration
> 
> **Service flow**
> 
> ![image](https://user-images.githubusercontent.com/65646971/108949108-1b9fb700-76a7-11eb-9375-4cc9e1ed20f5.png)
> 
> 1. User requests login to GitHub API Server
> 
> 2. The GitHub API Server triggers a GitHub login Dialog with specific queries to the user.
> 
> 3. When GitHub login authentication is complete, pass permissions with access_token
> 
> 4. Authorization Server validates tokens and privileges received from the Client Web App
> 
> 6. When validation is complete, the requested access_token is considered valid
> 
> 7. The server resends access_token with the requested resource (login authentication completed)
> 
> 8. Once login authentication is complete, protected resources are accessible, refresh Token periodically issued, and Token renewed.
> 
> * For users in GitHub Enterprise Cloud accounts, requests for resources owned by the same GitHub Enterprise Cloud account using OAuth tokens increase the hourly request limit to 15,000. For unauthenticated requests, the speed limit allows only up to 60 requests per hour. <br/> Therefore, the above process is absolutely necessary!
<br/>


## *Addition Commentary*
> 
### Issues
> 
> - According to [GitHub Docs](https://docs.github.com/en)'s GitHub REST API, All API access is via HTTPS at https://api.github.com and all data is sent and received by JSON.
> - < GitHub API >
>   - page 제한 : 여러 항목을 반환하는 요청은 기본적으로 30 개 항목으로 페이지가 매겨진다. 이 때 최대 100개의 page에 대한 정보만 제공한다. 그래서 각 레포별 최대 100개의 커밋 기록에 대해 오늘 커밋 수, 어제 커밋 수를 반환한다. 다른 api들이 100개 제한이 없는 이유에 대해서는, 깃허브 공식문서에 따르면 기술적인 이유로 모든 엔드 포인트가 page 매개 변수를 존중하는 것은 아니라고 명시되어 있기 때문이다. 이 부분은 향후 REST API가 아닌 GraphQL API를 이용하면 해결이 될 것으로 예상.
>   - 각 레포별 대시보드 기능을 제공하는 이유 : [GitHub REST API](https://docs.github.com/en/rest) 레퍼런스에 따라 커밋 통계 기록을 내는데 유용한 기능들은 각 레포지토리 별로만 제공한다. 
>   - default 브랜치 기준으로 대시보드를 제공하는 이유 : [GitHub REST API](https://docs.github.com/en/rest) 레퍼런스에 따라 커밋 통계 기록을 내는데 팔요한 api들의 데이터는 default branch에 대한 정보만 제공된다고 되어있다. 그렇기에 개인 깃허브 프로필에서 보이는 잔디 기록들도 디폴트 브랜치 기준으로 집계되는 것임을 유추할 수 있었다.
>   - 속도 제한 : 레포별 기록을 모두 수합하여 전체 레포에 대한 대시보드도 나타내고 싶었으나, '기본 인증 또는 OAuth를 사용하는 API 요청의 경우 시간당 최대 5,000 개의 요청을 만들 수 있다'는 REST API 공식 문서에 따라 각 레포를 돌며 전체 레포에 대한 기록을 나타낸다고 가정할 시, django-scheduler를 통해 주기적으로 대시보드 기록을 업데이트 할 예정인 서비스의 특성 상 레포의 수가 늘어날 수록 시간당 요청 수가 기하급수적으로 증가하여 속도 제한에 걸릴 것으로 예상되어 특정 레포에 대한 대시보드 기능을 제공하는 것으로 서비스 방향성을 수정하였다.
> - < Update dashboard statistics/rankings with Django-Scheduler >
>   - GitHub REST API 자체 속도 제한 규정으로 대시보드 통계는 매일 자정, 랭킹 기능은 일주일 단위로 업데이트 될 예정이다.
> - < Deployment >
>   - 처음에는 AWS EC2를 통해 클라우드 디비에 올라가도록 배포를 도전하였으나 React Web App과 Django 통신에 필수적인 Https 설정을 하면서 로드밸런서 설정 문제가 생겼다.
>   - 해로쿠 배포를 통해 https 문제를 해결하였으며 jandevelop.com 도메인을 구입해 연결해주었다.

### Plans (향후 계획)
> Based on user-specific dashboard information stored in DB, point system will be implemented and accumulated ranking will be provided based on real-time ranking using django-scheduler among service users and accumulated information.

### Tools 
> - [VSCode](https://code.visualstudio.com/docs/?dv=win)
> - [Insomnia](https://insomnia.rest/)
> - [Slack](https://slack.com/intl/ko-kr/)
> - [Mysql Workbench](https://www.mysql.com/products/workbench/) 
