import type {
  ApiErrorResponse,
  ApiResponse,
  ConversationData,
  ConversationListItem,
  DailySummaryData,
  HandoffRecord,
  KnowledgeGapRecord,
  MessageResponseData,
  MockBusinessRecord,
  MockNotificationRecord,
  ScenarioPackDetail,
  ScenarioPackSummary
} from './types';

const API_BASE = '/api/v1';

const CONSOLE_ROLE_KEY = 'zycs_console_role';

export type ConsoleRole = 'admin' | 'viewer';

export function getConsoleRole(): ConsoleRole {
  const stored = localStorage.getItem(CONSOLE_ROLE_KEY);
  return stored === 'admin' ? 'admin' : 'viewer';
}

export function setConsoleRole(role: ConsoleRole): void {
  localStorage.setItem(CONSOLE_ROLE_KEY, role);
}

function consoleRoleHeader(): Record<string, string> {
  return { 'X-Console-Role': getConsoleRole() };
}

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
  const { headers: optionHeaders, ...rest } = options ?? {};
  const response = await fetch(`${API_BASE}${path}`, {
    ...rest,
    headers: {
      'Content-Type': 'application/json',
      ...((optionHeaders as Record<string, string> | undefined) ?? {})
    }
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

export function getScenarioPack(scenarioPackCode: string): Promise<ApiResponse<ScenarioPackDetail>> {
  return requestJson<ScenarioPackDetail>(`/scenario-packs/${scenarioPackCode}`);
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

export function listConversations(): Promise<ApiResponse<ConversationListItem[]>> {
  return requestJson<ConversationListItem[]>('/conversations');
}

export function listHandoffs(): Promise<ApiResponse<HandoffRecord[]>> {
  return requestJson<HandoffRecord[]>('/handoffs');
}

export function updateHandoffStatus(
  handoffId: string,
  status: string,
  resolutionNote: string
): Promise<ApiResponse<HandoffRecord>> {
  return requestJson<HandoffRecord>(`/handoffs/${handoffId}`, {
    method: 'PATCH',
    headers: consoleRoleHeader(),
    body: JSON.stringify({ status, resolution_note: resolutionNote })
  });
}

export function listKnowledgeGaps(): Promise<ApiResponse<KnowledgeGapRecord[]>> {
  return requestJson<KnowledgeGapRecord[]>('/knowledge-gaps');
}

export function updateKnowledgeGapStatus(
  gapId: string,
  status: string,
  resolutionNote: string
): Promise<ApiResponse<KnowledgeGapRecord>> {
  return requestJson<KnowledgeGapRecord>(`/knowledge-gaps/${gapId}`, {
    method: 'PATCH',
    headers: consoleRoleHeader(),
    body: JSON.stringify({ status, resolution_note: resolutionNote })
  });
}

export function listMockNotifications(): Promise<ApiResponse<MockNotificationRecord[]>> {
  return requestJson<MockNotificationRecord[]>('/notifications/mock');
}

export function createMockNotification(
  eventType: string,
  relatedId: string
): Promise<ApiResponse<MockNotificationRecord>> {
  return requestJson<MockNotificationRecord>('/notifications/mock', {
    method: 'POST',
    headers: consoleRoleHeader(),
    body: JSON.stringify({ event_type: eventType, related_id: relatedId, target_type: 'feishu' })
  });
}

export function getDailySummary(): Promise<ApiResponse<DailySummaryData>> {
  return requestJson<DailySummaryData>('/summaries/daily');
}

export function listMockBusinessRecords(): Promise<ApiResponse<MockBusinessRecord[]>> {
  return requestJson<MockBusinessRecord[]>('/mock-business');
}
