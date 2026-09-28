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
| Test voix native S01 | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 + @Audio1 (voix de référence) | 71b6f7fc1552dbd5b38381a538ffca35 | success | `avatar/S01_voix_v1.mp4` | **retenu** | 378 cr |
| Test voix native A01 | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 + @Audio1 (voix de référence) | f7972aed71e5cc5ae5cc835fda7b2b18 | success | `avatar/A01_voix_v1.mp4` | **retenu** | 567 cr |
| Clip voix native A02 | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 + @Audio1 = extrait A01 (voix seule) | 2489c5e62a97016ddc37ea6dae19b889 | success | `avatar/A02_voix_v1.mp4` | recalée : « carences » mal prononcé | 252 cr |
| Clip voix native A03 | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 + @Audio1 = extrait A03 | 218eb5fab58f911e6e2b4b3778c59997 | success | `avatar/A03_voix_v1.mp4` | **retenu** | 441 cr |
| Clip voix native A04 | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 + @Audio1 = extrait A01 (voix seule) | 7cd1fe8a90f39160fa938ef3dd92b766 | success | `avatar/A04_voix_v1.mp4` | **retenu** | 252 cr |
| Clip voix native A05 | v1 | bytedance/seedance-2-5 720p, generate_audio, @Image1 + @Audio1 = extrait A05 | 47e34f7d7f7f54d03888c2dacdbeb12f | success | `avatar/A05_voix_v1.mp4` | **retenu** | 378 cr |
| Image I1 | v1 | nano-banana-2 1K | e1add4f177e3951a1a10c5ec676f4430 | success | `sorties/images/I1_v1.png` | remplacée par v2 (style scientifique) | 8 cr |
| Image I2 | v1 | nano-banana-2 1K | c4c8171cef32b1014d1702b345b34f59 | success | `sorties/images/I2_v1.png` | remplacée par v2 (style scientifique) | 8 cr |
| Image I3 | v1 | nano-banana-2 1K | 69394883d6aa29a0b6c8957dfffa11da | success | `sorties/images/I3_v1.png` | remplacée par v2 (style scientifique) | 8 cr |
| Image I4 | v1 | nano-banana-2 1K | 1eded99ee16ebaaa9a5b5806cbf52f14 | success | `sorties/images/I4_v1.png` | remplacée par v2 (photo culinaire, demande : style scientifique de E1) | 8 cr |
| Image I5 | v1 | nano-banana-2 1K | 4a1d9d1555a5fd39dc80c215bc32fdfd | success | `sorties/images/I5_v1.png` | remplacée par v2 (photo culinaire, demande : style scientifique de E1) | 8 cr |
| Image I6 | v1 | nano-banana-2 1K | 66a8f822003abddf47023edfc1458a52 | success | `sorties/images/I6_v1.png` | remplacée par v2 (photo culinaire, demande : style scientifique de E1) | 8 cr |
| Image I7 | v1 | nano-banana-2 1K | cdf1a024553af02b09941ac6da6454e0 | success | `sorties/images/I7_v1.png` | remplacée par v2 (photo culinaire, demande : style scientifique de E1) | 8 cr |
| Image I8 | v1 | nano-banana-2 1K | eb321c881677cd76ced4a4bf9e40b6cd | success | `sorties/images/I8_v1.png` | remplacée par v2 (photo culinaire, demande : style scientifique de E1) | 8 cr |
| Image E1 | v1 | nano-banana-2 1K | d71de2ad6fd3a931810e295ec26b08b8 | success | `sorties/images/E1_v1.png` | **retenue** | 8 cr |
| Image I4 | v2 | nano-banana-2 1K | 4e01065fe9d19c9c5389e8794fa5f024 | success | `sorties/images/I4_v2.png` | **retenue** | 8 cr |
| Image I5 | v2 | nano-banana-2 1K | 931221b7db22cdad4a3bdac859542792 | success | `sorties/images/I5_v2.png` | **retenue** | 8 cr |
| Image I6 | v2 | nano-banana-2 1K | 0439499def8ba8f6ae485ab6f77de4bd | success | `sorties/images/I6_v2.png` | **retenue** | 8 cr |
| Image I7 | v2 | nano-banana-2 1K | 6d9f6f6dcaee18682a8a7d2d12c36c67 | success | `sorties/images/I7_v2.png` | **retenue** | 8 cr |
| Image I8 | v2 | nano-banana-2 1K | f66a82baf89d2d31c7dd0c703db02f68 | success | `sorties/images/I8_v2.png` | **retenue** | 8 cr |
| Clip voix native A02 | v2 | bytedance/seedance-2-5 720p, generate_audio, @Image1 + @Audio1, consigne de prononciation « carences » | e1ebf5a1a8fd0ed465a19374ee07dba1 | success | `avatar/A02_voix_v2.mp4` | **retenu** | 252 cr |
| Image I1 | v2 | nano-banana-2 1K, style scientifique E1 | 9e78d92cc4d48711179e94e3baa5ecd7 | success | `sorties/images/I1_v2.png` | **retenu** | 8 cr |
| Image I2 | v2 | nano-banana-2 1K, style scientifique E1 | 29d005988ecbcb4a945a13d846642a10 | success | `sorties/images/I2_v2.png` | **retenu** | 8 cr |
| Image I3 | v2 | nano-banana-2 1K, style scientifique E1 | 829a7265ade84ba14b985d2d842692c1 | success | `sorties/images/I3_v2.png` | **retenu** | 8 cr |
| Animation E1 | v1 | minimax-h3/image-to-video 768P, 9 s | 5ef89a00b9d61c06848886c4c1b63e5e | success | `sorties/animation/E1_v1.mp4` | en attente de validation | 72 cr |

**Total : 5362 crédits ≈ 26.81 $.**

Leçon : sur KIE, Seedance 2.5 ne combine pas première image et audio ; avec l'audio en simple référence, les lèvres ne suivent pas la voix. Solution retenue : garder les clips Seedance et recaler la bouche avec Volcengine video-to-video lip sync (≈ 8 cr/s).


Correction : les prompts des premières générations Seedance écrivaient « Image 1 / Audio 1 » sans la balise `@`, et generate_audio était désactivé. Tests voix native : balises `@Image1` / `@Audio1`, Seedance génère voix et lèvres ensemble.
