var React = require('react');
var ReactDOM = require('react-dom');

/**
 * Component for the Blockly sandbox
 *
 */
export default class MinibotBlockly extends React.Component {
    constructor(props){
        super(props);
        this.scriptToCode = this.scriptToCode.bind(this);
    }

    /* Runs after component loads - this generates the blockly stuff */
    componentDidMount(){
        var _this = this;
        _this.workspace = window.Blockly.inject('blocklyDiv',
            {
                toolbox: document.getElementById('toolbox'),
                grid: {
                    spacing:20,
                    length:3,
                    colour: '#ccc',
                    snap: true
                },
                trashcan: true,
                scroll: true
            });

        /* Realtime code generation
          (Every drag/drop or change in visual code will be
          reflected in actual code view) */
        _this.workspace.addChangeListener(function(event){
            console.log('workspace change listener');
            _this.scriptToCode();
        });
    }

    /* Helper for realtime code generation (Blockly => Python) */
    scriptToCode() {
        console.log("scriptToCode");
        document.getElementById('data').value = window.Blockly.Python.workspaceToCode(this.workspace);
    }

    upload(event){
        console.log("upload listener");
        var _this = this;
        var file = event.target.files[0];
        var reader = new FileReader();
        reader.onload = function(event) {
            _this.state.data = event.target.result;
            document.getElementById("data").value = event.target.result;
        };
        reader.readAsText(file);
    }

    loadFileAsBlocks(event){
  	    var xmlToLoad = document.getElementById("blockUpload").files[0];

 	    var xmlReader = new FileReader();
 	    xmlReader.onload = function(event){
            var textFromFileLoaded = event.target.result;
            console.log(textFromFileLoaded);
            // document.getElementById("blockdata").value = textFromFileLoaded;
            var dom = Blockly.Xml.textToDom(textFromFileLoaded);


            Blockly.getMainWorkspace().clear();
            Blockly.Xml.domToWorkspace(dom, Blockly.getMainWorkspace());
         };

 	    xmlReader.readAsText(xmlToLoad, "UTF-8");
 	 }

    render(){
        var blocklyStyle = {margin:'0', height: '70vh', width: '55vw'};
        return (
            <div id="blockly" className = "box">
                <div id ="blocklyDiv" style={blocklyStyle}>Blockly</div><br/>
                <form>
                    <input
                        type="file"
                        id="blockUpload"
                        multiplesize="1"
                        accept=".xml"
                        onChange = {this.loadFileAsBlocks}
                        //onChange = {this.upload}
                    />
                </form>
            </div>
        )
    }
}
