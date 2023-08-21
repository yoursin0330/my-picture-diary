# my-picture-diary

나만의 그림일기 작성하기

## 개발 환경 및 개발 기간

- 개발 환경
  Django 4.2.3, HTML, CSS, JavaScript
- 개발 기간
  2023/07/17 ~ 2023/07/20, 08/21

## 기능

- User : 회원가입, 로그인, 로그아웃
- Post : 게시글 CRUD. 일기의 그림 작성
- Comment : 댓글 작성, 삭제

## DB 구조

![DB diagram](image.png)

## URL

- '' : 인덱스 페이지

### 일기

- 'diary/' : 일기 리스트
- 'diary/write/' : 일기 작성
- 'diary/detail/<int:pk>/' : 일기 조회
- 'diary/detail/<int:pk>/delete/' : 일기 삭제

### 일기 댓글

- 'diary/detail/<int:pk>/comment/write/' : 댓글 작성
- 'diary/detail/<int:pk>/comment/delete/' : 댓글 삭제

### 사용자 페이지

- 'register/' : 회원가입 페이지
- 'login/' : 로그인 페이지
- 'logout/' : 로그아웃

## 실행 화면

![인덱스 화면](readme/index.png)
![회원가입](readme/user_register.png)
![로그인](readme/user_login.png)
![일기 리스트](readme/blog_list.png)
![게시글 상세 페이지](readme/blog_detail.png)
![게시물 작성](readme/blog_write.png)

## 아쉬웠던 점

- canvas 저장 부분에 시간 할애를 많이 해 효율적으로 시간을 분배하지 못한 점
- 구상 당시의 디자인을 적용하지 못한 점
