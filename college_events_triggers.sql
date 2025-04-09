DELIMITER $$

-- Trigger: Check for overlapping events at the same location and time.
CREATE TRIGGER CheckEventOverlap
BEFORE INSERT ON Events
FOR EACH ROW
BEGIN
  IF EXISTS (
    SELECT *
    FROM Events
    WHERE lname = NEW.lname
      AND event_date = NEW.event_date
      AND ((NEW.end_time > start_time AND NEW.start_time < end_time))
  ) THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Overlapping event at the same location/time!';
  END IF;
END$$

-- Trigger: Activate an RSO if at least 5 members exist.
CREATE TRIGGER ActivateRSO
AFTER INSERT ON Students_RSOs
FOR EACH ROW
BEGIN
  IF (SELECT COUNT(*) FROM Students_RSOs WHERE rso_id = NEW.rso_id) >= 5 THEN
    UPDATE RSOs SET status = 'active' WHERE rso_id = NEW.rso_id;
  END IF;
END$$

-- Trigger: Deactivate an RSO if fewer than 5 members exist.
CREATE TRIGGER DeactivateRSO
AFTER DELETE ON Students_RSOs
FOR EACH ROW
BEGIN
  IF (SELECT COUNT(*) FROM Students_RSOs WHERE rso_id = OLD.rso_id) < 5 THEN
    UPDATE RSOs SET status = 'inactive' WHERE rso_id = OLD.rso_id;
  END IF;
END$$

-- (Optional) Trigger for RSO creation enforcement if using an intermediate table.
-- Note: This is based on your ER diagram’s note that RSO creation requires at least 5 members.
CREATE TRIGGER CheckRSOMembers
BEFORE INSERT ON RSOs
FOR EACH ROW
BEGIN
  -- This is a placeholder trigger.
  -- In a complete implementation, you might check that the new RSO will have at least five initial members.
  -- For example, you could query an associated temporary table or require the application logic to enforce it.
  IF (NEW.status = 'active') THEN
    IF ( (SELECT COUNT(*) FROM Students_RSOs WHERE rso_id = NEW.rso_id) < 5 ) THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'An RSO must have at least five members to be activated.';
    END IF;
  END IF;
END$$

DELIMITER ;
