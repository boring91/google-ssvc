--+migrate-no-transaction
ALTER TABLE tasks
    ADD COLUMN data JSONB
