-- --------------------------------------------------------------------------------
-- Routine DDL
-- Note: comments before and after the routine body will not be stored by the server
-- --------------------------------------------------------------------------------
DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `enroll`(studid INT, subjid INT)
BEGIN
    DECLARE no_more_products INT DEFAULT 0;
    DECLARE prd_date VARCHAR(10);
    DECLARE pyear INT;
    DECLARE pmonth INT;
    DECLARE pday INT;
    DECLARE expired BOOLEAN DEFAULT FALSE;

    DECLARE cur_sched CURSOR FOR
        SELECT sched FROM subjects WHERE subjid = subjid;

    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET no_more_products = 1;

    OPEN cur_sched;

    FETCH cur_sched INTO prd_date;

    REPEAT
        -- Extract year, month, and day from expiration date
        SET pyear = LEFT(prd_date, 4);
        SET pmonth = SUBSTRING(prd_date, 6, 2);
        SET pday = SUBSTRING(prd_date, 9, 2);

        -- Check if the product is expired
        IF pyear < YEAR(NOW()) THEN
		  SET expired = TRUE;
        elseif pyear = YEAR(NOW()) and pmonth <= MONTH(NOW())  THEN
		  SET expired = TRUE;
        END IF;


        -- If the product is not expired, insert the order
        IF NOT expired THEN
            INSERT INTO enroll (studid, subjid) VALUES (studid, subjid);
        END IF;

        FETCH cur_sched INTO prd_date;

    UNTIL no_more_products = 1
    END REPEAT;

    CLOSE cur_sched;

END
