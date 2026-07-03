from flask import Flask, render_template, request, redirect
import os
import sqlite3


app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form["name"]
        bio = request.form["bio"]

        image = request.files["image"]

        filename = image.filename
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        conn = sqlite3.connect("profiles.db")
        cursor = conn.cursor()

        cursor.execute(
    "INSERT INTO profiles (name, bio, image) VALUES (?, ?, ?)",
    (name, bio, filename)
)

        conn.commit()
        conn.close()

        return render_template(
            "index.html",
            name=name,
            bio=bio,
            image="uploads/" + filename
        )

    return render_template("index.html")
@app.route("/profiles")
def profiles():

    search = request.args.get("search", "")

    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM profiles WHERE name LIKE ? ORDER BY id DESC",
            ('%' + search + '%',)
        )
    else:
        cursor.execute(
            "SELECT * FROM profiles ORDER BY id DESC"
        )

    all_profiles = cursor.fetchall()
    total_profiles = len(all_profiles)

    conn.close()

    return render_template(
        "profiles.html",
        profiles=all_profiles,
        search=search,
        total_profiles=total_profiles
    )
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_profile(id):

    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        bio = request.form["bio"]

        cursor.execute(
            "UPDATE profiles SET name=?, bio=? WHERE id=?",
            (name, bio, id)
        )

        conn.commit()
        conn.close()

        return redirect("/profiles")

    cursor.execute("SELECT * FROM profiles WHERE id=?", (id,))
    profile = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        profile=profile
    )
@app.route("/delete/<int:id>")
def delete_profile(id):

    conn = sqlite3.connect("profiles.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM profiles WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/profiles")


if __name__ == "__main__":
    app.run(debug=True)



    