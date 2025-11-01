-- Clean setup for test database
-- This script creates all required tables in the correct order

-- Drop tables in reverse order of dependencies
DROP TABLE IF EXISTS history_tasks;
DROP TABLE IF EXISTS volunteer_history;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS event_requirements;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS volunteer_skills;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS volunteers;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS user_skills;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name            VARCHAR(100)    NOT NULL,
  email           VARCHAR(255)    NOT NULL,
  password_hash   VARCHAR(255)    NOT NULL,
  state           CHAR(2)         NULL,
  created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_email (email)
);

-- Create skills table
CREATE TABLE skills (
  id    BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name  VARCHAR(100)    NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY (name)
);

-- Create user_skills table
CREATE TABLE user_skills (
  user_id  BIGINT UNSIGNED NOT NULL,
  skill_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (user_id, skill_id),
  CONSTRAINT fk_user_skills_user  FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
  CONSTRAINT fk_user_skills_skill FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- Create profiles table
CREATE TABLE profiles (
  user_id      BIGINT UNSIGNED NOT NULL,
  full_name    VARCHAR(120)    NOT NULL,
  address1     VARCHAR(255)    NOT NULL,
  address2     VARCHAR(255)    NULL,
  city         VARCHAR(100)    NOT NULL,
  state        CHAR(2)         NOT NULL,
  zip          VARCHAR(20)     NOT NULL,
  preferences  TEXT            NULL,
  availability JSON            NULL,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  CONSTRAINT fk_profiles_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create notifications table
CREATE TABLE notifications (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id    BIGINT UNSIGNED NOT NULL,
  type       ENUM('info','success','warning','error') NOT NULL DEFAULT 'info',
  message    TEXT            NOT NULL,
  is_read    BOOLEAN         NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_notifications_user (user_id, is_read, created_at),
  CONSTRAINT fk_notifications_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create volunteers table
CREATE TABLE volunteers (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id      BIGINT UNSIGNED NULL,
  email        VARCHAR(255)    NULL,
  name         VARCHAR(100)    NULL,
  phone        VARCHAR(40)     NULL,
  availability VARCHAR(100)    NOT NULL,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_volunteers_user (user_id),
  CONSTRAINT fk_volunteers_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Create admins table
CREATE TABLE admins (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id      BIGINT UNSIGNED NULL,
  phone        VARCHAR(40)     NULL,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY (user_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Create volunteer_skills table
CREATE TABLE volunteer_skills (
  volunteer_id BIGINT UNSIGNED NOT NULL,
  skill_id     BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (volunteer_id, skill_id),
  CONSTRAINT fk_vol_skills_vol   FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
  CONSTRAINT fk_vol_skills_skill FOREIGN KEY (skill_id)     REFERENCES skills(id)     ON DELETE CASCADE
);

-- Create events table
CREATE TABLE events (
  id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  ownerid          BIGINT UNSIGNED NOT NULL,
  name             VARCHAR(160)    NOT NULL,
  description      TEXT            NULL,
  date             DATE            NOT NULL,
  location         VARCHAR(255)    NULL,
  max_volunteers   INT UNSIGNED    NOT NULL DEFAULT 10,
  urgency          ENUM('low','medium','high') NOT NULL DEFAULT 'low',
  img              VARCHAR(255)    NULL,
  time_label       VARCHAR(160)    NULL,
  created_at       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_events_date (date, urgency)
);

-- Create event_requirements table
CREATE TABLE event_requirements (
  event_id BIGINT UNSIGNED NOT NULL,
  skill_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (event_id, skill_id),
  CONSTRAINT fk_evt_req_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
  CONSTRAINT fk_evt_req_skill FOREIGN KEY (skill_id) REFERENCES skills(id)  ON DELETE CASCADE
);

-- Create matches table
CREATE TABLE matches (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  volunteer_id  BIGINT UNSIGNED NOT NULL,
  event_id      BIGINT UNSIGNED NOT NULL,
  status        ENUM('pending','confirmed','cancelled') NOT NULL DEFAULT 'confirmed',
  matched_at    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_matches_unique (volunteer_id, event_id),
  KEY idx_matches_event (event_id, status),
  CONSTRAINT fk_matches_volunteer FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
  CONSTRAINT fk_matches_event     FOREIGN KEY (event_id)     REFERENCES events(id)     ON DELETE CASCADE
);

-- Create volunteer_history table
CREATE TABLE volunteer_history (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  volunteer_id BIGINT UNSIGNED NOT NULL,
  event_id     BIGINT UNSIGNED NOT NULL,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY (volunteer_id, created_at),
  FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE
);

-- Create history_tasks table
CREATE TABLE history_tasks (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  history_id   BIGINT UNSIGNED NOT NULL,
  name         VARCHAR(160)    NOT NULL,
  completed    BOOLEAN         NOT NULL DEFAULT FALSE,
  volunteer_id BIGINT UNSIGNED DEFAULT NULL,
  score        INT             NULL,
  PRIMARY KEY (id),
  KEY (history_id),
  FOREIGN KEY (history_id) REFERENCES volunteer_history(id) ON DELETE CASCADE,
  FOREIGN KEY (volunteer_id) REFERENCES users(id) ON DELETE SET NULL
);
