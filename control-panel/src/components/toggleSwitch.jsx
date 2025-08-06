import React, { useState } from "react";

function ToggleSwitch({ label, param, onChange }) {
  const [checked, setChecked] = useState(false);

  const handleToggle = () => {
    const newVal = !checked;
    setChecked(newVal);
    onChange(param, newVal);
  };

  return (
    <div className="control toggle-switch-row">
      <label className="option-label-inline">{label}</label>
      <label className="switch">
        <input type="checkbox" checked={checked} onChange={handleToggle} />
        <span className="slider"></span>
      </label>
    </div>
  );
}

export default ToggleSwitch;