# SE01-Web-Engineering_UoA

## Project title

**The Blogs**

## Short description

The proposed web application allows the user to create blog posts in a shared blog space.
{ユーザーが共有のブログスペースに記事（ブログポスト）を作成・投稿できるWebアプリケーションです}

## Main user actions

- Register in the system with a unique user name and password, and start writing their own blog posts.
{一意のユーザー名とパスワードでシステムに登録し、自分のブログ記事を執筆・投稿する}

- Display all blog posts sorted by date, with the most recent post shown first.
{日付順（最新順）に並べられたすべてのブログ記事を閲覧する}

- Display the list of authors and show only the blog posts written by a selected author.
{著者のリストを表示し、選択した特定の著者が書いた記事のみを表示する}

- Select a date in the calendar and display all posts written on that day.
{カレンダーから日付を選択し、その日に書かれたすべての記事を表示する}

- (Optional) Type a string in the search box to find and display all blog posts containing that string in the title.{(optional)検索ボックスに文字列を入力し、タイトルにその文字列が含まれる記事を検索する}

## Basic data model idea

- `Users` table: Unique user ID, user name, and password.
{`Users` テーブル: ユーザーを一意に識別するID、ユーザー名、パスワード}

- `Posts` table: Post ID, title, text content, creation date, and author (foreign key to the Users table).
{`Posts` テーブル: 記事ID、タイトル、本文(テキストコンテンツ)、作成日、著者(`Users` テーブルへの外部キー)}

## Note on the user interface

- The main screen will display a list of posts, limiting the number of posts per page. If there are more matching posts, the app should clearly display "Next" and "Previous" links for pagination.
{メイン画面には記事のリストが表示され、1ページあたりの表示件数を制限する 。記事が多い場合は「次へ」「前へ」のリンクを明確に表示し、ページネーション（ページ送り）ができるようにする}

- Author names should act as links to the author's post list.
{記事に表示される著者名はリンクとして機能し、クリックするとその著者の記事一覧へ遷移する}

- A calendar UI will be used to make date-based filtering easy and intuitive for the user.
{カレンダーUIを用いて、ユーザーが直感的に日付ベースのフィルタリングを行えるようにする}


---

## Environment & Tools

- **Python version**: 3.11+
- **Package Manager**: uv
- **Framework**: Django
- **Development Tools**: Ruff (Formatting & Linting), Coverage (Test coverage)

---

## Setup Instructions (macOS / Linux)

Follow these steps to set up the development environment on your local machine:

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd the-blogs
   ```

2. **Create a virtual environment using uv:**
   ```bash
   uv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   uv sync
   ```

5. **Run the development server (Once Django is configured):**
   ```bash
   python manage.py runserver
   ```