-- ============================================
-- Clear All Data from Event Matcher Database
-- ============================================
-- This script removes all data but keeps the schema intact

USE `eventmatcher`;

-- Disable foreign key checks to allow truncating tables with foreign keys
SET FOREIGN_KEY_CHECKS = 0;

-- Truncate all tables (removes all data but keeps structure)
-- Order matters: child tables first, then parent tables
TRUNCATE TABLE `history_tasks`;
TRUNCATE TABLE `volunteer_history`;
TRUNCATE TABLE `matches`;
TRUNCATE TABLE `event_requirements`;
TRUNCATE TABLE `volunteer_skills`;
TRUNCATE TABLE `user_skills`;
TRUNCATE TABLE `notifications`;
TRUNCATE TABLE `profiles`;
TRUNCATE TABLE `events`;
TRUNCATE TABLE `volunteers`;
TRUNCATE TABLE `admins`;
TRUNCATE TABLE `skills`;
TRUNCATE TABLE `users`;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

SELECT 'All data cleared successfully! Schema preserved.' as Status;
