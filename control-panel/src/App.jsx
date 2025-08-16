import React, { useState, useEffect } from "react";
import ParameterSlider from "./components/parameterSlider";
import ToggleSwitch from "./components/ToggleSwitch";
import OptionSelector from "./components/OptionSelector";
import { sendMessage } from "./websocket";
import "./App.css";

function App() {
  // stati locali per calcolare i vincoli
  const [darkness, setDarkness] = useState(10.5);
  const [rain, setRain] = useState(0);
  const [turbolence, setTurbolence] = useState(0);
  const [forcedVoice, setForcedVoice] = useState("calm"); // per forzare Calm quando serve

  // vincoli
  const allDisabled = darkness < 10.5;

  const rainEnabled      = !allDisabled && darkness > 10.5;
  const lightningEnabled = rainEnabled && rain > 10000;
  const turbEnabled      = rainEnabled && rain > 10000;
  const rumblingEnabled  = rainEnabled && rain > 10000;

  const worriedEnabled   = rainEnabled && rain > 10000;
  const masksEnabled     = turbEnabled && turbolence > 0.005;
  const panicEnabled     = turbEnabled && turbolence > 0.005;

  // quando Darkness scende sotto 10.5 → forza Calm
  useEffect(() => {
    if (darkness < 10.5) {
      setForcedVoice("calm");
      sendMessage({ type: "command", action: "toggle_param", param: "voices", value: "calm" });
    } else {
      // fuori dal blocco, non forziamo una voce specifica
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

        {/* DARKNESS: sempre abilitato */}
        <ParameterSlider
          label="Darkness"
          param="exposure"
          min={9}
          max={12}
          step={0.1}
          value={darkness}
          onChange={(p, v) => {
            setDarkness(v);
            safeSendSlider(true, p, v);
          }}
        />

        {/* RAIN: abilitato solo se darkness > 10.5 */}
        <ParameterSlider
          label="Rain Intensity"
          param="rain"
          min={0}
          max={20000}
          step={100}
          value={rain}
          disabled={!rainEnabled}
          onChange={(p, v) => {
            setRain(v);
            safeSendSlider(rainEnabled, p, v);
          }}
        />

        {/* LIGHTNING: abilitato se rain > 10000 */}
        <ToggleSwitch
          label="Lightning"
          param="lightning"
          disabled={!lightningEnabled}
          onChange={(p, v) => safeSendToggle(lightningEnabled, p, v)}
        />

        {/* TURBOLENCE: abilitato se rain > 10000 */}
        <ParameterSlider
          label="Turbolence"
          param="turbolence"
          min={0}
          max={0.015}
          step={0.001}
          value={turbolence}
          disabled={!turbEnabled}
          onChange={(p, v) => {
            setTurbolence(v);
            safeSendSlider(turbEnabled, p, v);
          }}
        />

        {/* RUMBLING: abilitato se rain > 10000 */}
        <ToggleSwitch
          label="Rumbling"
          param="rumbling"
          disabled={!rumblingEnabled}
          onChange={(p, v) => safeSendToggle(rumblingEnabled, p, v)}
        />

        {/* OXYGEN MASKS: abilitate se turbolence > 0.005 */}
        <ToggleSwitch
          label="Oxygen Masks"
          param="oxygenMasks"
          disabled={!masksEnabled}
          onChange={(p, v) => safeSendToggle(masksEnabled, p, v)}
        />

        {/* VOICES:
            - Calm sempre disponibile
            - Worried abilitato se rain > 10000
            - Panic   abilitato se turbolence > 0.005
            - Se darkness < 10.5 → forziamo calm
        */}
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
            // rispetta i vincoli anche qui
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
