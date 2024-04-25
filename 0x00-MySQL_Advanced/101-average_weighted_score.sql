-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.


DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
-- declare user_id to use in loop
DECLARE user_id INT;
DECLARE sum_of_factors INT DEFAULT 0;
DECLARE weighted_scores INT DEFAULT 0; 
DECLARE average FLOAT DEFAULT 0;

DECLARE done BOOLEAN DEFAULT FALSE;
-- declaring a cursor
DECLARE cur CURSOR FOR 
	SELECT id FROM users;

-- set the end of the cursor
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

-- open Cursor
OPEN cur;

-- loop through user ids
read_loop: LOOP
	-- fetch a user_id from user_ids
	FETCH cur INTO user_id;
	
	IF done THEN
		LEAVE read_loop;
	END IF;
	
	-- print user_id
	-- SELECT user_id AS MESSAGE;

	SELECT sum(weight) INTO sum_of_factors FROM projects
	WHERE id IN
	(SELECT project_id FROM corrections WHERE user_id = user_id);

	SELECT sum(weight * score) INTO weighted_scores
	FROM projects, corrections
	WHERE
	projects.id = corrections.project_id
	AND
	corrections.user_id = user_id;

	SET average = weighted_scores / sum_of_factors;

	-- -- updating the users score
	UPDATE users SET average_score = average WHERE id = user_id;
	
END LOOP;
END $$

DELIMITER ;