-- Bảng người dùng
CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	email TEXT,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
--Bảng thiết bị
CREATE TABLE device (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	type TEXT,
	location TEXT,
	user_id INTEGER,
	FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Bảng log sự kiện
CREATE TABLE log (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	device_id INTEGER,
	event TEXT,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (device_id) REFERENCES device(id)
);

-- Bảng dữ liệu cảm biến
CREATE TABLE sensor_data (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	device_id INTEGER,
	sensor_type TEXT,
	value TEXT,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (device_id) REFERENCES device(id)
);

-- Bảng phản hồi AI
CREATE TABLE ai_response (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	request TEXT,
	response TEXT,
	audio_path TEXT,
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Bảng lưu file âm thanh vào/ra
CREATE TABLE audio_file (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	file_path TEXT NOT NULL,
	direction TEXT CHECK(direction IN ('in', 'out')),
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Bảng lưu dữ liệu người dùng phục vụ nhận diện khuôn mặt
CREATE TABLE face_user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	name TEXT NOT NULL,
	face_embedding BLOB NOT NULL,
	image_path TEXT,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES user(id)
);
