# Storytelling Benchmark Results Viewer

## 描述

这是一个用于展示和交互式探索 **Storytelling 图像生成 Benchmark** 结果的静态网站。该网站旨在清晰地呈现不同模型在多个评估维度上的表现，并提供深入分析具体生成实例的功能。

主要特性包括：

*   **中英双语界面:** 支持英语和中文切换。
*   **响应式设计:** 适应不同屏幕尺寸。
*   **概览页面:** 提供项目介绍、核心发现、排行榜摘要、新闻、资源链接和引用信息。
*   **详细排行榜:**
    *   展示所有评估运行的详细得分。
    *   支持按多个指标（如 CRef, SRef, Overall Score 等）进行排序。
    *   **可展开行:** 点击 "+" 图标可查看每个评估维度的详细子项得分。
*   **结果浏览器:**
    *   以垂直堆叠的方式并排展示多个模型的生成序列。
    *   同步滚动和聚焦高亮当前查看的镜头 (Shot)。
    *   联动显示当前镜头的输入脚本和相关角色参考图。
*   **指标定义页面:** 详细解释 Benchmark 中使用的所有评估指标及其子项。
*   **数据集页面:** 介绍所使用的 Benchmark 数据集（如 WildStory）的结构和信息。

## 项目结构

```
bmk_leaderboard/
├── index.html             # P1: 概览与排行榜摘要 (主页)
├── leaderboard_detail.html # P?: 详细排行榜 (含展开行)
├── model_detail.html      # P2: (可选) 模型/方法详情页 (当前链接指向这里，但主要信息已移至详细排行榜)
├── story_detail.html      # P3: 结果浏览器 (交互式镜头对比)
├── metrics.html           # P4: 评估指标释义
├── dataset.html           # P5: Benchmark 数据集介绍
├── css/
│   └── style.css          # 全局样式表
├── js/
│   └── main.js            # 全局 JavaScript (语言切换, 排序, 展开/折叠, 导航)
├── data/
│   └── placeholder_data.js # 存储中英文翻译文本
└── img/
    └── placeholder*.png   # 占位符图片
```

## 数据说明

*   **当前状态:** 目前网站中的大部分数据（如排行榜得分、结果浏览器中的图像路径和子项得分）使用的是**占位符**。
*   **`story_detail.html` 数据:** 结果浏览器页面的交互数据目前硬编码在 `story_detail.html` 文件底部的 `<script>` 块内的 `storyData` JavaScript 对象中。你需要修改这个对象，填入真实的图像路径和故事/角色信息。
*   **`leaderboard_detail.html` 数据:** 详细排行榜的子项得分目前直接写在 HTML 的隐藏行 (`<tr class="details-row">`) 中。你需要用真实数据替换这些占位符。主行的聚合分数也需要更新。
*   **数据结构:** 关于 Benchmark 输入数据的预期结构，请参考 `dataset.html` 页面中展示的 `stories_data` 格式。

## 如何使用

1.  **本地浏览:** 克隆或下载此仓库。直接在你的网页浏览器中打开 `index.html` 文件即可开始浏览。
2.  **部署:** 由于这是纯静态网站，你可以将整个 `bmk_leaderboard` 文件夹部署到任何支持静态文件的托管服务上，例如：
    *   GitHub Pages
    *   Netlify
    *   Vercel
    *   或其他 Web 服务器。

## 定制与数据集成

1.  **替换占位符文本:** 修改 `data/placeholder_data.js` 文件来更新界面上的静态文本翻译。修改各个 HTML 文件中直接写入的占位符内容（如 `index.html` 的介绍、新闻等）。
2.  **集成排行榜数据:**
    *   修改 `leaderboard_detail.html` 中 `<tbody>` 内的主行 (`tr.main-row`) 数据。
    *   用真实的子项得分填充每个主行后面的隐藏详情行 (`tr.details-row`) 中的 `<dd>` 元素。
    *   更新 `index.html` 中的排行榜摘要表格。
3.  **集成结果浏览器数据:**
    *   修改 `story_detail.html` 文件底部的 `storyData` JavaScript 对象。你需要根据你的输出文件结构，为每个故事的每个镜头提供脚本、涉及的角色 key，以及**每个模型**在该镜头生成的**图像路径**。
    *   更新 `storyData` 对象中的 `characters` 部分，提供角色 key、名称和**角色参考图**的正确路径。
4.  **替换图像:** 将 `img/` 目录下的占位符图片替换为实际的角色参考图和模型生成的图像。确保 HTML 和 `storyData` 中的 `src` 路径正确。
5.  **添加/移除模型:**
    *   在 `leaderboard_detail.html` 和 `index.html` 的表格中添加/删除行。
    *   在 `story_detail.html` 的模型选择器 (`#model-selector-checkboxes`) 中添加/删除复选框。
    *   更新 `story_detail.html` 中的 `storyData` 对象，包含新模型的数据。
    *   (可选) 在 `data/placeholder_data.js` 中添加模型名称的翻译。

## 许可证

[在此处添加你的项目许可证信息，例如：]
本项目代码和结果根据 [许可证名称，例如 Apache 2.0] 许可证授权。数据集本身可能遵循其原始来源的许可证。

## 引用

[在此处添加引用信息，例如：]
如果你在研究中使用了此 Benchmark 或网站，请引用：
```bibtex
@misc{yourbenchmark2024,
  title={Storytelling Benchmark Results Viewer},
  author={Your Name/Team},
  year={2024},
  howpublished={\url{Your Project URL}},
}
```

