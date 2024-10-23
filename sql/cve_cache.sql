CREATE TABLE cve_cache
(
    id            UUID PRIMARY KEY      DEFAULT gen_random_uuid(),
    created_time  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified_time TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cve_id        VARCHAR(32)  NOT NULL,
    source        VARCHAR(128) NOT NULL,
    data          TEXT
);
CREATE INDEX idx_cve_cache_cve_id ON cve_cache (cve_id);
CREATE UNIQUE INDEX idx_cve_cache_cve_id_source ON cve_cache (cve_id, source);


CREATE TRIGGER cve_cache_update_modified_time
    BEFORE UPDATE
    ON cve_cache
    FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
