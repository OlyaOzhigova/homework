--Создание таблицы c жанрами
CREATE TABLE style (
    style_id SERIAL PRIMARY KEY,
    style_name VARCHAR(255) NOT NULL);

---- Создание таблицы с исполнителнителями
   CREATE TABLE performer (
    performer_id SERIAL PRIMARY KEY,
    performer_name VARCHAR(255) NOT NULL
);
-- Создание таблицы с альбомами
CREATE TABLE album (
    album_id SERIAL PRIMARY KEY,
    name_album VARCHAR(255) NOT NULL,
    year_of_production INT NOT NULL
);
--создание таблицы с треками
CREATE TABLE track (
    track_id SERIAL PRIMARY KEY,
    track_name VARCHAR(255) NOT NULL,
    track_duration TIME,
    album_id INT NOT NULL,
    FOREIGN KEY (album_id) REFERENCES album(album_id)
);
--создание таблицы со сборниками
CREATE TABLE compilation (
	compilation_id SERIAL PRIMARY KEY,
	compilation_name VARCHAR(255) NOT NULL,
	year_of_production INT NOT NULL
);
--Исполнители и их альбомы
CREATE TABLE performer_album (
	performer_id INT NOT NULL,
	album_id INT NOT NULL,
	PRIMARY KEY (performer_id, album_id),
	FOREIGN KEY (performer_id) REFERENCES performer(performer_id),
	FOREIGN KEY (album_id) REFERENCES album(album_id)
);

--Жанры и Исполнители
CREATE TABLE performer_style (
	performer_id INT NOT NULL,
	style_id INT NOT NULL,
	PRIMARY KEY (performer_id, style_id),
	FOREIGN KEY (performer_id) REFERENCES performer(performer_id),
	FOREIGN KEY (style_id) REFERENCES style(style_id)
);
--Данные о треках и сборниках
CREATE TABLE compilation_track (
	compilation_id INT NOT NULL,
	track_id INT NOT NULL,
	PRIMARY KEY (compilation_id, track_id),
	FOREIGN KEY (compilation_id) REFERENCES compilation(compilation_id),
	FOREIGN KEY (track_id) REFERENCES track(track_id)
);
