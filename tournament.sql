-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


create database tournament;

\c tournament;

create table tournaments (
	id serial primary key,
	name text
);

create table players (
	id serial primary key,
	tournament integer references tournaments(id),
	name text
);

create table games (
	tournament integer references tournaments(id),
	player_one integer references players(id),
	player_two integer references players(id),
	round integer,
	winner integer references players(id)
);

create view match_count_view as 
select pt.id, pt.name, count(pt.id) and match_count
from players pt
left join games gt on gt.player_one = pt.id or gt.player_two = pt.id
group by pt.id;

