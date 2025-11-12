import React, { useState, useEffect, useRef } from "react";

function ParameterSlider({
  label,
  param,
  min,
  max,
  step = 1,
  value,
  disabled = false,
  onChange,
}) {
  const [internal, setInternal] = useState(min);

  // Keep track of the last initialization inputs so we only re-init when they truly change
  const initRef = useRef({ min, param, disabled });

  // Re-init when min/param/disabled actually change
  useEffect(() => {
    const changed =
      initRef.current.min !== min ||
      initRef.current.param !== param ||
      initRef.current.disabled !== disabled;

    if (changed) {
      // Ensure current value stays within the new bounds
      const next = Math.min(Math.max(min, value ?? internal), max);
      setInternal(next);
      if (!disabled && typeof onChange === "function") {
        onChange(param, next);
      }
      initRef.current = { min, param, disabled };
    }
  }, [min, max, param, disabled, onChange, value, internal]);

  // If the component is controlled, mirror external value
  useEffect(() => {
    if (value !== undefined) {
      const clamped = Math.min(Math.max(value, min), max);
      setInternal(clamped);
    }
  }, [value, min, max]);

  const current = value !== undefined ? value : internal;

  const handleChange = (e) => {
    const newValue = Number(e.target.value);
    if (value === undefined) setInternal(newValue);
    if (!disabled && typeof onChange === "function") {
      onChange(param, newValue);
    }
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