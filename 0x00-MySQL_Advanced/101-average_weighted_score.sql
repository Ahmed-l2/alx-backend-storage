-- SQL script that creates a stored procedure ComputeAverageScoreForUser that
-- computes and store the average weighted score for all students.

DELIMITER $$ 
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users
    SET average_score = (
        SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = users.id
    );
END $$ 
DELIMITER ;