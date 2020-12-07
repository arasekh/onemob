create database virtualclass;
create user virtualclass_user with encrypted password 'vcspswrd';
grant all privileges on database virtualclass to virtualclass_user;