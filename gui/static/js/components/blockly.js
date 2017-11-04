var React = require('react');
var ReactDOM = require('react-dom');

/**
 * Component for the Blockly sandbox
 *
 */
export default class Blockly extends React.Component {
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

    render(){
        var blocklyStyle = {margin:'0', height: '70vh', width: '55vw'};
        return (
            <div id="blockly" className = "box">
                <div id ="blocklyDiv" style={blocklyStyle}>Blockly</div>
            </div>
        )
    }
}

