from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TRIGGER CheckEventOverlap
            BEFORE INSERT ON Events
            FOR EACH ROW
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM Events
                    WHERE lname = NEW.lname
                    AND event_date = NEW.event_date
                    AND (NEW.end_time > start_time AND NEW.start_time < end_time)
                ) THEN
                    SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'Overlapping event at the same location/time!';
                END IF;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS CheckEventOverlap;"
        ),
        migrations.RunSQL(
            """
            CREATE TRIGGER ActivateRSO
            AFTER INSERT ON Students_RSOs
            FOR EACH ROW
            BEGIN
                IF (SELECT COUNT(*) FROM Students_RSOs WHERE rso_id = NEW.rso_id) >= 5 THEN
                    UPDATE RSOs SET status = 'active' WHERE rso_id = NEW.rso_id;
                END IF;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS ActivateRSO;"
        ),
        migrations.RunSQL(
            """
            CREATE TRIGGER DeactivateRSO
            AFTER DELETE ON Students_RSOs
            FOR EACH ROW
            BEGIN
                IF (SELECT COUNT(*) FROM Students_RSOs WHERE rso_id = OLD.rso_id) < 5 THEN
                    UPDATE RSOs SET status = 'inactive' WHERE rso_id = OLD.rso_id;
                END IF;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS DeactivateRSO;"
        ),
        migrations.RunSQL(
            """
            CREATE TRIGGER CheckRSOMembers
            BEFORE INSERT ON RSOs
            FOR EACH ROW
            BEGIN
                IF NEW.status = 'active' THEN
                    IF (SELECT COUNT(*) FROM Students_RSOs WHERE rso_id = NEW.rso_id) < 5 THEN
                        SIGNAL SQLSTATE '45000'
                        SET MESSAGE_TEXT = 'An RSO must have at least five members to be activated.';
                    END IF;
                END IF;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS CheckRSOMembers;"
        ),
    ]
