var React = require('react');

/**
 * Component for the new scenarios system
 * Will contain:
 * Loading, saving, editing, adding scenarios to simulator
 *
 */
export default class Scenarios extends React.Component {
    //TODO WIP
    constructor(props) {
        super(props);
        this.state = {
            scenario: {}, //a scenario JSON, initially empty
            filename: ""
        };

        this.editScenario = this.editScenario.bind(this);

        this.addScenario = this.addScenario.bind(this);
        this.saveScenario = this.saveScenario.bind(this);
        this.loadScenario = this.loadScenario.bind(this);
    }

    editScenario(event){
        /* TODO handles when any scenario object is edited
        This does NOT change anything, it constructs a scenario JSON from the scenarioObject JSONs
        in the child components, and then passes it to changeScenario
        */
        console.log('the current scenario has been edited');
        var scenario = {};
        this.changeScenario(scenario);
    }

    /* changes the scenario in state and on the display, takes JSON as input*/
    changeScenario(scenario){
        //TODO
        console.log("change scenario listener");
    }

    /* handler for add scenario (load currently displayed scenario into simulator) */
    addScenario(event){
        console.log("add scenario listener");
        axios({
            method:'POST',
            url:'/addScenario',
            data: JSON.stringify(this.state.scenario),
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

    saveScenario(event){
        console.log("save scenario listener");

        var scenario = this.state.scenario;
        var filename = this.state.filename;

        //Implemented the same way as Python script saving. This might not work so use axios code if it doesn't
        event.preventDefault();
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(this.state.scenario)));
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
            var scenario = JSON.parse(event.target.result);
            _this.state.scenario = scenario;
            _this.changeScenario(scenario);
        };
        reader.readAsText(file);
    }

    render() {
        return(
            <div id ="component_scenarios" className = "box">Scenarios</div>
        )
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