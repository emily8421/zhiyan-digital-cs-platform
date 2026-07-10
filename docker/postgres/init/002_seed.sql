INSERT INTO zycs_scenario_packs (id, code, name, description, status, source_ref, is_mock)
VALUES
  ('sp_product_business', 'product_business', '产品型客户场景包', '面向灯饰、制造、标准或半标准产品销售企业的 Phase2 DB 地基样例。', 'active', 'SRC-SP-PRODUCT-001', true),
  ('sp_project_business', 'project_business', '项目型客户场景包', '面向智能家居方案商、项目交付型企业的 Phase2 DB 地基样例。', 'active', 'SRC-SP-PROJECT-001', true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO zycs_knowledge_items (id, scenario_pack_id, title, content, tags, source_ref, status, is_mock)
VALUES
  ('kb_product_001', 'sp_product_business', '灯带规格咨询', 'Phase2 DB 地基样例中可说明常见灯带规格、颜色和定制方向，具体价格与交期需转人工确认。', '["产品咨询", "灯带"]'::jsonb, 'SRC-SP-PRODUCT-001', 'active', true),
  ('kb_product_002', 'sp_product_business', '售后处理边界', '售后问题可先收集故障现象和订单编号，赔付、退换货结论需人工确认。', '["售后", "风险边界"]'::jsonb, 'SRC-PRD-001', 'active', true),
  ('kb_project_001', 'sp_project_business', '方案开发阶段说明', 'Phase2 DB 地基样例中可说明需求澄清、方案开发、联调测试和交付验收等阶段。', '["项目咨询", "方案开发"]'::jsonb, 'SRC-SP-PROJECT-001', 'active', true),
  ('kb_project_002', 'sp_project_business', '技术资料获取说明', '客户可先说明项目阶段和资料类型，涉及合同、报价或承诺事项需转人工。', '["技术资料", "风险边界"]'::jsonb, 'SRC-PRD-001', 'active', true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO zycs_rule_items (id, scenario_pack_id, rule_type, pattern, action, response_template, priority, source_ref, enabled)
VALUES
  ('rule_product_001', 'sp_product_business', 'risk', '投诉|曝光|赔偿|合同|最低价|保证交期', 'handoff', '价格、交期、赔付、合同和投诉问题必须转人工。', 10, 'SRC-PRD-001', true),
  ('rule_project_001', 'sp_project_business', 'risk', '合同|赔偿|违约|保证上线|法律责任', 'handoff', '合同、赔付、上线承诺和法律责任问题必须转人工。', 10, 'SRC-PRD-001', true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO zycs_mock_business_records (id, scenario_pack_id, record_type, external_ref, status, summary, next_step, eta, payload, is_mock)
VALUES
  ('mock_order_001', 'sp_product_business', 'order', 'HC-ORDER-001', '生产排期中', 'Mock 订单 HC-ORDER-001 已进入生产排期，等待物料齐套。', '物料齐套后进入生产。', '2026-07-10', '{"demo_source":"scenario_pack"}'::jsonb, true),
  ('mock_order_002', 'sp_product_business', 'order', 'HC-ORDER-002', '质检中', 'Mock 订单 HC-ORDER-002 已完成生产，正在质检。', '质检通过后安排包装。', '2026-07-08', '{"demo_source":"scenario_pack"}'::jsonb, true),
  ('mock_project_001', 'sp_project_business', 'project', 'XS-PROJ-001', '方案开发阶段', 'Mock 项目 XS-PROJ-001 已完成需求澄清，正在输出方案。', '方案评审后进入联调准备。', '2026-07-12', '{"demo_source":"scenario_pack"}'::jsonb, true),
  ('mock_project_002', 'sp_project_business', 'project', 'XS-PROJ-002', '联调测试阶段', 'Mock 项目 XS-PROJ-002 正在进行设备与平台联调。', '联调通过后安排交付验收。', '2026-07-15', '{"demo_source":"scenario_pack"}'::jsonb, true),
  ('mock_ticket_001', 'sp_project_business', 'ticket', 'XS-TICKET-001', '售后处理中', 'Mock 售后单 XS-TICKET-001 已分配给售后同事处理。', '售后同事确认现场信息后回复。', '2026-07-09', '{"demo_source":"scenario_pack"}'::jsonb, true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO zycs_notifications (id, target_type, event_type, related_id, payload, send_status, is_mock)
VALUES
  ('notif_seed_handoff', 'feishu', 'handoff', 'seed_handoff', '{"mock":true,"title":"转人工提醒样例","channel":"feishu_mock"}'::jsonb, 'mocked', true),
  ('notif_seed_gap', 'feishu', 'knowledge_gap', 'seed_gap', '{"mock":true,"title":"知识缺口提醒样例","channel":"feishu_mock"}'::jsonb, 'mocked', true),
  ('notif_seed_summary', 'console', 'summary', 'seed_summary', '{"mock":true,"title":"日报摘要样例","channel":"console"}'::jsonb, 'mocked', true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO zycs_daily_summaries (id, summary_date, scenario_pack_id, conversation_count, handoff_count, gap_count, open_item_count, content)
VALUES
  ('summary_seed_today', CURRENT_DATE, NULL, 0, 0, 0, 0, 'Phase2 DB 地基样例日报：数据库已初始化，业务尚未切换到 PostgreSQL。')
ON CONFLICT (id) DO NOTHING;

INSERT INTO zycs_audit_logs (id, request_id, actor_type, action, resource_type, resource_id, safe_detail)
VALUES
  ('audit_seed_db_foundation', 'seed', 'system', 'seed_db_foundation', 'database', 'zycs', '{"mock":true,"note":"Phase2 Sprint-8A DB foundation seed"}'::jsonb)
ON CONFLICT (id) DO NOTHING;

