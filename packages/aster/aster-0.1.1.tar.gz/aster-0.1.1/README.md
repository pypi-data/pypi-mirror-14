aster (WIP)
===========
A pythonic serverless web application framework for minimalist.

It provides abstraction of cloud computing services like AWS, namely, with aster you are able to create an application without vendor lock-in.

> **Aster is in Work In Progress and we warmly welcome your contributions!** 


Features
--------
- [x] Python 2.7
- [x] Supports [Amazon Web Services](https://aws.amazon.com/)
- [x] Git integration
- [x] gulp integration
- [x] virtualenv integration
- Automated deployment
  - [x] AWS: S3
  - [x] AWS: Lambda
  - [x] AWS: APIGateway
  - [ ] AWS: CloudFront
- [ ] Database (ORM)
- [ ] Job management (cron and event source)
- [ ] Testing framework
- [ ] Mailer
- [ ] AWS: VPC support
- [ ] AWS: CloudWatch support
- [ ] AWS: SNS support
- [ ] AWS: Cognito support


Getting Started
---------------
Install aster by `pip`.
```
pip3 install aster
```

Create a new project.
```
aster new hello
```

Deploy a Hello World application!
```
aster deploy
```


Files
-----
```
app
 ├── README.md        --- your app's README
 ├── api              --- API endpoints
 ├── assets           --- assets: JavaScript and CSS (SCSS)
 ├── public           --- static files
 ├── config           --- configuration files
 ├── gulpfile.js      --- gulpfile
 ├── package.json     --- packages for gulp
 └── requirements.txt --- packages for APIs
```


Why don't you support Python3?
------------------------------
This is because AWS Lambda does not support Python3; it supports only Python 2.7.


Documentaion
------------
TODO


Examples
--------
TODO


License
-------
Public Domain

