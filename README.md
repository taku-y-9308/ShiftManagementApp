[![CircleCI](https://dl.circleci.com/status-badge/img/gh/taku-y-9308/ShiftManagementApp-heroku/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/taku-y-9308/ShiftManagementApp-heroku/tree/main)
# 概要
シフト提出、編集、閲覧をスマホから簡単に行えるWebアプリです。  
herokuデプロイ版です。  
https://shiftmanagementapp-heroku.herokuapp.com/
# 使用技術
**フロントエンド**
- jQuery 3.4.1
- Bootstrap 4.3.1
- Googlechart
- FullCalender 5.10.2
- HTML/CSS
  
**バックエンド**
- Python 3.9.11
- Django 3.2.13
  
**インフラ**
- heroku
  
**その他**
- CircleCI
    - mainブランチへマージすることで自動テストを実行
    - 自動テストをパスすると、コンテナをビルドしてしてherokuへ自動デプロイを実行
  
![heroku-構成図 drawio-4](https://user-images.githubusercontent.com/66234583/181701969-7c6c8834-0087-4244-88ef-eef51829c6c4.svg)



