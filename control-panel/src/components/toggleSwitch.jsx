import React, { useState } from "react";

function ToggleSwitch({ label, param, onChange }) {
  const [checked, setChecked] = useState(false);

  const handleToggle = () => {
    const newVal = !checked;
    setChecked(newVal);
    onChange(param, newVal);
  };

  return (
    <div style={{ margin: "15px 0" }}>
      <label>{label}</label>
      <input type="checkbox" checked={checked} onChange={handleToggle} />
    </div>
  );
}

export default ToggleSwitch;