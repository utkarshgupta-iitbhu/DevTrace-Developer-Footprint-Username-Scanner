import customtkinter as ctk
import requests
import concurrent.futures
import webbrowser
import time
import random
import csv
import json
import os
from tkinter import filedialog, messagebox

TARGET_SITES = {
    "Codeforces": {"url": "https://codeforces.com/profile/{}", "category": "Coding"},
    "LeetCode": {"url": "https://leetcode.com/{}", "category": "Coding"},
    "CodeChef": {"url": "https://www.codechef.com/users/{}", "category": "Coding"},
    "AtCoder": {"url": "https://atcoder.jp/users/{}", "category": "Coding"},
    "HackerRank": {"url": "https://www.hackerrank.com/{}", "category": "Coding"},
    "TopCoder": {"url": "https://www.topcoder.com/members/{}", "category": "Coding"},
    "SPOJ": {"url": "https://www.spoj.com/users/{}/", "category": "Coding"},
    "PyPI": {"url": "https://pypi.org/user/{}/", "category": "Coding"},
    
    "GitHub": {"url": "https://github.com/{}", "category": "Version Control"},
    "GitLab": {"url": "https://gitlab.com/{}", "category": "Version Control"},
    "DockerHub": {"url": "https://hub.docker.com/u/{}", "category": "Version Control"},
    "Replit": {"url": "https://replit.com/@{}", "category": "Version Control"},
    
    "Kaggle": {"url": "https://www.kaggle.com/{}", "category": "AI"},
    "HuggingFace": {"url": "https://huggingface.co/{}", "category": "AI"},
    
    "Medium": {"url": "https://medium.com/@{}", "category": "Blogging"},
    "Dev.to": {"url": "https://dev.to/{}", "category": "Blogging"},
    "Hashnode": {"url": "https://hashnode.com/@{}", "category": "Blogging"},
    
    "Steam": {"url": "https://steamcommunity.com/id/{}", "category": "Gaming"},
    "Chess.com": {"url": "https://www.chess.com/member/{}", "category": "Gaming"},
    "Lichess": {"url": "https://lichess.org/@/{}", "category": "Gaming"},
    
    "Instagram": {"url": "https://www.instagram.com/{}/", "category": "Social Media"},
    "Twitter": {"url": "https://twitter.com/{}", "category": "Social Media"},
    "Reddit": {"url": "https://www.reddit.com/user/{}", "category": "Social Media"},
    "Pinterest": {"url": "https://www.pinterest.com/{}/", "category": "Social Media"},
    
    "TryHackMe": {"url": "https://tryhackme.com/p/{}", "category": "Cybersecurity"}
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FootprintScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("OSINT: Developer Footprint Scanner")
        self.root.state('zoomed')
        
        self.result_rows = []
        self.raw_scan_data = []
        self.found_count = 0    
        
        self.setup_ui()

    def setup_ui(self):
        self.switch_theme = ctk.CTkSwitch(self.root, text="Dark Mode", command=self.toggle_theme)
        self.switch_theme.select()
        self.switch_theme.place(relx=0.95, rely=0.02, anchor="ne")

        self.lbl_title = ctk.CTkLabel(self.root, text="🔍 Footprint Scanner", font=ctk.CTkFont(size=28, weight="bold"))
        self.lbl_title.pack(pady=(30, 5))

        self.lbl_sub = ctk.CTkLabel(self.root, text="Cross-Platform Username Correlation", text_color="gray")
        self.lbl_sub.pack(pady=(0, 10))

        self.search_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.search_frame.pack(pady=10)

        self.entry_username = ctk.CTkEntry(self.search_frame, width=300, placeholder_text="Enter target username", font=ctk.CTkFont(size=14))
        self.entry_username.pack(side="left", padx=10)
        self.entry_username.bind("<Return>", lambda event: self.start_scan())

        self.btn_scan = ctk.CTkButton(self.search_frame, text="Scan Network", width=120, font=ctk.CTkFont(weight="bold"), command=self.start_scan)
        self.btn_scan.pack(side="left")

        self.filter_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.filter_frame.pack(pady=5)
        
        ctk.CTkLabel(self.filter_frame, text="Filter Results: ", font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        categories = ["All", "Coding", "Version Control", "AI", "Gaming", "Social Media", "Blogging", "Cybersecurity"]
        self.combo_category = ctk.CTkOptionMenu(self.filter_frame, values=categories, command=self.apply_filter, width=200)
        self.combo_category.pack(side="left", padx=5)

        self.btn_export = ctk.CTkButton(self.filter_frame, text="💾 Export Data", width=100, fg_color="#8e44ad", hover_color="#9b59b6", state="disabled", command=self.export_results)
        self.btn_export.pack(side="left", padx=15)

        self.lbl_status = ctk.CTkLabel(self.root, text="Ready.", font=ctk.CTkFont(size=14))
        self.lbl_status.pack(pady=(10, 5))

        self.progressbar = ctk.CTkProgressBar(self.root, width=450)
        self.progressbar.pack(pady=5)
        self.progressbar.set(0)

        self.results_frame = ctk.CTkScrollableFrame(self.root, width=550, height=400)
        self.results_frame.pack(pady=15, fill="both", expand=True, padx=20)

    def toggle_theme(self):
        if self.switch_theme.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def check_website(self, site_name, url_template, username, category):
        time.sleep(random.uniform(0.1, 0.6))
        
        url = url_template.format(username)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        try:
            if site_name == "Codeforces":
                api_url = f"https://codeforces.com/api/user.info?handles={username}"
                api_response = requests.get(api_url, timeout=5)
                if api_response.status_code == 200 and api_response.json().get("status") == "OK":
                    return (site_name, url, True, category)
                return (site_name, url, False, category)

            if site_name == "Chess.com":
                api_url = f"https://api.chess.com/pub/player/{username.lower()}"
                api_response = requests.get(api_url, headers=headers, timeout=5)
                if api_response.status_code == 200:
                    return (site_name, url, True, category)
                return (site_name, url, False, category)
                
            if site_name == "Lichess":
                api_url = f"https://lichess.org/api/user/{username}"
                api_response = requests.get(api_url, timeout=5)
                if api_response.status_code == 200:
                    return (site_name, url, True, category)
                return (site_name, url, False, category)

            response = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
            
            if response.status_code == 200:
                text_lower = response.text.lower()
                final_url = response.url.lower() 
                
                if "login" in final_url or "signin" in final_url:
                    return (site_name, url, False, category)

                if username.lower() not in final_url:
                    return (site_name, url, False, category)

                soft_404_phrases = [
                    "we could not find the page you were looking for",
                    "page not found",
                    "doesn't exist",
                    "not found",
                    "this user has not yet",
                    "this page does not exist",
                    "sorry, this page isn't available.",
                    "the page you were looking for doesn't exist",
                    "account suspended",
                    "user not found",
                    "could not be found",
                    "404 error",
                    "content not found"
                ]
                
                if any(phrase in text_lower for phrase in soft_404_phrases):
                    return (site_name, url, False, category)
                
                return (site_name, url, True, category)
            else:
                return (site_name, url, False, category)
                
        except requests.RequestException:
            return (site_name, url, False, category)

    def start_scan(self):
        username = self.entry_username.get().strip()
        if not username:
            return

        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        self.result_rows.clear() 
        self.raw_scan_data.clear()
        self.found_count = 0

        self.btn_scan.configure(state="disabled")
        self.btn_export.configure(state="disabled")
        self.combo_category.set("All") 
        self.progressbar.set(0)
        self.lbl_status.configure(text=f"Scanning {len(TARGET_SITES)} platforms for '{username}'...")
        
        if hasattr(self, 'executor') and self.executor:
            self.executor.shutdown(wait=False)
            
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        
        self.completed_tasks = 0
        self.total_tasks = len(TARGET_SITES)

        for site_name, site_data in TARGET_SITES.items():
            future = self.executor.submit(self.check_website, site_name, site_data["url"], username, site_data["category"])
            future.add_done_callback(self.process_result)

    def process_result(self, future):
        site_name, url, is_found, category = future.result()
        self.root.after(0, self.update_ui, site_name, url, is_found, category)

    def update_ui(self, site_name, url, is_found, category):
        self.completed_tasks += 1
        progress = self.completed_tasks / self.total_tasks
        self.progressbar.set(progress)

        if is_found:
            self.found_count += 1

        self.raw_scan_data.append({
            "Platform": site_name,
            "Category": category,
            "Exists": "Yes" if is_found else "No",
            "URL": url
        })

        row_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        self.result_rows.append({"frame": row_frame, "category": category})

        if is_found:
            lbl_site = ctk.CTkLabel(row_frame, text=f"✅ {site_name}", text_color="#2ecc71", font=ctk.CTkFont(weight="bold", size=15))
            lbl_site.pack(side="left", padx=10)
            lbl_cat = ctk.CTkLabel(row_frame, text=f"[{category}]", text_color="gray", font=ctk.CTkFont(size=11))
            lbl_cat.pack(side="left", padx=5)
            btn_open = ctk.CTkButton(row_frame, text="View Profile", width=80, height=24, fg_color="#3498db", hover_color="#2980b9", command=lambda link=url: webbrowser.open(link))
            btn_open.pack(side="right", padx=10)
        else:
            lbl_site = ctk.CTkLabel(row_frame, text=f"❌ {site_name}", text_color="#e74c3c", font=ctk.CTkFont(size=15))
            lbl_site.pack(side="left", padx=10)
            lbl_cat = ctk.CTkLabel(row_frame, text=f"[{category}]", text_color="#555555", font=ctk.CTkFont(size=11))
            lbl_cat.pack(side="left", padx=5)

        current_filter = self.combo_category.get()
        if current_filter == "All" or current_filter == category:
            row_frame.pack(fill="x", pady=5)

        if self.completed_tasks == self.total_tasks:
            self.lbl_status.configure(text=f"Scan Complete. Found on {self.found_count} / {self.total_tasks} platforms.")
            self.btn_scan.configure(state="normal")
            
            if self.found_count > 0:
                self.btn_export.configure(state="normal")
                
            if hasattr(self, 'executor') and self.executor:
                self.executor.shutdown(wait=False)

    def apply_filter(self, selected_category):
        for item in self.result_rows:
            item["frame"].pack_forget()
        for item in self.result_rows:
            if selected_category == "All" or item["category"] == selected_category:
                item["frame"].pack(fill="x", pady=5)

    def export_results(self):
        if not self.raw_scan_data:
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv"), ("JSON File", "*.json")],
            title="Export OSINT Data",
            initialfile=f"osint_report_{self.entry_username.get().strip()}"
        )
        
        if not filepath:
            return
            
        try:
            if filepath.endswith('.json'):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.raw_scan_data, f, indent=4)
            else:
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=["Platform", "Category", "Exists", "URL"])
                    writer.writeheader()
                    writer.writerows(self.raw_scan_data)
                    
            messagebox.showinfo("Export Successful", f"Data saved to:\n{os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save file:\n{str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = FootprintScanner(root)
    root.mainloop()