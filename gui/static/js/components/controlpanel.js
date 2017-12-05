var React = require('react');
var axios = require('axios');
var lastKeyPressed;
export default class ControlPanel extends React.Component {
    //TODO (#31): add listeners for Keyboard controls
    constructor(props) {
        super(props);
        this.state = {
            power: 50,
            discoveredBots: [],
            keyboard: false,
            xbox: false,
            trackedBots: [],
            scripts: [],
            currentScript: ""
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.updateDiscoveredBots = this.updateDiscoveredBots.bind(this);
        this.sendKV = this.sendKV.bind(this);
        this.startLogging = this.startLogging.bind(this);
        this.sendMotors = this.sendMotors.bind(this);
        this.removeBot = this.removeBot.bind(this);
        this.xboxToggle = this.xboxToggle.bind(this);
        this.getTrackedBots = this.getTrackedBots.bind(this);
        this.selectBot = this.selectBot.bind(this);
        this.selectScript = this.selectScript.bind(this);
        this.onKeyDown = this.onKeyDown.bind(this);
        window.addEventListener('keydown', this.onKeyDown);
        this.onKeyUp = this.onKeyUp.bind(this);
        window.addEventListener('keyup', this.onKeyUp);
    }

     /* sends a command to bot according to the button pressed */
    onKeyDown(event) {
        if (this.state.keyboard) {
            console.log('Keydown.');
            const pow = this.state.power;
            if (false) { //event.keyCode == lastKeyPressed) {
                // Stop
                this.sendMotors(0,0,0,0);
                lastKeyPressed = -1;
            }
            else {
                if(event.keyCode==87) {
                    // If the 'W' key is pressed,move forward
                    this.sendMotors(pow, pow, pow, pow);
                }
                else if(event.keyCode==83){
                    //If the 'S' ket is pressed,move backward
                    this.sendMotors(-pow, -pow, -pow, -pow);
                }
                else if (event.keyCode==65) {
                    // If the 'A' key is pressed,ccw
                    this.sendMotors(-pow, pow, -pow, pow);
                }
                else if (event.keyCode==68){
                    // If the 'D' key is pressed,cw
                    this.sendMotors(pow, -pow, pow, -pow);
                }
                else if (event.keyCode==81){
                    // If the 'Q' key is pressed,left
                    this.sendMotors(-pow, pow, pow, -pow);
                }
                else if (event.keyCode==69){
                    // If the 'E' key is pressed,right
                    this.sendMotors(pow, -pow, -pow, pow);
                }
                else{
                    return;
                }
                lastKeyPressed = event.keyCode;
            }
        }
    }

    onKeyUp(event) {
        this.sendMotors(0,0,0,0);
    }

    /* handler for input changes to modify the state */
    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        if (name=="xbox"){
            this.setState({
                [name]: target.checked
            });
            this.xboxToggle(target.checked);
        } else if (name=="keyboard"){
            this.setState({
                [name]: target.checked
            });
            console.log(this.state.keyboard)
        } else {
            this.setState({
                [name]: value
            });
        }
    }

    /**
     * Updates tracked bots before page load.
     */
    componentWillMount() {
        this.getTrackedBots();
        this.getScripts();
    }

    /* sends a key-value command to bot */
    sendKV(event){
        const pow = this.state.power;
        const target = event.target;
        if(target.id=="fwd") {
            this.sendMotors(pow, pow, pow, pow);
        }
        else if(target.id=="bck") {
            this.sendMotors(-pow, -pow, -pow, -pow);
        }
        else if(target.id=="lft") {
            this.sendMotors(-pow, pow, -pow, pow);
        }
        else if(target.id=="rt") {
            this.sendMotors(pow, -pow, pow, -pow);
        }
        else if(target.id=="cw"){
            this.sendMotors(pow, -pow, pow, -pow);
        }
        else if(target.id=="ccw"){
            this.sendMotors(-pow, pow, -pow, pow);
        }
        else if(target.id=="stop"){
            this.sendMotors(0,0,0,0);
        }
        else if(target.id=="log") {
            this.startLogging();
        }
        else if(target.id=="run") {
            axios({
                method:'POST',
                url:'/sendKV',
                data: JSON.stringify({
                    key: "RUN",
                    value: this.state.currentScript,
                    name: this.props.currentBot
                }),
            })
            .then(function(response) {
                console.log('sent kv');
            })
            .catch(function (error) {
                console.warn(error);
            });
        }
        else {
            axios({
                method:'POST',
                url:'/sendKV',
                data: JSON.stringify({
                    key: document.getElementById('kv_key').value,
                    value: document.getElementById('kv_value').value,
                    name: this.props.currentBot
                }),
            })
            .then(function(response) {
                console.log('sent kv');
            })
            .catch(function (error) {
                console.warn(error);
            });
        }
    }

