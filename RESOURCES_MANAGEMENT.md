# 📦 Resources Management Guide

Your project currently uses a `resources/` directory containing **4.4GB** of audio and content files. This is significantly larger than what standard Git repositories handle well. This guide explains how to effectively manage these assets.

---

## 🏗 Current Architecture

- **Path:** `/resources` (Root directory)
- **Size:** ~4.4 GB
- **Access:** Symlinked via `public/resources` → `../resources`
- **Structure:**
  ```text
  resources/
  ├── audio/          # M4A/MP3 Audio files (~363 files)
  └── conversation/   # Transcript modules
  ```

## 🚩 The Problem
GitHub (and most Git providers) has a strict limit of **100MB per file** and recommends repositories stay under **1GB-5GB**. Pushing 4.4GB will likely fail or become unmanageable (slow cloning).

---

## ✅ Strategy A: Cloud Storage (Recommended for Production)

Move your audio files to a Content Delivery Network (CDN) or Object Storage like **AWS S3**, **Cloudflare R2**, or **Google Cloud Storage**.

### Why?
- **Fast:** Users download audio from a server near them.
- **Cheap:** Much cheaper than Git LFS bandwidth.
- **Scalable:** Unlimited storage.
- **Clean Repo:** Your code remains lightweight.

### Implementation Steps
1. **Upload `resources/audio`** to an S3 Bucket (e.g., `podcast-assets`).
2. **Update Data:** Change your `all-episodes-mapped.json` audio URLs.
   - **From:** `/resources/audio/Elementary/001_...`
   - **To:** `https://cdn.yourdomain.com/audio/Elementary/001_...`
3. **Delete Local Audio:** Remove heavy files from the repo.

---

## 🛠 Strategy B: Git LFS (Large File Storage)

If you want to keep files in the same repo, you **MUST** use Git Large File Storage (LFS).

### Setup
1. **Install Git LFS:**
   ```bash
   git lfs install
   ```
2. **Track Audio Files:**
   ```bash
   git lfs track "*.m4a"
   git lfs track "*.mp3"
   ```
3. **Commit Attributes:**
   ```bash
   git add .gitattributes
   git commit -m "Configure Git LFS for audio"
   ```

### ⚠️ Warnings
- **Bandwidth Limits:** GitHub Free has a monthly bandwidth limit (1GB). You will hit this quickly with a 4.4GB repo.
- **Cost:** You will likely need to pay for Data Packs on GitHub.

---

## 🚀 Strategy C: Deployment (Vercel/Netlify)

If you are deploying this as a static site (e.g., to Vercel):

1. **Vercel Limits:** Vercel has a 4GB limit for deployments (and lower for free tier). Deploying 4.4GB of code+assets often fails.
2. **Symlinks:** Symlinks outside the publish directory sometimes behave unexpectedly depending on the build environment.

**Best Deployment Path:**
1. **Keep Code in Git:** `src`, `public` (without heavy resources).
2. **Host Audio Externally:** (Strategy A).
3. **Build:** Your app simply points to the external URLs.

---

## 📝 Recommendation

**Go with Strategy A (Cloud Storage).**

1. Create a **Cloudflare R2** bucket (it's S3-compatible and has zero egress fees).
2. Upload your `resources/audio` folder there.
3. Write a small script to update `all-episodes-mapped.json` to point to the new URL.
4. Add `resources/audio` to your `.gitignore` so you keep them local for dev but don't push them.

### Example .gitignore Update
```gitignore
# Ignore large audio files
resources/audio/
```
