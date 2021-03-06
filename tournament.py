#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM games;")
    conn.commit()
    conn.close()
    
    

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS NUM FROM players;")
    count = cursor.fetchone()
    conn.close()
    return count[0]
    
    
    

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT into players (name) values (%s);", (name,))
    conn.commit()
    conn.close()
    

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor();
    cursor.execute(
        "SELECT wcv.id, wcv.name, wcv.wins, mcv.match_count as matches "
        "from win_count_view wcv "
        "inner join match_count_view mcv on wcv.id = mcv.id "
        "order by wins desc ")
    retval = cursor.fetchall()
    conn.close()
    return retval
                   


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT into games (player_one, player_two, winner) values "
        "(%s, %s, %s); ", (winner, loser, winner))
    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect();
    cursor = conn.cursor();
    cursor.execute("SELECT * FROM win_count_view")
    id1 = 0
    name1 = None
    retval = []
    for row in cursor:
        # First player is not defined so define the first player
        if(name1 is None):
            name1 = row[1]
            id1 = row[0]
        # First player is defined to add a tuple to the final list. 
        else:
            retval.append((id1, name1, row[0], row[1]))
            print(retval)
            name1 = None
    return retval


