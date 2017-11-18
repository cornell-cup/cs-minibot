/*
	Code generators for custom blocks.
*/

// ================ MOVE BLOCK ================ //
Blockly.Blocks['move'] = {
  init: function() {
    this.jsonInit(miniblocks.move);
  }
};

Blockly.Python['move'] = function(block) {
	// from blockly
  var dropdown_direction = block.getFieldValue('direction');
	var number_speed = block.getFieldValue('speed');
	
  //string representation of function
  var fcn = {
    fwd: "move_forward(",
    bkw: "move_backward("
  }[dropdown_direction];
	return [fcn+number_speed+")", Blockly.Python.ORDER_NONE];
};

// ================ TURN BLOCK ================ //
Blockly.Blocks['turn'] = {
  init: function() {
    this.jsonInit(miniblocks.turn);
  }
};

Blockly.Python['turn'] = function(block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_power = block.getFieldValue('power');
  var code = dropdown_direction+"("+number_power+")";
  return [code, Blockly.Python.ORDER_NONE];
};

// ================ SET WHEELPOWER BLOCK ================ //
Blockly.Blocks['setwheelpower'] = {
  init: function() {
    this.jsonInit(miniblocks.setwheelpower);
  }
};
Blockly.Python['setwheelpower'] = function(block) {
  var wheels = ['FL', 'FR', 'BL', 'BR']
  var power = [0,0,0,0];

  // dealing with wrong inputs
  for(var i=0; i<4; i++){
    power[i] = Blockly.Python.valueToCode(block, wheels[i], Blockly.Python.ORDER_ATOMIC) || 0;
    if(power[i] < 100) {
    }
    else if(power[i] > 100) {
      alert("Oops! Please insert a number between 0 and 100.");
      power[i] = 100;
    }
    else {
      alert("Oops! Please insert a number between 0 and 100.");
      power[i] = 0;
    }
  }
  var code = 'set_wheel_power(' 
    + power[0] + ',' 
    + power[1] + ',' 
    + power[2] + ',' 
    + power[3] + ')';
  return [code, Blockly.Python.ORDER_NONE];
};

// ================== WAIT BLOCK ================== //
Blockly.Blocks['wait'] = {
  init: function(){
    this.jsonInit(miniblocks.wait);
  }
};
Blockly.Python['wait'] = function(block) {
  var time = Blockly.Python.valueToCode(block, 'time', Blockly.Python.ORDER_ATOMIC) || 0;
  var code = 'wait(' + time + ')';
  return [code, Blockly.Python.ORDER_NONE];
};

// ================== COLOR SENSOR BLOCK ================== //
Blockly.Blocks['minibot_color'] = {
  init: function(){
    this.jsonInit(miniblocks.minibot_color);
  }
};

Blockly.Python['minibot_color'] = function(block) {
  var dropdown_hue = block.getFieldValue('hue');
  var code = 'colorSensed = ' + dropdown_hue;
  return [code, Blockly.Python.ORDER_NONE];
};

//* NEW BLOCK TEST *//

// ================ MOVE BLOCKS ================ //

Blockly.Blocks['move_power'] = {
  init: function() {
    this.jsonInit(miniblocks.move_power);
  }
};

Blockly.Python['move_power'] = function(block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_speed = block.getFieldValue('speed');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Blocks['move_power_time'] = {
  init: function() {
    this.jsonInit(miniblocks.move_power_time);
  }
};

Blockly.Python['move_power_time'] = function(block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_speed = block.getFieldValue('speed');
  var number_seconds = block.getFieldValue('seconds');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Blocks['stop_moving'] = {
  init: function() {
    this.jsonInit(miniblocks.stop_moving);
  }
};

Blockly.Python['stop_moving'] = function(block) {
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Blocks['set_power'] = {
  init: function() {
    this.jsonInit(miniblocks.set_power);
  }
};

Blockly.Python['set_power'] = function(block) {
  var dropdown_motor_name = block.getFieldValue('motor_name');
  var number_speed = block.getFieldValue('speed');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

// ================ TURN BLOCKS ================ //

Blockly.Blocks['turn_power'] = {
  init: function() {
    this.jsonInit(miniblocks.turn_power);
  }
};

Blockly.Python['turn_power'] = function(block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_percent = block.getFieldValue('percent');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Blocks['turn_power_time'] = {
  init: function() {
    this.jsonInit(miniblocks.turn_power_time);
  }
};

Blockly.Python['turn_power_time'] = function(block) {
  var dropdown_direction = block.getFieldValue('direction');
  var number_percent = block.getFieldValue('percent');
  var number_seconds = block.getFieldValue('seconds');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

// ================ WAIT BLOCK ================ //

Blockly.Blocks['wait_seconds'] = {
  init: function() {
    this.jsonInit(miniblocks.wait_seconds);
  }
};

Blockly.Python['wait_seconds'] = function(block) {
  var number_seconds = block.getFieldValue('seconds');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

// ================ COMMUNICATION BLOCKS ================ //

Blockly.Blocks['send_commands'] = {
  init: function() {
    this.jsonInit(miniblocks.send_commands);
  }
};

Blockly.Python['send_commands'] = function(block) {
  var dropdown_bot_name = block.getFieldValue('bot_name');
  var statements_send_commands = Blockly.Python.statementToCode(block, 'send_commands');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Blocks['wait_for_commands'] = {
  init: function() {
    this.jsonInit(miniblocks.wait_for_commands);
  }
};

Blockly.Python['wait_for_commands'] = function(block) {
  var dropdown_bot_name = block.getFieldValue('bot_name');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Blocks['while_wait_for_commands'] = {
  init: function() {
    this.jsonInit(miniblocks.while_wait_for_commands);
  }
};

Blockly.Python['while_wait_for_commands'] = function(block) {
  var dropdown_bot_name = block.getFieldValue('bot_name');
  var statements_wait_commands = Blockly.Python.statementToCode(block, 'wait_commands');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

// ================ COLOR SENSING BLOCKS ================ //

Blockly.Blocks['sees_color'] = {
  init: function() {
    this.jsonInit(miniblocks.sees_color);
  }
};

Blockly.Python['sees_color'] = function(block) {
  var dropdown_sensor_name = block.getFieldValue('sensor_name');
  var dropdown_color_name = block.getFieldValue('color_name');
  // TODO: Assemble Python into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.Python.ORDER_NONE];
};