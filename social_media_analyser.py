import json
import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# SOCIAL MEDIA ANALYSER - SINGLE VS CODE FILE
# ============================================================
# This version combines:
# 1. OOP based Social Media Analyser
# 2. Users and Posts management
# 3. Post analysis
# 4. Overall report
# 5. Individual user report
# 6. Likes-based performance:
#       Below 100       -> Poor
#       100 to 50,000   -> Average
#       50,001 to 100k  -> Good
#       Above 100,000   -> Excellent
#
# No separate JSON file is required. The data is included below.
# ============================================================


class SocialMediaError(Exception):
    pass


class SocialMediaPost:
    def __init__(self, post_id, content, platform, likes, comments, shares):
        if not post_id.strip():
            raise SocialMediaError("Post ID cannot be empty.")
        if not content.strip():
            raise SocialMediaError("Post content cannot be empty.")
        if not platform.strip():
            raise SocialMediaError("Platform cannot be empty.")
        if likes < 0 or comments < 0 or shares < 0:
            raise SocialMediaError("Likes, comments and shares cannot be negative.")

        self.post_id = post_id.strip().upper()
        self.content = content.strip()
        self.platform = platform.strip()
        self.likes = likes
        self.comments = comments
        self.shares = shares

    @property
    def engagement(self):
        return self.likes + self.comments + self.shares


class User:
    def __init__(self, user_id, name, username):
        if not user_id.strip():
            raise SocialMediaError("User ID cannot be empty.")
        if not name.strip():
            raise SocialMediaError("Name cannot be empty.")
        if not username.strip():
            raise SocialMediaError("Username cannot be empty.")

        self.user_id = user_id.strip().upper()
        self.name = name.strip()
        self.username = username.strip()
        self.posts = []

    def add_post(self, post):
        self.posts.append(post)

    @property
    def total_likes(self):
        return sum(post.likes for post in self.posts)

    @property
    def total_comments(self):
        return sum(post.comments for post in self.posts)

    @property
    def total_shares(self):
        return sum(post.shares for post in self.posts)

    @property
    def total_engagement(self):
        return self.total_likes + self.total_comments + self.total_shares


class SocialMediaAnalyser:
    def __init__(self):
        self.users = {}
        self.posts = {}

    def add_user(self, user_id, name, username):
        user = User(user_id, name, username)
        if user.user_id in self.users:
            raise SocialMediaError(f"User ID '{user.user_id}' already exists.")
        self.users[user.user_id] = user
        return user

    def add_post(self, user_id, post_id, content, platform, likes, comments, shares):
        uid = user_id.strip().upper()
        if uid not in self.users:
            raise SocialMediaError(f"No user found with ID '{uid}'.")

        post = SocialMediaPost(
            post_id, content, platform, likes, comments, shares
        )

        if post.post_id in self.posts:
            raise SocialMediaError(f"Post ID '{post.post_id}' already exists.")

        self.posts[post.post_id] = post
        self.users[uid].add_post(post)
        return post

    def most_popular_post(self):
        if not self.posts:
            raise SocialMediaError("No posts available for analysis.")
        return max(self.posts.values(), key=lambda post: post.engagement)


# ============================================================
# LIKES PERFORMANCE RULE
# ============================================================

def get_performance(likes):
    """Return the report category based on likes."""
    if likes < 100:
        return "Poor"
    elif likes <= 50000:
        return "Average"
    elif likes <= 100000:
        return "Good"
    else:
        return "Excellent"


# ============================================================
# ORIGINAL USER DATA FROM THE PROVIDED JSON
# ============================================================

