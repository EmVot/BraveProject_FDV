import React, { useState } from "react";

function ToggleSwitch({ label, param, onChange, disabled = false }) {
  const [checked, setChecked] = useState(false);

  const handleToggle = () => {
    if (disabled) return;
    const newVal = !checked;
    setChecked(newVal);
    onChange(param, newVal);
  };

  return (
    <div className={`control toggle-switch-row ${disabled ? "disabled" : ""}`}>
      <label className="option-label-inline">{label}</label>
      <label className={`switch ${disabled ? "switch-disabled" : ""}`}>
        <input type="checkbox" checked={checked} onChange={handleToggle} disabled={disabled} />
        <span className="slider"></span>
      </label>
    </div>
  );
}

export default ToggleSwitch;