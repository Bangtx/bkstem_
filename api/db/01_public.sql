DROP TABLE IF EXISTS account CASCADE;
CREATE TABLE account
(
  id bigserial NOT NULL,
  name text,
  gender text,
  date_of_birth date,
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
  status int,
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
  room text,
  teacher_id bigint,
  assistant_teacher bigint[],
  student_ids bigint[],
  class_time_ids bigint[],
  start_date date,
  total_days int,
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
  date date,
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
  date date,
  classroom_id bigint,
  student_id bigint,
  teacher_id bigint,
  notification text,
  type text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_notification PRIMARY KEY (id)
);

DROP TABLE IF EXISTS score CASCADE;
CREATE TABLE score
(
  id bigserial NOT NULL,
  date date,
  classroom_id bigint,
  student_id bigint,
  teacher_id bigint,
  score json, -- { specking: number, reading: number, writing, listening: number }
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_score PRIMARY KEY (id)
);

DROP TABLE IF EXISTS schedule CASCADE;
CREATE TABLE schedule
(
  id bigserial NOT NULL,
  classroom_id bigint,
  title text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_schedule PRIMARY KEY (id)
);

DROP TABLE IF EXISTS home_work CASCADE;
CREATE TABLE home_work
(
  id bigserial NOT NULL,
  date date,
  deadline date,
  classroom_id bigint,
  schedule_id bigint,
  question_id bigint,
  is_exactly bool default false,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_home_work PRIMARY KEY (id)
);

DROP TABLE IF EXISTS home_work_file CASCADE;
CREATE TABLE home_work_file
(
  id bigserial NOT NULL,
  date date,
  title text,
  deadline date,
  classroom_id bigint,
  file_question bigint,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_home_work_file PRIMARY KEY (id)
);

DROP TABLE IF EXISTS file_result_student CASCADE;
CREATE TABLE file_result_student
(
  id bigserial NOT NULL,
  home_work_file int,
  class_room bigint,
  student bigint,
  msg text,
  name text,
  url text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_file_result_student PRIMARY KEY (id)
);

DROP TABLE IF EXISTS file_question CASCADE;
CREATE TABLE file_question
(
  id bigserial NOT NULL,
  name text,
  url text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_file_question PRIMARY KEY (id)
);

DROP TABLE IF EXISTS question CASCADE;
CREATE TABLE question
(
  id bigserial NOT NULL,
  answers json,
  result text,
  image text,
  audio text,
  type smallint, -- 0(multichoice) or 1
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_question PRIMARY KEY (id)
);

DROP TABLE IF EXISTS audio_file CASCADE;
CREATE TABLE audio_file
(
  id bigserial NOT NULL,
  url text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_audio_file PRIMARY KEY (id)
);

DROP TABLE IF EXISTS question_student CASCADE;
CREATE TABLE question_student
(
  id bigserial NOT NULL,
  question_id bigint,
  student_id bigint,
  result text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_question_student PRIMARY KEY (id)
);

DROP TABLE IF EXISTS slide CASCADE;
CREATE TABLE slide
(
  id bigserial NOT NULL,
  title text,
  classroom bigint,
  remark text,
  url text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_slide PRIMARY KEY (id)
);


DROP TABLE IF EXISTS self_learning CASCADE;
CREATE TABLE self_learning
(
  id bigserial NOT NULL,
  date date,
  student bigint,
  classroom bigint,
  absent_type int,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_self_learning PRIMARY KEY (id)
);
