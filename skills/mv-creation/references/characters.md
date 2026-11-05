# 角色组件

需要 Clawd、表情动画、角色视角或自定义角色时阅读。下面是 p5 模板（`assets/painted-character/src/clawd.js`）的接口；水彩 Skia 引擎（`assets/engines/watercolor-clawd/code/clawd.py`）是它的移植，函数名、表情名、视角和动作一致，区别是选项用 dict 传：`clawd(x, y, u, {...})`，男女主直接用 `him()` / `her()`。角色设定（配色、识别物、走位）见 references/cast.md。

## 选择与复用

- 用户选择 Clawd 时使用 `assets/painted-character/src/clawd.js`；角色是 Claude Code 吉祥物，保留其真实名称与来源，不把它描述为原创角色。
- 用户提供角色图时，先确定其比例、轮廓、颜色、标志特征；将绘制函数或素材放在共享角色文件，各镜头只改变姿态、位置和表情。
- 自定义角色可参考组件的动作与表情结构，按设计重画身体和面部。仅改 `col`、`hat` 等参数是现有角色的变体，不等于完整的新角色系统。
- 无角色作品可以用道具、环境、文字或抽象图形推进情绪。

## 依赖与坐标

`clawd.js` 依赖 p5.js、p5.brush 与 `src/core.js` 的 `paint`、调色板、时间和随机函数。跨引擎迁移时需要适配绘图接口，不能把它直接粘贴进 PIL/Skia 使用。

模板加载顺序：`config.js → core.js → clawd.js → timeline.js → 场景文件`。模板原生画布 1920×1080；`clawd(x, y, u, options)` 的 `(x,y)` 是脚底中心，含腿高约 `8u`、身体宽约 `10u`。`u` 按构图决定。

## 基本调用

```js
// 场景函数中，t 为全片时间。
const mood = emotions(t, [[0, 'thinking'], [2, 'surprised'], [3, 'happy']]);
clawd(960, 820, 28, { ...mood, boilKey: 'lead' });

// 表情与动作都可能返回 dy/sq 等字段；需要叠加的字段显式相加。
const face = feel('happy', t);
const hop = jump(t, 4, 4.7, 3);
clawd(960, 820, 28, {
  ...face, ...hop,
  dy: (face.dy || 0) + (hop.dy || 0),
  sq: (face.sq || 0) + (hop.sq || 0),
  boilKey: 'lead'
});
```

| 能力 | API / 参数 |
|---|---|
| 单个表情 | `feel(name, t, overrides)`，同时包含脸和身体的待机动作 |
| 连续情绪 | `emotions(t, [[秒, 名称, 可选覆盖], ...])`，含表情切换的预备与回弹 |
| 五个视角 | `view: 'front' / 'q' / 'side' / 'qback' / 'back'`；`flip: true` 镜像 |
| 转身 | `turn(t, t0, t1, a0, a1)`；朝向以圈计，`0` 正面、`.25` 右侧、`.5` 背面 |
| 动作 | `move(style, t, seed)`、`jump`、`take`、`stroll`，参数见源码注释 |
| 舞蹈 | `dancer(x,y,u,style,t,extra)`；`extra` 中同名参数优先 |
| 外观 | `col/dk/lt`、`hat`、`eyes/mouth`、`lookX/lookY`、`blush/gloom`、`emote` |
| 道具 | `armL(u,sw)` / `armR(u,sw)` 在手端画道具，`draw(u,sw)` 在身体局部坐标画附加物 |

31 个表情：`neutral, happy, excited, laugh, love, shy, proud, smug, relieved, sad, cry, angry, furious, scared, surprised, confused, thinking, idea, determined, sleepy, bored, nervous, suspicious, disgusted, dizzy, cool, starstruck, ko, playful, mischief, hopeful`。

动作：`bounce, hop, roof, sway, spin, wave, walk, run, idle, stomp, shimmy, mix`。这些默认随 `PROJECT.bpm` 变化；安静段可直接给固定姿态或减弱位移，不必始终跳动。

用 `assets/painted-character/docs/emotions.jpg`、`views.jpg` 查模型表，或初始化后运行：

```bash
node render.mjs --loop=emotions --sheet=1 --cols=1 --w=1920 --out=out/check/emotions.jpg
node render.mjs --loop=views --sheet=1 --cols=1 --w=1920 --out=out/check/views.jpg
```

角色跨镜头保持形体与特征；让眼神、身体、手臂依次传达反应。角色增减导致绘制顺序变化时，用稳定 `boilKey`，避免无关部位抖动。
