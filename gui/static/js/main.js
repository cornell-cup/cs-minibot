var React = require('react');
var ReactDOM = require('react-dom');
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';

/**
 * Component for the Navbar on top
 * Currently this does nothing except display some text and an image
 */
class Platform extends React.Component {
    render () {
        return (
            <div className="navbar">
                <h1>MiniBot GUI</h1>
            </div>
        )
    }
}

ReactDOM.render(
    <Platform/>, document.getElementById('root')
);