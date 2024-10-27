CREATE
    OR REPLACE FUNCTION update_modified_column()
    RETURNS TRIGGER AS
$$
BEGIN
    new.modified_time
        = CURRENT_TIMESTAMP;
    RETURN new;
END;
$$
    LANGUAGE plpgsql;