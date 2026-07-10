import { useEffect, useMemo, useState } from 'react';

import {
  ApiClientError,
  createMockNotification,
  getConsoleRole,
  getDailySummary,
  getScenarioPack,
  listConversations,
  listHandoffs,
  listKnowledgeGaps,
  listMockBusinessRecords,
  listMockNotifications,
  listScenarioPacks,
  setConsoleRole,
  updateHandoffStatus,
  updateKnowledgeGapStatus
} from '../../shared/apiClient';
import type { ConsoleRole } from '../../shared/apiClient';
import type {
  ConversationListItem,
  DailySummaryData,
  HandoffRecord,
  KnowledgeGapRecord,
  MockBusinessRecord,
  MockNotificationRecord,
  ScenarioPackDetail,
  ScenarioPackSummary
} from '../../shared/types';

type TabKey = 'overview' | 'conversations' | 'handoffs' | 'gaps' | 'notifications' | 'scenarios' | 'mockData';
type DetailRecord =
  | ConversationListItem
  | HandoffRecord
  | KnowledgeGapRecord
  | MockNotificationRecord
  | ScenarioPackSummary
  | MockBusinessRecord
  | ScenarioPackDetail
  | DailySummaryData
  | null;

type ConsoleState = {
  summary: DailySummaryData | null;
  conversations: ConversationListItem[];
  handoffs: HandoffRecord[];
  gaps: KnowledgeGapRecord[];
  notifications: MockNotificationRecord[];
  scenarioPacks: ScenarioPackSummary[];
  mockRecords: MockBusinessRecord[];
};

const tabs: Array<{ key: TabKey; label: string }> = [
  { key: 'overview', label: '概览' },
  { key: 'conversations', label: '会话' },
  { key: 'handoffs', label: '待跟进' },
  { key: 'gaps', label: '缺口' },
  { key: 'notifications', label: '通知' },
  { key: 'scenarios', label: '场景包' },
  { key: 'mockData', label: 'Mock 数据' }
];

const initialState: ConsoleState = {
  summary: null,
  conversations: [],
  handoffs: [],
  gaps: [],
  notifications: [],
  scenarioPacks: [],
  mockRecords: []
};

function filterByPack<T extends { scenario_pack_code?: string }>(records: T[], packCode: string): T[] {
  if (packCode === 'all') return records;
  return records.filter((record) => record.scenario_pack_code === packCode);
}

