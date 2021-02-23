# 잔디의 같이
#### Django REST API, GitHub Oauth2.0 로그인 가능한 React Client Web Application


## *Introduction*

### Link
> https://www.jandevelop.com/

### Summary

> - Project 소개
>   - Commit Dahs-board Web Application
>   - Github Social Login 기능 구현
>   - 토큰이 유효하다면 웹 브라우저를 통해 서비스 가능
>   - 서버는 RESTful하게 설계되었기 때문에 HTTP 의 ruequst 이용한 대시보드 서비스 가능 
>   - 10분이 지나면 자동으로 토큰 만료되고 로그아웃 처리 
>   - JWT를 이용한 OAuth 2.0 Auth 프로토콜 기반의 인증 서버 
>   - GitHub 계정으로 로그인하면 서버에 자동으로 회원 가입
>  <br/>
> 
> - BACKEND (Djagno Authentication Server)
>   - Django를 이용하여 회원(User), 랭킹() 정보 저장용 REST API 구현 
>   - 지금 상태 기준으로는 : Django를 이용하여 대시보드 정보 송출용 REST API 구현
>   - JWT를 이용한 OAuth 2.0 Auth 프로토콜 기반으로 Authentication 및 Authorization 구현
>  <br/>
> 
> - FRONTEND (React Webapp Client)
>   - React를 이용하여 로그인 및 Dash-borad 서비스용 Web 구현
>   - OAuth 2.0 GitHub API 이용하여 깃허브 계정으로 소셜 로그인 구현
>   - React Web을 통하여 회원 가입 가능하고, GitHub 계정으로 로그인하면 서버에 자동 회원 가입


### Requirements

