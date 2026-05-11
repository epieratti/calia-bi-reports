# Social Blade e TikTok (Upfluence) — Squad Always ON Loterias, lote 3 (11/05/2026)

**Fonte:** [Social Blade](https://socialblade.com) — páginas públicas por handle (`/instagram/user/<handle>`) e por ID de canal no YouTube (`/youtube/channel/UC…`).

**Metodologia (alinhada ao repo):** mesma abordagem descrita em `loterias2026-20260406/research/SOCIAL_BLADE_INSTAGRAM.md` / `SOCIAL_BLADE_YOUTUBE.md`: leitura das estatísticas exibidas no painel público do Social Blade, com **URL por perfil** preservada no dossiê. **Nota operacional:** o IP do ambiente de automação pode receber *Access denied* ou desafio *Just a moment* (Cloudflare) em requisições **headless**; quando necessário, usar **contexto de browser isolado por URL**, **UA de desktop Chrome** (não `HeadlessChrome` no user-agent) e espera de vários segundos após `domcontentloaded` até os campos **Followers / Subscribers** deixarem de mostrar apenas *spinner*. Para YouTube, quando `socialblade.com/youtube/c/<handle>` retorna **Not Found**, obter o **`channelId` `UC…`** a partir da página pública `https://www.youtube.com/@<handle>` e abrir `socialblade.com/youtube/channel/UC…`.

## Instagram

| Nome | Usuário | Seguidores | Seguindo | Mídias | Engaj. | Curtidas méd. | Coment. méd. | URL |
| --- | --- | ---:| ---:| ---:| ---:| ---:| ---:| --- |
| Raquel Real | raquelrealoficial | 457.283 | 1.255 | 1.868 | 8,29% | 37.324,5 | 573,63 | [SB](https://socialblade.com/instagram/user/raquelrealoficial) |
| Morgana Camila | morganacamila | 643.349 | 4.023 | 1.407 | 4,46% | 27.548,93 | 1.129,07 | [SB](https://socialblade.com/instagram/user/morganacamila) |
| Paulo Victor Freitas | seufreitaz | 1.185.010 | 1.413 | 907 | 6,1% | 70.379,5 | 1.937,19 | [SB](https://socialblade.com/instagram/user/seufreitaz) |

**`@pvfreitazzz`:** tentativa `socialblade.com/instagram/user/pvfreitazzz` → página **Not Found** na mesma janela de coleta (não há ficha agregada para esse handle).

## YouTube

| Nome | Canal (SB) | Inscritos (SB) | Views totais (SB) | Vídeos (SB) | URL |
| --- | --- | ---:| ---:| ---:| --- |
| Raquel Real | `UCGfbSg8Vfpk2aEtqlKrCE9Q` | 12,9K | 500.657 | 70 | [SB](https://socialblade.com/youtube/channel/UCGfbSg8Vfpk2aEtqlKrCE9Q) |
| Paulo Victor Freitas | `UCcnKdtKNLTpIDaZg_ayAD3A` | 18,3K | 12.550.362 | 523 | [SB](https://socialblade.com/youtube/channel/UCcnKdtKNLTpIDaZg_ayAD3A) |
| Morgana Camila | `@morganacamila` (YouTube) | — | — | — | O canal público [youtube.com/@morganacamila](https://www.youtube.com/@morganacamila) está **vazio** (audiência mínima). O Social Blade responde que o criador **não atinge o mínimo** para constar na base (mensagem do site na coleta). **Não** usar como proxy da narradora citada na imprensa sem outra prova de URL. |

**Data dos números:** **11/05/2026** (conferir de novo na data da veiculação).

## TikTok (Upfluence — Free TikTok Profile Audit)

**Fonte:** [Upfluence](https://www.upfluence.com/) — produto «Free TikTok Profile Audit» (captura manual **11/05/2026**). Estimativas de audiência e engajamento do agregador; não substituem painéis proprietários da plataforma.

| Creator | Handle TikTok | Seguidores | Engaj. | Curtidas totais | Mulheres / homens | Vídeos | Notas |
| --- | --- | ---:| ---:| ---:| ---:| ---:| --- |
| Raquel Real | @raqrealoficial | 252,5K | 8,00% | 12,7M | 54,52% / 45,48% | 804 | Médias/vídeo no dossiê: com. 76,72; curt. 20,1K; part. 707,2; reprod. 137,0K; seguindo 310 |
| Morgana Camila | @morganacamila_ | 108,4K | 0,98% | 2,7M | 44,42% / 55,58% | 88 | O @morganacamila **sem** sublinhado não corresponde à narradora da imprensa |
| Paulo Victor | @seufreitaz | 297,9K | — | 2,1M | — | — | Audit **not found**; seguidores/curtidas/cabeçalho: **154** seguindo (TikTok) |

## Complemento (imprensa e menções em terceiros — refletido no HTML)

Rastreio adicional com **URL no dossiê** (eixos de brand safety), sem substituir a coleta Social Blade/Upfluence acima:

- **Raquel Real:** [Terra — CPI das Bets / ironia](https://www.terra.com.br/diversao/gente/influenciadora-faz-piada-com-virginia-na-cpi-das-bets-e-bebe-reborn,f6a0354ca294b72240c1e0ee55d005115kla7moz.html); [TikTok — sketch Senado 17/06/2024](https://www.tiktok.com/@raqrealoficial/video/7381957732682747141).
- **Morgana Camila:** [Diário do Nordeste — desfile Maranguape](https://diariodonordeste.verdesmares.com.br/entretenimento/zoeira/arrasa-na-major-morgana-camila-viraliza-desfile-civico-de-maranguape-com-humor-e-originalidade-1.3275714); menções «tigrinho» em **posts de terceiros** (calibragem no HTML: [Instagram](https://www.instagram.com/reel/DXsSOCPjqVw/), [TikTok](https://www.tiktok.com/@aurineidecamurupim/video/7479943335419890949), [TV Brasil no TikTok](https://www.tiktok.com/@tvbrasil/video/7547391274421193989)).
- **Paulo Victor Freitas:** [Instagram @seufreitaz](https://www.instagram.com/seufreitaz/); [LinkedIn /in/pvfreitaz](https://www.linkedin.com/in/pvfreitaz); [g1 em Reels](https://www.instagram.com/reel/DPjBNmajr50/); menções «tigrinho» em **terceiros** ([reel 1](https://www.instagram.com/reel/DWhaB70jz5t/), [post](https://www.instagram.com/p/DWUqhN2Eetk/), [reel 2](https://www.instagram.com/reel/DVEsSj4kbtI/)).

**Homônimo a não misturar:** matéria sobre outra pessoa (ex.: «Raquel Brito» + tigrinho) não se aplica à Raquel Real deste dossiê.
