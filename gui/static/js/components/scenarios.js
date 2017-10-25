var React = require('react');
var axios = require('axios');

export default class ScenariosItem extends React.Component {
    constructor() {
        super();
        this.state = {
            type: 'Type',
            angle: '0',
            size: '0',
            posx: '0',
            posy: '0',
            items: [{type: "bot", angle: "90", size: "2", posx: "3", posy: "4"}],

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
    saveScenario(event){
        console.log("save scenario listener");

        var scenario = {items: this.state.items};
        var filename = this.state.filename;

        //Implemented the same way as Python script saving. This might not work so use axios code if it doesn't
        event.preventDefault();
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
    }

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