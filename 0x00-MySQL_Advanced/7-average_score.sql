-- Write a SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student. Note: An average score can be a decimal

-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- 		user_id, a users.id value (you can assume user_id is linked to an existing users)

DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN

DECLARE user_score DECIMAL(10, 2);

-- SELECT AVG(score) INTO user_score FROM corrections WHERE user_id = user_id;
SELECT SUM(score) / COUNT(*) INTO user_score FROM corrections WHERE corrections.user_id = user_id;

UPDATE users SET average_score = user_score WHERE id = user_id;

END$$

DELIMITER ;
