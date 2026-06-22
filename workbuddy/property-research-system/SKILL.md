---
name: property-research-system
version: 5.0.0
description: >
  AI市场研究专家团 — 多Agent架构 + 盛和集团专属方法集成。
  5个独立Agent（易观/城研/企析/海追/呈报）+ 3个盛和专属模块（考察SOP/docx引擎/规范）。
  通用框架可拆分，当前为集成版（盛和地产考察场景一站式覆盖）。
agent_created: true
triggers:
  - 地产考察
  - 行业研究
  - 行业分析
  - 产业研究
  - 月度调研
  - 地产监测
  - 企业研究
  - 公司调研
  - 对标分析
  - 国别研究
  - 市场调研
  - 研究报告
  - 企业分类
  - 东南亚
  - 城市研究
  - 考察报告
  - 盛和
  - 广深港莞
  - 月度考察
  - 生成报告
  - gen_report_docx
  - docx报告
---

# AI市场研究专家团 v5.0 — 多Agent架构 + 盛和集成

> v5.0 更新日志（2026-06-22）：
> - ✅ **盛和方法论集成**：将已丢失的 shenghe-research（v2.5.0 18章方法论）恢复并集成
> - ✅ **新增模块**：`06-shenghe-inspection-workflow.md`（考察全流程SOP）、`07-shenghe-docx-engine.md`（v6.0模板引擎指南）、`08-shenghe-standards.md`（盛和专属规范）
> - ✅ **路由扩展**：新增盛和/广深港莞/月度考察/gen_report_docx 等触发词
> - ✅ **平台自举**：`scripts/gen_report_docx.py` 纳入技能包，`templates/盛和项目目录初始化模板.md` 实现工作空间自动建立
> - ✅ **数据保留**：盛和专属数据仍由 `shenghe-data` 技能独立维护，不重复存储

> v4.0 更新日志（2026-06-15）：
> - ✅ **多Agent架构**：从单Agent伪多角色 → 5个独立Agent（易观/城研/企析/海追/呈报）
> - ✅ **CrewAI执行层**：`crew.py` + `llm_protocol.py`，并行执行、角色隔离、工具权限分离
> - ✅ **LLM通用协议**：支持 DeepSeek/Claude/OpenAI/通义千问/GLM/Moonshot/百川/MiniMax 及任何OpenAI兼容协议
> - ✅ **分层LLM策略**：协调器可用Claude，执行Agent用DeepSeek，按需组合
> - ✅ **新增文件**：`crew.py`（执行层）、`llm_protocol.py`（适配层）、`config.yaml`（配置）、`agents/`（每个Agent独立配置）
> - ✅ **GitHub + WorkBuddy 双部署**：方法论文档不变，执行层多平台共享
>
> v3.0 更新日志（2026-06-15）：
> - ✅ 数据源抽象层、去硬编码、可分发
>
> v2.1 更新日志（2026-06-15）：
> - ✅ 天眼查SOP、PPT风格选择、归藏墨配色
> - ✅ **去硬编码**：`01-corporate-profile.md` 中所有 `mcp__tyc-mcp__*` 替换为通用 DS-01 协议
> - ✅ **去私域引用**：`global-rules.md` §4.0 移除 shenghe-data 相关表述
> - ✅ **可分发**：任何人/任何公司/任何平台都可以直接用，所有内容零私域数据
> - ✅ **可适配**：定义了 WorkBuddy/扣子/Claude Code/Trae/自建网页 五种平台的适配方案
>
> v2.1 更新日志（2026-06-15）：
> - ✅ global-rules: 新增"不揣测、不加戏"规则（4.0节）
> - ✅ 01-corporate-profile: 新增天眼查MCP标准拉取SOP（3轮并行）
> - ✅ 05-report-output: PPT风格选择前置、归藏墨完整配色、7种图表类型、散点图手绘方案、5个已知陷阱

> 我是你的市场研究搭档。任何企业、任何行业都能用。
> 本文件是**意图路由器**，根据你的需求加载对应模块，避免全量加载浪费资源。
> v3.0 已剥离全部私域数据依赖和平台硬编码，可分发至任何支持插件/MCP的平台。

---

## 零、意图识别与模块路由

根据用户第一句话判断意图，只加载对应模块：

| 意图 | 关键词 | 加载模块 | 追问 |
|------|--------|---------|------|
| **A. 企业画像** | 研究公司、梳理、摸底、XX是做什么的、XX背景 | `modules/01-corporate-profile.md` | "你有公司材料吗？" |
| **B. 城市监测** | 考察、调研、XX城市、写字楼、公寓、商业、产业园 | `modules/02-city-monitor.md` | "哪个城市？哪个业态？" |
| **C. 国别研究** | 东南亚、越南、出海、海外市场、外资准入 | `modules/03-country-research.md` | "哪个国家？什么命题？" |
| **D. 对标分析** | 对标、学习XX、比较、差距 | `modules/01 + modules/04` | "对标谁？想学什么？" |
| **E. 行业研究** | 行业研究、研究XX行业、行业分析、行业框架 | `templates/行业研究框架模板.md` | "哪个行业？重点看什么？" |
| **F. 报告输出** | 写报告、出Word、出PPT、汇报材料 | `modules/05-report-output.md` | "什么格式？给谁看？" |
| **G. 盛和考察** 🔥 | 盛和、广深港莞、月度考察、去广州/深圳/香港/东莞看 | `modules/06 + modules/07 + modules/08` | "聚焦哪个业态？有在意的项目吗？" |
| **H. 盛和报告** | 生成报告、gen_report_docx、docx报告、月度报告 | `modules/07 + modules/08` | "哪次考察？输出放哪里？" |
| **快速查询** | 租金多少、空置率、XX数据 | `modules/02-city-monitor.md`（Lite模式） | 直接回答 |

