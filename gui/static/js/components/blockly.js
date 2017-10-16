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

// /* ======================= BASIC SETUP ======================== */
// /* Blockly Configurations */
// var workspace = Blockly.inject('blocklyDiv',
//     {
//         toolbox: document.getElementById('toolbox'),
//         grid: {
//             spacing:20,
//             length:3,
//             colour: '#ccc',
//             snap: true
//         },
//         trashcan: true,
//         scroll: true
//     });
//
// /* Realtime code generation
//
//   (Every drag/drop or change in visual code will be
//   reflected in actual code view) */
// workspace.addChangeListener(function(event){
//     setCode(getBlocklyScript());
// });
//
//
