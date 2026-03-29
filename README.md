# 📊 LinkedIn Post Tracker

A simple, user-friendly web app to track your LinkedIn post performance and get actionable insights to grow your engagement and followers.

## ✨ Features

### 📝 Easy Post Logging
- Log each LinkedIn post with a simple form
- Track post date, type (text, image, carousel, video, document, poll)
- Record your post caption for reference
- Input performance metrics: views, likes, comments, and shares

### 📈 Real-Time Analytics
- **Key Metrics Dashboard**: See total posts, views, engagement, and engagement rate at a glance
- **Performance Trends**: Visualize how your engagement and views change over time
- **Content Type Analysis**: See which post types get the best engagement

### 💡 AI-Powered Insights
- **Top Performer**: Identify your best-performing post type
- **Best Content Type**: Get data-driven recommendations on what format works best
- **Engagement Trends**: See if your engagement is growing or declining
- **Smart Recommendations**: Get specific tips based on your data

### 📊 Beautiful Visualizations
- Interactive charts showing your trends over time
- Doughnut chart comparing engagement by content type
- Color-coded metrics for quick insights

## 🚀 How to Use

1. **Open the app**: Open `index.html` in any web browser (no installation needed!)
2. **Add a post**: Fill in the form with:
   - Date you posted
   - Post type
   - What the post was about
   - Views, likes, comments, shares
3. **Get insights**: The dashboard automatically analyzes your data and shows:
   - Key metrics and trends
   - What's working best
   - Recommendations for growth

## 💾 Data Storage
- All data is saved locally in your browser (localStorage)
- No accounts, no logins, no data sent anywhere
- Your data stays on your computer

## 📱 Responsive Design
- Works on desktop, tablet, and mobile
- Beautiful LinkedIn-inspired design
- Easy to use on any device

## 🎯 Tips for Growth

Based on your data, the tracker will show you:
- Which content types get the most engagement
- When your posts perform best (by comparing performance over time)
- Your engagement rate trends
- Specific recommendations to increase followers

## 🔄 Export & Backup

To backup your data:
1. Open browser DevTools (F12)
2. Go to Console
3. Paste: `copy(localStorage.getItem('linkedinPosts'))`
4. Save this somewhere safe

To restore:
1. Open browser DevTools
2. Go to Console
3. Paste: `localStorage.setItem('linkedinPosts', 'YOUR_PASTED_DATA')`

---

**Made to help you grow on LinkedIn! Track, analyze, and optimize your content.** 📈
