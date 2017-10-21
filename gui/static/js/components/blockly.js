var React = require('react');
var ReactDOM = require('react-dom');

<<<<<<< HEAD
export default class Blockly extends React.Component {
    //TODO getBlocklyScript does not work
=======
/**
 * Component for the Blockly sandbox
 *
 */
export default class Blockly extends React.Component {
    //TODO getBlocklyScript does not workw
>>>>>>> develop
    constructor(props){
        super(props);
        this.getBlocklyScript = this.getBlocklyScript.bind(this);
    }

<<<<<<< HEAD
=======
    /* Runs after component loads - this generates the blockly stuff */
>>>>>>> develop
    componentDidMount(){
        var workspace = window.Blockly.inject('blocklyDiv',
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
<<<<<<< HEAD

=======
>>>>>>> develop
          (Every drag/drop or change in visual code will be
          reflected in actual code view) */
        workspace.addChangeListener(function(event){
            document.getElementById('data').value = this.getBlocklyScript();
        });
    }

<<<<<<< HEAD
=======
    /* Translates Blockly code to Python,
     * CURRENTLY BROKEN */
>>>>>>> develop
    getBlocklyScript() { return window.Blockly.Python.workspaceToCode(workspace); }

    render(){
        var blocklyStyle = {margin:'0', height: '70vh', width: '55vw'};
        return (
            <div id="blockly" className = "box">
                <div id ="blocklyDiv" style={blocklyStyle}>Blockly</div>
            </div>
        )
    }
}