function App() {
  const [activeTab, setActiveTab] = useState<TabKey>('overview');
  const [data, setData] = useState<ConsoleState>(initialState);
  const [selected, setSelected] = useState<DetailRecord>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdatedAt, setLastUpdatedAt] = useState<string>('');
  const [role, setRole] = useState<ConsoleRole>(getConsoleRole);
  const [scenarioFilter, setScenarioFilter] = useState<string>('all');

  const canWrite = role === 'admin';

  function handleRoleChange(next: ConsoleRole) {
    setRole(next);
    setConsoleRole(next);
  }

  useEffect(() => {
    void refreshConsoleData();
  }, []);

  const visibleConversations = useMemo(
    () => filterByPack(data.conversations, scenarioFilter),
    [data.conversations, scenarioFilter]
  );
  const visibleHandoffs = useMemo(
    () => filterByPack(data.handoffs, scenarioFilter),
    [data.handoffs, scenarioFilter]
  );
  const visibleGaps = useMemo(() => filterByPack(data.gaps, scenarioFilter), [data.gaps, scenarioFilter]);
  const visibleMockRecords = useMemo(
    () => filterByPack(data.mockRecords, scenarioFilter),
    [data.mockRecords, scenarioFilter]
  );

  const activeCount = useMemo(() => {
    const counts: Record<TabKey, number> = {
      overview: data.summary ? 1 : 0,
      conversations: visibleConversations.length,
      handoffs: visibleHandoffs.length,
      gaps: visibleGaps.length,
      notifications: data.notifications.length,
      scenarios: data.scenarioPacks.length,
      mockData: visibleMockRecords.length
    };
    return counts[activeTab];
  }, [activeTab, data, visibleConversations, visibleHandoffs, visibleGaps, visibleMockRecords]);

  async function refreshConsoleData() {
    try {
      setIsLoading(true);
      setError(null);
      const [
        summaryResponse,
        conversationResponse,
        handoffResponse,
        gapResponse,
        notificationResponse,
        scenarioResponse,
        mockRecordResponse
      ] = await Promise.all([
        getDailySummary(),
        listConversations(),
        listHandoffs(),
        listKnowledgeGaps(),
        listMockNotifications(),
        listScenarioPacks(),
        listMockBusinessRecords()
      ]);
      setData({
        summary: summaryResponse.data,
        conversations: conversationResponse.data,
        handoffs: handoffResponse.data,
        gaps: gapResponse.data,
        notifications: notificationResponse.data,
        scenarioPacks: scenarioResponse.data,
        mockRecords: mockRecordResponse.data
      });
      setSelected(summaryResponse.data);
      setLastUpdatedAt(new Date().toLocaleString());
    } catch (caughtError) {
      setError(formatError(caughtError));
    } finally {
      setIsLoading(false);
    }
  }

  async function handleHandoffUpdate(record: HandoffRecord, status: string) {
    try {
      setIsUpdating(true);
      setError(null);
      const response = await updateHandoffStatus(record.handoff_id, status, 'Demo 控制台已更新处理状态。');
      setData((current) => ({
        ...current,
        handoffs: current.handoffs.map((item) => (item.handoff_id === record.handoff_id ? response.data : item))
      }));
      setSelected(response.data);
    } catch (caughtError) {
      setError(formatError(caughtError));
    } finally {
      setIsUpdating(false);
    }
  }

  async function handleGapUpdate(record: KnowledgeGapRecord, status: string) {
    try {
      setIsUpdating(true);
      setError(null);
      const response = await updateKnowledgeGapStatus(record.gap_id, status, 'Demo 控制台已更新缺口状态。');
      setData((current) => ({
        ...current,
        gaps: current.gaps.map((item) => (item.gap_id === record.gap_id ? response.data : item))
      }));
      setSelected(response.data);
    } catch (caughtError) {
      setError(formatError(caughtError));
    } finally {
      setIsUpdating(false);
    }
  }

  async function handleCreateNotification(eventType: string, relatedId: string) {
    try {
      setIsUpdating(true);
      setError(null);
      const response = await createMockNotification(eventType, relatedId);
      setData((current) => ({
        ...current,
        notifications: [response.data, ...current.notifications]
      }));
      setActiveTab('notifications');
      setSelected(response.data);
    } catch (caughtError) {
      setError(formatError(caughtError));
    } finally {
      setIsUpdating(false);
    }
  }

  async function handleScenarioSelect(pack: ScenarioPackSummary) {
    try {
      setIsUpdating(true);
      setError(null);
      const response = await getScenarioPack(pack.code);
      setSelected(response.data);
    } catch (caughtError) {
      setError(formatError(caughtError));
    } finally {
      setIsUpdating(false);
    }
  }

  return (
    <main className="page-shell">
      <header className="hero-card">
        <div>
          <p className="eyebrow">Demo 控制台</p>
          <h1>知衍数字客服运营台</h1>
          <p>查看会话、待跟进、知识缺口、Mock 通知和日报摘要；不接真实组织或生产数据。</p>
        </div>
        <div className="header-actions">
          <span className="demo-badge">Demo</span>
          <span className="demo-badge">Mock 数据</span>
          <div className="role-switch" role="group" aria-label="控制台角色（Demo）">
            <button
              type="button"
              className={role === 'admin' ? 'active' : ''}
              onClick={() => handleRoleChange('admin')}
            >
              管理员
            </button>
            <button
              type="button"
              className={role === 'viewer' ? 'active' : ''}
              onClick={() => handleRoleChange('viewer')}
            >
              只读
            </button>
          </div>
          <button onClick={refreshConsoleData} disabled={isLoading || isUpdating}>
            刷新
          </button>
        </div>
      </header>

      {error ? <section className="error-card">{error}</section> : null}

      <section className="toolbar-card">
        <nav className="tabs" aria-label="控制台导航">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              className={tab.key === activeTab ? 'active' : ''}
              onClick={() => {
                setActiveTab(tab.key);
                setSelected(tab.key === 'overview' ? data.summary : null);
              }}
            >
              {tab.label}
            </button>
          ))}
        </nav>
        <div className="filter-row">
          <label htmlFor="scenario-filter">当前演示场景包：</label>
          <select
            id="scenario-filter"
            value={scenarioFilter}
            onChange={(event) => setScenarioFilter(event.target.value)}
          >
            <option value="all">全部</option>
            {data.scenarioPacks.map((pack) => (
              <option key={pack.code} value={pack.code}>
                {pack.name}
              </option>
            ))}
          </select>
          {role === 'viewer' ? (
            <span className="hint-badge">只读模式：写操作已禁用（后端同样拦截）</span>
          ) : null}
        </div>
        <p>{isLoading ? '加载 Demo 数据中…' : `当前列表 ${activeCount} 条，最近刷新：${lastUpdatedAt || '待刷新'}`}</p>
      </section>

      <section className="content-grid">
        <div className="list-panel">
          {isLoading ? <EmptyState text="正在加载 Demo 控制台数据…" /> : null}
          {!isLoading && activeTab === 'overview' && data.summary ? (
            <Overview summary={data.summary} onSelect={setSelected} />
          ) : null}
          {!isLoading && activeTab === 'conversations' ? (
            <ConversationList records={visibleConversations} onSelect={setSelected} />
          ) : null}
          {!isLoading && activeTab === 'handoffs' ? (
            <HandoffList
              records={visibleHandoffs}
              isUpdating={isUpdating}
              canWrite={canWrite}
              onSelect={setSelected}
              onUpdate={handleHandoffUpdate}
              onNotify={handleCreateNotification}
            />
          ) : null}
          {!isLoading && activeTab === 'gaps' ? (
            <GapList
              records={visibleGaps}
              isUpdating={isUpdating}
              canWrite={canWrite}
              onSelect={setSelected}
              onUpdate={handleGapUpdate}
              onNotify={handleCreateNotification}
            />
          ) : null}
          {!isLoading && activeTab === 'notifications' ? (
            <NotificationList records={data.notifications} onSelect={setSelected} />
          ) : null}
          {!isLoading && activeTab === 'scenarios' ? (
            <ScenarioList records={data.scenarioPacks} onSelect={handleScenarioSelect} />
          ) : null}
          {!isLoading && activeTab === 'mockData' ? (
            <MockRecordList records={visibleMockRecords} onSelect={setSelected} />
          ) : null}
        </div>

        <aside className="detail-panel">
          <h2>右侧详情栏</h2>
          {selected ? <RecordDetail record={selected} /> : <EmptyState text="请选择左侧记录查看详情。" />}
        </aside>
      </section>
    </main>
  );
}

