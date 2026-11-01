# Product screenshots and demo video

The homepage "See it in action" section shows example screens until you add real files here. Each one replaces its example screen automatically.

| File | Shows |
|---|---|
| `dashboard.png` | Role Center / home page with KPIs |
| `inventory.png` | Item list with stock by location |
| `sales-order.png` | A sales order with lines and totals |
| `warehouse-pick.png` | A warehouse pick with take/place lines |
| `demo.mp4` | 60–90 second walkthrough. After adding it, run `python3 src/build.py` so the video section is added to the homepage. |
| `demo-poster.jpg` | Still image (16:9) shown behind the play button |

Tips: capture from your own demo company (for example CRONUS) at 1600px wide or more, use example data only, and keep each PNG under about 400 KB.

## Homepage hero images

The homepage shows one of the `hero-*.webp` images (plus `hero-flow.webp`) at random on each visit. To add or remove one, edit `HERO_SET` in `src/build.py` and rebuild.