> - BACKEND (Djagno Authentication Server)
>   - [Python 3.6](https://www.python.org/downloads/release/python-360/)
>   - [Django 3.1.6](https://docs.djangoproject.com/en/3.1/)
>   - [Django REST Framework 3.12.2](https://www.django-rest-framework.org/)
>   - [Django REST Framework JWT 1.11.0](https://github.com/jpadilla/django-rest-framework-jwt) 
>  <br/>
> 
> - FRONTEND (React Webapp Client)
>  <br/>
> 
> - Database
>   - [SQLite 3.34](https://www.sqlite.org/releaselog/3_34_1.html)
>   - 향후 [MySQL 5.6](https://dev.mysql.com/downloads/mysql/5.6.html) 로 upgrade 예정

### Backend End-points

> **Resource modeling**
> 
> - 인증(Token 발급 및 갱신) 관련 API 
> 
>   |  HTTP |  Path |  Method |  Request |  목적 |
>   | --- | --- | --- | --- | --- |
>   |**POST** |/login/|CREATE| None |Google의 ID 토큰을 받아 JWT를 반환|
>   |**GET** |/validate/|READ| Access Token |JWT를 받아 토큰을 검증하여 상태코드로 반환|
>   |**POST** |/refresh/|CREATE| Access Token |JWT를 받아 토큰을 검증하여 새로운 토큰 반환|
> 
> - 회원(User) 리소스 관련 API (예정)
> 
>   |  HTTP |  Path |  Method |  Request |  목적 |
>   | --- | --- | --- | --- | --- |
>   |**GET** |/user/|LIST| Access Token |모든 User 조회|
>   |**POST** |/user/|CREATE| Access Token |하나의 User 생성|
>   |**GET** |/user/current/|READ| Access Token |현재 접속중인 User 조회|
> 
> - Repository 리소스 관련 API
> 
>   |  HTTP |  Path |  Method |  Request |  목적 |
>   | --- | --- | --- | --- | --- |
>   |**GET** |/repolist/|LIST| Access Token |Repository List 조회|
>
> - Dash-Board 리소스 관련 API
> 
>   |  HTTP |  Path |  Method |  Request |  목적 |
>   | --- | --- | --- | --- | --- |
>   |**GET** |/dashboard/|READ| Access Token |User 이름, 사진 반환|
>   |**GET** |/dashboard/commit/|READ| Access Token & Repository Name |Commit 관련 value 반환|
>   |**GET** |/dashboard/tendency/|READ| Access Token & Repository Name |DevTendency 반환|
>   |**GET** |/dashboard/contribution/|READ| Access Token & Repository Name |Graph - Contributor value 반환|
>   |**GET** |/dashboard/day/|READ| Access Token & Repository Name |Graph - DayTendency value 반환|
>   |**GET** |/dashboard/language/|READ| Access Token & Repository Name |Graph - Language value 반환|
>   |**GET** |/dashboard/time/|READ| Access Token & Repository Name |Graph - TimeTendency value 반환|
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

### Frontend Components

> **Component description**
> 
>

### System configuration
> 
> **Service flow**
> 
> <img src="" alt="ppt이미지 첨부예정" width='90%'/>
> 
> 1. 사용자는 GitHub API Server에 로그인을 요청
> 
> 2. GitHub API Server는 사용자에게 특정 쿼리들을 붙인 GitHub 로그인 Dialog를 트리거
> 
> 3. GitHub 로그인 인증이 완료되면, access_token과 함께 권한을 전달
> 
> 4. Authorization Server는 Client Web App으로 부터 받은 토큰과 권한의 유효성을 검증
> 
> 6. 검증이 완료되면, 요청한 access_token이 유효하다고 간주
> 
> 7. 서버는 요청한 리소스와 함께 access_token을 다시 전송 (로그인 인증 과정 완료)
> 
> 8. 로그인 인증이 완료되면 Public 뿐만 아니라 Protected 리소스에 접근 가능하고, Refresh Token 주기적으로 발급하며 Token을 갱신 
> 
> * GitHub Enterprise Cloud 계정에 속한 사용자의 경우 OAuth 토큰을 사용하여 동일한 GitHub Enterprise Cloud 계정이 소유한 리소스에 대한 요청은 시간당 요청 한도가 15,000 개로 늘어난다. 인증되지 않은 요청의 경우 속도 제한은 시간당 최대 60개의 요청만을 허용한다. 그러므로 위 과정이 반드시 필요!
<br/>


## *Addition Commentary*
> 
### Issues (시행착오)
> 
> - [GitHub Docs](https://docs.github.com/en)의 GitHub REST API 문서에 따르면 모든 API 액세스는 https://api.github.com.의 HTTPS를 통해 이루어지며 모든 데이터는 JSON으로 송수신된다.
> - GitHub API 관련 한계
>   - page 제한 : 여러 항목을 반환하는 요청은 기본적으로 30 개 항목으로 페이지가 매겨진다. 이 때 최대 100개의 page에 대한 정보만 제공한다. 그래서 각 레포별 최대 100개의 커밋 기록에 대해 오늘 커밋 수, 어제 커밋 수를 반환한다. 다른 api들이 100개 제한이 없는 이유에 대해서는, 깃허브 공식문서에 따르면 기술적인 이유로 모든 엔드 포인트가 page 매개 변수를 존중하는 것은 아니라고 명시되어 있기 때문이다. 이 부분은 향후 REST API가 아닌 GraphQL API를 이용하면 해결이 될 것으로 예상.
>   - access_token 파기 : [Expiring user-to-server access tokens for GitHub Apps](https://developer.github.com/changes/2020-04-30-expiring-user-to-server-access-tokens-for-github-apps/) 문서에 따라 8시간 후에 자동으로 파기되고 현재로썬 JANDEVELOPER에서 파기시킬 방법은 없다.
>   - 각 레포별 대시보드 기능을 제공하는 이유 : [GitHub REST API](https://docs.github.com/en/rest) 레퍼런스에 따라 커밋 통계 기록을 내는데 유용한 기능들은 각 레포지토리 별로만 제공한다. 
>   - default 브랜치 기준으로 대시보드를 제공하는 이유 : [GitHub REST API](https://docs.github.com/en/rest) 레퍼런스에 따라 커밋 통계 기록을 내는데 팔요한 api들의 데이터는 default branch에 대한 정보만 제공된다고 되어있다. 그렇기에 개인 깃허브 프로필에서 보이는 잔디 기록들도 디폴트 브랜치 기준으로 집계되는 것임을 유추할 수 있었다.
>   - 속도 제한 : 레포별 기록을 모두 수합하여 전체 레포에 대한 대시보드도 나타내고 싶었으나, '기본 인증 또는 OAuth를 사용하는 API 요청의 경우 시간당 최대 5,000 개의 요청을 만들 수 있다'는 REST API 공식 문서에 따라 각 레포를 돌며 전체 레포에 대한 기록을 나타낸다고 가정할 시, django-scheduler를 통해 주기적으로 대시보드 기록을 업데이트 할 예정인 서비스의 특성 상 레포의 수가 늘어날 수록 시간당 요청 수가 기하급수적으로 증가하여 속도 제한에 걸릴 것으로 예상되어 특정 레포에 대한 대시보드 기능을 제공하는 것으로 서비스 방향성을 수정하였다.
> - Django-Scheduler를 통한 대시보드 통계/랭킹 업데이트
>   - GitHub REST API 자체 속도 제한 규정으로 대시보드 통계는 매일 자정, 랭킹 기능은 일주일 단위로 업데이트 될 예정이다.
> - 배포 관련
>   - 처음에는 AWS EC2를 통해 클라우드 디비에 올라가도록 배포를 도전하였으나 React Web App과 Django 통신에 필수적인 Https 설정을 하면서 로드밸런서 설정 문제가 생겼다.
>   - 해로쿠 배포를 통해 https 문제를 해결하였으며 jandevelop.com 도메인을 구입해 연결해주었다.

### Plans (향후 계획)
> - DB에 저장되어 있는 User별 대시보드 정보를 토대로 자체 랭킹 알고리즘을 구현하여 포인트 제도를 도입할 것이며 서비스 이용자들 사이에서의 django-scheduler를 이용한 실시간 랭킹, 누적된 정보를 바탕으로 누적 랭킹을 제공할 예정이다.

### Tools 
> - [VSCode](https://code.visualstudio.com/docs/?dv=win)
> - [Insomnia](https://insomnia.rest/)
> - [Slack](https://slack.com/intl/ko-kr/)
> - [Mysql Workbench](https://www.mysql.com/products/workbench/) 
