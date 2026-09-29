---
name: transition-hidden-cut
一句话: 藏切点转场三式——前景遮挡隐形切、对撞开屏、暖色漏光，硬切藏进遮挡/撞击/光峰的 1-3 帧里，观众看不见剪刀
适用: 两镜衔接处需要"无痕换景"或"仪式感开屏"时（技法卡，与 shot-transitions 六式同层选型）
时长: n/a（技法卡；各式占用帧数见参数表，从相邻镜头预算里划）
能量: n/a（技法卡，不占能量位）
---

## Résumé en français

- Ce que décrit la carte : trois transitions qui cachent un hard cut dans 1 à 3 frames où l'oeil est distrait par un mouvement ou une lumière (principe de misdirection). Même famille que le flash-cut, avec trois "cache-oeil" différents. Fiche technique, frames prises sur le budget des plans voisins.
- A, invisible-cut (occultation par un élément) : une grande carte (1600x1000 agrandie 1,6x) traverse l'écran en 14 frames avec un lourd flou de mouvement (obturateur 300, 12 échantillons, flou 8 px, quatre traînées), la coupe se fait au milieu quand tout est couvert. Le fond sortant est tiré de 40 px dans le sens du passage, le fond entrant revient de l'autre côté en 13 frames. Pour un faux plan-séquence.
- B, versus-slam (collision) : deux demi-écrans à bord oblique (environ 78°) foncent l'un vers l'autre depuis plus ou moins 1200 px en 10 frames avec accélération ; à l'impact, même frame : flash blanc 0,9 vers 0 en 3 frames, secousse de 12 px éteinte en 5 frames, tampon "VS" à l'échelle 1,6 vers 1 en 6 frames. Pour un avant/après ou une comparaison.
- C, light-leak-burn (fuite de lumière chaude) : trois halos orangés (#f6c878, #e8a44a, #d98a2b, 1500 à 2400 px, flou 90 px, mode screen) balaient en diagonale sur environ 70 frames ; montée de 27 frames, coupe au pic quand l'ancienne image est mangée à 70 %, décroissance de 43 frames. Au pic, contraste -45 % et luminosité +35 % sur l'image.
- Quand l'utiliser en full B-roll voix off :
  - A pour changer de lieu ou de scène sans que la voix marque de pause, quand on veut une continuité d'un seul souffle.
  - B seulement quand le script oppose deux choses (ancienne méthode contre nouvelle, avant contre après).
  - C pour un passage de chapitre chaleureux, ambiance naturelle, bien-être, cosmétique.
- Pièges signalés :
  - Une seule figure par raccord, et ne pas cumuler flash-cut et C dans le même film (deux effets lumineux).
  - A doit couvrir tout l'écran à la frame de coupe, vérifier image par image après changement de format (le 9:16 change la géométrie).
  - B sans opposition réelle devient un simple wipe oblique.
  - C respecte les contraintes de sobriété des effets de lumière : une seule occurrence, au service de la coupe.
  - Décider ces raccords au stade du découpage. Paramètres réglés sur placeholders.

## 意图
与 shot-transitions A 式 flash-cut 同族：flash-cut 用一层白闪盖住硬切，
这三式换了三种"障眼物"——扫过的前景卡片（A）、对撞的撞击帧（B）、
爬到顶峰的漏光（C）。共同原理是魔术误导：观众的眼睛被大动作/强光
吸走的那 1-3 帧里完成硬切，回过神来景已经换了，全程"看不见剪刀"。
flash-cut 是最素的一款；要方向感选 A，要仪式感选 B，要温度选 C。

## 三式选型
| 式 | 做法 | 适用接缝 |
|----|------|----------|
| A invisible-cut 前景遮挡隐形切 | 一张超画幅卡片带重运动模糊贴脸横扫，糊满全屏的遮挡帧内背景 A→B 硬切，卡片飞出观众以为还是同一镜 | 想让换景完全无痕的页面→页面；伪"一条 take"的主力款 |
| B versus-slam 对撞开屏 | 左右两半屏带斜切边从画外加速对冲撞合，撞击帧白闪+震屏+VS 盖章，切点就是撞击本身 | 对比/对阵语义的开屏或章节头（新旧方案、双产品、before/after）|
| C light-leak-burn 暖色漏光 | 三团暖色柔光沿对角线斜扫，光峰帧吞掉旧页约七成时硬切新页，光退散时新页已就位 | 想要暖调/胶片味的章节过渡；比白闪柔、有方向、有温度 |

## 参数表
| 参数 | 典型值 | 调节手感 |
|------|--------|----------|
| A 横扫 | 卡片 1600x1000 再 scale(1.6)，x 从 -2200→2600 共 14f，bezier(0.3,0,0.7,1)；切点在扫掠中点全遮帧（demo 里 f47） | 中点必须覆盖 -280..2280 糊满 1920 画幅；两端完全出画 |
| A 糊感 | 全场包 `<CameraMotionBlur shutterAngle={300} samples={12}>` + 卡片自身 blur(8px)/skewX(-v·0.018°) + 4 层手动残影（opacity 0.35→0.07、blur 14px、间隔 0.55f） | 三层糊叠出"贴脸呼啸"；只靠 CameraMotionBlur 糊不满遮挡窗口 |
| A 带风推挤 | 背景 ±40px：切前 A 被拖向扫掠方向（ease-in），切后 B 从反侧 13f 回稳（ease-out） | 卖"同一镜被风带了一下"的错觉，是无痕感的一半功劳 |
| B 斜缝几何 | clip-path polygon 斜边约 78°（缝顶 x=1075→缝底 x=845）；两半屏从 ±1200px 以 ease-in(cubic) 10f 对冲到位 | ease-in 加速才有"砸"感；垂直缝读作 PPT 分屏 |
| B 撞击三件套 | 撞击帧同发：白闪 0.9→0 共 3f + 整机 shake 12px·e^(−t/1.6) 约 5f 收干 + VS 字块 scale 1.6→1 back(2.6) overshoot 6f 压出 | 三件必须同帧起跑，错开一帧就散；震屏幅度须过肉眼阈值（可感性判例）|
| C 光层 | 3 团径向渐变（#f6c878/#e8a44a/#d98a2b，直径 1500/1950/2400px，blur 90px，mixBlendMode screen）沿右上→左下扫约 70f | 光团偏移沿扫掠方向拖尾排布，避免完美同心的"手电筒感" |
| C 光强包络 | ease-in 爬升 27f（蓄力）→ 峰值帧藏切 → ease-out 收敛 43f（余温）；峰值叠 8% 全屏暖罩 + 近白热核（opacity=intensity²） | 爬升慢收敛快会读作故障闪光；热核只在临近峰值烧起来 |
| C 冲淡 | 峰值时页面 filter：contrast 降 45%、brightness 抬 35% | 这是"烧穿"感的来源——光只叠不冲淡，读作贴了张贴纸 |

## 已知坑
- demo 在灰阶/占位素材上调校通过——参数是调校起点非实战定稿，
  首次实战须以真实素材回验
- C 式是 Q4 光效判例解封后首个入库光效手法——严守 Q4 三约束：
  单点使用（一支片一处，不群发）、正常速度回放自检好看才算过、
  光效服务切点而非装饰；与 flash-cut 同片混用算两次光效藏切
- A 式遮挡物必须真的全遮：demo 里 1600x1000 的卡要 scale(1.6) 才盖满
  1920 画幅——换素材尺寸后先逐帧检查切点帧有没有露出背景边缘，
  露一条缝整个魔术就穿帮
- B 式 VS 字块语义仅适配"对比/对阵"内容——没有两方对峙关系时
  别当通用转场用；去掉 VS 只留对撞则退化为一款斜缝 wipe，语义要求同降
- 转场不叠加（规矩同 shot-transitions）：一个接缝只用一式；
  这三式与六式同层选型，同片同类接缝别既用 flash-cut 又用 C 式
- 分镜表阶段就逐接缝标注（写进"关键动效"列），帧预算从相邻镜头划（R3）

## 参考实现
demos/transition/transition-hidden-cut/
（InvisibleCut.tsx / LightLeakBurn.tsx / VersusSlam.tsx）
