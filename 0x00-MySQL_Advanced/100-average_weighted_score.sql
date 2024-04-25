-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- 		user_id, a users.id value (you can assume user_id is linked to an existing users)

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN

DECLARE sum_of_factors INT DEFAULT 0;
DECLARE weighted_scores INT DEFAULT 0; 
DECLARE average FLOAT DEFAULT 0;

SELECT sum(weight) INTO sum_of_factors FROM projects
WHERE id IN
(SELECT project_id FROM corrections WHERE user_id = user_id);

-- print sum_of_factors
-- SELECT sum_of_factors AS MESSAGE;

SELECT sum(weight * score) INTO weighted_scores
FROM projects, corrections
WHERE
projects.id = corrections.project_id
AND
corrections.user_id = user_id;

-- print weighted_scores
-- SELECT weighted_scores AS MESSAGE;

SET average = weighted_scores / sum_of_factors;

-- -- updating the users score
UPDATE users SET average_score = average WHERE id = user_id;

END $$

DELIMITER ;