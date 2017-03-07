import json

__author__ = "Mario Gutierrez/wlwzrd"
__email__ = "mfdogutierrez@gmail.com"


def createHTML(ID):
    data = {"categoryID":"100548", "categoryName":"Toys", "tree": {"name":"Hello","children":[{"name":"Child 1"},{"name":"Child 2"}]}}
    head = '<!DOCTYPE html>'+\
           '<html lang="en">'+\
           '<head>'+\
           '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>'+\
           '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0"/>'+\
           '<title>Categories</title>'+\
           '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'+\
           '<style type="text/css">'+\
           'body {'+\
           'font-family: Menlo, Consolas, monospace;'+\
           'color: #444;'+\
           '}'+\
           '.item {'+\
           'cursor: pointer;'+\
           '}'+\
           '.bold {'+\
           'font-weight: bold;'+\
           '}'+\
           'ul {'+\
           'padding-left: 1em;'+\
           'line-height: 1.5em;'+\
           'list-style-type: dot;'+\
           '}'+\
           '</style>'+\
           '</head>'
    body = '<body>'+\
           '<nav class="navbar navbar-default">'+\
           '<div class="container-fluid"><div class="navbar-header"><h1 class="navbar-brand">Ebay Categories</h1></div></div>'+\
           '</nav>'+\
           '<div class="container">'+\
           '<div class="panel panel-primary">'+\
           '<div class="panel-heading">Category Tree for <span class="label label-success">ID:{categoryID}</span></div>'.format(categoryID=ID)+\
           '<div class="panel-body">'+\
           '<ul id="demo"><item class="item" :model="treeData"></item></ul>'+\
           ' </div>'+\
           '</div>'+\
           '</div>'
    
    scriptItemTemplate = """<script type="text/x-template" id="item-template"><li>
    <div :class="{bold: isFolder}" @click="toggle" @dblclick="changeType">
        <span class="label label-success">{{model.id}}</span> {{model.name}}
        <span v-if="isFolder">[{{open ? '-' : '+'}}]</span>
    </div>
      <ul v-show="open" v-if="isFolder">
        <item class="item" v-for="model in model.children" :model="model"></item>
      </ul>
    </li></script>"""

    scriptBootstrapVue = '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"'+\
                         ' integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa"'+\
                         'crossorigin="anonymous"></script>'+\
                         '<script type="text/javascript" src="https://unpkg.com/vue@latest/dist/vue.js"></script>'+\
                         '<script src="data.js"></script>'+\
                         '<script src="web.js"></script></body>'
    fileName = ID +".html"
    htmlFile = open(fileName,'w')
    htmlFile.write(head)
    htmlFile.write(body)
    htmlFile.write(scriptItemTemplate)
    htmlFile.write(scriptBootstrapVue)
    htmlFile.close()
 
def createJS(data):
    """ Create de Json Data
    """
    treeData = 'var data = ' + json.dumps(data["tree"]) + ';'
    htmlFile = open("123456.html",'w')
    jsFile = open("data.js",'w')
    jsFile.write(treeData)
    jsFile.close()

