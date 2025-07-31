--Задание 1

---- 1.1 добавить данные "не менее 3 жанров"
INSERT INTO style VALUES (11, 'Кантри');
INSERT INTO style VALUES (12, 'Фолк-музыка');
INSERT INTO style VALUES (13, 'Блюз');
INSERT INTO style VALUES (14, 'Джаз');

-- 1.2 добавить данные "не менее 4 исполнителей"
INSERT INTO performer VALUES (21, 'Алабама');
INSERT INTO performer VALUES (22, 'BB King');
INSERT INTO performer VALUES (23, 'Билли Холидей');
INSERT INTO performer VALUES (24, 'Боб Дилан');
INSERT INTO performer VALUES (25, 'Кэт Стивенс');
INSERT INTO performer VALUES (26, 'Wardruna');
INSERT INTO performer VALUES (27, 'Heilung');

-- 1.3 добавить данные "не менее 3 альбомов"
INSERT INTO album VALUES (31, 'Alabama Shakes Greatest Hits Full Album', '2019');
INSERT INTO album VALUES (32, 'Solitude song by Billie Holiday', '1952');
INSERT INTO album VALUES (33, 'Tea for the Tillerman song by Cat Stevens', '2020');
INSERT INTO album VALUES (34, 'Live At The Regal song by BB King', '1965');

-- 1.4 добавить данные "не менее 6 треков"
INSERT INTO track VALUES (41, 'Alabama Song', '00:02:59', '31');
INSERT INTO track VALUES (42, 'The Closer You Get song by Alabama', '00:02:59', '31');
INSERT INTO track VALUES (43, 'East of the Sun song by Billie Holiday', '00:03:29', '32');
INSERT INTO track VALUES (44, 'Blue Moon song by Billie Holiday', '00:02:10', '32');
INSERT INTO track VALUES (45, 'You Upset Me Baby song by BB King', '00:02:34', '34');
INSERT INTO track VALUES (46, 'Indianola Mississippi Seeds song by BB King', '00:01:59', '34');
INSERT INTO track VALUES (47, 'Singin’ The Blues song by BB King', '00:03:23', '34');

-- 1.5 добавить данные "не менее 4 сборников"
INSERT INTO compilation  VALUES (51, 'Flourishing', '1980');
INSERT INTO compilation  VALUES (52, 'Lunar night', '2010');
INSERT INTO compilation  VALUES (53, 'Melodies based', '2020');
INSERT INTO compilation  VALUES (54, 'Love and life', '2022');
--связки
INSERT INTO performer_album  VALUES (21, 31);
INSERT INTO performer_album  VALUES (22, 34);
INSERT INTO performer_album  VALUES (23, 32);
INSERT INTO performer_album  VALUES (25, 33);

INSERT INTO performer_style VALUES (21, 11);
INSERT INTO performer_style VALUES (22, 13);
INSERT INTO performer_style VALUES (22, 14);
INSERT INTO performer_style VALUES (23, 14);
INSERT INTO performer_style VALUES (24, 12);
INSERT INTO performer_style VALUES (24, 13);
INSERT INTO performer_style VALUES (24, 11);
INSERT INTO performer_style VALUES (24, 14);
INSERT INTO performer_style VALUES (26, 12);
INSERT INTO performer_style VALUES (27, 12);

INSERT INTO compilation_track VALUES (51, 41);
INSERT INTO compilation_track VALUES (51, 43);
INSERT INTO compilation_track VALUES (51, 45);
INSERT INTO compilation_track VALUES (52, 42);
INSERT INTO compilation_track VALUES (52, 46);
INSERT INTO compilation_track VALUES (53, 47);
INSERT INTO compilation_track VALUES (54, 41);
INSERT INTO compilation_track VALUES (54, 46);