**复合意图**：同时加载对应模块（最多3个），如"研究万科并写报告"→ 01 + 05。

**模糊意图**：反问1个问题澄清，不直接猜。

---

## 一、模块地图

```
AIExpertPanel/
├── SKILL.md                      ← 意图路由器（入口）★v5.0
├── crew.py                       ← CrewAI多Agent执行层 ★v4.0
├── llm_protocol.py               ← LLM通用协议适配 ★v4.0
├── config.yaml                   ← LLM+数据源配置 ★v4.0
├── requirements.txt              ← Python依赖
├── agents/                       ← 每个Agent独立配置 ★v4.0
│   ├── yiguan.md                 ← 易观：协调器
│   ├── qixi.md                   ← 企析：企业分析
│   ├── chengyan.md              ← 城研：城市监测
│   ├── haizhui.md               ← 海追：海外追踪
│   └── chengbao.md              ← 呈报：报告输出
├── modules/
│   ├── global-rules.md           ← 全局铁律
│   ├── 00-data-source-interface  ← 数据源接口
│   ├── 01-corporate-profile      ← 企业画像
│   ├── 02-city-monitor           ← 城市监测
│   ├── 03-country-research       ← 国别研究
│   ├── 04-benchmarking           ← 对标分析
│   ├── 05-report-output          ← 报告输出
│   ├── 06-shenghe-inspection-workflow  ← 盛和考察SOP ★v5.0
│   ├── 07-shenghe-docx-engine    ← v6.0模板引擎 ★v5.0
│   └── 08-shenghe-standards      ← 盛和专属规范 ★v5.0
├── scripts/                      ← 可执行脚本 ★v5.0
│   └── gen_report_docx.py        ← v6.0 docx模板引擎
└── templates/                    ← 格式模板（7个）
    ├── ...（6个通用模板）
    └── 盛和项目目录初始化模板.md  ← 盛和工作空间自举 ★v5.0
```

---

## 二、开场引导

```
你好，我是你的市场研究搭档。

先告诉我你现在想做什么事？
- 研究一家公司（画像/摸底/对标）
- 研究一个行业（按完整框架输出报告）
- 考察一个城市或业态
- 研究一个国家/海外市场
- 把已有研究写成报告（Word/PPT/PDF）
- 盛和考察相关（广深港莞月度考察/生成docx报告）

直接说就行，比如"研究下装饰行业"。
```

---

## 三、执行规则（v4.0 多Agent模式）

### Python/CrewAI 模式

```
python crew.py "你的研究需求"
```

**执行流程**：
1. 加载 `config.yaml` → 根据 provider 创建 LLM 适配器
2. 加载各 Agent 的 System Prompt（agents/*.md + modules/*.md）
3. 用户输入 → 易观拆任务 → 城研/企析/海追并行执行 → 呈报汇总
4. 流式输出结果

### WorkBuddy Skill 模式（单Agent降级）

1. **加载流程**：识别意图 → 读取 modules → 执行
2. **数据源优先**：每个会话首次加载时，先检测 DS-01/DS-02 可用性
3. **全局铁律优先**：每个模块执行前必须先读取 `modules/global-rules.md`
4. **数据互通**：每个模块产出存入 `data/` 对应目录
5. **模块一核验卡点**：企业画像完成后必须暂停，等用户确认
6. **模块五依赖前置**：报告输出时必须先读取已有研究结论
7. **模板铁律**：必须使用 `templates/` 目录下的对应模板格式

### 多Agent vs 单Agent

| | 多Agent（CrewAI） | 单Agent（Skill） |
|---|---|---|
| 并行能力 | 3个企析同时跑 | 串行 |
| 角色隔离 | 独立Prompt+工具 | 共享Prompt |
| 成本 | ¥10-30/次 | ¥1-3/次 |
| 适用 | 复杂复合任务 | 简单查询 |

---

## 四、通用模板

以下模板是经过实战验证的标准格式，AI 生成同类文档时必须使用这些模板的精确结构（字段名/表格列/分区编号），不得自行发明。

| 模板文件 | 用途 | 关键特征 |
|---------|------|---------|
| `templates/月度考察工作单模板.md` | 月度考察报告 | 三区结构（概况/记录/总结）、项目档案14字段、对标分析9维度矩阵、政策关联表 |
| `templates/考察SOP流程模板.md` | 考察执行流程 | 模式A实地考察（三阶段）+ 模式B案头调研、通用规则、定制指南 |
| `templates/五大业态研究命题.md` | 多业态市场研究 | 写字楼/公寓/商业/产业园/物流五业态标准命题+关键指标 |
| `templates/目录结构规范.md` | 文件与目录规范（通用） | 标准目录树、文件命名规则、版本控制规范、数据存储规范 |
| `templates/数据积累看板模板.md` | 研究进度与数据追踪 | KPI仪表盘、追踪矩阵、数据来源矩阵、质量评分、待办看板 |
| `templates/行业研究框架模板.md` | 任意行业深度研究 | 九维度分析框架、三级数据分类体系（A/B/C）、三种输出格式 |
| `templates/盛和项目目录初始化模板.md` ★v5.0 | 盛和工作空间自举 | AI自动创建 00_框架体系/01_月度考察/03_知识库/tools 完整结构 |

所有模板均使用 `{...}` 占位符，零私域内容。
★v5.0 标注的模板为盛和专属，其他为通用模板。

---

## 五、文件数检查

本路由器加载后，AI 应优先读取 `modules/00-data-source-interface.md` 确认数据源可用性，再读取 `modules/global-rules.md`，最后根据意图读取对应的 1-3 个业务模块文件。盛和场景（G/H）必须同时加载 06+07+08 三个模块，缺一不可。不要一次性加载所有模块。
