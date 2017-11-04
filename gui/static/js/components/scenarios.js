var React = require('react');
var axios = require('axios');

export default class ScenariosItem extends React.Component {
    constructor() {
        super();
        this.state = {
            type: 'scenario_object',
            angle: '',
            size: '1',
            posx: '',
            posy: '',
            items: [],
            numBots: 0,
            filename: "testscenario.txt",
            position: ''
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleRemove = this.handleRemove.bind(this);

        this.addScenario = this.addScenario.bind(this);
        this.saveScenario = this.saveScenario.bind(this);
        this.loadScenario = this.loadScenario.bind(this);
    }

    /* handler for add scenario (load currently displayed scenario into simulator) */
    addScenario(event){
        console.log("add scenario listener");
        axios({
            method:'POST',
            url:'/addScenario',
            data: JSON.stringify({items: this.state.items}),
            dataType: 'text',
            contentType: 'application/json; charset=utf-8'
        })
        .then(function(response) {
            console.log('added scenario successfully');
        })
        .catch(function (error) {
            console.log(error);
        });
    }

    /* saves currently loaded scenario to file */
    saveScenario(){
        console.log("save scenario listener");

        var scenario = {items: this.state.items};
        console.log("numBots:" + this.state.numBots);
        if (this.state.numBots != 1) alert("You need to add a bot!");
        else {
            //Implemented the same way as Python script saving. This might not work so use axios code if it doesn't
            //event . preventDefault ()
            var element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(this.state.items)));
            element.setAttribute('download', this.state.filename);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);

            // axios({
            //     method:'POST',
            //     url:'/saveScenario',
            //     data: {scenario: scenario, name: filename},
            //     dataType: 'text',
            //     contentType: 'application/json; charset=utf-8'
            // })
            // .then(function(response) {
            //     console.log('saved scenario successfully');
            // })
            // .catch(function (error) {
            //     console.log(error);
            // });
        }

    }

    /* handler for load scenario (load scenario from file) */
    loadScenario(event){
        console.log("loading scenario listener");
        //implement the same way as python script upload button in interface
        var _this = this;
        var file = event.target.files[0];
        var reader = new FileReader();
        reader.onload = function(event) {
            var scenario = JSON.parse(event.target.result).items;
            _this.setState({items: scenario});
        };
        reader.readAsText(file);
        console.log("done");
    }

    /* handles input change for input fields */
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

    /* checks that object contains correct info and adds object to list*/
    handleSubmit() {
        console.log("handle submit");
        console.log(this.state);

        //check that inputs are valid
        if (this.state.angle > 360) alert("The angle is too large!");
        else if (this.state.type == 'simulator.simbot' && this.state.numBots == 1) alert("You already have one bot!");
        else if (this.state.angle == '' || this.state.posx == '' || this.state.posy == '') alert("Fields cannot be empty!");
        else {
            var li = this.state.items;
            var string = "[" + this.state.posx + "," + this.state.posy + "]";
            console.log(this.state.type);

            if (this.state.type == "simulator.simbot") {
                console.log("add bot");
                this.state.numBots++;
                console.log("numBot:" + this.state.numBots);
                li.push({type: this.state.type, angle: this.state.angle, position: string});
            } else {
                li.push({type: this.state.type, angle: this.state.angle, size: this.state.size, position: string});
            }

            this.setState({items: li});
        }
    }

    /* removes selected object from list*/
    handleRemove(event) {
        console.log("handle remove");
        console.log(this.state);
        var li = this.state.items;
        if (li[event.idx].type == "simulator.simbot") {
            this.state.numBots--;
        }
        console.log("type1: " + li[event.idx].type);
        console.log("numBot: " + this.state.numBots);
        li.splice(event.idx, 1);
        this.setState({items: li});
    }
    
    render() {
        var styles = {
            ScenariosItem: {
                padding: '10px',
                marginTop: '10px',
                marginRight: '10px'
            },

            Form: {
                marginLeft: '15px',
                marginRight: '15px',
                marginTop: '5px',
                marginBottom: '5px'
            },

            Button: {
                marginLeft: '10px',
                marginRight: '15px'
            }
        }
        var _this = this;
        return(
            <div id = "scenariobox" className = "box">
                <button onClick={this.saveScenario} style={styles.Button}>Save</button>
                <button style={styles.Button}>Load</button>
                <button style={styles.Button}>Add to Simulator</button>
                <table style={styles.ScenariosItem}>
                    <tbody>
                        <tr>
                            <th>Type: </th>
                            <th>
                                <select name="type" value={this.state.value} onChange={this.handleInputChange} style={styles.Form}>
                                    <option value ="scenario_object">Scenario Object</option>
                                    <option value = "simulator.simbot">Simulated Minibot</option>
                                </select>
                            </th>
                            <td><button style={styles.Button} onClick={this.handleSubmit}>Add</button></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th>Angle: </th>
                            <td><input type="number" name="angle" onChange={this.handleInputChange} style={styles.Form}/></td>
                            <th>Size: </th>
                            <td><input type="number" name="size"  disabled={this.state.type == "simulator.simbot"} onChange={this.handleInputChange} style={styles.Form}/></td>
                        </tr>
                        <tr>
                            <th>Position X: </th>
                            <td><input type="number" name="posx" onChange={this.handleInputChange} style={styles.Form}/></td>
                            <th>Position Y: </th>
                            <td><input type="number" name="posy" onChange={this.handleInputChange} style={styles.Form}/></td>
                        </tr>
                    </tbody>
                </table>
                {this.state.items.map(function (item, idx) {
                    return(
                        <div style={styles.ScenariosItem} key={idx}>
                            <table>
                                <tbody>
                                    <tr>
                                        <th>Type: </th>
                                        <td>{item.type}</td>
                                        <td></td>
                                        <td></td>
                                    </tr>
                                    <tr>
                                        <th>Angle: </th>
                                        <td>{item.angle}</td>
                                        <th>Size: </th>
                                        <td>{item.size}</td>
                                    </tr>
                                    <tr>
                                        <th>Position: </th>
                                        <td>{item.position}</td>
                                        <td><button style={styles.Button} onClick = {() => _this.handleRemove({idx})}>Remove</button></td>
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
    }
}

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