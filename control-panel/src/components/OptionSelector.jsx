import React, { useState, useEffect } from "react";

function OptionSelector({ label, param, options, onChange, forceValue }) {
  const [selected, setSelected] = useState("calm");

  // forza selezione (es. quando darkness < 10.5 → calm)
  useEffect(() => {
    if (forceValue && forceValue !== selected) {
      setSelected(forceValue);
    }
  }, [forceValue, selected]);

  const handleSelect = (opt) => {
    if (opt.disabled) return;
    setSelected(opt.value);
    onChange(param, opt.value);
  };

  return (
    <div className="control option-selector-horizontal">
      <label className="option-label-inline">{label}:</label>
      <div className="option-buttons-inline">
        {options.map((opt, index) => (
          <button
            key={index}
            className={`option-button ${selected === opt.value ? "selected" : ""} ${opt.disabled ? "disabled" : ""}`}
            onClick={() => handleSelect(opt)}
            disabled={!!opt.disabled}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default OptionSelector;