    /* sends a motor command to bot
     * input: front left, front right, back left, back right (all ints)
     **/
    sendMotors(fl,fr,bl,br){
        const _this = this;
        axios({
            method:'POST',
            url:'/commandBot',
            data: JSON.stringify({
                name: this.props.currentBot,
                fl: fl,
                fr: fr,
                bl: bl,
                br: br
            }),
        })
        .then(function(response) {
            console.log('Sent motor command: ' + response)
        })
        .catch(function (error) {
            console.warn(error);
        });
    }

    /**
     * Gets bots currently tracked
     */
    getTrackedBots() {
        const _this = this;
        axios({
            method:'POST',
            url:'/getTrackedBots',
            })
                .then(function(response) {
                    _this.setState({trackedBots: response.data});
            })
                .catch(function (error) {
                    console.log(error);
        });
    }

    /**
     * Gets all avaliable scripts
     */
    getScripts() {
        const _this = this;
        axios({
            method:'GET',
            url:'/findScripts',
            })
                .then(function(response) {
                    _this.setState({scripts: response.data});
            })
                .catch(function (error) {
                    console.log(error);
        });
    }

    /**
     * Handles onChange for bot dropdown. Changes currently selected bot.
     */
    selectBot(event) {
        this.props.setCurrentBot(event.target.value);
    }

    /**
     * Handles onChange for script dropdown. Changes currently selected script.
     */
    selectScript(event) {
        this.setState({currentScript: event.target.value});
    }

    /* starts data logging */
    startLogging(){
        console.log("logging data listener");
        axios({
            method:'POST',
            url:'/logdata',
            data: JSON.stringify({name: this.props.currentBot}),
            processData: false,
        })
        .then(function(response) {
            console.log('started logging data');
        })
        .catch(function (error) {
            console.warn(error);
        });
    }

    /* removes selected bot from list */
    removeBot(){
        console.log("remove bot listener");
        axios({
            method:'POST',
            url:'/removeBot',
            data: JSON.stringify({name: this.props.currentBot}),
        })
        .then(function(response) {
            console.log('removed bot successfully');
        })
        .catch(function (error) {
            console.warn(error);
        });
    }


    /* toggles xbox controls on or off */
    xboxToggle(checked){
        console.log('xboxToggle '+checked);
        if (checked){
            axios({
                method:'POST',
                url:'/runXbox',
                data: JSON.stringify({name: this.props.currentBot}),
            })
            .then(function(response) {
                console.log('successfully toggled Xbox ON');
            })
            .catch(function (error) {
                console.warn(error);
            });
        } else {
            axios({
                method:'POST',
                url:'/stopXbox',
                data: JSON.stringify({name: this.props.currentBot}),
            })
            .then(function(response) {
                console.log('successfully toggled Xbox OFF');
            })
            .catch(function (error) {
                console.warn(error);
            });
        }
    }


    updateDiscoveredBots(){
        //TODO (#32) - change below request to axios
        //        $.ajax({
        //            method: "POST",
        //            url: '/discoverBots',
        //            dataType: 'json',
        //            data: '',
        //            contentType: 'application/json',
        //            success: function (data) {
        //                 //Check if discovered_bots and data are the same (check length and then contents)
        //                if(data.length != discovered_bots.length){
        //                    //If not then clear list and re-make displayed elements
        //                    redoDiscoverList(data);
        //                }
        //                else{
        //                    //Check value to ensure both structures contain the same data
        //                    for(let x=0;x<data.length;x++){
        //                        if(data[x]!=discovered_bots[x]){
        //                            redoDiscoverList(data);
        //                            //Prevent the list from being remade constantly
        //                            break;
        //                        }
        //                    }
        //                }
        //                setTimeout(updateDiscoveredBots,3000); // Try again in 3 sec
        //            }
        //        });
    }

    redoDiscoverList(data){
        let new_bots = [];

        for (let i = 0; i < data.length; i++) {
            //Trim the forward-slash
            var ip_address = data[i].substring(1);
            new_bots.push(ip_address)
        }
        this.setState({discoveredBots: new_bots})
    }

