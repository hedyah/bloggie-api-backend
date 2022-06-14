from flask import Flask, jsonify, request
from helpers.dbhelpers import run_query
import sys

app = Flask(__name__)

@app.get('/api/blogsite')
def blog_get():
    get_content = run_query("SELECT * from blog_content")
    resp = []
    for content in get_content:
        an_obj = {}
        an_obj['id']= content[0]
        an_obj['userContent'] = content[1]
        an_obj['username']= content[2]
        resp.append(an_obj)
    if not get_content:
        return jsonify("Error, couldn't reach your request!"),422
    return jsonify(resp),200

@app.post('/api/blogsite')
def blog_post():
    data = request.json
    create_post = data.get('userContent')
    blog_user = data.get('username')
    if not create_post:
        return jsonify("Missing required argument/ not able to post : 'usercontent'"),422
    if not blog_user:
        return jsonify("missing required argument : username")
    #DB write
    run_query("INSERT INTO blog_content (content, username) VALUE (?,?)", 
                [create_post,blog_user])
    return jsonify("Post created sucsessfully!"), 201

@app.patch('/api/blogsite')
def blog_patch():
    data = request.json
    edit_post = data.get('userContent')
    blog_user= data.get('userid')
    if not edit_post:
        return jsonify("missing argunemt required/not able to edit : userContent"),422
    if not blog_user:
        return jsonify("missing required argument : userid "),422
    #DB write
    run_query("UPDATE blog_content SET content=? WHERE id=?", 
                [edit_post, blog_user])
    return jsonify ("Edited post sucsessfully!"), 201

@app.delete('/api/blogsite')
def blog_delete():
    data = request.json
    blog_user = data.get('userid')
    if not blog_user:
        return jsonify("missing required argument : userid"),422
    #DB write
    run_query("DELETE FROM blog_content WHERE id=?", [blog_user])
    return jsonify ("Deleted post sucessfully!"),201

if len(sys.argv) > 1:
    mode = sys.argv[1]
    
else:
    print("missing requriement argument: testing")
    exit()

if mode == "testing":
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif mode == "production":
    import bjoern
    print("running production mode")
    bjoern.run(app, "0.0.0.0", 5005)
else:
    print("invalid mode, please chose either 'testing' or 'production'")
    exit()