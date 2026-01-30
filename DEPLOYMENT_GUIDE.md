# Complete Deployment Guide: GitHub to Streamlit Cloud

## Prerequisites
- GitHub account
- Git installed on your computer (optional, can use GitHub web interface)

---

## Method 1: Using GitHub Web Interface (Easiest)

### Step 1: Create a New Repository on GitHub

1. Go to [github.com](https://github.com)
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `bank-digitization-calculator` (or any name you prefer)
   - **Description**: "Streamlit app to calculate bank digitization scores"
   - **Public** or **Private** (both work with Streamlit Cloud)
   - ✅ Check "Add a README file"
4. Click **"Create repository"**

### Step 2: Upload Files to GitHub

1. In your new repository, click **"Add file"** → **"Upload files"**
2. Drag and drop these files:
   - `digitization_score_calculator.py`
   - `requirements.txt`
   - `.gitignore`
3. You can update the README.md if needed
4. Scroll down and click **"Commit changes"**

### Step 3: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in"** and authorize with your GitHub account
3. Click **"New app"** (or **"Create app"**)
4. Fill in the deployment settings:
   - **Repository**: Select `your-username/bank-digitization-calculator`
   - **Branch**: `main` (or `master`)
   - **Main file path**: `digitization_score_calculator.py`
   - **App URL**: Choose a custom URL (e.g., `bank-digitization-calculator`)
5. Click **"Deploy!"**

### Step 4: Wait for Deployment

- Streamlit will install dependencies and launch your app
- This usually takes 2-5 minutes
- Once complete, you'll see your app running!

---

## Method 2: Using Git Command Line

### Step 1: Initialize Git Repository Locally

```bash
# Navigate to your project folder
cd /path/to/your/project

# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Bank digitization calculator"
```

### Step 2: Create Repository on GitHub and Push

```bash
# Create a new repo on github.com first, then:

# Add remote
git remote add origin https://github.com/YOUR-USERNAME/bank-digitization-calculator.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud

Follow Step 3 from Method 1 above.

---

## Important Files Explanation

### `digitization_score_calculator.py`
- Your main Streamlit application code
- This is what Streamlit Cloud will run

### `requirements.txt`
- Lists all Python packages needed
- Streamlit Cloud automatically installs these
- Current dependencies:
  ```
  streamlit==1.31.0
  pandas==2.1.4
  PyPDF2==3.0.1
  ```

### `.gitignore`
- Tells Git which files to ignore
- Prevents uploading unnecessary files (logs, cache, etc.)

### `README.md`
- Documentation for your repository
- Shows up on your GitHub repo homepage

---

## Troubleshooting

### Issue: App won't deploy
**Solution**: Check the deployment logs in Streamlit Cloud for errors

### Issue: Missing dependencies
**Solution**: Make sure all imports are listed in `requirements.txt`

### Issue: File not found errors
**Solution**: Ensure file paths are relative and all files are in the repo

### Issue: App crashes on file upload
**Solution**: Check PDF file compatibility and error handling in code

---

## Managing Your Deployed App

### Updating the App
1. Make changes to your code locally
2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. Streamlit Cloud automatically redeploys!

### Viewing Logs
- Click on your app in Streamlit Cloud dashboard
- Click "Manage app" → "Logs"

### Restarting the App
- In Streamlit Cloud dashboard
- Click "⋮" menu → "Reboot app"

### Deleting the App
- In Streamlit Cloud dashboard
- Click "⋮" menu → "Delete app"

---

## Next Steps

After deployment:
1. ✅ Test your app with sample PDFs
2. ✅ Share the URL with your team
3. ✅ Monitor usage and logs
4. ✅ Update as needed

Your app URL will be: `https://YOUR-APP-NAME.streamlit.app`

---

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Guides](https://guides.github.com)

---

## Quick Reference Commands

```bash
# Check git status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View remote URL
git remote -v
```

---

Good luck with your deployment! 🚀
