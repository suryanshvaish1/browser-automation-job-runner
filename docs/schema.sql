CREATE TABLE jobs (

    id SERIAL PRIMARY KEY,

    job_id UUID UNIQUE NOT NULL,

    url TEXT NOT NULL,

    goal TEXT NOT NULL,

    status VARCHAR(50) NOT NULL,

    result JSONB,

    error TEXT,

    logs JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);