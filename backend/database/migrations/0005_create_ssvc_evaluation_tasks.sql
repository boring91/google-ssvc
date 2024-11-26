CREATE TABLE tasks
(
    id            UUID PRIMARY KEY     DEFAULT gen_random_uuid(),
    created_time  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified_time TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status        VARCHAR(32) NOT NULL DEFAULT 'queued',
    type          VARCHAR(32) NOT NULL
);

CREATE TABLE ssvc_result_task_links
(
    id           UUID PRIMARY KEY     DEFAULT gen_random_uuid(),
    created_time TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    task_id      UUID        NOT NULL REFERENCES tasks (id) ON DELETE CASCADE,
    result_id    UUID REFERENCES ssvc_results (id) ON DELETE CASCADE,
    cve_id          VARCHAR(32) NOT NULL,
    notes        VARCHAR
);

CREATE TRIGGER tasks_modified_time
    BEFORE UPDATE
    ON tasks
    FOR EACH ROW
EXECUTE FUNCTION update_modified_column()