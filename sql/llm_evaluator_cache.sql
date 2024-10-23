CREATE TABLE llm_evaluator_cache
(
    id             UUID PRIMARY KEY     DEFAULT gen_random_uuid(),
    created_time   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified_time  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    llm            VARCHAR(16) NOT NULL,
    cve_id         VARCHAR(32) NOT NULL,
    decision_point VARCHAR(64) NOT NULL,
    data           TEXT
);

CREATE INDEX idx_llm_evaluator_cache_cve_id ON llm_evaluator_cache (cve_id);
CREATE UNIQUE INDEX idx_llm_evaluator_cache_llm_cve_id_decision_point ON llm_evaluator_cache (llm, cve_id, decision_point);

CREATE TRIGGER llm_evaluator_cache_update_modified_time
    BEFORE UPDATE
    ON llm_evaluator_cache
    FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
