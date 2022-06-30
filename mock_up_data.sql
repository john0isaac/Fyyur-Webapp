-- Venue
INSERT INTO "Venue" VALUES (1, 'The Musical Hop', 'Jazz, Reggae, Swing, Classical, Folk', '1015 Folsom Street', 'San Francisco', 'CA', '123-123-1234', 'https://www.themusicalhop.com', 'https://www.facebook.com/TheMusicalHop', TRUE, 'We are on the lookout for a local artist to play every two weeks. Please call us.', 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60');
INSERT INTO "Venue" VALUES (2, 'The Dueling Pianos Bar', 'Classical, R&B, Hip-Hop', '335 Delancey Street', 'New York', 'NY', '914-003-1132', 'https://www.theduelingpianos.com', 'https://www.facebook.com/theduelingpianos', FALSE, null, 'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80');
INSERT INTO "Venue" VALUES (3, 'Park Square Live Music & Coffee', 'Rock n Roll, Jazz, Classical, Folk', '34 Whiskey Moore Ave', 'San Francisco', 'CA', '415-000-1234', 'https://www.parksquarelivemusicandcoffee.com', 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', FALSE, null, 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80');
-- Artist
INSERT INTO "Artist" VALUES (4, 'Guns N Petals', 'Rock n Roll', 'San Francisco', 'CA', '326-123-5000', 'https://www.gunsnpetalsband.com', 'https://www.facebook.com/GunsNPetals', TRUE, 'Looking for shows to perform at in the San Francisco Bay Area!', 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80');
INSERT INTO "Artist" VALUES (5, 'Matt Quevedo', 'Jazz', 'New York', 'NY', '300-400-5000', 'https://www.theduelingpianos.com', null, FALSE, null, 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80');
INSERT INTO "Artist" VALUES (6, 'The Wild Sax Band', 'Jazz, Classical', 'San Francisco', 'CA', '432-325-5432', null, null, FALSE, null, 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80');
-- Show
INSERT INTO "Show" VALUES (1, 1, 4, '2019-05-21T21:30:00.000Z');
INSERT INTO "Show" VALUES (2, 3, 5, '2019-06-15T23:00:00.000Z');
INSERT INTO "Show" VALUES (3, 3, 6, '2035-04-01T20:00:00.000Z');
INSERT INTO "Show" VALUES (4, 3, 6, '2035-04-08T20:00:00.000Z');
INSERT INTO "Show" VALUES (5, 3, 6, '2035-04-15T20:00:00.000Z');

-- Fix Id Sequence
SELECT setval('"Venue_id_seq"', (SELECT MAX(id) from "Venue"));
SELECT setval('"Artist_id_seq"', (SELECT MAX(id) from "Artist"));
SELECT setval('"Show_id_seq"', (SELECT MAX(id) from "Show"));