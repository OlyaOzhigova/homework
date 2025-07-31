--Задание 2

--2.1. Название и продолжительность самого длительного трека
SELECT track_name, track_duration
FROM track
ORDER BY track_duration DESC
LIMIT 1;

--2.2. Название треков, продолжительность которых не менее 3,5 минут
SELECT track_name
FROM track
WHERE track_duration >= '00:03:30';

--2.3. Названия сборников, вышедших в период с 2018 по 2020 год включительно
SELECT compilation_name
FROM compilation
WHERE year_of_production BETWEEN 2018 AND 2020;

--2.4. Исполнители, чьё имя состоит из одного слова.
SELECT performer_name
FROM performer
WHERE performer_name NOT LIKE '% %';

--2.5. Название треков, которые содержат слово «мой» или «my»
SELECT track_name
FROM track
WHERE track_name LIKE '%мой%'
   OR track_name LIKE '%my%';

--Задание 3
--3.1. Количество исполнителей в каждом жанре.
SELECT s.style_name, COUNT(ps.performer_id) AS performer_count
FROM style s
LEFT JOIN performer_style ps ON s.style_id = ps.style_id
GROUP BY s.style_name;

--3.2. Количество треков, вошедших в альбомы 2019–2020 годов:
SELECT COUNT(t.track_id) AS track_count
FROM track t
JOIN album a ON t.album_id = a.album_id
WHERE a.year_of_production BETWEEN 2019 AND 2020;

--3.3. Средняя продолжительность треков по каждому альбому:
SELECT a.name_album, AVG(EXTRACT(EPOCH FROM t.track_duration)) AS average_duration
FROM album a
JOIN track t ON a.album_id = t.album_id
GROUP BY a.name_album;

--3.4. Все исполнители, которые не выпустили альбомы в 2020 году:
SELECT p.performer_name
FROM performer p
WHERE p.performer_id NOT IN (
    SELECT pa.performer_id
    FROM performer_album pa
    JOIN album a ON pa.album_id = a.album_id
    WHERE a.year_of_production = 2020
);
--3.5. Названия сборников, в которых присутствует конкретный исполнитель (например, исполнитель с именем "Билли Холидей"):
SELECT DISTINCT c.compilation_name
FROM compilation c
JOIN compilation_track ct ON c.compilation_id = ct.compilation_id
JOIN track t ON ct.track_id = t.track_id
JOIN album a ON t.album_id = a.album_id
JOIN performer_album pa ON a.album_id = pa.album_id
JOIN performer p ON pa.performer_id = p.performer_id
WHERE p.performer_name = 'Билли Холидей';

--Задание 4

--4.1 Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT DISTINCT a.name_album
FROM album a
JOIN performer_album pa ON a.album_id = pa.album_id
JOIN performer_style ps ON pa.performer_id = ps.performer_id
GROUP BY a.name_album, a.album_id
HAVING COUNT(DISTINCT ps.style_id) > 1;

--4.2 Наименования треков, которые не входят в сборники
SELECT track_name
FROM track
WHERE track_id NOT IN (
    SELECT track_id
    FROM compilation_track);

--4.3 Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, — теоретически таких треков может быть несколько.
   SELECT performer.performer_name
FROM performer
JOIN performer_album ON performer.performer_id = performer_album.performer_id
JOIN album ON performer_album.album_id = album.album_id
JOIN track ON album.album_id = track.album_id
WHERE track.track_duration = (
    SELECT MIN(track_duration)
    FROM track
);

