import React from "react";
import ParameterSlider from "./components/ParameterSlider";
import ToggleSwitch from "./components/ToggleSwitch";
import OptionSelector from "./components/OptionSelector";
import { sendMessage } from "./websocket";
import "./App.css"; // importa il CSS

function App() {

  const handleToggleChange = (param, value) => {
    sendMessage({
      type: "command",
      action: "toggle_param",
      param,
      value,
    });
  };

  const handleSliderChange = (param, value) => {
    sendMessage({
      type: "command",
      action: "update_param",
      param,
      value: Number(value),
    });
  };


  return (
    <div className="app">
      <h1 className="title">VR Control Panel</h1>
      <div className="panel">
        <ParameterSlider
          label="Exposure"
          param="exposure"
          min={9}
          max={12}
          step={0.1}
          onChange={handleSliderChange}
        />
        <ParameterSlider
          label="Rain Intensity"
          param="rain"
          min={0}
          max={20000}
          step={100}
          onChange={handleSliderChange}
        />
        <ToggleSwitch
          label="Lightning"
          param="lightning"
          onChange={handleToggleChange}
        />
        <ParameterSlider
          label="Turbolence"
          param="turbolence"
          min={0}
          max={2}
          step={0.1}
          onChange={handleSliderChange}
        />
        <ToggleSwitch
          label="Rumbling"
          param="rumbling"
          onChange={handleToggleChange}
        />
        <ToggleSwitch
          label="Oxygen Masks"
          param="oxygenMasks"
          onChange={handleToggleChange}
        />
        <OptionSelector
          label="Voices"
          param="voices"
          options={[
            { label: "Calm", value: "calm" },
            { label: "Worried", value: "worried" },
            { label: "Panic", value: "panic" },
          ]}
          onChange={handleToggleChange}
        />

      </div>
    </div>
  );
}

export default App;
