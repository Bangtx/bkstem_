DROP TABLE IF EXISTS account CASCADE;
CREATE TABLE account
(
  id bigserial NOT NULL,
  name text,
  password text,
  mail text,
  phone text,
  search_str text,
  order_num bigint,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_account PRIMARY KEY (id)
);

DROP TABLE IF EXISTS student CASCADE;
CREATE TABLE student
(
  id bigserial NOT NULL,
  account_id int,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_student PRIMARY KEY (id)
);

DROP TABLE IF EXISTS teacher CASCADE;
CREATE TABLE teacher
(
  id bigserial NOT NULL,
  account_id int,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_teacher PRIMARY KEY (id)
);

DROP TABLE IF EXISTS classroom CASCADE;
CREATE TABLE classroom
(
  id bigserial NOT NULL,
  name text,
  teacher_id bigint,
  student_ids bigint[],
  class_time_ids bigint[],
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_classroom PRIMARY KEY (id)
);

DROP TABLE IF EXISTS class_time CASCADE;
CREATE TABLE class_time
(
  id bigserial NOT NULL,
  date_of_week_id int,
  start_time time,
  stop_time time,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_class_time PRIMARY KEY (id)
);

DROP TABLE IF EXISTS date_of_week CASCADE;
CREATE TABLE date_of_week
(
  id bigserial NOT NULL,
  name text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_date_of_week PRIMARY KEY (id)
);

DROP TABLE IF EXISTS absent_type CASCADE;
CREATE TABLE absent_type
(
  id bigserial NOT NULL,
  type text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_absent_type PRIMARY KEY (id)
);

DROP TABLE IF EXISTS roll_call CASCADE;
CREATE TABLE roll_call
(
  id bigserial NOT NULL,
  classroom_id bigint,
  student_id bigint,
  teacher_id bigint,
  absent_type_id int,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_roll_call PRIMARY KEY (id)
);

DROP TABLE IF EXISTS notification CASCADE;
CREATE TABLE notification
(
  id bigserial NOT NULL,
  classroom_id bigint,
  student_id bigint[],
  teacher_id bigint,
  notification text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_notification PRIMARY KEY (id)
);