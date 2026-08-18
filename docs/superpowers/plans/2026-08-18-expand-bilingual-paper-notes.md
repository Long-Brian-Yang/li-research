# Expand Bilingual Paper Notes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将中日双语论文笔记升级为可检索、可比较、 DOI 可点击的详细 Markdown 文献库。

**Architecture:** 保留 `papers_zh.md` 与 `papers_ja.md` 两份独立读者版本；每篇论文采用统一元数据字段，并在文末加入扩充后的横向比较表。`README.md` 只作为入口，不重复论文内容。

**Tech Stack:** Markdown、Git、shell-based validation。

## Global Constraints

- 9 篇论文全部保留，不改变用户提供的 DOI。
- Review 必须在标题和类型字段中明确标注。
- 每篇至少包含 8 个关键词，并覆盖材料、结构、输运、稳定性、界面、力学、成本或应用中的相关维度。
- DOI 使用 `https://doi.org/...` 自动链接格式。
- 中文和日语版本的论文顺序、表格行数、DOI 必须一致。

### Task 1: 扩充中文版本

**Files:** Modify `papers_zh.md`

- [ ] 为每篇增加 `Type` 字段；第 9 篇标注 `Review`。
- [ ] 扩充关键词至每篇至少 8 项。
- [ ] 将 DOI 改为 `[10.xxxx/...](https://doi.org/10.xxxx/...)`。
- [ ] 增加按年份、材料、类型、室温传导度、结构/机制、稳定性、力学/成本、器件验证、核心贡献、DOI 的详细比较表。

### Task 2: 扩充日语版本

**Files:** Modify `papers_ja.md`

- [ ] 与中文版本保持完全相同的 9 篇顺序和字段。
- [ ] 使用自然日语翻译新增字段和表格内容；保留化学式、单位和英文专有名词。
- [ ] 将全部 DOI 改为可点击链接。

### Task 3: 验证一致性

**Files:** `README.md`, `papers_zh.md`, `papers_ja.md`

- [ ] 检查两个文件均有 9 个论文章节、9 个 DOI、至少 8 个关键词/篇。
- [ ] 检查所有 DOI 均匹配 `https://doi.org/` 链接。
- [ ] 检查表格列数和数据行数量一致。
- [ ] 检查 Git diff，提交并推送更新。

