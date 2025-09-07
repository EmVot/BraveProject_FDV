import React, { useState } from "react";

function ToggleSwitch({
  label,
  param,
  onChange,
  disabled = false,
  momentary = false,      // se true: invia solo ON e poi torna OFF da solo
  autoResetDelay = 300,   // ms prima dell'auto-reset
  onAutoReset,            // callback opzionale: avvisa il parent che è tornato OFF
}) {
  const [checked, setChecked] = useState(false);

  const handleToggle = () => {
    if (disabled) return;

    if (!checked) {
      // Passaggio OFF -> ON
      setChecked(true);
      onChange?.(param, true);

      if (momentary) {
        setTimeout(() => {
          setChecked(false);
          // Non inviamo OFF al backend
          onAutoReset?.(param); // avvisa il parent per resettare eventuali stati esterni
        }, autoResetDelay);
      }
    } else {
      // Passaggio ON -> OFF (solo se NON momentary)
      if (!momentary) {
        setChecked(false);
        onChange?.(param, false);
      }
    }
  };

  return (
    <div className={`control toggle-switch-row ${disabled ? "disabled" : ""}`}>
      <label className="option-label-inline">{label}</label>
      <label className={`switch ${disabled ? "switch-disabled" : ""}`}>
        <input
          type="checkbox"
          checked={checked}
          onChange={handleToggle}
          disabled={disabled}
        />
        <span className="slider"></span>
      </label>
    </div>
  );
}

export default ToggleSwitch;