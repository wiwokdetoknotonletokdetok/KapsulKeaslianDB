CREATE OR REPLACE FUNCTION update_follow_counts_on_insert()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users
    SET followers = followers + 1
    WHERE id = NEW.id_following;

    UPDATE users
    SET followings = followings + 1
    WHERE id = NEW.id_follower;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_follow_counts_on_delete()
RETURNS TRIGGER AS $$
    BEGIN
    UPDATE users
    SET followers = followers - 1
    WHERE id = OLD.id_following;

    UPDATE users
    SET followings = followings - 1
    WHERE id = OLD.id_follower;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_update_follow_counts_after_insert
AFTER INSERT ON follow
FOR EACH ROW
EXECUTE FUNCTION update_follow_counts_on_insert();


CREATE TRIGGER trg_update_follow_counts_after_delete
AFTER DELETE ON follow
FOR EACH ROW
EXECUTE FUNCTION update_follow_counts_on_delete();
