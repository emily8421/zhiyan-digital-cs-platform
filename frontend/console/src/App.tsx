import { useEffect, useMemo, useState, type FormEvent } from 'react';

import {
  ApiClientError,
  createKnowledgeItem,
  createMockNotification,
  getConsoleRole,
  getDailySummary,
  getScenarioPack,
  getScenarioPackSourceMode,
  listConversations,
  listHandoffs,
  listKnowledgeGaps,
  listKnowledgeItems,
  listMockBusinessRecords,
  listMockNotifications,
  listScenarioPacks,
  setConsoleRole,
  updateHandoffStatus,
  updateKnowledgeItemStatus,
  updateKnowledgeGapStatus,
  updateScenarioPackSourceMode
} from '../../shared/apiClient';
import type { ConsoleRole } from '../../shared/apiClient';
import type {
  ConversationListItem,
  DailySummaryData,
  HandoffRecord,
  KnowledgeGapRecord,
  KnowledgeItemRecord,
  MockBusinessRecord,
  MockNotificationRecord,
  ScenarioPackDetail,
  ScenarioPackSummary,
  SourceModeData
} from '../../shared/types';

type TabKey = 'overview' | 'conversations' | 'handoffs' | 'gaps' | 'knowledgeItems' | 'notifications' | 'scenarios' | 'mockData';
type DetailRecord =
  | ConversationListItem
  | HandoffRecord
  | KnowledgeGapRecord
  | KnowledgeItemRecord
  | MockNotificationRecord
  | ScenarioPackSummary
  | MockBusinessRecord
  | ScenarioPackDetail
  | DailySummaryData
  | null;

type EvidenceTone = 'default' | 'danger' | 'success' | 'neutral';

type EvidenceItem = {
  label: string;
  value: string;
  tone?: EvidenceTone;
};

type ConsoleState = {
  summary: DailySummaryData | null;
  conversations: ConversationListItem[];
  handoffs: HandoffRecord[];
  gaps: KnowledgeGapRecord[];
  knowledgeItems: KnowledgeItemRecord[];
  notifications: MockNotificationRecord[];
  scenarioPacks: ScenarioPackSummary[];
  mockRecords: MockBusinessRecord[];
};

const tabs: Array<{ key: TabKey; label: string }> = [
  { key: 'overview', label: '概览' },
  { key: 'conversations', label: '会话' },
  { key: 'handoffs', label: '待跟进' },
  { key: 'gaps', label: '缺口' },
  { key: 'knowledgeItems', label: '知识条目' },
  { key: 'notifications', label: '通知' },
  { key: 'scenarios', label: '场景包' },
  { key: 'mockData', label: 'Mock 数据' }
];

const initialState: ConsoleState = {
  summary: null,
  conversations: [],
  handoffs: [],
  gaps: [],
  knowledgeItems: [],
  notifications: [],
  scenarioPacks: [],
  mockRecords: []
};

function filterByPack<T extends { scenario_pack_code?: string }>(records: T[], packCode: string): T[] {
  if (packCode === 'all') return records;
  return records.filter((record) => record.scenario_pack_code === packCode);
}

function getRecordValue(record: Exclude<DetailRecord, null>, key: string): unknown {
  return (record as Record<string, unknown>)[key];
}

function getTextValue(record: Exclude<DetailRecord, null>, key: string): string | null {
  const value = getRecordValue(record, key);
  return typeof value === 'string' && value.trim() ? value : null;
}

function getMockValue(record: Exclude<DetailRecord, null>): boolean {
  const mockValue = getRecordValue(record, 'mock') ?? getRecordValue(record, 'is_mock');
  return mockValue === true;
}

function formatEnvironment(environment: string): string {
  if (environment === 'demo_sandbox') return 'Demo Sandbox';
  return environment;
}

