-- Write a SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student. Note: An average score can be a decimal

-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- 		user_id, a users.id value (you can assume user_id is linked to an existing users)

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
DECLARE average FLOAT DEFAULT 0;
SELECT SUM(score) / count(*) INTO average FROM corrections
WHERE user_id = user_id;

-- updating the users score
UPDATE users SET average_score = average WHERE id = user_id;

END $$

DELIMITER ;