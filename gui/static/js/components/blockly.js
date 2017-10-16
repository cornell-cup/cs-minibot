var React = require('react');

export default class Blockly extends React.Component {
    //TODO THIS DOES NOT WORK ???
    componentDidMount(){
        /* Blockly Configurations */
//        setUpBlockly();
    }
    render(){
        return (
            <div id ="blocklyDiv" className = "box">Blockly</div>
        )
    }
}