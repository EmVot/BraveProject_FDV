import React, { useState } from "react";

function ParameterSlider({ label, param, min, max, step = 1, onChange }) {
  const [value, setValue] = useState(9);

  const handleChange = (e) => {
    const newValue = Number(e.target.value);
    setValue(newValue);
    onChange(param, newValue);
  };

  return (
    <div className="control option-selector-horizontal">
      <label className="option-label-inline">{label}</label>
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        step={step}
        onChange={handleChange}
      />
    </div>
  );
}

export default ParameterSlider;