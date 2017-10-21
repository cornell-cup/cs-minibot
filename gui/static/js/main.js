var React = require('react');
var ReactDOM = require('react-dom');
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import Python from './components/python.js';
import Blockly from './components/blockly.js';
import ControlPanel from './components/controlpanel.js';
import Scenarios from './components/scenarios.js';
import AddBot from './components/addbot.js';
import GridView from './components/gridview.js';

//var Python = require('./components/python.js');

class Navbar extends React.Component {
    render () {
        return (
            <div className="navbar">
                <img className="logo" src = "./static/img/logo.png"/><h1>MiniBot GUI</h1>
            </div>
        )
    }
}

class Platform extends React.Component {
    render() {
        return (
            <div id='platform'>
                <Navbar/>
                <Tabs>
                    <TabList>
                        <Tab>Setup</Tab>
                        <Tab>Coding/Control</Tab>
                    </TabList>

                    <TabPanel>
                        <SetupTab />
                    </TabPanel>
                    <TabPanel>
                        <ControlTab />
                    </TabPanel>
                </Tabs>
            </div>
        )
    }
}
//Setup Tab
class SetupTab extends React.Component {
    render() {
        return (
            <div id ="tab_setup">
                <div className="row">
                    <div className="col-md-6">
                        <AddBot/>
                        <GridView/>
                    </div>
                    <div className="col-md-6">
                        <Scenarios/>
                    </div>
                </div>
            </div>
        )
    }
}


//Control Tab
class ControlTab extends React.Component {
    render(){
        return (
            <div id ="tab_control">
                <div className="row">
                    <div className="col-md-7">
                        <Blockly/>
                        <GridView/>
                    </div>
                    <div className="col-md-5">
                        <Python/>
                        <ControlPanel/>
                    </div>
                </div>
            </div>
        )
    }
}

ReactDOM.render(
    <Platform/>, document.getElementById('root')
);