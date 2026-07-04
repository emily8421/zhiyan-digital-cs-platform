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

export type ConversationData = {
  conversation_id: string;
  status: string;
  scenario_pack_code: string;
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
