var React = require('react');

<<<<<<< HEAD
export default class ScenariosItem extends React.Component {
    constructor() {
        super();
        this.state = {
            type: 'Type',
            angle: '0',
            size: '0',
            posx: '0',
            posy: '0',
            items: [{type: "bot", angle: "90", size: "2", posx: "3", posy: "4"}]
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleRemove = this.handleRemove.bind(this);
    }


//    handleAdd() {
//        var li = this.state.items;
//        li.push({type: "bot", angle: "30", size: "3", posx:"3", posy:"3"});
//        this.setState({items: li});
//    }

    handleInputChange(event) {
        console.log("handle input change");
        console.log(this.state);
        const target = event.target;
        const value = target.value;
        const name = target.name;
        this.setState({
            [name]: value
        });
    }

    handleSubmit() {
        console.log("handle submit");
        console.log(this.state);
        var li = this.state.items;
        li.push({type: this.state.type, angle: this.state.angle, size: this.state.size, posx: this.state.posx, posy: this.state.posy});
        this.setState({items: li});
    }

    handleRemove(event) {
        console.log("handle remove");
        console.log(this.state);
        console.log(event.idx);
        var li = this.state.items;
        li.splice(event.idx, 1);
        this.setState({items: li});
    }

    render() {
        var styles = {
            ScenariosItem: {
                padding: '5px',
                marginTop: '10px',
                background: '#f7f6ff',
                borderRadius: '3px'
            },

            Form: {
                marginLeft: '15px',
                marginRight: '15px',
                marginTop: '5px',
                marginBottom: '5px'
            }
        }
        var _this = this;
        return(
            <div id = "scenariobox" style={styles.ScenariosItem}>
                <button>Save</button>
                <button>Load</button>
                <button onClick={this.handleSubmit}>Add</button>
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <input type="text" name="type" onChange={this.handleInputChange} style={styles.Form}/>
                            </td>
                            <td></td>
                        </tr>
                        <tr>
                            <td><input type="text" name="angle" onChange={this.handleInputChange} style={styles.Form}/></td>
                            <td><input type="text" name="size" onChange={this.handleInputChange} style={styles.Form}/></td>
                        </tr>
                        <tr>
                            <td><input type="text" name="posx" onChange={this.handleInputChange} style={styles.Form}/></td>
                            <td><input type="text" name="posy" onChange={this.handleInputChange} style={styles.Form}/></td>
                        </tr>
                    </tbody>
                </table>
                {this.state.items.map(function (item, idx) {
                    return(
                        <div>
                            <table>
                                <tbody>
                                    <tr>
                                        <td>{item.type}</td>
                                        <td></td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <td>{item.angle}</td>
                                        <td>{item.size}</td>
                                        <td><button onClick = {() => _this.handleRemove({idx})}>Remove</button></td>
                                    </tr>
                                    <tr>
                                        <td>{item.posx}</td>
                                        <td>{item.posy}</td>
                                        <td></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    );
                })
                }
            </div>
        );
=======
/**
 * Component for the new scenarios system
 * Will contain:
 * Loading, saving, editing, adding scenarios to simulator
 *
 */
export default class Scenarios extends React.Component {
    //TODO
    render() {
        return(
            <div id ="component_scenarios" className = "box">Scenarios</div>
        )
>>>>>>> develop
    }
}
//
// //adding a scenario from the value in the scenario viewer
// $('#addScenario').click(function() {
//     console.log("add scenario from interface.js")
//     var scenario = $("#scenario").val();
//
//     $.ajax({
//         method: "POST",
//         url: '/addScenario',
//         dataType: 'text',
//         data: JSON.stringify({
//             scenario: scenario.toString()
//         }),
//         contentType: 'application/json; charset=utf-8',
//         success: function (data){
//             console.log("successfully added scenario: "+data);
//         }
//     });
// });
//
// //saving a scenario to a txt file with the specified filename
// $('#saveScenario').click(function() {
//     console.log("saving a scenario")
//     var scenario = $("#scenario").val();
//     var filename = $("#scenarioname").val();
//
//     $.ajax({
//         method: "POST",
//         url: '/saveScenario',
//         dataType: 'text',
//         data: JSON.stringify({scenario: scenario.toString(),
//             name: filename.toString()}),
//         contentType: 'application/json; charset=utf-8',
//         success: function (data){
//             console.log("successfully saved scenario: "+data);
//         }
//     });
// });
//
// /**loading a scenario - just type in a name, no need for directory or file
//  extension*/
// $('#loadScenario').click(function() {
//     active_bots = [];
//     discovered_bots = [];
//
//     var filename = $("#scenarioname").val();
//     console.log("loading scenario: "+filename.toString());
//     $.ajax({
//         method: "POST",
//         url: '/loadScenario',
//         dataType: 'text',
//         data: JSON.stringify({'name':filename.toString()}),
//         contentType: 'application/json; charset=utf-8',
//         success: function (data){
//             $("#scenario").val(data);
//             console.log("successfully loaded scenario: "+data);
//         },
//         error: function(data){
//             console.log("error: please enter the name of an existing scenario")
//         }
//     });
// });