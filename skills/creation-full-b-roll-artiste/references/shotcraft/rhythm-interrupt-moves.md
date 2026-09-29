---
name: rhythm-interrupt-moves
一句话: 打断节奏两式——jump-cut-punch-in 三级跳切推近、strobe-black-frames 频闪黑帧
适用: 用"打断连续性"本身当节奏器：顿挫推近（B）、窒息逼近（C）；与 beat-cut-moves（切点排布）、montage-rhythm（段落呼吸）互补
时长: B ~4.5s / C ~4.5s
能量: B 中 / C 高
---

## Résumé en français

- Ce que décrit la carte : deux figures qui cassent volontairement la continuité, la rupture elle-même devenant le rythme. Elles complètent beat-cut-moves (espacement des coupes) et montage-rhythm-moves (respiration des segments).
- Variante B, jump-cut-punch-in (environ 4,5 s, énergie moyenne) : même cadrage, même point d'origine, trois paliers d'échelle sans interpolation (1,0 puis 1,6 puis 2,6), chaque palier tenu au moins 35 frames (1,2 s), le dernier au moins 45 frames. À chaque saut, 2 frames d'assombrissement à 0,92 qui font "tic".
- Variante C, strobe-black-frames (environ 4,5 s, énergie haute) : frames noires de 2 frames insérées selon une table fixe (40, 48, 55, 61, 66, 70, 73, 76, 79) avec des intervalles qui se resserrent de 8 à 3 frames, puis le dernier noir s'ouvre sur un hard cut à l'échelle 1,35 avec pulsation de 2 frames. Hold d'au moins 50 frames après.
- Quand l'utiliser en full B-roll voix off :
  - B pour resserrer progressivement sur le détail décisif pendant que la voix insiste ("regarde, plus près, c'est là"), utile sur un chiffre, une étiquette, une texture.
  - C uniquement comme compte à rebours avant le climax du film, avec une musique qui monte.
- Pièges signalés :
  - Les deux figures manipulent l'axe du temps, donc jamais combinées avec speed-ramp-freeze sur le même plan.
  - C comporte un avertissement photosensibilité (épilepsie) et n'a de sens qu'avec le son, une seule fois par vidéo.
  - B exige de garder exactement le même point d'origine, sinon ce sont trois plans différents et non un jump cut.
  - Un jump cut sans tic sonore ressemble à une perte d'images. Paramètres réglés sur placeholders.

## 意图
库内节奏卡管的都是"怎么切、切多密"；这两式管**怎么断**——观众预期
连续，你偏打断，打断方式即表达：B 是空间断——同构图三次无补间跳大
（1x→1.6x→2.6x），戈达尔跳切的顿挫，比连续推近更有"看这里、再近点、
就是它"的指令感；C 是存在断——画面与纯黑交替频闪且间隔收紧，
高潮前的窒息倒数。选型：强制聚焦指标用 B，高潮前蓄压用 C。

## 两式选型
| 式 | 做法 | 适用 |
|----|------|------|
| B jump-cut-punch-in | transform-origin 钉目标中心，三档 scale 阶梯跳变（零补间），每跳 2f 加深脉冲当 tick | 逐级逼近核心指标；纪录片式盯住 |
| C strobe-black-frames | 全屏黑帧按写死帧号表闪现（每次 2f，间隔 8f→3f 收敛），末闪掀开即硬切放大落定 | 全片最高潮前的倒数蓄压 |

## 参数表
| 参数 | 典型值 | 调节手感 |
|------|--------|----------|
| B 跳挡 | 1.0→1.6→2.6，各 hold ≥35f | 挡差 <1.5× 读作画面抖了一下 |
| B tick | 跳变帧起 2f brightness 0.92 全画面脉冲 | 无 tick 的跳切读作丢帧 |
| C 帧号表 | [40,48,55,61,66,70,73,76,79] 各 2f 纯黑 | 间隔必须收敛；等距频闪只是闪没有"逼近" |
| C 落锤 | 末闪掀开一帧到位 scale 1.35 + 2f 加深脉冲 | 掀开后还在原构图，频闪就白憋了 |
| 收尾 | B 末挡 ≥45f / C 硬切后 ≥50f 真静止 | 打断系事后 hold 从重给 |

## 已知坑
- demo 在灰阶/占位素材上调校通过——参数是调校起点非实战定稿，
  首次实战须以真实素材回验
- 两式与 speed-ramp-freeze 都动"时间轴"，同一镜头只能有一个时间
  操纵者
- C 式**光敏警示**：频闪画面需注意光敏性癫痫观众提示；且必须配乐
  渐强同步（无声频闪读作信号故障），全片 ≤1 次
- B 式三挡构图必须同 origin（钉死目标中心）——每挡重新构图就是
  三个镜头，不是跳切
- 声音强依赖：B 每跳一声 tick、C 每闪一声打点（sound-design §4.5）

## 参考实现
demos/rhythm/rhythm-interrupt-moves/
（JumpCutPunchIn.tsx / StrobeBlackFrames.tsx）