    render(){
        var styles = {
            runBtn: {
                marginLeft: 10,
            }
        }
        return (
            <div id ="component_controlpanel" className = "box">
                Control Panel<br/>
                <h4>Movement controls:</h4>
                <br/>
                <table>
                    <tbody>
                    <tr>
                        <td>
                            <label>
                                Choose bot:
                                <select value={this.props.currentBot} onChange={this.selectBot} id="botlist" name="bots">
                                    <option value="(DEBUG) Sim Bot">(DEBUG) Sim Bot</option>
                                    {
                                        this.state.trackedBots.map(function(botname, idx){
                                            return <option
                                                        key={idx}
                                                        value={botname}>
                                                   {botname}
                                                   </option>
                                        })
                                    }
                                </select>
                            </label>
                        </td>
                        <td><button className="btn btn-danger" id="removeBot" onClick={this.removeBot}>Remove Bot</button></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td>Power ({this.state.power}):</td>
                        <td><input id="power" type="range" name="power" min="0" max="100" value={this.state.power} defaultValue="50" onChange={this.handleInputChange}/></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td className="controlgrid"><button className="btn" id="ccw" onClick={this.sendKV}>turn CCW</button></td>
                        <td className="controlgrid"><button className="btn" id="fwd" onClick={this.sendKV}>forward</button></td>
                        <td className="controlgrid"><button className="btn" id="cw" onClick={this.sendKV}>turn CW</button></td>
                    </tr>
                    <tr>
                        <td className="controlgrid"><button className="btn" id="lft" onClick={this.sendKV}>left</button></td>
                        <td className="controlgrid"><button className="btn btn-danger" id="stop" onClick={this.sendKV}>STOP</button></td>
                        <td className="controlgrid"><button className="btn" id="rt" onClick={this.sendKV}>right</button></td>
                    </tr>
                    <tr>
                        <td className="controlgrid"><button className="btn btn-success" id="log" onClick={this.sendKV}>log data</button></td>
                        <td className="controlgrid"><button className="btn" id="bck" onClick={this.sendKV}>backward</button></td>
                        <td className="controlgrid"></td>
                    </tr>
                    <tr>
                        <td>
                            Keyboard Controls <br/>
                            <label className="switch">
                                <input name="keyboard" type="checkbox" id="keyboard-controls" onChange={this.handleInputChange} />
                                <span className="slider"></span>
                            </label>
                        </td>
                        <td></td>
                        <td>
                            Xbox Controls <br/>
                            <label className="switch">
                                <input name="xbox" type="checkbox" id="xbox-controls" onChange={this.handleInputChange}/>
                                <span className="slider"></span>
                            </label>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <label>
                    Choose Script: 
                    <select onChange={this.selectScript} id="scriptlist" name="scripts">
                        <option value=""></option>
                        {
                            this.state.scripts.map(function(scriptname, idx){
                                return <option
                                            key={idx}
                                            value={scriptname}>
                                       {scriptname}
                                       </option>
                            })
                        }
                    </select>
                    <button style={styles.runBtn} className="btn btn-success btn-sm" id="run" onClick={this.sendKV}>Run Script</button>
                </label>
            </div>
        )
    }
}

// $(document).ready(function() {
//     /*
//      * Event listener for key inputs. Sends to selected bot.
//      */
//     var lastKeyPressed;
//     window.onkeydown = function (e) {
//         let keyboardEnable = document.getElementById('keyboard-controls').checked;
//         if (!keyboardEnable) return;
//
//         let pow = getPower();
//         let code = e.keyCode ? e.keyCode : e.which;
//
//         if (code === lastKeyPressed) return;
//
//         if (code === 87) {
//             // w=forward
//             sendMotors(pow, pow, pow, pow);
//
//         } else if (code === 83) {
//             // s=backward
//             sendMotors(-pow, -pow, -pow, -pow);
//
//         } else if (code == 65) {
//             // a=ccw
//             sendMotors(-pow, pow, -pow, pow);
//
//         } else if (code == 68) {
//             // d=cw
//             sendMotors(pow, -pow, pow, -pow);
//
//         } else if (code == 81) {
//             // q=left
//             sendMotors(-pow, pow, pow, -pow);
//
//         } else if (code == 69) {
//             // e=right
//             sendMotors(pow, -pow, -pow, pow);
//         } else {
//             return;
//         }
//         lastKeyPressed = code;
//     };
//
//     window.onkeyup = function (e) {
//         let keyboardEnable = document.getElementById('keyboard-controls').checked;
//         if (!keyboardEnable) return;
//
//         let code = e.keyCode ? e.keyCode : e.which;
//
//         if (code === lastKeyPressed) {
//             // Stop
//             sendMotors(0,0,0,0);
//             lastKeyPressed = -1;
//         }
//     };
// });
//
// /*
// *   Send KV -- allows users to manually send key and value to bot (for debugging/testing
//     purposes)
// */
// function sendKV(){
//     $.ajax({
//         method:'POST',
//         url:'/sendKV',
//         dataType: 'json',
//         data: JSON.stringify({
//             key:$("#kv_key").val(),
//             value:$("#kv_value").val(),
//             name:getBotID()
//         }),
//         contentType: 'application/json'
//     });
// }