function buildEvidenceItems(record: Exclude<DetailRecord, null>): EvidenceItem[] {
  const items: EvidenceItem[] = [];
  const isMock = getMockValue(record);
  const environment = getTextValue(record, 'environment');
  const sourceSystem = getTextValue(record, 'source_system');
  const sourceRef = getTextValue(record, 'source_ref');
  const scenarioPackCode = getTextValue(record, 'scenario_pack_code') ?? getTextValue(record, 'code');
  const answerType = getTextValue(record, 'answer_type');
  const sourceRefsValue = getRecordValue(record, 'source_refs');

  if (isMock) {
    items.push({ label: '数据口径', value: 'Mock / Demo 数据', tone: 'success' });
  }
  if (environment) {
    items.push({ label: 'environment', value: formatEnvironment(environment), tone: 'neutral' });
  }
  if (sourceSystem) {
    items.push({ label: 'source_system', value: sourceSystem, tone: 'neutral' });
  }
  if (sourceRef) {
    items.push({ label: 'source_ref', value: sourceRef, tone: 'default' });
  }
  if (Array.isArray(sourceRefsValue) && sourceRefsValue.length) {
    items.push({ label: 'source_refs', value: sourceRefsValue.map(String).join(' / '), tone: 'default' });
  }
  if (scenarioPackCode) {
    items.push({ label: '场景包', value: scenarioPackCode, tone: 'neutral' });
  }
  if (answerType) {
    items.push({ label: 'answer_type', value: answerType, tone: answerType === 'handoff' ? 'danger' : 'default' });
  }

  return items;
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
  const [sourceMode, setSourceMode] = useState<SourceModeData | null>(null);
  const [sourceModeLoading, setSourceModeLoading] = useState(false);

  const canWrite = role === 'admin';

  const sourceModePack =
    scenarioFilter !== 'all'
      ? scenarioFilter
      : data.scenarioPacks[0]?.code ?? 'product_business';

  function handleRoleChange(next: ConsoleRole) {
    setRole(next);
    setConsoleRole(next);
  }

  useEffect(() => {
    void refreshConsoleData();
  }, []);

  useEffect(() => {
    if (!sourceModePack) return;
    void refreshSourceMode(sourceModePack);
  }, [sourceModePack]);

  const visibleConversations = useMemo(
    () => filterByPack(data.conversations, scenarioFilter),
    [data.conversations, scenarioFilter]
  );
  const visibleHandoffs = useMemo(
    () => filterByPack(data.handoffs, scenarioFilter),
    [data.handoffs, scenarioFilter]
  );
  const visibleGaps = useMemo(() => filterByPack(data.gaps, scenarioFilter), [data.gaps, scenarioFilter]);
  const visibleKnowledgeItems = useMemo(
    () => filterByPack(data.knowledgeItems, scenarioFilter),
    [data.knowledgeItems, scenarioFilter]
  );
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
      knowledgeItems: visibleKnowledgeItems.length,
      notifications: data.notifications.length,
      scenarios: data.scenarioPacks.length,
      mockData: visibleMockRecords.length
    };
    return counts[activeTab];
  }, [activeTab, data, visibleConversations, visibleHandoffs, visibleGaps, visibleKnowledgeItems, visibleMockRecords]);

  async function refreshConsoleData() {
    try {
      setIsLoading(true);
      setError(null);
      const [
        summaryResponse,
        conversationResponse,
        handoffResponse,
        gapResponse,
        knowledgeItemResponse,
        notificationResponse,
        scenarioResponse,
        mockRecordResponse
      ] = await Promise.all([
        getDailySummary(),
        listConversations(),
        listHandoffs(),
        listKnowledgeGaps(),
        listKnowledgeItems(),
        listMockNotifications(),
        listScenarioPacks(),
        listMockBusinessRecords()
      ]);
      setData({
        summary: summaryResponse.data,
        conversations: conversationResponse.data,
        handoffs: handoffResponse.data,
        gaps: gapResponse.data,
        knowledgeItems: knowledgeItemResponse.data,
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

  async function refreshSourceMode(packCode: string) {
    try {
      setSourceModeLoading(true);
      const response = await getScenarioPackSourceMode(packCode);
      setSourceMode(response.data);
    } catch (caughtError) {
      setError(formatError(caughtError));
    } finally {
      setSourceModeLoading(false);
    }
  }

  async function handleSourceModeChange(mode: string) {
    if (!sourceModePack) return;
    try {
      setSourceModeLoading(true);
      setError(null);
      const response = await updateScenarioPackSourceMode(sourceModePack, mode);
      setSourceMode(response.data);
    } catch (caughtError) {
      setError(formatError(caughtError));
    } finally {
      setSourceModeLoading(false);
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

  async function handleUpdateKnowledgeItem(record: KnowledgeItemRecord, status: string) {
    try {
      setIsUpdating(true);
      setError(null);
      const response = await updateKnowledgeItemStatus(record.item_id, status);
      setData((current) => ({
        ...current,
        knowledgeItems: current.knowledgeItems.map((item) =>
          item.item_id === record.item_id ? response.data : item
        )
      }));
      setSelected(response.data);
    } catch (caughtError) {
      setError(formatError(caughtError));
    } finally {
      setIsUpdating(false);
    }
  }

  async function handleCreateKnowledgeItem(payload: {
    scenario_pack_code: string;
    title: string;
    content: string;
    source_ref: string;
    tags: string[];
  }) {
    try {
      setIsUpdating(true);
      setError(null);
      const response = await createKnowledgeItem({ ...payload, status: 'draft' });
      setData((current) => ({
        ...current,
        knowledgeItems: [response.data, ...current.knowledgeItems]
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
          <span className="demo-badge">Demo Sandbox</span>
          <span className="demo-badge">Mock 数据</span>
          <span className="demo-badge muted">真实系统未接入</span>
          <span className="demo-badge muted">LLM 默认关闭</span>
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

      <section className="sandbox-banner" aria-label="Demo Sandbox 演示边界">
        <div>
          <strong>Demo Sandbox 演示模式</strong>
          <p>
            当前 Console 只展示 Mock / Sandbox 证据：标准模拟业务数据、可追溯 source_ref 和可选飞书测试群；真实 CRM / ERP / OA / 工单与真实 LLM 自动答复均未启用。
          </p>
        </div>
        <div className="sandbox-badges" aria-label="演示状态标签">
          <span>数据源模式：{sourceMode ? formatEnvironment(sourceMode.source_mode) : '加载中…'}</span>
          {sourceMode && sourceMode.gate_status === 'no_go' ? (
            <span className="hint-badge">真实数据 Not configured / No-Go</span>
          ) : null}
          <span>Mock 数据</span>
          <span>source_ref 可追溯</span>
          <span>真实系统 No-Go</span>
          <span>LLM 默认关闭</span>
        </div>
        {canWrite && sourceModePack ? (
          <div className="source-mode-switch">
            <label htmlFor="source-mode-select">
              切换数据源模式（场景包 {sourceModePack}）
            </label>
            <select
              id="source-mode-select"
              value={sourceMode?.source_mode ?? 'demo_sandbox'}
              disabled={sourceModeLoading}
              onChange={(event) => void handleSourceModeChange(event.target.value)}
            >
              {(sourceMode?.available_modes ?? ['demo_sandbox']).map((mode) => (
                <option key={mode} value={mode}>
                  {formatEnvironment(mode)}
                </option>
              ))}
            </select>
            {sourceMode && sourceMode.gate_status === 'no_go' ? (
              <span className="hint-badge">
                门禁未通过：{sourceMode.gate_reasons.join('、') || '未配置'}
              </span>
            ) : null}
          </div>
        ) : null}
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
          {!isLoading && activeTab === 'knowledgeItems' ? (
            <KnowledgeItemList
              records={visibleKnowledgeItems}
              scenarioPacks={data.scenarioPacks}
              isUpdating={isUpdating}
              canWrite={canWrite}
              onSelect={setSelected}
              onUpdate={handleUpdateKnowledgeItem}
              onCreate={handleCreateKnowledgeItem}
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

function KnowledgeItemList({
  records,
  scenarioPacks,
  isUpdating,
  canWrite,
  onSelect,
  onUpdate,
  onCreate
}: {
  records: KnowledgeItemRecord[];
  scenarioPacks: ScenarioPackSummary[];
  isUpdating: boolean;
  canWrite: boolean;
  onSelect: (record: DetailRecord) => void;
  onUpdate: (record: KnowledgeItemRecord, status: string) => void;
  onCreate: (payload: {
    scenario_pack_code: string;
    title: string;
    content: string;
    source_ref: string;
    tags: string[];
  }) => void;
}) {
  const defaultPack = scenarioPacks[0]?.code ?? '';
  const [packCode, setPackCode] = useState(defaultPack);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [sourceRef, setSourceRef] = useState('');
  const [tagsInput, setTagsInput] = useState('');

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!title.trim() || !content.trim() || !sourceRef.trim() || !packCode) return;
    onCreate({
      scenario_pack_code: packCode,
      title: title.trim(),
      content: content.trim(),
      source_ref: sourceRef.trim(),
      tags: tagsInput
        .split(/[,，]/)
        .map((item) => item.trim())
        .filter(Boolean)
    });
    setTitle('');
    setContent('');
    setSourceRef('');
    setTagsInput('');
  }

  return (
    <div className="record-list">
      {canWrite ? (
        <form className="knowledge-form" onSubmit={handleSubmit}>
          <h3>新增知识候选（draft，转正后才生效）</h3>
          <label>
            场景包
            <select value={packCode} onChange={(event) => setPackCode(event.target.value)}>
              {scenarioPacks.map((pack) => (
                <option key={pack.code} value={pack.code}>
                  {pack.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            标题
            <input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="知识标题" />
          </label>
          <label>
            内容
            <textarea
              value={content}
              onChange={(event) => setContent(event.target.value)}
              placeholder="知识正文"
              rows={2}
            />
          </label>
          <label>
            来源(source_ref)
            <input value={sourceRef} onChange={(event) => setSourceRef(event.target.value)} placeholder="SRC-XXX" />
          </label>
          <label>
            标签(逗号分隔)
            <input value={tagsInput} onChange={(event) => setTagsInput(event.target.value)} placeholder="产品规格,待确认" />
          </label>
          <button type="submit" disabled={isUpdating}>
            新增 draft 知识候选
          </button>
        </form>
      ) : null}
      {!records.length ? (
        <EmptyState text="暂无知识条目。可在「知识缺口」审核 accepted 后生成，或上方手动新增。" />
      ) : null}
      {records.map((record) => {
        const tone: 'success' | 'neutral' = record.status === 'active' ? 'success' : 'neutral';
        const label =
          record.status === 'active'
            ? '已生效·问答可命中'
            : record.status === 'draft'
              ? '知识候选'
              : '已归档';
        const origin = record.origin_gap_id ? `来自缺口 ${record.origin_gap_id}` : '手动新增';
        return (
          <article key={record.item_id} className="record-card" onClick={() => onSelect(record)}>
            <div className="record-title">
              <h3>{record.title}</h3>
              <StatusBadge label={label} tone={tone} />
            </div>
            <p>{record.content}</p>
            <MetaRow
              values={[record.scenario_pack_code, record.source_ref, origin, record.updated_at]}
              mock={record.mock}
            />
            <div className="action-row" onClick={(event) => event.stopPropagation()}>
              {record.status === 'draft' ? (
                <button disabled={isUpdating || !canWrite} onClick={() => onUpdate(record, 'active')}>
                  转正为已生效
                </button>
              ) : null}
              {record.status === 'active' ? (
                <button
                  className="secondary"
                  disabled={isUpdating || !canWrite}
                  onClick={() => onUpdate(record, 'archived')}
                >
                  归档
                </button>
              ) : null}
            </div>
          </article>
        );
      })}
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
          <MetaRow
            values={[
              record.record_type,
              record.scenario_pack_code,
              formatEnvironment(record.environment),
              record.source_system,
              record.source_ref,
              record.eta ?? '无 ETA'
            ]}
            mock={record.mock}
          />
        </article>
      ))}
    </div>
  );
}

function RecordDetail({ record }: { record: Exclude<DetailRecord, null> }) {
  return (
    <div className="detail-body">
      <DemoEvidenceSummary record={record} />
      <pre>{JSON.stringify(record, null, 2)}</pre>
    </div>
  );
}

function DemoEvidenceSummary({ record }: { record: Exclude<DetailRecord, null> }) {
  const evidenceItems = buildEvidenceItems(record);
  return (
    <div className="evidence-summary">
      <div className="record-title">
        <h3>演示证据摘要</h3>
        <MockBadge mock={getMockValue(record)} />
      </div>
      <p>用于演示讲解的边界摘要；完整原始响应仍保留在下方 JSON 中。</p>
      <div className="evidence-grid">
        {evidenceItems.length ? (
          evidenceItems.map((item) => (
            <span key={`${item.label}-${item.value}`} className={`evidence-chip ${item.tone ?? 'default'}`}>
              <strong>{item.label}</strong>
              {item.value}
            </span>
          ))
        ) : (
          <span className="evidence-chip neutral">
            <strong>演示边界</strong>
            当前记录未提供 source_ref；请以下方 JSON 为准。
          </span>
        )}
      </div>
      <p className="boundary-note">真实业务系统、生产飞书、真实客户数据和真实 LLM 自动答复仍未接入。</p>
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

function StatusBadge({
  label,
  tone = 'default'
}: {
  label: string;
  tone?: 'default' | 'danger' | 'success' | 'neutral';
}) {
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