function Overview({ summary, onSelect }: { summary: DailySummaryData; onSelect: (record: DetailRecord) => void }) {
  const cards = [
    ['会话数', summary.conversation_count],
    ['自动回答', summary.auto_answer_count],
    ['转人工', summary.handoff_count],
    ['知识缺口', summary.gap_count],
    ['未结案', summary.open_item_count],
    ['通知', summary.notification_count]
  ];
  return (
    <div className="summary-grid">
      {cards.map(([label, value]) => (
        <button key={label} className="summary-card" onClick={() => onSelect(summary)}>
          <span>{label}</span>
          <strong>{value}</strong>
        </button>
      ))}
      <article className="wide-card" onClick={() => onSelect(summary)}>
        <MockBadge mock={summary.mock} />
        <h3>{summary.summary_date} 日报摘要</h3>
        <p>{summary.content}</p>
      </article>
    </div>
  );
}

function ConversationList({ records, onSelect }: { records: ConversationListItem[]; onSelect: (record: DetailRecord) => void }) {
  if (!records.length) return <EmptyState text="暂无演示会话数据。" />;
  return (
    <div className="record-list">
      {records.map((record) => (
        <article key={record.conversation_id} className="record-card" onClick={() => onSelect(record)}>
          <div className="record-title">
            <h3>{record.conversation_id}</h3>
            <StatusBadge label={record.status} tone={record.risk_level === 'high' ? 'danger' : 'default'} />
          </div>
          <p>{record.last_message}</p>
          <MetaRow values={[record.scenario_pack_code, record.risk_level, record.updated_at]} mock={record.mock} />
        </article>
      ))}
    </div>
  );
}

function HandoffList({
  records,
  isUpdating,
  canWrite,
  onSelect,
  onUpdate,
  onNotify
}: {
  records: HandoffRecord[];
  isUpdating: boolean;
  canWrite: boolean;
  onSelect: (record: DetailRecord) => void;
  onUpdate: (record: HandoffRecord, status: string) => void;
  onNotify: (eventType: string, relatedId: string) => void;
}) {
  if (!records.length) return <EmptyState text="暂无待跟进 Demo 数据。" />;
  return (
    <div className="record-list">
      {records.map((record) => (
        <article key={record.handoff_id} className="record-card" onClick={() => onSelect(record)}>
          <div className="record-title">
            <h3>{record.reason}</h3>
            <StatusBadge label={record.status} tone={record.risk_level === 'high' ? 'danger' : 'default'} />
          </div>
          <p>{record.summary}</p>
          <MetaRow values={[record.suggested_owner, record.conversation_id, record.updated_at]} mock={record.mock} />
          <div className="action-row" onClick={(event) => event.stopPropagation()}>
            <button disabled={isUpdating || !canWrite} onClick={() => onUpdate(record, 'processing')}>
              标记处理中
            </button>
            <button disabled={isUpdating || !canWrite} onClick={() => onUpdate(record, 'closed')}>
              标记已关闭
            </button>
            <button
              className="secondary"
              disabled={isUpdating || !canWrite}
              onClick={() => onNotify('handoff', record.handoff_id)}
            >
              生成通知
            </button>
          </div>
        </article>
      ))}
    </div>
  );
}

