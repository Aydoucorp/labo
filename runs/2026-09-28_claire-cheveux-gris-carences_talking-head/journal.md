# Journal des générations · Claire · Cheveux gris et carences · Talking head

Tarif KIE standard : 1 crédit ≈ 0,005 $.

| Étape | Variante | Modèle | ID de tâche | État | Fichier | Statut | Coût |
|---|---|---|---|---|---|---|---|
| Image de départ 9:16 | v1 | gpt-image-2-image-to-image 1K | 00f81dea8dc023f723df08f1998d8d1f | success | `sorties/config/depart_9x16_v1.png` | **retenue** | 6 cr |
| Image de départ 9:16 | v2 | gpt-image-2-image-to-image 1K | 2748248dac7d6e3cf7c358795a38c69a | success | `sorties/config/depart_9x16_v2.png` | non retenue | 6 cr |
| Image de départ 9:16 | v3 | gpt-image-2-image-to-image 1K | 64d446d6b26c401bc920ae8c0352b1fe | success | `sorties/config/depart_9x16_v3.png` | non retenue | 6 cr |
| Image de départ 1:1 | v1 | gpt-image-2-image-to-image 1K | bd0e7b153f696e2ddc4190a75cffe862 | success | `sorties/config/depart_1x1_v1.png` | **retenue** | 6 cr |
| Image de départ 1:1 | v2 | gpt-image-2-image-to-image 1K | 70770164cb593812da53099657c771c7 | success | `sorties/config/depart_1x1_v2.png` | non retenue | 6 cr |
| Clip avatar A02 | v1 | bytedance/seedance-2-5 720p (image en référence + audio en référence) | f5947fc398283ecd3b63e69c88b1e3b4 | success | `avatar/A02_v1.mp4` | lèvres non synchronisées sur la voix → recalé | 252 cr |
| Clip avatar S01 | v1 | bytedance/seedance-2-5 720p (image en référence + audio en référence) | a0022874bf14003a0e0e7e031b933ae3 | success | `avatar/S01_v1.mp4` | lèvres non synchronisées sur la voix → recalé | 378 cr |
| Clip avatar A01 | v1 | bytedance/seedance-2-5 720p (image en référence + audio en référence) | ee11611c8b54e7f68f48d7647d6eff69 | success | `avatar/A01_v1.mp4` | lèvres non synchronisées sur la voix → recalé | 567 cr |
| Clip avatar A03 | v1 | bytedance/seedance-2-5 720p (image en référence + audio en référence) | b7614ff93d81d3f8c249796a67eeeb1e | success | `avatar/A03_v1.mp4` | lèvres non synchronisées sur la voix → recalé | 441 cr |
| Clip avatar A04 | v1 | bytedance/seedance-2-5 720p (image en référence + audio en référence) | cd05227ba7938e35fe5c188c6a4b9fe9 | success | `avatar/A04_v1.mp4` | lèvres non synchronisées sur la voix → recalé | 252 cr |
| Clip avatar A05 | v1 | bytedance/seedance-2-5 720p (image en référence + audio en référence) | 23432a1e68c54b4bc5387a9c1608be65 | success | `avatar/A05_v1.mp4` | lèvres non synchronisées sur la voix → recalé | 378 cr |
| Test S01 | v1 | kling/ai-avatar-pro | e128d3613dd699ebcfb84c7a954117c8 | success | `avatar/S01_kling_v1.mp4` | abandonné : rendu moins réaliste, sous-titres parasites | 80 cr |
| Recalage lèvres S01 | v1 | volcengine/video-to-video-lip-sync (lite) | 04feb1ca212cd405b36df4f3f50951ae | success | `avatar/S01_v1_lipsync.mp4` | **retenu** | 40 cr |
| Recalage lèvres A01 | v1 | volcengine/video-to-video-lip-sync (lite) | b8962676f2f90e4b44ca64e92d68911f | success | `avatar/A01_v1_lipsync.mp4` | en attente de validation | 64 cr |
| Recalage lèvres A02 | v1 | volcengine/video-to-video-lip-sync (lite) | 40754c6b09952ebc403681d579e7776f | success | `avatar/A02_v1_lipsync.mp4` | en attente de validation | 32 cr |
| Recalage lèvres A03 | v1 | volcengine/video-to-video-lip-sync (lite) | 9777a8d7b49340faa16a208dfd9ee7ab | success | `avatar/A03_v1_lipsync.mp4` | en attente de validation | 48 cr |
| Recalage lèvres A04 | v1 | volcengine/video-to-video-lip-sync (lite) | b27e3298a1d76acd3537b9e365517a73 | success | `avatar/A04_v1_lipsync.mp4` | en attente de validation | 32 cr |
| Recalage lèvres A05 | v1 | volcengine/video-to-video-lip-sync (lite) | bc9d6b223b83c9c086c40f0d1b4816cd | success | `avatar/A05_v1_lipsync.mp4` | en attente de validation | 40 cr |
| Test voix native S01 | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 + @Audio1 (voix de référence) | 71b6f7fc1552dbd5b38381a538ffca35 | success | `avatar/S01_voix_v1.mp4` | en attente de validation (mots exacts selon Whisper) | 378 cr |
| Test voix native A01 | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 + @Audio1 (voix de référence) | f7972aed71e5cc5ae5cc835fda7b2b18 | success | `avatar/A01_voix_v1.mp4` | en attente de validation (« blanchiment précoce » à vérifier à l'oreille) | 567 cr |

**Total : 3579 crédits ≈ 17.90 $.**

Leçon : sur KIE, Seedance 2.5 ne combine pas première image et audio ; avec l'audio en simple référence, les lèvres ne suivent pas la voix. Solution retenue : garder les clips Seedance et recaler la bouche avec Volcengine video-to-video lip sync (≈ 8 cr/s).


Correction : les prompts des premières générations Seedance écrivaient « Image 1 / Audio 1 » sans la balise `@`, et generate_audio était désactivé. Tests voix native : balises `@Image1` / `@Audio1`, Seedance génère voix et lèvres ensemble.
