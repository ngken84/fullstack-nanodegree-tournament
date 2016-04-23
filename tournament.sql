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
select p2.id, p2.name, count(pt.id) as match_count
from games g1 full join games g2 on 0 = 1
inner join players pt on
(pt.id = g1.player_one or pt.id = g2.player_two)
right join players p2 on p2.id = pt.id
group by pt.id, p2.id;


create view win_count_view as 
select p2.id, p2.name, count(p1.id) as wins from games gt 
inner join players p1 on gt.winner = p1.id 
right join players p2 on p2.id = p1.id 
group by p1.id, p2.id;