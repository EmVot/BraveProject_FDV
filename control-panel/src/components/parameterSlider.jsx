import React, { useState, useEffect } from "react";

function ParameterSlider({ label, param, min, max, step = 1, value, disabled = false, onChange }) {
  const [internal, setInternal] = useState(min);

  useEffect(() => {
    setInternal(min);
    if (!disabled) {
      onChange(param, min);
    }
  }, [min, param]);

  useEffect(() => {
    if (value !== undefined) setInternal(value);
  }, [value]);

  const current = value !== undefined ? value : internal;

  const handleChange = (e) => {
    const newValue = Number(e.target.value);
    if (value === undefined) setInternal(newValue);
    if (!disabled) onChange(param, newValue);
  };

  return (
    <div
      className={`control option-selector-horizontal ${disabled ? "disabled" : ""}`}
      style={{ opacity: disabled ? 0.5 : 1 }}
    >
      <label className="option-label-inline">{label}</label>
      <input
        type="range"
        min={min}
        max={max}
        value={current}
        step={step}
        onChange={handleChange}
        disabled={disabled}
      />
    </div>
  );
}

export default ParameterSlider;