from flask import Flask,jsonify,render_template,request
import requests
import json

app=Flask("__name__")

@app.route('/deneme')
def get_data():
    return requests.get('https://api.stackexchange.com/users').content




@app.route('/get_tags',methods=['GET'])
def get_tag():
    tags_json=requests.get("https://api.stackexchange.com/docs").content
    
    return tags_json
"""
methods[""]=
  
"""
@app.route('/')
def index():
    methods={"tags":"http://127.0.0.1:5000/tags"}
    methods["tags/{tags}/info"]="http://127.0.0.1:5000/tags_info"
    methods["tags/required"]="http://127.0.0.1:5000/tags_required"
    methods["tags/synonyms"]="http://127.0.0.1:5000/tags_synonyms"
    methods["tags/{tags}/synonyms"]="https://api.stackexchange.com/2.2/tags/%7Btags%7D/synonyms?order=desc&sort=creation&site=stackoverflow"
    return render_template("index.html",methods=methods)


@app.route("/tags")
def tags():
    tags_json=requests.get("https://api.stackexchange.com/2.2/tags?order=desc&sort=popular&site=stackoverflow").content
    doc=tags_json.decode("utf-8")
    return render_template("tags.html",json_obj=doc)


## tags/{tags}/info

@app.route("/tags_info")
def tags_info():
    tags_info=requests.get("https://api.stackexchange.com/2.2/tags/%7Btags%7D/info?order=desc&sort=popular&site=stackoverflow").content
    doc=tags_info.decode("utf-8")
    return render_template("tags_info.html",json_obj=doc,go="/tags_info",textbox_name="Tag")

#if it's post run that method
@app.route("/tags_info",methods=['POST'])
def post_tag_info():
    tags_name=request.form["file_name"]
    url="https://api.stackexchange.com/2.2/tags/"+tags_name+"/info?order=desc&sort=popular&site=stackoverflow"

    tags_info=requests.get(url).content
    doc=tags_info.decode("utf-8")
    return render_template("tags_info.html",json_obj=doc,go="forward/",textbox_name="FileName")



@app.route("/tags_required")
def tags_required():
    tags_info=requests.get("https://api.stackexchange.com/2.2/tags/required?order=desc&sort=popular&site=stackoverflow").content
    doc=tags_info.decode("utf-8")
    return render_template("tags_required.html",json_obj=doc,go="/tags_required",textbox_name="inname")



@app.route("/tags_required",methods=['POST'])
def post_tags_required():
    
    tags_name=request.form["file_name"]
    url="https://api.stackexchange.com/docs/required-tags#order=desc&sort=popular&inname="+tags_name+"&filter=default&site=stackoverflow&run=true"

    tags_req=requests.get(url).content
    doc=tags_req.decode("utf-8")
    return render_template("tags_required.html",json_obj=doc,go="forward/",textbox_name="FileName")


## Tags Synoyms

@app.route("/tags_synonyms")
def tags_synonyms():
    url="https://api.stackexchange.com/2.2/tags/%7Btags%7D/synonyms?order=desc&sort=creation&site=stackoverflow"
    tags_synonyms=requests.get(url).content
    doc=tags_synonyms.decode("utf-8")
    return render_template("tags_synonyms.html",json_obj=doc,go="/tags_synonyms",textbox_name="tags")



@app.route("/tags_synonyms",methods=['POST'])
def post_tags_synonyms():
    
    tags_name=request.form["file_name"]
    url="https://api.stackexchange.com/2.2/tags/"+tags_name+"/synonyms?order=desc&sort=creation&site=stackoverflow"

    tags_req=requests.get(url).content
    doc=tags_req.decode("utf-8")
    return render_template("tags_synonyms.html",json_obj=doc,go="forward/",textbox_name="FileName")


@app.route('/layout')
def layout():
 
    return render_template("layout.html")

@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    json_text=request.form["text_area"]
    file_name=request.form["file_name"]
    
    dict_json= json.loads(json_text)
   
    
    with open(file_name+'.json', 'w') as outfile:
        json.dump(dict_json, outfile,indent=3)

    return "file saved as:"+file_name+".json"





if __name__=="__main__":
    app.run(debug=True)