# GitHub Repository Manager

A modern, minimal, and responsive web application to manage your GitHub repositories easily from any device.  
Built with Flask, this app lets you log in with your GitHub account, view all your repositories, and perform bulk and individual actions — such as changing visibility, viewing on GitHub, and deleting repositories — all from a beautiful, user-friendly interface.

---

## ✨ Features

- **GitHub OAuth Login:** Securely log in with your GitHub account (OAuth).
- **All Repositories at a Glance:** See all your repos, both public and private, in a clean card-style list view.
- **Bulk Actions:** Select multiple repos for mass deletion or visibility change.
- **Individual Repo Actions:**  
  - View on GitHub  
  - Toggle visibility (public/private)  
  - Delete (with modal confirmation)
- **Search & Filter:**  
  - Instant search by name/description  
  - Filter by visibility and language  
  - Sort by name, date, or last update
- **Mobile Responsive:** Looks and works amazing on any device!
- **Modern UI:** Minimal, card-style design, subtle animations, and intuitive controls.
- **Public for Everyone:** Anyone with a GitHub account can log in and manage their own repositories.

---

## 🌐 Live Demo

[github-repo-manager-lemon.vercel.app](https://github-repo-manager-lemon.vercel.app)

---

## 🚀 Getting Started (Local Development)

1. **Clone the repo**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    cd YOUR_REPO_NAME
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**

    Create a `.env` file in the project root:
    ```env
    GITHUB_CLIENT_ID=your_github_oauth_client_id
    GITHUB_CLIENT_SECRET=your_github_oauth_client_secret
    GITHUB_CALLBACK_URL=http://localhost:3000/auth/callback
    FLASK_SECRET_KEY=your_super_secret_key
    ```

4. **Run the app**
    ```bash
    flask run
    ```
    Or, for development with auto-reload:
    ```bash
    FLASK_ENV=development flask run
    ```

5. **Visit**
    - Go to [http://localhost:3000](http://localhost:3000) in your browser.


## 🛡️ Security & Privacy

- Your GitHub credentials are never stored.
- All actions require explicit user authentication via GitHub OAuth.
- By default, all GitHub users can log in and manage their own repositories.

---

## 🙋 FAQ

**Q: Can anyone log in?**  
A: Yes, anyone with a GitHub account can log in and manage their own repositories.

**Q: Is this app open-source?**  
A: Yes! Contributions are welcome.

---

## 👨‍💻 Developer

Developed by **Khandaker Atik**  
Email: [Khandakeratik43@gmail.com](mailto:Khandakeratik43@gmail.com)

---

## 📄 License

[MIT License](LICENSE)