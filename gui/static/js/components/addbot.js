var React = require('react');

var axios = require('axios');

/**
 * Component for displaying each discovered bot
 *
 */
class DiscoveredBot extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        var styles = {
            ipAddress: {
                float: "left",
                marginRight: 5,
                marginBottom: 0,
            },
            bottomSpacing: {
                marginBottom: 5
            }
        }
        return (
            <div style={styles.bottomSpacing} className="discoveredBot">
                <p style={styles.ipAddress}>{this.props.ip_address}</p>
                <button
                    id={'discoverBot' + this.props.idx}
                    value={this.props.ip_address}
                    onClick={() => this.props.changeIPAddress(this.props.ip_address)} className="btn btn-sm addBot">
                    Add
                </button>
            </div>
        )
    }
}


/**
 * Component for the add bot interface
 */
export default class AddBot extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            ip: "",
            port: "10000",
            name: "Bot0",
            type: "minibot",
            discoveredBots: [],
            trackedBots: []
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.updateDiscoveredBots = this.updateDiscoveredBots.bind(this);
        this.changeIPAddress = this.changeIPAddress.bind(this);
        this.addBot = this.addBot.bind(this);
        this.getTrackedBots = this.getTrackedBots.bind(this);
    }

    /**
     * Updates discovered bots and tracked bots before page load.
     */
    componentWillMount() {
        this.updateDiscoveredBots()
        this.getTrackedBots()
    }

    /**
     * Handles input change for input fields.
     */
    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }

    /**
     * Gets discovered bots.
     */
    updateDiscoveredBots(){
        const _this = this;
        axios({
            method:'POST',
            url:'/discoverBots',
        })
            .then(function(response) {
                _this.redoDiscoverList(response.data);
        })
            .catch(function (error) {
                console.log(error);
        });
    }

    /**
     * Updates list of discoverable bots.
     * @param {Object.<string>} data Array of data which contains IPs of discovered bots.
     */
    redoDiscoverList(data){
        let new_bots = [];

        for (let i = 0; i < data.length; i++) {
            var ip_address = data[i];
            new_bots.push(ip_address);
        }

        this.setState({discoveredBots: new_bots});
    }

    /**
     * Changes IP address in input box.
     */
    changeIPAddress(ip) {
        this.setState({ip: ip});
    }

    /**
     * Adds bot to basestation.
     */
    addBot() {
        const _this = this;
        axios({
            method:'POST',
            url:'/addBot',
            data: JSON.stringify({
                ip: this.state.ip,
                port: this.state.port,
                name: this.state.name,
                type: this.state.type
            })
            })
                .then(function(response) {
                    console.log('Succesfully Added');
                    _this.getTrackedBots()
            })
                .catch(function (error) {
                    console.log(error);
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
                    _this.setState({trackedBots: response.data})

            })
                .catch(function (error) {
                    console.log(error);
        });
    }

    render(){
        const _this = this;
        var styles = {
            ActiveBotHeader: {
                height: '25%'
            },
            ActiveBotTitle: {
                float: "left",
                marginRight: 5
            },
            addedBots: {
                marginBottom: 0,
            }
        }

        return (
            <div id ="component_addbot" className = "box">
                <div className = "row">
                    <div className = "col-md-6">
                        Add a Bot
                        <table>
                            <tbody>
                            <tr>
                                <th>IP: </th>
                                <th><input type="text" name="ip" id="ip" value={this.state.ip} onChange={this.handleInputChange}/></th>
                            </tr>
                            <tr>
                                <th>Port: </th>
                                <th><input type="text" name="port" id="port" value={this.state.port} onChange={this.handleInputChange}/></th>
                            </tr>
                            <tr>
                                <th>Name: </th>
                                <th><input type="text" name="name" id="name" value={this.state.name} onChange={this.handleInputChange}/></th>
                            </tr>
                            <tr>
                                <th>Type: </th>
                                <th>
                                    <select id="bot-type" name="type" value={this.state.type} onChange={this.handleInputChange}>
                                        <option value ="minibot">Minibot</option>
                                        <option value = "simbot">Simbot</option>
                                    </select>
                                </th>
                            </tr>
                            </tbody>
                        </table>
                        <button id="addBot" onClick={this.addBot}>Add Bot</button>

                        <div className="trackedBots">
                        {
                            this.state.trackedBots.map(function(name, key){
                                return <p key={key} style={styles.addedBots}>{name}</p>
                            })
                        }
                        </div>
                    </div>
                    <div className = "col-md-6">
                        <div className="activeBotHeader" style={styles.ActiveBotHeader}>
                            <p style={styles.ActiveBotTitle}>Select an Active Bot</p>
                            <button className="refresh-discovery" onClick={this.updateDiscoveredBots}>
                                Refresh
                            </button>
                        </div>
                        <div className="discoveredBots" id="discovered">
                            {
                                this.state.discoveredBots.map(function(ip, idx){
                                    return <DiscoveredBot
                                                key={idx}
                                                idx={idx}
                                                ip_address={ip}
                                                changeIPAddress={_this.changeIPAddress} />;
                                })
                            }
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}