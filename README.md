# Paladin EnviroTech — Homepage Directions

Static prototype of two homepage directions for Paladin EnviroTech, exported from Claude Design.

Use the control in the lower left to switch between:

- **1a — Proof**
- **1b — Domestic supply**

## Deploying to Vercel

This is a plain static site. No build step, no dependencies to install.

```bash
git init
git add .
git commit -m "Paladin homepage directions prototype"
git branch -M main
git remote add origin git@github.com:YOUR-ORG/paladin-homepage-prototype.git
git push -u origin main
```

Then in Vercel: **Add New → Project → Import** the repo. When asked for a framework preset, choose **Other**. Leave the build command and output directory empty and deploy. Vercel serves `index.html` from the repo root.

To deploy without GitHub, run `npx vercel` from this folder.

## Structure

```
index.html      the prototype (both directions in one file)
support.js      Claude Design runtime, required
fonts/          Restart Hard, referenced by @font-face
assets/         local images and the social preview
vercel.json     noindex headers and asset caching
```

## Notes

**Runtime dependencies.** `support.js` pulls React, ReactDOM, and Babel from unpkg.com at page load, so the prototype needs an internet connection and will not render from a `file://` URL. To preview locally, run `python3 -m http.server 8000` in this folder and open `http://localhost:8000`.

**Remote images.** Photography, logos, and the Paladin wordmark load directly from `paladinenvirotech.com`. If those files move or are renamed on the live site, they will break here. Worth copying them into `assets/` before this goes to anyone outside the team.

**Fonts.** The four Restart Hard weights are served as `.otf` from this repo, which makes them publicly downloadable. Check the license terms cover web embedding before putting this on a public URL.

**Indexing.** The site is set to noindex via both a meta tag and an HTTP header. If a client link needs to stay private, add Vercel password protection on the project as well.
