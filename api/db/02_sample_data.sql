CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

INSERT INTO account(name, password, mail, phone)
VALUES ('admin', '5f4dcc3b5aa765d61d8327deb882cf99', 'admin@gmail.com', null);

INSERT INTO date_of_week(name)
VALUES ('Thứ 2'), ('Thứ 3'), ('Thứ 4'), ('Thứ 5'), ('Thứ 6'), ('Thứ 7'), ('Chủ nhật');

INSERT INTO absent_type(type)
VALUES ('Đúng giờ'), ('Nghỉ có phép'), ('Nghỉ không phép'), ('Muộn có phép'), ('Muộn không phép')

