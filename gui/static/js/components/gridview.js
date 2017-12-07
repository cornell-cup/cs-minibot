var React = require('react');
var axios = require('axios');

/**
 * Component for the grid view of the simulated bots.
 */
export default class GridView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            ms_per_update: 33, // modbot update interval in ms
            tracked_objects: [], //list of JSON objects representing either bots or obstacles
            viewWidth:  520, //size of simulator display in pixels
            startScale: 4, //number of meters displayed by simulator at start, 4 is 4x4 meters

            x_int: 520/4, // actual spacing between grid lines
            y_int: 520/4,

            scale: 100, //percentage, 100% is equal to 4x4 grid displayed, with each grid being 130pixels wide
            xOffset: 0, //for purposes of adjusting viewport, this is a raw pixel value
            yOffset: 0, //same as above

            // pixi elements for displaying information
            stage: new PIXI.Container(),
            back: new PIXI.Container(),
            botContainer: new PIXI.Container(),
            gridContainer: new PIXI.Container(),
            grid: PIXI.autoDetectRenderer(520, 520),
            imageLoader: PIXI.loader,

            // occupancy matrix
            listBots: [],
            occupancyMatrix: null,
            path: null,
            foundPath: false,
            omPresent: false,

            backgroundSprite: null,
            lock: false,
            lastTime: new Date()
        };

        // Setup
        this.setup = this.setup.bind(this);
        this.drawGridLines = this.drawGridLines.bind(this);

        // Display
        this.displayObjects = this.displayObjects.bind(this);
        this.drawBot = this.drawBot.bind(this);
        this.drawScenarioObject = this.drawScenarioObject.bind(this);

        // Occupancy Matrix
        this.displayOccupancyMatrix = this.displayOccupancyMatrix.bind(this);
        this.padOccupancyMatrix = this.padOccupancyMatrix.bind(this);
        this.fillOccupancyMatrix = this.fillOccupancyMatrix.bind(this);

        // Helper functions
        this.toDegrees = this.toDegrees.bind(this);
        this.newBot = this.newBot.bind(this);
        this.getNewVisionData = this.getNewVisionData.bind(this);
        // TODO (#73): Implement pollBotNames().
        // this.pollBotNames = this.pollBotNames.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    }

    /**
     * Executes after the component gets rendered.
     **/
    componentDidMount() {
        // TODO (#73): Implement background image loading.
        $("#view").append(this.state.grid.view);

        /* temporarily disabled background image loading */
        // try {
        //     var loadUrl = 'static/img/line.png';
        //     var imageLoader = this.state.imageLoader;
        //     imageLoader.add('background', loadUrl);
        //     imageLoader.once("complete", ()=>{this.imageLoaded();});
        //     imageLoader.load();
        // }
        // catch (err) {
        //     console.log("background failed to load! using white background");
        //     var background = PIXI.Texture.WHITE;
        //     background.width = 1300;
        //     background.height = 1300;
        //     this.setup(background);
        // }

        console.log("using white background");
        var background = PIXI.Texture.WHITE;
        this.setup(background);
    }

    /**
     * Handler for input changes to modify the state.
     * @param {Event} event Event which triggers input change.
     **/
    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        this.setState({
            [name]: value
        });

        // Handles zooming and panning
        if(name=="xOffset"||name=="yOffset"||name=="scale"){
            const scale = this.state.scale;
            const VIEW_WIDTH = this.state.viewWidth;

            this.state.x_int = VIEW_WIDTH/4*(scale/100);
            this.state.y_int = VIEW_WIDTH/4*(scale/100);

            var stage = this.state.stage;
            var grid = this.state.grid;

            this.state.gridContainer.removeChildren();
            this.state.botContainer.removeChildren();
            this.drawGridLines();

            if(this.state.occupancyMatrix !== null) {
                this.displayOccupancyMatrix(40, 40, 1.0);
            }

            this.displayObjects();
            // TODO (#73): Impelment fillOccupancyMatrix().
            // this.fillOccupancyMatrix(scale, x, y);
            grid.render(stage);
        }
    }

    /**
      * Helper function which takes in a number for radians and
      * outputs a number for degrees.
      * @param {float} radians Radian value to convert to degrees.
      * @return {float} Converted value (in degrees).
      */
    toDegrees(radians) {
        return 180 * radians / Math.PI;
    }

    /**
     * Handler for when background image has loaded successfully.
     **/
    imageLoaded(){
        console.log('background successfully loaded!');
        var background = PIXI.Texture.fromImage('static/img/line.png');
        this.setup(background);
    }

    /**
     * Continue setup of GridView
     * @param {PIXI.Texture} background Texture object for the background
     *     of the GridView.
     **/
    setup(background) {
        console.log('setting up grid view');
        const backgroundSprite = new PIXI.Sprite(background);
        const scale = this.state.scale;

        backgroundSprite.scale.x =  1300*scale/100;
        backgroundSprite.scale.y =  1300*scale/100;

        backgroundSprite.position.x = 0;
        backgroundSprite.position.y = 0;

        this.state.backgroundSprite = backgroundSprite;
        this.state.back.addChild(backgroundSprite);

        this.drawGridLines();
        this.displayObjects();

        this.getNewVisionData();
        // this.pollBotNames();

        var stage = this.state.stage;
        stage.addChild(this.state.back);
        stage.addChild(this.state.botContainer);
        stage.addChild(this.state.gridContainer);

        var grid = this.state.grid;
        grid.view.style.border = "1px dashed black";
        grid.view.style.position = "absolute";
        grid.view.style.display = "block";
        grid.render(stage);
    }

    /**
     *  Sets up grid lines within view.
     *  - 40x40 grid, 4x4 initially visible
     *  - standard coordinate system: 1 unit = 1 meter
     *  - start position: bottom left corner = (0,0)
     **/
    drawGridLines() {
        var lines_y = [];
        var lines_x = [];
        var VIEW_WIDTH = this.state.viewWidth;
        const scale = this.state.scale;
        const xOffset = parseInt(this.state.xOffset);
        const yOffset = parseInt(this.state.yOffset);
        const x_int = this.state.x_int;
        const y_int = this.state.y_int;

        for(var i=0; i<40; i=i+1){
            //horizontal lines
            lines_y[i] = new PIXI.Graphics();
            lines_y[i].lineStyle(1, 0x0000FF, 1);

            lines_y[i].moveTo(0,VIEW_WIDTH-(i-20)*y_int+yOffset);
            lines_y[i].lineTo(VIEW_WIDTH,VIEW_WIDTH-(i-20)*y_int+yOffset);

            this.state.gridContainer.addChild(lines_y[i]);

            //vertical lines
            lines_x[i] = new PIXI.Graphics();
            lines_x[i].lineStyle(1, 0x0000FF, 1);

            lines_x[i].moveTo((i-20)*x_int+xOffset,0);
            lines_x[i].lineTo((i-20)*x_int+xOffset,VIEW_WIDTH);
            this.state.gridContainer.addChild(lines_x[i]);
        }
    }

    /**
     * Pseudo-constructor for a bot object.
     *
     * @param {float} x The x coordinate of new bot.
     * @param {float} y The y coordinate of new bot.
     * @param {float} angle The angle of new bot, in radians.
     * @param {string} id The id for the new bot.
     * @param {float} size The size of the new bot, in meters
     * @return {Object} Object which contains information about
     *     the virtual bot.
    */
    newBot(x, y, angle, id, size, type) {
        // TODO: Create a Bot class.
        var bot = {
            x: x,
            y: y,
            angle: angle,
            id: id,
            size: size,
            type: type
        };
        return bot;
    }

    /**
     * Displays all objects being tracked by the gridview.
     **/
    displayObjects() {
        const botArray = this.state.tracked_objects;
        const scale = this.state.scale;
        const xOffset = parseInt(this.state.xOffset);
        const yOffset = parseInt(this.state.yOffset);
        for(var b=0; b<botArray.length;b++) {
            if (botArray[b].type=='bot'){
                this.drawBot(botArray[b]);
            } else {
                this.drawScenarioObject(botArray[b]);
            }
        }
    }

    /**
     * Draws a single bot onto the GridView centered at (x, y).
     * @param {Object} b JSON object representing a bot.
     **/
    drawBot(b) {
        const scale = this.state.scale;
        const xOffset = parseInt(this.state.xOffset);
        const yOffset = parseInt(this.state.yOffset);
        const VIEW_WIDTH = this.state.viewWidth;
        const x_int = this.state.x_int;
        const y_int = this.state.y_int;
        if (b.size == 0) b.size = 1;
        var size = b.size*x_int;
        var bot = new PIXI.Graphics();
        bot.beginFill(0x0EB530); //green
        bot.drawRect(0, 0, size, size);
        bot.pivot = new PIXI.Point(size/2, size/2);
        bot.rotation = -b.angle;
        bot.endFill();

        var cx = (b.x)*x_int+xOffset;
        var cy = VIEW_WIDTH - ((b.y)*y_int)+yOffset;
        bot.x = cx;
        bot.y = cy;

        // draw bot coordinate text
        let botCoordText = new PIXI.Text('(' + b.x.toFixed(2) + ',' + b.y.toFixed(2) + ',' + toDegrees(b.angle).toFixed(2) + ')',{fontFamily : 'Arial', fontSize: 11, fill : 0xff1010, align : 'center'});
        botCoordText.x = cx;
        botCoordText.y = cy + 14; //arbitrary constant for offset

        var sensor1 = new PIXI.Graphics();
        sensor1.beginFill(0xFF0000); //red
        sensor1.drawCircle(0, 0, size/10);
        sensor1.endFill();

        var sensor2 = new PIXI.Graphics();
        sensor2.beginFill(0xFF0000); //red
        sensor2.drawCircle(0, 0, size/10);
        sensor2.endFill();

        sensor1.x = cx+size/Math.sqrt(3)*Math.cos(b.angle+Math.PI/6);
        sensor1.y = cy-size/Math.sqrt(3)*Math.sin(b.angle+Math.PI/6);

        sensor2.x = cx+size/Math.sqrt(3)*Math.cos(b.angle-Math.PI/6);
        sensor2.y = cy-size/Math.sqrt(3)*Math.sin(b.angle-Math.PI/6);

        var botContainer = this.state.botContainer;
        botContainer.addChild(bot);
        botContainer.addChild(sensor1);
        botContainer.addChild(sensor2);
        botContainer.addChild(botCoordText);
    }

    /**
     * Draw a single scenario object onto the GridView
     * at (x, y).
     * @param {Object} scenario_obj Scenario object.
     */
    drawScenarioObject(scenario_obj) {
        const scale = this.state.scale;
        const xOffset = parseInt(this.state.xOffset);
        const yOffset = parseInt(this.state.yOffset);
        const VIEW_WIDTH = this.state.viewWidth;
        const x_int = this.state.x_int;
        const y_int = this.state.y_int;

        var size = scenario_obj.size*x_int;
        var scenarioObject = new PIXI.Graphics();

        scenarioObject.beginFill(0x0EB530);
        scenarioObject.drawRect(0, 0, size, size);
        scenarioObject.pivot = new PIXI.Point(size/2, size/2);
        scenarioObject.rotation = scenario_obj.angle;
        scenarioObject.endFill();

        var cx = (scenario_obj.x)*x_int;
        var cy = VIEW_WIDTH - ((scenario_obj.y)*y_int);
        scenarioObject.x = cx+xOffset;
        scenarioObject.y = cy+yOffset;

        this.state.botContainer.addChild(scenarioObject);
    }

    // TODO (#73): Implement or remove pollBotNames().
    // pollBotNames() {
    //     axios({
    //         method:'GET',
    //         url:'/trackedBots',
    //         dataType: 'json'
    //     })
    //     .then(function(response) {
    //         console.log('polled bot names');
    //         var data = response.data;
    //         var listBotsPrev = this.state.listBots;
    //         var listBots = [];
    //         for (var b in data) {
    //             var bot = data[b];
    //             listBots.push({name: bot.name});
    //         }
    //         // if (listBots.length !== listBotsPrev.length) {
    //         //     this.redoDropdown(listBots);
    //         // } else {
    //         //     for(let i = 0; i < listBots.length; i=i+1) {
    //         //         if (listBots[i].name !== listBotsPrev[i].name) {
    //         //             this.redoDropdown(listBots);
    //         //             break;
    //         //         }
    //         //     }
    //         // }
    //         setTimeout(this.pollBotNames,2000);
    //     }).catch(function (error) {
    //         console.warn(error);
    //         setTimeout(this.pollBotNames,2000);
    //     });
    // }

    /**
     * Updates location of bots on grid after getting location
     * information from the BaseStation.
     **/
    getNewVisionData() {
        const _this = this;
        const MILLIS_PER_VISION_UPDATE = 66;
        try {
            axios({
                url: '/updateloc',
                method: 'GET',
                dataType: 'json'
            }).then(
                function visionDataGot(response) {
                    var data = response.data;
                    var currentTime = new Date();
                    var elapsed = (currentTime - _this.state.lastTime);
                    _this.state.lastTime = currentTime;
                    var timeout = MILLIS_PER_VISION_UPDATE;
                    if (elapsed > MILLIS_PER_VISION_UPDATE) {
                        timeout = 2*MILLIS_PER_VISION_UPDATE - elapsed;
                        if (timeout < 0) {
                            timeout = 0;
                        }
                    }
                    setTimeout(_this.getNewVisionData,timeout);
                    var stage = _this.state.stage;
                    var grid = _this.state.grid;
                    var botContainer = _this.state.botContainer;
                    if (!_this.state.lock) {
                        _this.state.lock = true;
                        var visionData = [];
                        botContainer.removeChildren();
                        for (var b in data) {
                            var item = data[b];
                            visionData.push(_this.newBot(item.x, item.y, item.angle, item.id, item.size, item.type));
                        }
                        _this.state.tracked_objects = visionData;
                        stage.removeChild(_this.state.gridContainer);
                        _this.state.gridContainer = new PIXI.Container();
                        _this.drawGridLines();
                        stage.addChild(_this.state.gridContainer);
                        _this.displayObjects();
                        grid.render(stage);
                        _this.state.lock = false;
                    }
                }
            ).catch((error) => {
                console.warn(error);
                setTimeout(_this.getNewVisionData, MILLIS_PER_VISION_UPDATE * 10);
            });
        } catch (error) {
            console.warn(error);
            setTimeout(_this.getNewVisionData, MILLIS_PER_VISION_UPDATE * 10);
        }
    }

    /**
     * Displays occupancy matrix.
     * @param {int} height Height of matrix.
     * @param {int} width Width of matrix.
     * @param {int} size Size of matrix.
     */
    displayOccupancyMatrix(height, width, size) {
    // TODO (#73): Implement displaying occupancy matrix. Old code below.
    //     $.ajax({
    //         method: "POST",
    //         url: '/postOccupancyMatrix',
    //         dataType: 'json',
    //         data: JSON.stringify({
    //             height:height,
    //             width: width,
    //             size: size}),
    //         contentType: 'application/json',
    //         success: function(data) {
    //             console.log("Occupancy matrix post successful");
    //             omPresent = true;
    //             occupancyMatrix = data;
    //             occupancyMatrix = this.padOccupancyMatrix();
    //
    //             $.ajax({
    //                 method: "POST",
    //                 url: '/postDijkstras',
    //                 dataType: 'json',
    //                 data: JSON.stringify({
    //                     matrix: occupancyMatrix}),
    //                 contentType: 'application/json',
    //                 success: function(data) {
    //                     path = data;
    //                     this.fillOccupancyMatrix(scale, xOffset, yOffset);
    //                 }
    //             });
    //         }
    //     });
    }

    /**
     * Iterates through the occupancy matrix. When a 1 is encountered in a cell, all of the
     * adjacent cells will be marked by a 1. This is to increase the margin so that any path
     * planning algorithm will not choose a path too close to an obstacle.
     *
     * @returns {Array<Array<int>>} 2-D array of occupancy matrix.
     **/
    padOccupancyMatrix() {
        var occupancyMatrix = this.state.occupancyMatrix;
        var temp = [];
        for(var i = 0; i < occupancyMatrix.length; i++) {
            temp.push([]);
            for(var j = 0; j < occupancyMatrix[0].length; j++) {
                temp[i].push(occupancyMatrix[i][j]);
            }
        }
        for(var i = 0; i < occupancyMatrix.length; i++) {
            for(var j = 0; j < occupancyMatrix.length; j++) {
                if(occupancyMatrix[i][j] === 1) {
                    if(i-1 >= 0) {
                        temp[i-1][j] = 1;
                    }
                    if(i+1 < occupancyMatrix.length) {
                        temp[i+1][j] = 1;
                    }
                    if(j-1 >= 0) {
                        temp[i][j-1] = 1;
                    }
                    if(j+1 < occupancyMatrix[0].length) {
                        temp[i][j+1] = 1;
                    }
                    if(j-1 >= 0 && i-1 >= 0) {
                        temp[i-1][j-1] = 1;
                    }
                    if(j+1 < occupancyMatrix[0].length && i+1 < occupancyMatrix.length) {
                        temp[i+1][j+1] = 1;
                    }
                    if(j+1 < occupancyMatrix[0].length && i-1 > 0) {
                        temp[i-1][j+1] = 1;
                    }
                    if(j-1 > 0 && i+1 < occupancyMatrix.length) {
                        temp[i+1][j-1] = 1;
                    }
                }
            }
        }
        return temp;
    }

    /**
     * Populates the PIXI view with the squares corresponding to
     * the occupancy matrix and path.
     *
     * @param {int} scale Scaling of gridview.
     * @param {int} xOffset How much X value should be offset by.
     * @param {int} yOffset How much Y value should be offset by.
     **/
    fillOccupancyMatrix(scale, xOffset, yOffset) {
        const VIEW_WIDTH = this.state.viewWidth;
        const x_int = this.state.x_int;
        const y_int = this.state.y_int;
        var occupancyMatrix = this.state.occupancyMatrix;
        var path = this.state.path;
        var botContainer = this.state.botContainer;

        for(var i = 0; i < occupancyMatrix.length; i++) {
            for(var j = 0; j < occupancyMatrix[0].length; j++) {
                //If this cell corresponds to a cell on path to the occupancy matrix, color it purple
                if(path[i][j] == 1) {

                    var scenarioObject = new PIXI.Graphics();

                    scenarioObject.beginFill(0x8822A4);
                    scenarioObject.drawRect(0, 0, x_int, y_int);
                    scenarioObject.endFill();

                    var cx = (i)*x_int+xOffset;
                    var cy = (j)*y_int+yOffset;
                    scenarioObject.x = cx;
                    scenarioObject.y = cy;
                    botContainer.addChild(scenarioObject);
                }
                //If this cell corresponds to a cell that is filled in in the occupancy matrix, color it blackish
                else if(occupancyMatrix[i][j] == 1) {
                    var size = 65;
                    var scenarioObject = new PIXI.Graphics();

                    scenarioObject.beginFill(0x123212);
                    scenarioObject.drawRect(0, 0, x_int, y_int);
                    scenarioObject.endFill();

                    var cx = (i)*x_int+xOffset;
                    var cy = (j)*y_int+yOffset;
                    scenarioObject.x = cx;
                    scenarioObject.y = cy;
                    botContainer.addChild(scenarioObject);
                }
            }
        }
    }


    // TODO (#72): Implement keyboard control for panning. Old code shown below for reference.

    //     /* for moving the viewport */
    //     document.onkeydown = function (e) {
    //         let code = e.keyCode ? e.keyCode : e.which;
    //
    //         if (code === 37) {
    //             //move view left
    //             xOffset+=3;
    //         } else if (code === 39) {
    //             //move view right
    //             xOffset-=3;
    //
    //         } else if (code == 38) {
    //             //move view up
    //             yOffset+=3;
    //
    //         } else if (code == 40) {
    //             // move view down
    //             yOffset-=3;
    //         } else {
    //             return;
    //         }
    //
    //         gridContainer.removeChildren();
    //         botContainer.removeChildren();
    //         drawGridLines(scale, xOffset, yOffset);
    // //    displayOccupancyMatrix(40, 40, 1.0);
    //
    //         displayObjects(bots, scale, xOffset, yOffset);
    //         fillOccupancyMatrix(scale, xOffset, yOffset);
    //
    //         grid.render(stage);
    //     };
    // window.addEventListener("keydown", function(e) {
    //     // space and arrow keys
    //     if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
    //         e.preventDefault();
    //     }
    // }, false);

    render() {
        return(
            <div id ="component_view" className = "box">
                <table><tbody>
                    <tr>
                        <td className = "gridControlTable">Scale ({this.state.scale}):</td>
                        <td className = "gridControlTable"><input id="scale" type="range" name="scale" min="25" max="100" className = "gridControl" value={this.state.scale} defaultValue="100" onChange={this.handleInputChange}/></td>
                    </tr>
                    <tr>
                        <td className = "gridControlTable">X Offset ({this.state.xOffset}):</td>
                        <td className = "gridControlTable"><input id="xOffset" type="range" name="xOffset" min="-100" max="100" className = "gridControl" value={this.state.xOffset} defaultValue="0" onChange={this.handleInputChange}/></td>
                    </tr>
                    <tr>
                        <td className = "gridControlTable">Y Offset ({this.state.yOffset}):</td>
                        <td className = "gridControlTable"><input id="yOffset" type="range" name="yOffset" min="-100" max="100" className = "gridControl" value={this.state.yOffset} defaultValue="0" onChange={this.handleInputChange}/></td>
                    </tr>
                </tbody></table>
                <div id ="view"></div>
            </div>
        );
    }
}
