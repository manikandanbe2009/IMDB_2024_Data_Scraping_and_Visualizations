create database imdbdatadb;
use imdbdatadb;
create table imdbmovielist2024 (
 Movie_Name varchar(250),
 Genre varchar(80),
 Ratings float,
 Voting_Counts varchar(20),
 Duration varchar(20)
);

desc imdbmovielist2024;

select * from imdbmovielist2024;