# 반려가족과의 행복한 순간, GoDoG 🐕
<img src="https://user-images.githubusercontent.com/130967356/268191180-f1f1e9cd-2379-4126-9341-922151bbe83b.png">

<div align=center>
  <h2>사용한 개발 Tool💻</h2>  
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Java-F7DF1E?style=flat&logo=javascript&logoColor=white"/>
  <img src="https://img.shields.io/badge/AmazonAWS-232F3E?style=flat&logo=amazonaws&logoColor=white"/>
  <img src="https://img.shields.io/badge/Android Studio-3DDC84?style=flat&logo=androidstudio&logoColor=white"/>
  <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white"/>
  <br>
  <img src="https://img.shields.io/badge/Serverless-FD5750?style=flat&logo=serverless&logoColor=white"/>
  <img src="https://img.shields.io/badge/Postman-FF6C37?style=flat&logo=postman&logoColor=white"/>
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Firebase-FFCA28?style=flat&logo=firebase&logoColor=white"/>
  <img src="https://img.shields.io/badge/Github-181717?style=flat&logo=github&logoColor=white"/>
</div>

<br>
<br>
<h2>🌐 바로가기</h2>

- Figma 화면기획서 : https://www.figma.com/proto/MJRqZZjh5cfzvLpQewLdMk/walk?type=design&node-id=204-582&t=WmC8c2gizHdNtQr6-1&scaling=scale-down&page-id=0%3A1&starting-point-node-id=204%3A582&show-proto-sidebar=1&mode=design
- ERD cloud : https://www.erdcloud.com/d/yJ74eC2KMiisGuhBi
- API 명세서 : https://documenter.getpostman.com/view/28003812/2s9Y5WxiSb
- 백엔드 GitHub Respository : https://github.com/kje0058/project-walking-app
- 프론트엔드 GitHub Respository : https://github.com/kje0058/project-walk-app-android

<br>
<h2>📅 프로젝트 기간</h2>

- 2023년 7월 ~ 9월 (3개월)

<br>
<h2>💡 프로젝트 기획 의도</h2>

한국인 4명 가운데 1명이 반려동물을 키우는 반려인구 1500만 시대가 열리며,

이에 따라 반려동물을 ‘우리 딸, 아들’ ‘막둥이’라고 칭하는 등 가족처럼 여기는 펫펨족을 겨냥한 시장도 성장하고 있습니다.

반려동물과 가장 많은 시간을 함께하는 산책을 색다르게 보내기 위해 다른 산책 서비스에는 없는 **"산책로 추천 앱"** 을 기획하게 되었습니다. 

<br>
<h2>🐕 프로젝트 소개</h2>

내 반려가족과 함께 하는 즐거운 산책!

채팅, 커뮤니티로 기능으로 친구와 소통이 가능하고, TMap 보행자 경로 API를 사용하여 주변의 산책로를 추천해주는 기능으로 색다른 산책을 해볼 수 있습니다.

<br>
<h2>📌 서버 아키텍처</h2>

<img width="600" alt="image" src="https://github.com/GoDoG-app/project-GoDoG-server/assets/130967340/137b69a0-1796-411d-b9ef-2e5594a45cce">
<br>

<br>
<h2>📰 ERD</h2>

<img width="709" alt="image" src="https://github.com/GoDoG-app/project-GoDoG-android/assets/130967340/156ee4ca-8b1c-4112-a5ff-11fdb6ed3ca5">
<br>

<br>
<h2>📑 API</h2>

![GoDoG API2](https://github.com/GoDoG-app/project-GoDoG-android/assets/130967340/95914f78-f868-48da-bc4a-03f5bbd6950b)
<br>

<br>
<h2>📚 프로젝트 백엔드 사용 기술</h2>

- 파이썬 프레임워크인 Flask Rest API 개발 기능   
- JWT(JSON Web Token)을 이용하여 회원가입/로그인 기능 구현 및 유저에게 Access Token 부여  
- 이미지 데이터를 AWS S3 버킷에 저장 기능
- MySQL DB로 데이터 저장 관리
- Serverless 프레임워크를 이용하여 AWS IAM을 통해 발급받은 Access Key로 AWS lambda에 함수 배포 기능  
-  math 라이브러리를 사용하여 사용자의 현재 위치를 기반으로 랜덤한 위도와 경도 생성  
- Haversine 공식을 사용하여 두 지점사이의 거리를 구하는 Query문을 작성하고 주변 사용자를 검색하고 가까운 사용자를 추천하는 기능 

<br>
<h2>📱 프로젝트 시연 동영상</h2>

https://drive.google.com/file/d/1ZpAn0eP5NPqrZfY4rBPOdqAR7lLDeX8q/view?resourcekey

<br>
<h2>🔥 에러사항</h2>
<details>
<summary>문제1. 워터풀 개발방식👆</summary>
  
- 백엔드에서 개발한 API를 중간에 한꺼번에 배포하다보니 어디서 에러가 발생한지 모르는 상황 발생
- 대처: 애자일 개발방식으로 변경
  
  서버를 새로 만들어 API를 하나씩 테스트하고 배포하는 애자일 방식으로 개발을 진행하여 에러를 찾았고,
  라이브러리를 설치할 때 자동 설치된 라이브러리의 버전 문제였고 버전을 낮춰 해결

<img src="https://github.com/GoDoG-app/project-GoDoG-android/assets/130967356/a7d735f2-03f5-494c-86ab-fc7dbad73be3">
</details>

<details>
<summary>문제2.  Git push, pull시 충돌에러👆</summary>

- 팀원 두명이 같은 파일을 수정해서 동시에 git에 올려 충돌 발생
- 대처 : Git push시 팀원간의 소통
  
  Git branch를 만들어 git pull, push 상황을 공유하고 충돌이 더이상 일어나지 않게 Slack에서 소통함
  Git Gragh를 확인하여 git push 상황을 체크함

<img src="https://github.com/GoDoG-app/project-GoDoG-android/assets/130967356/68cabf96-47c7-4b5d-b220-b15c71d692c3">
</details>

<br>
<h2>👨‍💻 팀원</h2>

|이름|깃허브|역할|
|------|---|---|
|김정은|https://github.com/kje0058|조장 / 친구 추천, 카카오 로그인 및Firebase 채팅 개발|
|김예진|https://github.com/blue618020|조원 / 안드로이드 기능 개발|
|최태욱|https://github.com/skdixodnr|조원 / 서버 기능 개발|
|황덕우|https://github.com/the9world|조원 / TMap 지도 및 산책관련 기능 개발|
