# 概要
シフト提出、編集、閲覧をスマホから簡単に行えるWebアプリです。  
AWS版とheroku版を提供しております。  
AWS版: https://shiftmanagementapp.com  
ID: test@mail.com  
PASS: testuser  
  
heroku版: https://shiftmanagementapp-heroku.herokuapp.com
# 特徴
- トップページは今月のシフトがひと目で確認できるカレンダー仕様
![スクリーンショット 2022-05-26 17 36 11](https://user-images.githubusercontent.com/66234583/170451739-9a803d85-5831-43d0-96c7-d349bc9f2a88.png)  
  
- 日付クリックで非同期でシフトをサーバーに送信
![スクリーンショット 2022-05-26 17 36 00](https://user-images.githubusercontent.com/66234583/170451672-6c52b051-f6e0-41f8-8193-f4af99976435.png)  
  
- 特定の日のシフト確認はわかりやすいタイムラインを使用
![スクリーンショット 2022-05-26 17 36 56](https://user-images.githubusercontent.com/66234583/170451571-5ee56d35-6238-41bb-8894-d330fe39de35.png)  

- 管理者はタイムラインクリックすることでシフト編集が可能
![スクリーンショット 2022-05-26 17 40 03](https://user-images.githubusercontent.com/66234583/170452082-461ce166-0b7f-4331-9a77-6594252cb33b.png)  

- 店のシフトを誰でも閲覧できるのを防ぐため、アカウント登録は管理者の承認制
![スクリーンショット 2022-07-14 17 51 52](https://user-images.githubusercontent.com/66234583/180380212-237f835e-e99d-45ae-8959-e4b459a8a942.png)  
## その他特徴
- LINE MessagingAPIを用いたアカウント連携とシフト前日のLINE通知機能(heroku版)
- シフト編集モード機能で締め切り後でも一時的に提出できるようにする救済モード
- ユーザーの状態、時期によってカレンダーの表示範囲を動的に変更
- シフト公開設定から公開する範囲を管理者が選択可能
# 使用技術
**フロントエンド**
- jQuery 3.4.1
- Bootstrap 4.3.1
- GoogleCharts
- FullCalender 5.10.2
- HTML/CSS
  
**バックエンド**
- Python 3.7.10
- Django 3.2.13
  
**インフラ**
- Docker 20.10.14
- AWS
    - ECS,ECR,EC2,RDS,ELB,S3,SES,Route53
- heroku

**その他**
- CircleCI
    - mainブランチへマージすることで自動テストを実行
    - 自動テストをパスすると、コンテナをビルドしてしてheroku,ECRへ自動デプロイを実行

![ecs-構成図 drawio-3](https://user-images.githubusercontent.com/66234583/184472486-99bb3297-5cb6-48c3-b30a-f76edaadac48.svg)





