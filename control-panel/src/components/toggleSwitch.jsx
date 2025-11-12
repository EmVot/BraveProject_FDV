import React, { useState } from "react";

function ToggleSwitch({
  label,
  param,
  onChange,
  disabled = false,
  momentary = false,      
  autoResetDelay = 300,  
  onAutoReset,            
}) {
  const [checked, setChecked] = useState(false);

  const handleToggle = () => {
    if (disabled) return;

    if (!checked) {
      setChecked(true);
      onChange?.(param, true);

      if (momentary) {
        setTimeout(() => {
          setChecked(false);
          onAutoReset?.(param);
        }, autoResetDelay);
      }
    } else {
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