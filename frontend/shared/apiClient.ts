import type {
  ApiErrorResponse,
  ApiResponse,
  ConversationData,
  MessageResponseData,
  ScenarioPackSummary
} from './types';

const API_BASE = '/api/v1';

export class ApiClientError extends Error {
  readonly code: string;
  readonly requestId: string;
  readonly details: Record<string, unknown>;

  constructor(response: ApiErrorResponse) {
    super(response.error.message);
    this.name = 'ApiClientError';
    this.code = response.error.code;
    this.requestId = response.request_id;
    this.details = response.error.details;
  }
}

async function requestJson<T>(path: string, options?: RequestInit): Promise<ApiResponse<T>> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {})
    },
    ...options
  });
  const body = await response.json();
  if (!response.ok) {
    throw new ApiClientError(body as ApiErrorResponse);
  }
  return body as ApiResponse<T>;
}

export function listScenarioPacks(): Promise<ApiResponse<ScenarioPackSummary[]>> {
  return requestJson<ScenarioPackSummary[]>('/scenario-packs');
}

export function createConversation(scenarioPackCode: string): Promise<ApiResponse<ConversationData>> {
  return requestJson<ConversationData>('/conversations', {
    method: 'POST',
    body: JSON.stringify({
      channel: 'h5',
      scenario_pack_code: scenarioPackCode,
      customer_alias: 'demo_customer'
    })
  });
}

export function sendMessage(
  conversationId: string,
  content: string
): Promise<ApiResponse<MessageResponseData>> {
  return requestJson<MessageResponseData>(`/conversations/${conversationId}/messages`, {
    method: 'POST',
    body: JSON.stringify({ content })
  });
}