DATA = {
    "users": [
        {
            "user_id": "U001",
            "name": "Kasturi",
            "username": "@kasturi"
        },
        {
            "user_id": "U002",
            "name": "Rahul",
            "username": "@rahul"
        },
        {
            "user_id": "U003",
            "name": "Ananya",
            "username": "@ananya"
        },
        {
            "user_id": "U004",
            "name": "madhu",
            "username": "@madhu"
        },
        {
            "user_id": "U005",
            "name": "Ramya",
            "username": "@ramya"
        },
        {
            "user_id": "U006",
            "name": "NANDINI",
            "username": "@NAN"
        }
    ],
    "posts": [
        {
            "post_id": "P001",
            "content": "Learning Python is fun!",
            "platform": "Instagram",
            "likes": 250,
            "comments": 35,
            "shares": 20,
            "user_id": "U001"
        },
        {
            "post_id": "P002",
            "content": "My first Tkinter project",
            "platform": "Facebook",
            "likes": 180,
            "comments": 25,
            "shares": 15,
            "user_id": "U002"
        },
        {
            "post_id": "P003",
            "content": "Exploring AI and Data Science",
            "platform": "Instagram",
            "likes": 420,
            "comments": 70,
            "shares": 45,
            "user_id": "U003"
        },
        {
            "post_id": "P005",
            "content": "EXTITED TO SHARE MY EXPO",
            "platform": "LinkedIn",
            "likes": 127,
            "comments": 54,
            "shares": 7,
            "user_id": "U006"
        }
    ]
}


# ============================================================
# GUI APPLICATION
# ============================================================

class SocialMediaAnalyserApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.system = SocialMediaAnalyser()
        self.load_data()

        self.title("Social Media Analyser")
        self.geometry("1000x700")
        self.minsize(850, 600)

        self.build_gui()
        self.refresh_all()

    # --------------------------------------------------------
    # Load embedded data
    # --------------------------------------------------------
    def load_data(self):
        for user in DATA["users"]:
            self.system.add_user(
                user["user_id"],
                user["name"],
                user["username"]
            )

        for post in DATA["posts"]:
            self.system.add_post(
                post["user_id"],
                post["post_id"],
                post["content"],
                post["platform"],
                post["likes"],
                post["comments"],
                post["shares"]
            )

    # --------------------------------------------------------
    # GUI
    # --------------------------------------------------------
    def build_gui(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=6)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.users_tab = ttk.Frame(notebook)
        self.posts_tab = ttk.Frame(notebook)
        self.analyse_tab = ttk.Frame(notebook)
        self.report_tab = ttk.Frame(notebook)

        notebook.add(self.users_tab, text="Users")
        notebook.add(self.posts_tab, text="Posts")
        notebook.add(self.analyse_tab, text="Analyse")
        notebook.add(self.report_tab, text="Individual Report")

        self.build_users_tab()
        self.build_posts_tab()
        self.build_analyse_tab()
        self.build_report_tab()

    # --------------------------------------------------------
    # USERS TAB
    # --------------------------------------------------------
    def build_users_tab(self):
        frame = self.users_tab

        form = ttk.LabelFrame(frame, text="Add Social Media User")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="User ID").grid(row=0, column=0, padx=5, pady=5)
        self.uid_entry = ttk.Entry(form)
        self.uid_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Name").grid(row=0, column=2, padx=5, pady=5)
        self.uname_entry = ttk.Entry(form)
        self.uname_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Username").grid(row=0, column=4, padx=5, pady=5)
        self.username_entry = ttk.Entry(form)
        self.username_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(form, text="Add User", command=self.add_user).grid(
            row=0, column=6, padx=10, pady=5
        )

        columns = ("id", "name", "username", "posts", "likes", "engagement")
        self.users_table = ttk.Treeview(frame, columns=columns, show="headings")

        headings = {
            "id": "User ID",
            "name": "Name",
            "username": "Username",
            "posts": "Posts",
            "likes": "Total Likes",
            "engagement": "Total Engagement"
        }

        for column in columns:
            self.users_table.heading(column, text=headings[column])
            self.users_table.column(column, width=145, anchor="center")

        self.users_table.pack(fill="both", expand=True, padx=10, pady=10)

    def add_user(self):
        try:
            user = self.system.add_user(
                self.uid_entry.get(),
                self.uname_entry.get(),
                self.username_entry.get()
            )
            messagebox.showinfo("Success", f"User added: {user.name}")
            self.uid_entry.delete(0, tk.END)
            self.uname_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.refresh_all()
        except SocialMediaError as error:
            messagebox.showerror("Error", str(error))

    def refresh_users_table(self):
        self.users_table.delete(*self.users_table.get_children())

        for user in self.system.users.values():
            self.users_table.insert(
                "",
                "end",
                values=(
                    user.user_id,
                    user.name,
                    user.username,
                    len(user.posts),
                    user.total_likes,
                    user.total_engagement
                )
            )

    # --------------------------------------------------------
    # POSTS TAB
    # --------------------------------------------------------
    def build_posts_tab(self):
        frame = self.posts_tab

        form = ttk.LabelFrame(frame, text="Add Social Media Post")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="User").grid(row=0, column=0, padx=5, pady=5)
        self.post_user_cb = ttk.Combobox(form, state="readonly", width=25)
        self.post_user_cb.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Post ID").grid(row=0, column=2, padx=5, pady=5)
        self.post_id_entry = ttk.Entry(form)
        self.post_id_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Content").grid(row=1, column=0, padx=5, pady=5)
        self.content_entry = ttk.Entry(form, width=40)
        self.content_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        ttk.Label(form, text="Platform").grid(row=2, column=0, padx=5, pady=5)
        self.platform_entry = ttk.Entry(form)
        self.platform_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Likes").grid(row=2, column=2, padx=5, pady=5)
        self.likes_entry = ttk.Entry(form)
        self.likes_entry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(form, text="Comments").grid(row=3, column=0, padx=5, pady=5)
        self.comments_entry = ttk.Entry(form)
        self.comments_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form, text="Shares").grid(row=3, column=2, padx=5, pady=5)
        self.shares_entry = ttk.Entry(form)
        self.shares_entry.grid(row=3, column=3, padx=5, pady=5)

        ttk.Button(form, text="Add Post", command=self.add_post).grid(
            row=4, column=1, columnspan=2, padx=10, pady=10
        )

        columns = (
            "id", "content", "platform", "likes",
            "comments", "shares", "performance"
        )

        self.posts_table = ttk.Treeview(frame, columns=columns, show="headings")

        headings = {
            "id": "Post ID",
            "content": "Content",
            "platform": "Platform",
            "likes": "Likes",
            "comments": "Comments",
            "shares": "Shares",
            "performance": "Performance"
        }

        for column in columns:
            self.posts_table.heading(column, text=headings[column])
            self.posts_table.column(column, width=120, anchor="center")

        self.posts_table.pack(fill="both", expand=True, padx=10, pady=10)

    def add_post(self):
        try:
            user_value = self.post_user_cb.get()
            if not user_value:
                raise SocialMediaError("Please select a user.")

            user_id = user_value.split(" - ")[0]

            likes = int(self.likes_entry.get())
            comments = int(self.comments_entry.get())
            shares = int(self.shares_entry.get())

            post = self.system.add_post(
                user_id,
                self.post_id_entry.get(),
                self.content_entry.get(),
                self.platform_entry.get(),
                likes,
                comments,
                shares
            )

            messagebox.showinfo("Success", f"Post added: {post.post_id}")

            for entry in (
                self.post_id_entry,
                self.content_entry,
                self.platform_entry,
                self.likes_entry,
                self.comments_entry,
                self.shares_entry
            ):
                entry.delete(0, tk.END)

            self.refresh_all()

        except ValueError:
            messagebox.showerror(
                "Error", "Likes, comments and shares must be numbers."
            )
        except SocialMediaError as error:
            messagebox.showerror("Error", str(error))

    def refresh_posts_table(self):
        self.posts_table.delete(*self.posts_table.get_children())

        for post in self.system.posts.values():
            self.posts_table.insert(
                "",
                "end",
                values=(
                    post.post_id,
                    post.content,
                    post.platform,
                    post.likes,
                    post.comments,
                    post.shares,
                    get_performance(post.likes)
                )
            )

    # --------------------------------------------------------
    # ANALYSE TAB
    # --------------------------------------------------------
    def build_analyse_tab(self):
        frame = self.analyse_tab

        form = ttk.LabelFrame(frame, text="Analyse Social Media Post")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Select Post").grid(
            row=0, column=0, padx=5, pady=10
        )

        self.analyse_post_cb = ttk.Combobox(
            form, state="readonly", width=50
        )
        self.analyse_post_cb.grid(row=0, column=1, padx=5, pady=10)

        ttk.Button(
            form, text="Analyse", command=self.analyse_post
        ).grid(row=0, column=2, padx=10)

        self.analysis_text = tk.Text(
            frame, height=20, font=("Courier New", 11)
        )
        self.analysis_text.pack(
            fill="both", expand=True, padx=10, pady=10
        )
        self.analysis_text.config(state="disabled")

    def analyse_post(self):
        value = self.analyse_post_cb.get()
        if not value:
            messagebox.showwarning("Select Post", "Please select a post.")
            return

        post_id = value.split(" - ")[0]
        post = self.system.posts[post_id]

        status = (
            "HIGH ENGAGEMENT" if post.engagement >= 300
            else "MEDIUM ENGAGEMENT" if post.engagement >= 150
            else "LOW ENGAGEMENT"
        )

        result = [
            "=" * 60,
            "SOCIAL MEDIA POST ANALYSIS",
            "=" * 60,
            f"Post ID       : {post.post_id}",
            f"Content       : {post.content}",
            f"Platform      : {post.platform}",
            "-" * 60,
            f"Likes         : {post.likes:,}",
            f"Comments      : {post.comments:,}",
            f"Shares        : {post.shares:,}",
            f"Total         : {post.engagement:,}",
            f"Likes Report  : {get_performance(post.likes)}",
            "-" * 60,
            f"Engagement Status : {status}",
            "=" * 60
        ]

        self.analysis_text.config(state="normal")
        self.analysis_text.delete("1.0", tk.END)
        self.analysis_text.insert(tk.END, "\n".join(result))
        self.analysis_text.config(state="disabled")

    # --------------------------------------------------------
    # INDIVIDUAL USER REPORT TAB
    # --------------------------------------------------------
    def build_report_tab(self):
        frame = self.report_tab

        title = ttk.Label(
            frame,
            text="INDIVIDUAL USER REPORT",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(15, 5))

        info = ttk.Label(
            frame,
            text="Select an individual user to check their likes-based report."
        )
        info.pack(pady=(0, 10))

        selection = ttk.Frame(frame)
        selection.pack(fill="x", padx=15, pady=5)

        ttk.Label(
            selection,
            text="Select User:",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=(0, 10))

        self.report_user_cb = ttk.Combobox(
            selection, state="readonly", width=45
        )
        self.report_user_cb.pack(side="left", fill="x", expand=True)

        ttk.Button(
            selection,
            text="VIEW REPORT",
            command=self.show_user_report
        ).pack(side="left", padx=(10, 0))

        legend = ttk.Label(
            frame,
            text=(
                "Below 100 = Poor  |  100–50,000 = Average  |  "
                "50,001–100,000 = Good  |  Above 100,000 = Excellent"
            ),
            font=("Arial", 9)
        )
        legend.pack(pady=10)

        self.report_text = tk.Text(
            frame,
            wrap="word",
            font=("Consolas", 10),
            padx=12,
            pady=12
        )
        self.report_text.pack(
            fill="both", expand=True, padx=15, pady=10
        )

        self.report_text.tag_configure(
            "title", font=("Consolas", 14, "bold")
        )
        self.report_text.tag_configure(
            "subtitle", font=("Consolas", 11, "bold")
        )
        self.report_text.tag_configure(
            "poor", font=("Consolas", 10, "bold")
        )
        self.report_text.tag_configure(
            "average", font=("Consolas", 10, "bold")
        )
        self.report_text.tag_configure(
            "good", font=("Consolas", 10, "bold")
        )
        self.report_text.tag_configure(
            "excellent", font=("Consolas", 10, "bold")
        )

        self.report_text.config(state="disabled")

    def show_user_report(self):
        selected = self.report_user_cb.get()

        if not selected:
            messagebox.showwarning(
                "Select User", "Please select a user first."
            )
            return

        user_id = selected.split(" - ")[0]
        user = self.system.users.get(user_id)

        if user is None:
            messagebox.showerror("Error", "User not found.")
            return

        posts = user.posts

        self.report_text.config(state="normal")
        self.report_text.delete("1.0", tk.END)

        self.report_text.insert(
            tk.END, "INDIVIDUAL USER REPORT\n", "title"
        )
        self.report_text.insert(tk.END, "=" * 60 + "\n")
        self.report_text.insert(tk.END, f"Name     : {user.name}\n")
        self.report_text.insert(tk.END, f"Username : {user.username}\n")
        self.report_text.insert(tk.END, f"User ID  : {user.user_id}\n")
        self.report_text.insert(tk.END, "-" * 60 + "\n")

        if not posts:
            self.report_text.insert(
                tk.END, "No posts found for this user.\n"
            )
            self.report_text.config(state="disabled")
            return

        total_likes = user.total_likes
        total_comments = user.total_comments
        total_shares = user.total_shares

        for index, post in enumerate(posts, start=1):
            category = get_performance(post.likes)

            self.report_text.insert(
                tk.END, f"POST {index}\n", "subtitle"
            )
            self.report_text.insert(
                tk.END, f"Post ID      : {post.post_id}\n"
            )
            self.report_text.insert(
                tk.END, f"Platform     : {post.platform}\n"
            )
            self.report_text.insert(
                tk.END, f"Content      : {post.content}\n"
            )
            self.report_text.insert(
                tk.END, f"Likes        : {post.likes:,}\n"
            )
            self.report_text.insert(
                tk.END, f"Comments     : {post.comments:,}\n"
            )
            self.report_text.insert(
                tk.END, f"Shares       : {post.shares:,}\n"
            )
            self.report_text.insert(tk.END, "Performance  : ")
            self.report_text.insert(
                tk.END, category + "\n", category.lower()
            )
            self.report_text.insert(tk.END, "-" * 60 + "\n")

        average_likes = total_likes / len(posts)
        overall_category = get_performance(average_likes)

        self.report_text.insert(
            tk.END, "USER SUMMARY\n", "subtitle"
        )
        self.report_text.insert(tk.END, "=" * 60 + "\n")
        self.report_text.insert(
            tk.END, f"Total Posts     : {len(posts)}\n"
        )
        self.report_text.insert(
            tk.END, f"Total Likes     : {total_likes:,}\n"
        )
        self.report_text.insert(
            tk.END, f"Average Likes   : {average_likes:,.0f}\n"
        )
        self.report_text.insert(
            tk.END, f"Total Comments  : {total_comments:,}\n"
        )
        self.report_text.insert(
            tk.END, f"Total Shares    : {total_shares:,}\n"
        )
        self.report_text.insert(tk.END, "Overall Report  : ")
        self.report_text.insert(
            tk.END, overall_category + "\n", overall_category.lower()
        )

        self.report_text.config(state="disabled")

    # --------------------------------------------------------
    # REFRESH ALL
    # --------------------------------------------------------
    def refresh_all(self):
        self.refresh_users_table()
        self.refresh_posts_table()

        user_values = [
            f"{user.user_id} - {user.name} ({user.username})"
            for user in self.system.users.values()
        ]
        self.post_user_cb["values"] = user_values
        self.report_user_cb["values"] = user_values

        post_values = [
            f"{post.post_id} - {post.content}"
            for post in self.system.posts.values()
        ]
        self.analyse_post_cb["values"] = post_values

        if user_values:
            if not self.post_user_cb.get():
                self.post_user_cb.current(0)
            if not self.report_user_cb.get():
                self.report_user_cb.current(0)

        if post_values and not self.analyse_post_cb.get():
            self.analyse_post_cb.current(0)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    app = SocialMediaAnalyserApp()
    app.mainloop()
