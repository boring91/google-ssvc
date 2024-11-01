CREATE TABLE ssvc_results
(
    id            UUID PRIMARY KEY     DEFAULT gen_random_uuid(),
    created_time  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified_time TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cve_id        VARCHAR(32) NOT NULL,
    result        TEXT        NOT NULL
);

CREATE UNIQUE INDEX ix_ssvc_results_cve_id ON ssvc_results (cve_id);

CREATE TRIGGER ssvc_results_modified_time
    BEFORE UPDATE
    ON ssvc_results
    FOR EACH ROW
EXECUTE FUNCTION update_modified_column();