import React, { useState, useEffect } from "react";
import ParameterSlider from "./components/parameterSlider";
import ToggleSwitch from "./components/toggleSwitch";
import OptionSelector from "./components/OptionSelector";
import { sendMessage } from "./websocket";
import "./App.css";

function App() {
  const [darkness, setDarkness] = useState(10.5);
  const [rain, setRain] = useState(0);
  const [turbolence, setTurbolence] = useState(0);

  const [lightningOn, setLightningOn] = useState(false);
  const [masksOn, setMasksOn] = useState(false);

  const [forcedVoice, setForcedVoice] = useState("calm"); 

  const allDisabled = darkness < 10.5;

  const rainEnabled      = !allDisabled && darkness > 10.4;
  const lightningEnabled = rainEnabled && rain > 9999;
  const turbEnabled      = rainEnabled && rain > 9999;
  const rumblingEnabled  = rainEnabled && rain > 9999;

  const worriedEnabled   = rainEnabled && rain > 9999;
  const masksEnabled     = turbEnabled && turbolence > 0.0045;
  const panicEnabled     = turbEnabled && turbolence > 0.0045;

  useEffect(() => {
    if (darkness < 10.5) {
      setForcedVoice("calm");
      sendMessage({ type: "command", action: "toggle_param", param: "voices", value: "calm" });
    } else {
      setForcedVoice(undefined);
    }
  }, [darkness]);

  const safeSendToggle = (enabled, param, value) => {
    if (!enabled) return;
    sendMessage({ type: "command", action: "toggle_param", param, value });
  };

  const safeSendSlider = (enabled, param, value) => {
    if (!enabled) return;
    sendMessage({ type: "command", action: "update_param", param, value: Number(value) });
  };

  return (
    <div className="app">
      <h1 className="title">VR Control Panel</h1>
      <div className="panel">

        {/* DARKNESS */}
        <ParameterSlider
          label="Darkness"
          param="exposure"
          min={9}
          max={12}
          step={0.1}
          value={darkness}
          onChange={(p, v) => {
            // se Rain > 10000, non scende sotto 10.5
            const minClamp = (rain > 10000) ? 10.5 : 9;
            const clamped = v < minClamp ? minClamp : v;

            setDarkness(clamped);
            safeSendSlider(true, p, clamped);
          }}
        />

        {/* RAIN */}
        <ParameterSlider
          label="Rain Intensity"
          param="rain"
          min={0}
          max={20000}
          step={100}
          value={rain}
          disabled={!rainEnabled}
          onChange={(p, v) => {
            // se Lightning è ON, non scende sotto 10000
            const minClamp = lightningOn ? 10000 : 0;
            const clamped = v < minClamp ? minClamp : v;

            setRain(clamped);
            safeSendSlider(rainEnabled, p, clamped);
          }}
        />

        {/* LIGHTNING */}
        <ToggleSwitch
        label="Flash"
        param="flash"
        disabled={!lightningEnabled}
        momentary
        autoResetDelay={500} // opzionale
        onChange={(p, v) => {
          if (!lightningEnabled) return;
          if (v) {
            // invia SOLO ON
            setLightningOn(true); 
            sendMessage({ type: "command", action: "toggle_param", param: p, value: true });
          }
        }}
        onAutoReset={() => {
          setLightningOn(false);
        }}
      />



        {/* TURBOLENCE */}
        <ParameterSlider
          label="Turbolence"
          param="turbolence"
          min={0}
          max={0.015}
          step={0.001}
          value={turbolence}
          disabled={!turbEnabled}
          onChange={(p, v) => {
            // se Masks è ON, non scende sotto 0.005
            const minClamp = masksOn ? 0.005 : 0;
            const clamped = v < minClamp ? minClamp : v;

            setTurbolence(clamped);
            safeSendSlider(turbEnabled, p, clamped);
          }}
        />

        {/* RUMBLING */}
        <ToggleSwitch
          label="Rumbling"
          param="rumbling"
          disabled={!rumblingEnabled}
          onChange={(p, v) => safeSendToggle(rumblingEnabled, p, v)}
        />

        {/* OXYGEN MASKS */}
        <ToggleSwitch
          label="Oxygen Masks"
          param="oxygenMasks"
          disabled={!masksEnabled}
          onChange={(p, v) => {
            setMasksOn(v); 
            safeSendToggle(masksEnabled, p, v);
          }}
        />

        {/* VOICES */}
        <OptionSelector
          label="Voices"
          param="voices"
          options={[
            { label: "Calm",    value: "calm",    disabled: false },
            { label: "Worried", value: "worried", disabled: !worriedEnabled || allDisabled },
            { label: "Panic",   value: "panic",   disabled: !panicEnabled   || allDisabled },
          ]}
          forceValue={forcedVoice}
          onChange={(p, v) => {
            if (v === "worried" && (!worriedEnabled || allDisabled)) return;
            if (v === "panic"   && (!panicEnabled   || allDisabled)) return;
            safeSendToggle(true, p, v);
          }}
        />

      </div>
    </div>
  );
}

export default App;