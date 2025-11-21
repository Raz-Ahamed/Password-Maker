import itertools
import os
import time
import datetime  # তারিখ ও সময়ের জন্য নতুন মডিউল

def banner():
    print("""
    =============================================
       BD MASTER GEN (With Timestamp)
       Saves file locally with Date & Time
    =============================================
    """)

def create_master_wordlist():
    banner()
    
    # --- 1. লোকেশন সেট করা (যেখানে স্ক্রিপ্ট আছে, সেখানেই সেভ হবে) ---
    # এই লাইনটি নিশ্চিত করে ফাইলটি যেন আপনার পাইথন ফাইলের পাশেই সেভ হয়
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    print(f"[*] Working Directory: {script_directory}")
    print("[*] Please enter target details (Press Enter to skip)\n")

    # --- 2. INPUTS ---
    profile = {}
    profile['first'] = input("> First Name (e.g. Farhana): ").strip()
    profile['last']  = input("> Last Name: ").strip()
    profile['nick']  = input("> Nickname: ").strip()
    profile['partner']= input("> Partner Name: ").strip()
    profile['phone'] = input("> Phone Number: ").strip() 

    print("\n[*] Generating Wordlist with Timestamp...")
    time.sleep(1)

    # --- 3. DATA PREPARATION ---
    base_words = [profile['first'], profile['last'], profile['nick'], profile['partner']]
    base_words = [w for w in base_words if w] 

    # BD Common Words
    bd_slang = [
        "bangladesh", "dhaka", "iloveyou", "valobashi", "taka_de", 
        "taka_nai", "fokir", "bolbo_na", "ami_jani_na", "bristivija", 
        "ma_baba", "internet", "password", "joybangla", "shonar_bangla",
        "free_wifi", "cholo_jai", "amarnam", "khulna", "chittagong",
        "taka_nai_bag_a"
    ]

    # Number Lists
    years = [str(y) for y in range(1900, 2051)]
    short_nums = [str(n) for n in range(0, 1000)] # 0-999
    repeats = ["111", "222", "333", "444", "555", "666", "777", "888", "999",
               "000", "123", "1234", "12345", "12345678", "007", "786"]

    # Phone Parts Logic
    phone_parts = []
    if profile['phone']:
        p = profile['phone']
        phone_parts.append(p)           
        if len(p) >= 6:
            phone_parts.append(p[:6])   
            phone_parts.append(p[-6:])  
        if len(p) >= 4:
            phone_parts.append(p[-4:])  

    final_list = set()

    # --- 4. GENERATION LOGIC ---

    # Step 1: BD Slang
    for w in bd_slang:
        final_list.add(w)
        final_list.add(w + "123")
        final_list.add(w + "@123")

    # Step 2: User Names Processing
    for word in base_words:
        forms = [word, word.lower(), word.capitalize(), word.upper()]
        all_suffixes = years + short_nums + repeats + phone_parts

        for form in forms:
            final_list.add(form) 

            for suff in all_suffixes:
                final_list.add(form + suff)           # Name123
                final_list.add(form + "@" + suff)     # Name@123
                final_list.add(form + "#" + suff)     # Name#123
                final_list.add(form + "_" + suff)     # Name_123
                final_list.add(form + "." + suff)     # Name.123
                final_list.add(form + "@#" + suff)    # Name@#123
                final_list.add(form + "#@" + suff)    # Name#@123

    # Step 3: Phone Specific
    for part in phone_parts:
        final_list.add(part)
        final_list.add(part + "@123")
        final_list.add(part + "#123")

    # Step 4: Combinations
    if len(base_words) >= 2:
        for a, b in itertools.permutations(base_words, 2):
            final_list.add(a + b)             
            final_list.add(a + "@" + b)       
            final_list.add(a + "123" + b)     

    # --- 5. SAVING FILE WITH TIMESTAMP ---
    
    # বর্তমান সময় বের করা (Format: Year-Month-Day_Hour-Minute-Second)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # ফাইলের নাম সেট করা
    filename = f"passlist_{current_time}.txt"
    
    # ফাইলের পুরো পাথ (Location + Name)
    full_file_path = os.path.join(script_directory, filename)

    try:
        with open(full_file_path, "w") as f:
            for password in final_list:
                f.write(password + "\n")
        
        print("\n" + "="*60)
        print(f" [SUCCESS] Wordlist Created!")
        print(f" [NAME]    {filename}")  # ফাইলের নাম দেখাবে
        print(f" [PATH]    {full_file_path}") # পুরো লোকেশন দেখাবে
        print("="*60)

    except Exception as e:
        print(f"[Error] {e}")

if __name__ == "__main__":
    create_master_wordlist()