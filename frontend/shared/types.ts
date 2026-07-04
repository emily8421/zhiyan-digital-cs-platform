export type ApiResponse<T> = {
  request_id: string;
  data: T;
  meta: {
    mock: boolean;
  };
};

export type ApiErrorResponse = {
  request_id: string;
  error: {
    code: string;
    message: string;
    details: Record<string, unknown>;
  };
};

export type ScenarioPackSummary = {
  code: string;
  name: string;
  description: string;
  source_refs: string[];
  knowledge_count: number;
  rule_count: number;
  mock_business_count: number;
  demo_questions: string[];
};

export type ScenarioPackDetail = {
  code: string;
  name: string;
  description: string;
  source_refs: string[];
  demo_questions: string[];
  intents: Array<{
    code: string;
    name: string;
    examples: string[];
  }>;
  knowledge_items: Array<{
    id: string;
    title: string;
    content: string;
    source_ref: string;
  }>;
  rule_items: Array<{
    id: string;
    rule_type: string;
    pattern: string;
    action: string;
    source_ref: string;
  }>;
  mock_business_records: Array<{
    record_type: string;
    external_ref: string;
    status: string;
    summary: string;
    next_step: string;
    eta: string | null;
    is_mock: boolean;
  }>;
  handoff_rules: Array<{
    code: string;
    description: string;
  }>;
};

export type ConversationData = {
  conversation_id: string;
  channel: string;
  scenario_pack_code: string;
  status: string;
  risk_level: string;
  last_message: string;
  customer_alias: string | null;
  updated_at: string;
  mock: boolean;
};

export type ConversationListItem = {
  conversation_id: string;
  channel: string;
  scenario_pack_code: string;
  status: string;
  risk_level: string;
  last_message: string;
  updated_at: string;
  mock: boolean;
};

export type MessageResponseData = {
  message_id: string;
  intent: string;
  answer_type: string;
  answer: string;
  source_ref: string;
  handoff: Record<string, unknown> | null;
  knowledge_gap: Record<string, unknown> | null;
};

export type HandoffRecord = {
  handoff_id: string;
  conversation_id: string;
  scenario_pack_code: string;
  reason: string;
  suggested_owner: string;
  status: string;
  risk_level: string;
  summary: string;
  resolution_note: string | null;
  updated_at: string;
  mock: boolean;
};

export type KnowledgeGapRecord = {
  gap_id: string;
  conversation_id: string;
  scenario_pack_code: string;
  question: string;
  tags: string[];
  status: string;
  resolution_note: string | null;
  updated_at: string;
  mock: boolean;
};

export type MockNotificationRecord = {
  notification_id: string;
  event_type: string;
  related_id: string;
  target_type: string;
  payload: Record<string, unknown>;
  send_status: string;
  created_at: string;
  mock: boolean;
};

export type DailySummaryData = {
  summary_date: string;
  conversation_count: number;
  auto_answer_count: number;
  handoff_count: number;
  gap_count: number;
  open_item_count: number;
  notification_count: number;
  content: string;
  mock: boolean;
};

export type MockBusinessRecord = {
  record_type: string;
  external_ref: string;
  scenario_pack_code: string;
  status: string;
  summary: string;
  next_step: string;
  eta: string | null;
  mock: boolean;
};
