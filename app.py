from flask import Flask , request , redirect , render_template
import random
import string
from models import (
    init_db,
    insert_url,
    get_url,
    get_all_urls,
    increment_visit_count,
    delete_url
    )

app = Flask(__name__)

init_db()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits  , k=length))

@app.route("/" , methods=['GET','POST'])
def home():
    if request.method == "POST":
        original_url = request.form["url"]  
        short_code = generate_short_code()
        insert_url(original_url,short_code)
        return redirect("/")
    
    all_urls = get_all_urls()
    return render_template("index.html" , all_urls=all_urls , len_all_urls = len(all_urls ) , total_visits = sum(url[2] for url in all_urls) , most_visited_site = [url[1] for url in all_urls if url[2] == max(url[2] for url in all_urls)])

@app.route("/delete", methods=["POST"])
def delete():
    short_code = request.form["short_code"]
    delete_url(short_code)   # your DB function
    return redirect("/")

@app.route("/<short_code>")
def increment_visit(short_code):
    print("Short code clicked:", short_code)
    original_url = get_url(short_code)[0]
    print("Original URL:", original_url)
    if original_url:
        increment_visit_count(short_code)
        return redirect(original_url)
    return "Short url not found ❌"


if __name__ == "__main__":
    app.run(debug=True)