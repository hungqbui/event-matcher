DROP DATABASE eventmatcher;
CREATE DATABASE IF NOT EXISTS eventmatcher;

USE eventmatcher;

CREATE TABLE IF NOT EXISTS users (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name            VARCHAR(100)    NOT NULL,
  email           VARCHAR(255)    NOT NULL,
  password_hash   VARCHAR(255)    NOT NULL,               -- store hashed pw, not plain
  state           CHAR(2)         NULL,                   -- from signup
  created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_email (email)
);

CREATE TABLE IF NOT EXISTS skills (
  id    BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name  VARCHAR(100)    NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY (name)
);

CREATE TABLE IF NOT EXISTS user_skills (
  user_id  BIGINT UNSIGNED NOT NULL,
  skill_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (user_id, skill_id),
  CONSTRAINT fk_user_skills_user  FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
  CONSTRAINT fk_user_skills_skill FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS profiles (
  user_id      BIGINT UNSIGNED NOT NULL,
  full_name    VARCHAR(120)    NOT NULL,
  address1     VARCHAR(255)    NOT NULL,
  address2     VARCHAR(255)    NULL,
  city         VARCHAR(100)    NOT NULL,
  state        CHAR(2)         NOT NULL,
  zip          VARCHAR(20)     NOT NULL,
  preferences  TEXT            NULL,                      -- "Prefer outdoor activities"
  availability JSON            NULL,                      -- e.g., ["Monday","Wednesday","Friday"]
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id),
  CONSTRAINT fk_profiles_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CHECK (JSON_VALID(availability))
);

CREATE TABLE IF NOT EXISTS notifications (
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

CREATE TABLE IF NOT EXISTS volunteers (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id      BIGINT UNSIGNED NULL,             -- link to users if applicable
  phone        VARCHAR(40)     NULL,
  availability VARCHAR(100)    NOT NULL,         -- e.g., "weekends","weekdays","evenings","flexible"
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_volunteers_user (user_id),
  CONSTRAINT fk_volunteers_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS admins (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id      BIGINT UNSIGNED NULL,             -- link to users if applicable
  phone        VARCHAR(40)     NULL,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY (user_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS volunteer_skills (
  volunteer_id BIGINT UNSIGNED NOT NULL,
  skill_id     BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (volunteer_id, skill_id),
  CONSTRAINT fk_vol_skills_vol   FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
  CONSTRAINT fk_vol_skills_skill FOREIGN KEY (skill_id)     REFERENCES skills(id)     ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS events (
  id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  ownerid       BIGINT UNSIGNED NOT NULL,        -- admin user who created
  name             VARCHAR(160)    NOT NULL,
  description      TEXT            NULL,
  date             DATE            NOT NULL,
  location         VARCHAR(255)    NULL,
  max_volunteers   INT UNSIGNED    NOT NULL DEFAULT 10,
  urgency          ENUM('low','medium','high') NOT NULL DEFAULT 'low',
  img              VARCHAR(255)    NULL,           -- optional asset path
  time_label       VARCHAR(160)    NULL,           -- the pretty "Sat, Nov 2 · 8:00 AM - 11:00 AM"
  created_at       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_events_date (date, urgency)
);

CREATE TABLE IF NOT EXISTS event_requirements (
  event_id BIGINT UNSIGNED NOT NULL,
  skill_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (event_id, skill_id),
  CONSTRAINT fk_evt_req_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
  CONSTRAINT fk_evt_req_skill FOREIGN KEY (skill_id) REFERENCES skills(id)  ON DELETE CASCADE
); 

CREATE TABLE IF NOT EXISTS matches (
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

CREATE TABLE IF NOT EXISTS volunteer_history (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  volunteer_id BIGINT UNSIGNED NOT NULL,        -- or user_id if you prefer; here we tie to volunteers
  event_id    BIGINT UNSIGNED NOT NULL,
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY (volunteer_id, created_at),
  FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS history_tasks (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  history_id   BIGINT UNSIGNED DEFAULT NULL,
  name         VARCHAR(160)    NOT NULL,
  completed    BOOLEAN         NOT NULL DEFAULT FALSE,
  volunteer_id BIGINT UNSIGNED DEFAULT NULL,
  event_id   BIGINT UNSIGNED DEFAULT NULL,
  score        INT             NULL,
  PRIMARY KEY (id),
  KEY (history_id),
  FOREIGN KEY (history_id) REFERENCES volunteer_history(id) ON DELETE CASCADE,
  FOREIGN KEY (volunteer_id) REFERENCES users(id) ON DELETE SET NULL,
  FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL
);
