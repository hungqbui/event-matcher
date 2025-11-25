-- ============================================
-- Mock Data for Event Matcher Database
-- ============================================
-- This file contains realistic sample data for testing and development
-- Run this after creating the database schema
-- Password for all test users is "password123" (SHA-256 hashed)

USE `eventmatcher`;

-- Disable foreign key checks temporarily for easier insertion
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. SKILLS
-- ============================================
INSERT INTO `skills` (`id`, `name`) VALUES
(1, 'Tree Planting'),
(2, 'Disaster Relief'),
(3, 'Youth Mentorship'),
(4, 'Food Drives'),
(5, 'Blood Drives'),
(6, 'Gardening'),
(7, 'Organizing'),
(8, 'First Aid'),
(9, 'Teaching'),
(10, 'Teamwork'),
(11, 'Environmental Awareness'),
(12, 'Communication'),
(13, 'Physical Stamina'),
(14, 'Fundraising'),
(15, 'Event Planning'),
(16, 'CPR Certified'),
(17, 'Bilingual Spanish'),
(18, 'Bilingual Vietnamese'),
(19, 'Computer Skills'),
(20, 'Social Media Management');

-- ============================================
-- 2. USERS (with SHA-256 hashed passwords)
-- ============================================
-- Password for all test users is "password123"
-- SHA-256 hash: ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
INSERT INTO `users` (`id`, `name`, `email`, `password_hash`, `state`, `created_at`) VALUES
(1, 'John Smith', 'john.smith@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-01-15 10:30:00'),
(2, 'Sarah Johnson', 'sarah.j@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-01-20 14:20:00'),
(3, 'Michael Chen', 'mchen@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-02-01 09:15:00'),
(4, 'Emily Rodriguez', 'emily.r@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-02-10 16:45:00'),
(5, 'David Williams', 'dwilliams@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-02-15 11:00:00'),
(6, 'Lisa Anderson', 'lisa.anderson@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-03-01 08:30:00'),
(7, 'Robert Taylor', 'rtaylor@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-03-05 13:20:00'),
(8, 'Maria Garcia', 'maria.garcia@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-03-10 10:45:00'),
(9, 'Admin User', 'admin@eventmatcher.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-01-01 00:00:00'),
(10, 'Jessica Martinez', 'jmartinez@email.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'TX', '2025-03-15 15:30:00');

-- ============================================
-- 3. USER SKILLS
-- ============================================
INSERT INTO `user_skills` (`user_id`, `skill_id`) VALUES
-- John Smith - Environmental volunteer
(1, 1), (1, 6), (1, 10), (1, 11),
-- Sarah Johnson - Healthcare volunteer
(2, 5), (2, 8), (2, 10), (2, 16),
-- Michael Chen - Youth mentor
(3, 3), (3, 9), (3, 10), (3, 12), (3, 18),
-- Emily Rodriguez - Community organizer
(4, 4), (4, 7), (4, 12), (4, 14), (4, 17),
-- David Williams - Event coordinator
(5, 7), (5, 10), (5, 12), (5, 15), (5, 19),
-- Lisa Anderson - Gardening expert
(6, 1), (6, 6), (6, 11), (6, 13),
-- Robert Taylor - Disaster response
(7, 2), (7, 8), (7, 10), (7, 13), (7, 16),
-- Maria Garcia - Social media coordinator
(8, 12), (8, 15), (8, 17), (8, 20),
-- Admin User - All skills
(9, 7), (9, 10), (9, 12), (9, 15),
-- Jessica Martinez - Teaching and mentorship
(10, 3), (10, 9), (10, 10), (10, 12);

-- ============================================
-- 4. ADMINS
-- ============================================
INSERT INTO `admins` (`id`, `user_id`, `phone`, `created_at`) VALUES
(1, 9, '713-555-0100', '2025-01-01 00:00:00');

-- ============================================
-- 5. VOLUNTEERS
-- ============================================
INSERT INTO `volunteers` (`id`, `user_id`, `phone`, `availability`, `created_at`) VALUES
(1, 1, '713-555-0101', 'weekends', '2025-01-15 10:30:00'),
(2, 2, '713-555-0102', 'evenings', '2025-01-20 14:20:00'),
(3, 3, '713-555-0103', 'flexible', '2025-02-01 09:15:00'),
(4, 4, '713-555-0104', 'weekends', '2025-02-10 16:45:00'),
(5, 5, '713-555-0105', 'weekdays', '2025-02-15 11:00:00'),
(6, 6, '713-555-0106', 'weekends', '2025-03-01 08:30:00'),
(7, 7, '713-555-0107', 'flexible', '2025-03-05 13:20:00'),
(8, 8, '713-555-0108', 'evenings', '2025-03-10 10:45:00'),
(9, 10, '713-555-0110', 'weekends', '2025-03-15 15:30:00');

-- ============================================
-- 6. VOLUNTEER SKILLS
-- ============================================
INSERT INTO `volunteer_skills` (`volunteer_id`, `skill_id`) VALUES
-- John Smith
(1, 1), (1, 6), (1, 10), (1, 11),
-- Sarah Johnson
(2, 5), (2, 8), (2, 10), (2, 16),
-- Michael Chen
(3, 3), (3, 9), (3, 10), (3, 12), (3, 18),
-- Emily Rodriguez
(4, 4), (4, 7), (4, 12), (4, 14), (4, 17),
-- David Williams
(5, 7), (5, 10), (5, 12), (5, 15), (5, 19),
-- Lisa Anderson
(6, 1), (6, 6), (6, 11), (6, 13),
-- Robert Taylor
(7, 2), (7, 8), (7, 10), (7, 13), (7, 16),
-- Maria Garcia
(8, 12), (8, 15), (8, 17), (8, 20),
-- Jessica Martinez
(9, 3), (9, 9), (9, 10), (9, 12);

-- ============================================
-- 7. EVENTS
-- ============================================
INSERT INTO `events` (`id`, `name`, `description`, `date`, `location`, `max_volunteers`, `urgency`, `img`, `time_label`, `ownerid`, `created_at`) VALUES
(1, 'Community Food Drive', 'Join us to collect and distribute food to local families in need. Volunteers will help sort donations and assemble boxes for distribution.', '2025-11-28', 'Houston Food Bank, 535 Portwall St, Houston, TX 77029', 20, 'medium', '/src/assets/FoodDrive.jpg', '2025-11-28T03:25', 9, '2025-10-01 10:00:00'),
(2, 'Neighborhood Tree Planting', 'Help us plant trees around the park to improve air quality and provide shade. Gloves and tools will be provided.', '2025-11-29', 'Memorial Park, 6501 Memorial Dr, Houston, TX 77007', 15, 'low', '/src/assets/TreePlant.jpg', '2025-11-29T10:00', 9, '2025-10-05 11:00:00'),
(3, 'Coastal Cleanup', 'A morning of beach cleanup to remove litter and protect marine life. All ages welcome; bring reusable water bottle.', '2025-11-30', 'Galveston Beach, 2501 Seawall Blvd, Galveston, TX 77550', 30, 'high', '/src/assets/VCleanupHome.webp', '2025-11-30T08:00', 9, '2025-10-10 09:00:00'),
(4, 'Youth Mentorship Program', 'Spend time mentoring local youth. Help with homework, career guidance, and life skills. Background check required.', '2025-12-02', 'Boys & Girls Club, 3400 Lyons Ave, Houston, TX 77020', 10, 'medium', '/src/assets/YouthMentor.jpg', '2025-12-02T16:00', 9, '2025-10-12 14:00:00'),
(5, 'Blood Drive', 'Help save lives by donating blood or volunteering to assist with registration and hospitality.', '2025-12-05', 'Gulf Coast Regional Blood Center, 1400 La Concha Ln, Houston, TX 77054', 12, 'high', '/src/assets/BloodDrive.webp', '2025-12-05T10:00', 9, '2025-10-15 08:30:00'),
(6, 'Disaster Relief Training', 'Learn essential disaster response skills and join our emergency response team. CPR and First Aid training included.', '2025-12-08', 'Red Cross Center, 2700 Southwest Fwy, Houston, TX 77098', 25, 'medium', '/src/assets/DisasterRelief.jpg', '2025-12-08T09:00', 9, '2025-10-20 10:00:00'),
(7, 'Community Garden Setup', 'Help us build raised garden beds and plant vegetables for a local community garden project.', '2025-12-12', 'Urban Harvest Community Garden, 2311 Canal St, Houston, TX 77003', 18, 'low', '/src/assets/TreePlant.jpg', '2025-12-12T08:00', 9, '2025-10-22 09:30:00'),
(8, 'Holiday Food Basket Assembly', 'Assemble and distribute holiday food baskets for families in need. Bring festive spirit!', '2025-12-20', 'Houston Food Bank, 535 Portwall St, Houston, TX 77029', 35, 'high', '/src/assets/FoodDrive.jpg', '2025-12-20T13:00', 9, '2025-10-25 11:00:00');

-- ============================================
-- 8. EVENT REQUIREMENTS
-- ============================================
INSERT INTO `event_requirements` (`event_id`, `skill_id`) VALUES
-- Community Food Drive
(1, 4), (1, 7), (1, 10), (1, 13),
-- Tree Planting
(2, 1), (2, 6), (2, 11), (2, 13),
-- Coastal Cleanup
(3, 11), (3, 10), (3, 13),
-- Youth Mentorship
(4, 3), (4, 9), (4, 10), (4, 12),
-- Blood Drive
(5, 5), (5, 8), (5, 12), (5, 16),
-- Disaster Relief Training
(6, 2), (6, 8), (6, 10), (6, 16),
-- Community Garden
(7, 1), (7, 6), (7, 10), (7, 13),
-- Holiday Food Baskets
(8, 4), (8, 7), (8, 10), (8, 14);

-- ============================================
-- 9. MATCHES
-- ============================================
INSERT INTO `matches` (`id`, `volunteer_id`, `event_id`, `status`, `matched_at`) VALUES
-- John Smith (environmental skills) - Tree Planting & Coastal Cleanup
(1, 1, 2, 'confirmed', '2025-10-06 10:30:00'),
(2, 1, 3, 'confirmed', '2025-10-11 14:20:00'),
-- Sarah Johnson (healthcare) - Blood Drive
(3, 2, 5, 'confirmed', '2025-10-16 09:15:00'),
-- Michael Chen (youth mentor) - Youth Mentorship
(4, 3, 4, 'confirmed', '2025-10-13 11:00:00'),
-- Emily Rodriguez (organizer) - Food Drive & Holiday Baskets
(5, 4, 1, 'confirmed', '2025-10-02 15:45:00'),
(6, 4, 8, 'pending', '2025-10-26 10:00:00'),
-- David Williams (event coordinator) - Multiple events
(7, 5, 1, 'confirmed', '2025-10-03 08:30:00'),
(8, 5, 4, 'confirmed', '2025-10-14 12:00:00'),
-- Lisa Anderson (gardening) - Tree Planting & Community Garden
(9, 6, 2, 'confirmed', '2025-10-07 09:00:00'),
(10, 6, 7, 'confirmed', '2025-10-23 11:30:00'),
-- Robert Taylor (disaster response) - Disaster Relief Training
(11, 7, 6, 'confirmed', '2025-10-21 13:45:00'),
-- Maria Garcia (social media) - Multiple events for promotion
(12, 8, 1, 'confirmed', '2025-10-04 10:15:00'),
(13, 8, 8, 'confirmed', '2025-10-27 14:30:00'),
-- Jessica Martinez (teaching) - Youth Mentorship
(14, 9, 4, 'confirmed', '2025-10-15 16:00:00');

-- ============================================
-- 10. PROFILES
-- ============================================
INSERT INTO `profiles` (`user_id`, `full_name`, `address1`, `address2`, `city`, `state`, `zip`, `preferences`, `availability`) VALUES
(1, 'John Smith', '123 Oak Street', 'Apt 4B', 'Houston', 'TX', '77001', 'Outdoor activities, environmental causes', '["Saturday", "Sunday"]'),
(2, 'Sarah Johnson', '456 Pine Avenue', NULL, 'Houston', 'TX', '77002', 'Healthcare, community wellness', '["Monday", "Wednesday", "Friday"]'),
(3, 'Michael Chen', '789 Maple Drive', NULL, 'Houston', 'TX', '77003', 'Youth development, education', '["Tuesday", "Thursday"]'),
(4, 'Emily Rodriguez', '321 Elm Street', 'Suite 200', 'Houston', 'TX', '77004', 'Community organizing, food security', '["Saturday", "Sunday"]'),
(5, 'David Williams', '654 Cedar Lane', NULL, 'Houston', 'TX', '77005', 'Event management, coordination', '["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]'),
(6, 'Lisa Anderson', '987 Birch Road', NULL, 'Houston', 'TX', '77006', 'Gardening, sustainability', '["Saturday", "Sunday"]'),
(7, 'Robert Taylor', '147 Willow Court', 'Unit 10', 'Houston', 'TX', '77007', 'Emergency response, disaster relief', '["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]'),
(8, 'Maria Garcia', '258 Ash Boulevard', NULL, 'Houston', 'TX', '77008', 'Social media, fundraising', '["Monday", "Wednesday", "Friday"]'),
(9, 'Admin User', '1 Admin Plaza', NULL, 'Houston', 'TX', '77000', 'System administration', '[]'),
(10, 'Jessica Martinez', '369 Spruce Avenue', 'Apt 3A', 'Houston', 'TX', '77009', 'Teaching, mentoring', '["Tuesday", "Thursday", "Saturday"]');

-- ============================================
-- 11. VOLUNTEER HISTORY
-- ============================================
INSERT INTO `volunteer_history` (`id`, `volunteer_id`, `event_id`, `created_at`) VALUES
(1, 1, 1, '2025-10-05 12:30:00'),
(2, 1, 2, '2025-09-15 14:30:00'),
(3, 2, 3, '2025-08-20 16:30:00'),
(4, 3, 4, '2025-09-30 17:30:00'),
(5, 4, 1, '2025-07-20 13:30:00'),
(6, 5, 2, '2025-08-10 18:30:00'),
(7, 6, 7, '2025-09-28 11:30:00'),
(8, 7, 6, '2025-09-07 20:00:00'),
(9, 8, 1, '2025-10-15 17:00:00'),
(10, 9, 4, '2025-09-20 15:30:00');

-- ============================================
-- 12. HISTORY TASKS
-- ============================================
-- Note: history_id is nullable, event_id references the event these tasks belong to
INSERT INTO `history_tasks` (`id`, `history_id`, `name`, `completed`, `volunteer_id`, `event_id`, `score`) VALUES
-- Event 1 (Community Food Drive) tasks - history_id 1
(1, 1, 'Collect litter in Zone A', 1, 1, 1, 90),
(2, 1, 'Plant flowers in garden beds', 1, 1, 1, 85),
(3, 1, 'Empty trash bins', 1, 1, 1, 80),
-- Event 2 (Tree Planting) tasks - history_id 2
(4, 2, 'Dig planting holes', 1, 1, 2, 95),
(5, 2, 'Plant saplings', 1, 1, 2, 90),
(6, 2, 'Water new trees', 1, 1, 2, 85),
-- Event 3 (Coastal Cleanup) tasks - history_id 3
(7, 3, 'Register donors', 1, 2, 3, 98),
(8, 3, 'Provide refreshments', 1, 2, 3, 95),
(9, 3, 'Monitor donor recovery', 1, 2, 3, 92),
-- Event 4 (Youth Mentorship) tasks - history_id 4
(10, 4, 'Math tutoring session', 1, 3, 4, 90),
(11, 4, 'Science project help', 1, 3, 4, 88),
(12, 4, 'Homework assistance', 1, 3, 4, 86),
-- Event 1 (Community Food Drive) tasks - history_id 5
(13, 5, 'Sort food items', 1, 4, 1, 94),
(14, 5, 'Pack family boxes', 1, 4, 1, 92),
(15, 5, 'Load vehicles', 1, 4, 1, 90),
-- Event 2 (Tree Planting) tasks - history_id 6
(16, 6, 'Volunteer check-in', 1, 5, 2, 96),
(17, 6, 'Stage management', 1, 5, 2, 94),
(18, 6, 'Cleanup coordination', 1, 5, 2, 92),
-- Event 7 (Community Garden) tasks - history_id 7
(19, 7, 'Weed garden beds', 1, 6, 7, 88),
(20, 7, 'Harvest vegetables', 1, 6, 7, 90),
(21, 7, 'Water plants', 1, 6, 7, 85),
-- Event 6 (Disaster Relief) tasks - history_id 8
(22, 8, 'Distribute supplies', 1, 7, 6, 99),
(23, 8, 'Coordinate volunteers', 1, 7, 6, 98),
(24, 8, 'Assess needs', 1, 7, 6, 97),
-- Event 1 (Community Food Drive) tasks - history_id 9
(25, 9, 'Create content', 1, 8, 1, 92),
(26, 9, 'Post updates', 1, 8, 1, 88),
(27, 9, 'Engage with followers', 1, 8, 1, 87),
-- Event 4 (Youth Mentorship) tasks - history_id 10
(28, 10, 'Prepare presentation', 1, 9, 4, 93),
(29, 10, 'Deliver talk', 1, 9, 4, 92),
(30, 10, 'Answer Q&A', 1, 9, 4, 89),
-- Additional unassigned tasks for current events (event_id set, history_id and volunteer_id NULL)
(31, NULL, 'Setup registration tables', 0, NULL, 1, 25),
(32, NULL, 'Greet volunteers', 0, NULL, 1, 20),
(33, NULL, 'Prepare soil', 0, NULL, 2, 30),
(34, NULL, 'Mark planting spots', 0, NULL, 2, 25),
(35, NULL, 'Sort recyclables', 0, NULL, 3, 35),
(36, NULL, 'Document cleanup progress', 0, NULL, 3, 30),
(37, NULL, 'Prepare activity materials', 0, NULL, 4, 40),
(38, NULL, 'Lead group discussion', 0, NULL, 4, 45),
(39, NULL, 'Setup donation station', 0, NULL, 5, 30),
(40, NULL, 'Monitor donor waiting area', 0, NULL, 5, 25);

-- ============================================
-- 13. NOTIFICATIONS
-- ============================================
INSERT INTO `notifications` (`id`, `user_id`, `type`, `message`, `is_read`, `created_at`) VALUES
(1, 1, 'success', 'You have been matched with "Neighborhood Tree Planting" event!', 1, '2025-10-06 10:30:00'),
(2, 1, 'info', 'Reminder: Coastal Cleanup is tomorrow at 8:00 AM', 0, '2025-11-21 18:00:00'),
(3, 2, 'success', 'Thank you for volunteering at the Blood Drive!', 1, '2025-08-20 17:00:00'),
(4, 2, 'info', 'You have been confirmed for the Blood Drive on Nov 25', 0, '2025-10-16 09:30:00'),
(5, 3, 'success', 'Your Youth Mentorship application has been approved', 1, '2025-10-13 11:15:00'),
(6, 3, 'warning', 'Please complete your background check by Nov 15', 0, '2025-11-01 09:00:00'),
(7, 4, 'success', 'You are confirmed for Community Food Drive', 1, '2025-10-02 16:00:00'),
(8, 4, 'info', 'New event matches your skills: Holiday Food Basket Assembly', 0, '2025-10-25 12:00:00'),
(9, 5, 'success', 'Thank you for coordinating the Community Festival!', 1, '2025-08-11 09:00:00'),
(10, 5, 'info', 'You have 2 upcoming events this month', 0, '2025-11-01 08:00:00'),
(11, 6, 'success', 'Great job on the Community Garden project!', 1, '2025-09-28 12:00:00'),
(12, 6, 'info', 'New gardening event available: Community Garden Setup', 0, '2025-10-23 11:45:00'),
(13, 7, 'success', 'Certificate earned: Disaster Relief Training', 1, '2025-09-08 10:00:00'),
(14, 7, 'info', 'Disaster Relief Training session starts Dec 1', 0, '2025-10-21 14:00:00'),
(15, 8, 'success', 'Your social media campaign reached 5,000 people!', 1, '2025-10-15 17:30:00'),
(16, 8, 'info', 'New volunteer opportunities need promotion', 0, '2025-10-27 15:00:00'),
(17, 10, 'success', 'Students loved your Career Day presentation!', 1, '2025-09-20 16:00:00'),
(18, 10, 'info', 'Youth Mentorship Program has an opening', 0, '2025-10-15 16:15:00'),
(19, 9, 'info', 'Volunteer John Smith claimed task "Setup registration tables" for Community Food Drive', 0, '2025-11-01 10:00:00'),
(20, 9, 'info', 'Volunteer Sarah Johnson claimed task "Sort recyclables" for Coastal Cleanup', 0, '2025-11-05 14:30:00');

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================
-- Uncomment to verify data was inserted correctly

-- SELECT COUNT(*) as total_users FROM users;
-- SELECT COUNT(*) as total_volunteers FROM volunteers;
-- SELECT COUNT(*) as total_events FROM events;
-- SELECT COUNT(*) as total_skills FROM skills;
-- SELECT COUNT(*) as total_matches FROM matches;
-- SELECT COUNT(*) as total_notifications FROM notifications;

-- Show events with volunteer counts
-- SELECT e.name, e.date, e.urgency, COUNT(m.id) as volunteer_count, e.max_volunteers
-- FROM events e
-- LEFT JOIN matches m ON e.id = m.event_id AND m.status = 'confirmed'
-- GROUP BY e.id
-- ORDER BY e.date;

-- Show volunteers with their skills
-- SELECT u.name, GROUP_CONCAT(s.name SEPARATOR ', ') as skills
-- FROM users u
-- JOIN volunteers v ON u.id = v.user_id
-- JOIN volunteer_skills vs ON v.id = vs.volunteer_id
-- JOIN skills s ON vs.skill_id = s.id
-- GROUP BY u.id;

-- ============================================
-- END OF MOCK DATA
-- ============================================

COMMIT;

SELECT 'Mock data inserted successfully!' as Status;
