import { FormEvent, useEffect, useMemo, useState } from 'react';

import {
  ApiClientError,
  createConversation,
  listScenarioPacks,
  sendMessage
} from '../../shared/apiClient';
import type { ConversationData, MessageResponseData, ScenarioPackSummary } from '../../shared/types';

type ChatMessage = {
  id: string;
  role: 'customer' | 'assistant';
  content: string;
  answerType?: string;
  sourceRef?: string;
  mock?: boolean;
  handoff?: Record<string, unknown> | null;
  knowledgeGap?: Record<string, unknown> | null;
};

const fallbackQuestions = [
  '灯带有什么规格？',
  '我想查一下 HC-ORDER-001 的生产进度',
  '项目开发有哪些阶段？',
  'XS-PROJ-001 到哪个阶段了？',
  'XS-TICKET-001 处理到哪了？',
  '如果客户要赔偿怎么办？'
];

function App() {
  const [scenarioPacks, setScenarioPacks] = useState<ScenarioPackSummary[]>([]);
  const [selectedPackCode, setSelectedPackCode] = useState('product_business');
  const [conversation, setConversation] = useState<ConversationData | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoadingPacks, setIsLoadingPacks] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const selectedPack = useMemo(
    () => scenarioPacks.find((pack) => pack.code === selectedPackCode),
    [scenarioPacks, selectedPackCode]
  );

  const quickQuestions = selectedPack?.demo_questions?.length
    ? selectedPack.demo_questions
    : fallbackQuestions;

  useEffect(() => {
    async function loadScenarioPacks() {
      try {
        setIsLoadingPacks(true);
        setError(null);
        const response = await listScenarioPacks();
        setScenarioPacks(response.data);
        if (response.data.some((pack) => pack.code === 'product_business')) {
          setSelectedPackCode('product_business');
        } else if (response.data[0]) {
          setSelectedPackCode(response.data[0].code);
        }
      } catch (loadError) {
        setError(formatError(loadError));
      } finally {
        setIsLoadingPacks(false);
      }
    }

    loadScenarioPacks();
  }, []);

  async function handleCreateConversation() {
    try {
      setIsCreating(true);
      setError(null);
      const response = await createConversation(selectedPackCode);
      setConversation(response.data);
      setMessages([
        {
          id: `welcome-${response.data.conversation_id}`,
          role: 'assistant',
          content: `已进入「${selectedPack?.name ?? selectedPackCode}」Demo 会话。你可以选择快捷问题或直接输入。`,
          answerType: 'demo_status',
          sourceRef: 'frontend:h5-demo',
          mock: response.meta.mock
        }
      ]);
    } catch (createError) {
      setError(formatError(createError));
    } finally {
      setIsCreating(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const content = input.trim();
    if (!content || isSending) {
      return;
    }

    try {
      setError(null);
      setIsSending(true);
      let activeConversation = conversation;
      if (!activeConversation) {
        const createResponse = await createConversation(selectedPackCode);
        activeConversation = createResponse.data;
        setConversation(createResponse.data);
      }

      const customerMessage: ChatMessage = {
        id: `customer-${Date.now()}`,
        role: 'customer',
        content
      };
      setMessages((current) => [...current, customerMessage]);
      setInput('');

      const response = await sendMessage(activeConversation.conversation_id, content);
      setMessages((current) => [...current, toAssistantMessage(response.data, response.meta.mock)]);
    } catch (sendError) {
      setError(formatError(sendError));
    } finally {
      setIsSending(false);
    }
  }

  function handleScenarioChange(nextCode: string) {
    setSelectedPackCode(nextCode);
    setConversation(null);
    setMessages([]);
    setError(null);
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <div>
          <p className="eyebrow">知衍数字客服 · H5 Demo</p>
          <h1>客户对话页</h1>
          <p className="hero-copy">
            本页面仅使用 Demo / Mock 数据。价格、交期、赔付、合同和法律责任不会自动承诺。
          </p>
        </div>
        <span className="status-pill">Mock Enabled</span>
      </section>

      <section className="panel scenario-panel">
        <label htmlFor="scenarioPack">场景包</label>
        <select
          id="scenarioPack"
          value={selectedPackCode}
          onChange={(event) => handleScenarioChange(event.target.value)}
          disabled={isLoadingPacks || isSending}
        >
          {scenarioPacks.map((pack) => (
            <option key={pack.code} value={pack.code}>
              {pack.name}
            </option>
          ))}
        </select>
        <button type="button" onClick={handleCreateConversation} disabled={isCreating || isLoadingPacks}>
          {conversation ? '重新创建 Demo 会话' : '创建 Demo 会话'}
        </button>
      </section>

      {selectedPack ? (
        <section className="panel pack-summary">
          <strong>{selectedPack.name}</strong>
          <p>{selectedPack.description}</p>
          <div className="summary-grid">
            <span>知识 {selectedPack.knowledge_count}</span>
            <span>规则 {selectedPack.rule_count}</span>
            <span>Mock 数据 {selectedPack.mock_business_count}</span>
          </div>
        </section>
      ) : null}

      <section className="chat-card">
        <div className="chat-header">
          <div>
            <h2>对话</h2>
            <p>{conversation ? `会话 ID：${conversation.conversation_id}` : '尚未创建会话，发送消息时会自动创建。'}</p>
          </div>
          <span className="demo-badge">Demo / Mock</span>
        </div>

        <div className="message-list" aria-live="polite">
          {messages.length === 0 ? (
            <div className="empty-state">选择快捷问题或输入客户问题，开始演示。</div>
          ) : (
            messages.map((message) => <MessageBubble key={message.id} message={message} />)
          )}
        </div>

        <div className="quick-questions">
          {quickQuestions.map((question) => (
            <button key={question} type="button" onClick={() => setInput(question)}>
              {question}
            </button>
          ))}
        </div>

        <form className="composer" onSubmit={handleSubmit}>
          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="请输入产品咨询、项目进度、售后或风险问题。"
            rows={3}
          />
          <button type="submit" disabled={!input.trim() || isSending || isLoadingPacks}>
            {isSending ? '发送中…' : '发送'}
          </button>
        </form>
      </section>

      {error ? <div className="error-card">{error}</div> : null}

      <section className="boundary-card">
        <strong>边界提示</strong>
        <p>不采集真实联系方式、订单、合同或客户隐私；无依据或高风险问题应转人工或记录知识缺口。</p>
      </section>
    </main>
  );
}

function MessageBubble({ message }: { message: ChatMessage }) {
  return (
    <article className={`message ${message.role}`}>
      <p>{message.content}</p>
      {message.role === 'assistant' ? (
        <div className="message-meta">
          {message.answerType ? <span>{message.answerType}</span> : null}
          {message.sourceRef ? <span>来源：{message.sourceRef}</span> : null}
          {message.mock ? <span>Mock</span> : null}
          {message.handoff ? <span>已转人工</span> : null}
          {message.knowledgeGap ? <span>知识缺口</span> : null}
        </div>
      ) : null}
    </article>
  );
}

function toAssistantMessage(data: MessageResponseData, mock: boolean): ChatMessage {
  return {
    id: data.message_id,
    role: 'assistant',
    content: data.answer,
    answerType: data.answer_type,
    sourceRef: data.source_ref,
    handoff: data.handoff,
    knowledgeGap: data.knowledge_gap,
    mock
  };
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
