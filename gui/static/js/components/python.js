var React = require('react');
var ReactDOM = require('react-dom');
var axios = require('axios');

/**
 * Component for the Python text box
 * Contains:
 * upload, download, send script
 */
export default class Python extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            filename:"myBlocklyCode.py",
            data: ""
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.download = this.download.bind(this);
        this.upload = this.upload.bind(this);
        this.send = this.send.bind(this);
        this.handleKeyInput = this.handleKeyInput.bind(this);
    }

    /* handles input change for file name and coding textboxes */
    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
        if (name=="data") {document.getElementById("data").value = this.state.data;}
    }


    /* DOWNLOAD FUNCTION
       Allows users to download raw code as a file. Users must
       manually input file name and file ext.
    */
    download(event){
        console.log("download listener");
        event.preventDefault();
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(this.state.data));
        element.setAttribute('download', this.state.filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }

    /* UPLOAD FUNCTION
        Allows users to upload previously written code as a file
        so that they may run Python scripts that have been written
        externally without Blockly.
    */

    upload(event){
        console.log("upload listener");
        var _this = this;
        var file = event.target.files[0];
        var reader = new FileReader();
        reader.onload = function(event) {
            _this.state.data = event.target.result;
            document.getElementById("data").value = event.target.result;
        };
        reader.readAsText(file);
    }

    /* Handler for key input; allows for tabs (4 spaces!!) in text box */
    handleKeyInput(event){
        if(event.keyCode===9){
            event.preventDefault();
            var data = this.state.data;
            var v=data.value;
            var s=data.selectionStart;
            var e=data.selectionEnd;
            data.value=v.substring(0, s)+'    '+v.substring(e);
            data.selectionStart=this.selectionEnd=s+1;
        }
    }

    /*
      RUN/SEND FUNCTION
      Clicking "run" will send Blockly scripts to the base station for
      the actual MiniBot.
    */
    send(){
            axios({
                method:'POST',
                url:'/sendKV',
                data: JSON.stringify({
                    key: 'SCRIPT',
                    value: document.getElementById('data').value,
                    name: this.props.currentBot
                }),
            })
            .then(function(response) {
                console.log('sent script');
            })
            .catch(function (error) {
                console.warn(error);
            });
    }

    render(){
        return (
            <div id ="python" className ="box">
                Python
                File Name: <input type="text" name="filename" value={this.state.filename} onChange={this.handleInputChange}/><br/>
                <textarea name="data" id="data" value={this.state.data} onChange={this.handleInputChange} onKeyDown={this.handleKeyInput} ></textarea><br/>
                    <button id="submit" onClick={this.download}>Download</button>
                <button id="send" onClick={this.send}>Run Code</button>
                <form>
                    <input
                        type="file"
                        id="upload"
                        multiplesize="1"
                        accept=".py"
                        onChange = {this.upload}
                    />
                </form>
            </div>
        )
    }
}