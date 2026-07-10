CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS zycs_scenario_packs (
  id text PRIMARY KEY,
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text NOT NULL DEFAULT '',
  status text NOT NULL DEFAULT 'active',
  source_ref text NOT NULL DEFAULT '',
  is_mock boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_scenario_packs_status_check CHECK (status IN ('draft', 'active', 'archived'))
);

CREATE TABLE IF NOT EXISTS zycs_conversations (
  id text PRIMARY KEY,
  channel text NOT NULL DEFAULT 'h5',
  scenario_pack_id text REFERENCES zycs_scenario_packs(id),
  customer_alias text,
  status text NOT NULL DEFAULT 'open',
  risk_level text NOT NULL DEFAULT 'low',
  is_mock boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_conversations_status_check CHECK (status IN ('open', 'handoff', 'closed')),
  CONSTRAINT zycs_conversations_risk_level_check CHECK (risk_level IN ('low', 'medium', 'high'))
);

CREATE TABLE IF NOT EXISTS zycs_messages (
  id text PRIMARY KEY,
  conversation_id text REFERENCES zycs_conversations(id) ON DELETE CASCADE,
  sender_type text NOT NULL,
  content text NOT NULL,
  intent text,
  answer_type text,
  source_ref text,
  is_mock boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_messages_sender_type_check CHECK (sender_type IN ('customer', 'assistant', 'staff', 'system')),
  CONSTRAINT zycs_messages_answer_type_check CHECK (answer_type IS NULL OR answer_type IN ('knowledge', 'rule', 'mock_business', 'handoff', 'gap'))
);

CREATE TABLE IF NOT EXISTS zycs_knowledge_items (
  id text PRIMARY KEY,
  scenario_pack_id text REFERENCES zycs_scenario_packs(id),
  title text NOT NULL,
  content text NOT NULL,
  tags jsonb NOT NULL DEFAULT '[]'::jsonb,
  source_ref text NOT NULL,
  status text NOT NULL DEFAULT 'active',
  embedding vector(3),
  is_mock boolean NOT NULL DEFAULT true,
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_knowledge_items_status_check CHECK (status IN ('draft', 'active', 'archived'))
);

CREATE TABLE IF NOT EXISTS zycs_rule_items (
  id text PRIMARY KEY,
  scenario_pack_id text REFERENCES zycs_scenario_packs(id),
  rule_type text NOT NULL,
  pattern text NOT NULL,
  action text NOT NULL,
  response_template text,
  priority integer NOT NULL DEFAULT 100,
  source_ref text NOT NULL,
  enabled boolean NOT NULL DEFAULT true,
  CONSTRAINT zycs_rule_items_action_check CHECK (action IN ('answer', 'handoff', 'gap', 'mock_lookup'))
);

CREATE TABLE IF NOT EXISTS zycs_mock_business_records (
  id text PRIMARY KEY,
  scenario_pack_id text REFERENCES zycs_scenario_packs(id),
  record_type text NOT NULL,
  external_ref text NOT NULL,
  status text NOT NULL,
  summary text NOT NULL,
  next_step text NOT NULL DEFAULT '',
  eta text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  is_mock boolean NOT NULL DEFAULT true,
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_mock_business_records_type_check CHECK (record_type IN ('order', 'project', 'ticket')),
  CONSTRAINT zycs_mock_business_records_mock_check CHECK (is_mock = true),
  CONSTRAINT zycs_mock_business_records_ref_unique UNIQUE (record_type, external_ref)
);

CREATE TABLE IF NOT EXISTS zycs_human_handoffs (
  id text PRIMARY KEY,
  conversation_id text REFERENCES zycs_conversations(id) ON DELETE SET NULL,
  reason text NOT NULL,
  risk_level text NOT NULL DEFAULT 'medium',
  suggested_owner text NOT NULL DEFAULT 'staff',
  status text NOT NULL DEFAULT 'open',
  source_message_id text REFERENCES zycs_messages(id) ON DELETE SET NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_human_handoffs_status_check CHECK (status IN ('open', 'processing', 'closed')),
  CONSTRAINT zycs_human_handoffs_risk_level_check CHECK (risk_level IN ('low', 'medium', 'high'))
);

CREATE TABLE IF NOT EXISTS zycs_knowledge_gaps (
  id text PRIMARY KEY,
  conversation_id text REFERENCES zycs_conversations(id) ON DELETE SET NULL,
  question text NOT NULL,
  suggested_tags jsonb NOT NULL DEFAULT '[]'::jsonb,
  status text NOT NULL DEFAULT 'new',
  resolution_note text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_knowledge_gaps_status_check CHECK (status IN ('new', 'reviewing', 'accepted', 'rejected', 'closed'))
);

CREATE TABLE IF NOT EXISTS zycs_notifications (
  id text PRIMARY KEY,
  target_type text NOT NULL DEFAULT 'feishu',
  event_type text NOT NULL,
  related_id text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  send_status text NOT NULL DEFAULT 'mocked',
  is_mock boolean NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_notifications_target_type_check CHECK (target_type IN ('feishu', 'console', 'log')),
  CONSTRAINT zycs_notifications_event_type_check CHECK (event_type IN ('handoff', 'knowledge_gap', 'summary')),
  CONSTRAINT zycs_notifications_send_status_check CHECK (send_status IN ('mocked', 'pending', 'sent', 'failed'))
);

CREATE TABLE IF NOT EXISTS zycs_daily_summaries (
  id text PRIMARY KEY,
  summary_date date NOT NULL,
  scenario_pack_id text REFERENCES zycs_scenario_packs(id),
  conversation_count integer NOT NULL DEFAULT 0,
  handoff_count integer NOT NULL DEFAULT 0,
  gap_count integer NOT NULL DEFAULT 0,
  open_item_count integer NOT NULL DEFAULT 0,
  content text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_daily_summaries_counts_check CHECK (
    conversation_count >= 0 AND handoff_count >= 0 AND gap_count >= 0 AND open_item_count >= 0
  )
);

CREATE TABLE IF NOT EXISTS zycs_audit_logs (
  id text PRIMARY KEY,
  request_id text,
  actor_type text NOT NULL DEFAULT 'system',
  action text NOT NULL,
  resource_type text NOT NULL,
  resource_id text,
  safe_detail jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT zycs_audit_logs_actor_type_check CHECK (actor_type IN ('customer', 'staff', 'system'))
);

CREATE INDEX IF NOT EXISTS idx_zycs_conversations_status_updated_at ON zycs_conversations(status, updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_zycs_messages_conversation_created_at ON zycs_messages(conversation_id, created_at);
CREATE INDEX IF NOT EXISTS idx_zycs_knowledge_items_pack_status ON zycs_knowledge_items(scenario_pack_id, status);
CREATE INDEX IF NOT EXISTS idx_zycs_rule_items_type_enabled_priority ON zycs_rule_items(rule_type, enabled, priority);
CREATE INDEX IF NOT EXISTS idx_zycs_mock_business_records_type_ref ON zycs_mock_business_records(record_type, external_ref);
CREATE INDEX IF NOT EXISTS idx_zycs_human_handoffs_status_risk_updated_at ON zycs_human_handoffs(status, risk_level, updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_zycs_knowledge_gaps_status_updated_at ON zycs_knowledge_gaps(status, updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_zycs_notifications_event_status_created_at ON zycs_notifications(event_type, send_status, created_at DESC);