function GapList({
  records,
  isUpdating,
  canWrite,
  onSelect,
  onUpdate,
  onNotify
}: {
  records: KnowledgeGapRecord[];
  isUpdating: boolean;
  canWrite: boolean;
  onSelect: (record: DetailRecord) => void;
  onUpdate: (record: KnowledgeGapRecord, status: string) => void;
  onNotify: (eventType: string, relatedId: string) => void;
}) {
  if (!records.length) return <EmptyState text="暂无知识缺口 Demo 数据。" />;
  return (
    <div className="record-list">
      {records.map((record) => (
        <article key={record.gap_id} className="record-card" onClick={() => onSelect(record)}>
          <div className="record-title">
            <h3>{record.question}</h3>
            <StatusBadge label={record.status} />
          </div>
          <MetaRow values={[record.scenario_pack_code, ...record.tags, record.updated_at]} mock={record.mock} />
          <div className="action-row" onClick={(event) => event.stopPropagation()}>
            {['reviewing', 'accepted', 'rejected', 'closed'].map((status) => (
              <button key={status} disabled={isUpdating || !canWrite} onClick={() => onUpdate(record, status)}>
                {status}
              </button>
            ))}
            <button
              className="secondary"
              disabled={isUpdating || !canWrite}
              onClick={() => onNotify('knowledge_gap', record.gap_id)}
            >
              生成通知
            </button>
          </div>
        </article>
      ))}
    </div>
  );
}

function NotificationList({ records, onSelect }: { records: MockNotificationRecord[]; onSelect: (record: DetailRecord) => void }) {
  if (!records.length) return <EmptyState text="暂无 Mock 通知记录。" />;
  return (
    <div className="record-list">
      {records.map((record) => (
        <article key={record.notification_id} className="record-card" onClick={() => onSelect(record)}>
          <div className="record-title">
            <h3>{record.event_type}</h3>
            <StatusBadge label={record.send_status} />
          </div>
          <p>{record.related_id}</p>
          <MetaRow values={[record.target_type, record.created_at]} mock={record.mock} />
        </article>
      ))}
    </div>
  );
}

function ScenarioList({ records, onSelect }: { records: ScenarioPackSummary[]; onSelect: (record: ScenarioPackSummary) => void }) {
  if (!records.length) return <EmptyState text="暂无场景包数据。" />;
  return (
    <div className="record-list">
      {records.map((record) => (
        <article key={record.code} className="record-card" onClick={() => onSelect(record)}>
          <div className="record-title">
            <h3>{record.name}</h3>
            <StatusBadge label={record.code} />
          </div>
          <p>{record.description}</p>
          <MetaRow
            values={[
              `知识 ${record.knowledge_count}`,
              `规则 ${record.rule_count}`,
              `Mock ${record.mock_business_count}`
            ]}
          />
        </article>
      ))}
    </div>
  );
}

function MockRecordList({ records, onSelect }: { records: MockBusinessRecord[]; onSelect: (record: DetailRecord) => void }) {
  if (!records.length) return <EmptyState text="暂无 Mock 业务数据。" />;
  return (
    <div className="record-list">
      {records.map((record) => (
        <article key={`${record.record_type}-${record.external_ref}`} className="record-card" onClick={() => onSelect(record)}>
          <div className="record-title">
            <h3>{record.external_ref}</h3>
            <StatusBadge label={record.status} />
          </div>
          <p>{record.summary}</p>
          <MetaRow values={[record.record_type, record.scenario_pack_code, record.eta ?? '无 ETA']} mock={record.mock} />
        </article>
      ))}
    </div>
  );
}

function RecordDetail({ record }: { record: Exclude<DetailRecord, null> }) {
  return (
    <div className="detail-body">
      <MockBadge mock={Boolean('mock' in record && record.mock)} />
      <pre>{JSON.stringify(record, null, 2)}</pre>
    </div>
  );
}

function MetaRow({ values, mock }: { values: Array<string | number>; mock?: boolean }) {
  return (
    <div className="meta-row">
      {values.filter(Boolean).map((value) => (
        <span key={String(value)}>{value}</span>
      ))}
      {mock ? <MockBadge mock={mock} /> : null}
    </div>
  );
}

function StatusBadge({ label, tone = 'default' }: { label: string; tone?: 'default' | 'danger' }) {
  return <span className={`status-badge ${tone}`}>{label}</span>;
}

function MockBadge({ mock }: { mock: boolean }) {
  return mock ? <span className="mock-badge">Mock</span> : null;
}

function EmptyState({ text }: { text: string }) {
  return <div className="empty-state">{text}</div>;
}

function formatError(error: unknown): string {
  if (error instanceof ApiClientError) {
    return `${error.code}：${error.message}`;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return '未知错误，请稍后重试。';
}

export default App;
