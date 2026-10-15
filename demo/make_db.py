"""Create a small demo.db for the sqlite server."""
import sqlite3

c = sqlite3.connect("demo.db")
c.executescript("""
DROP TABLE IF EXISTS cities;
CREATE TABLE cities (name TEXT, country TEXT, population INTEGER);
INSERT INTO cities VALUES ('Rabat', 'Morocco', 580000), ('Fes', 'Morocco', 1110000), ('Lisbon', 'Portugal', 545000);
""")
c.commit()
print("created demo.db")
