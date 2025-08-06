import React, { useState } from "react";

function OptionSelector({ label, param, options, onChange }) {
  const [selected, setSelected] = useState("calm");

  const handleSelect = (value) => {
    setSelected(value);
    onChange(param, value);
  };

  return (
    <div className="control option-selector-horizontal">
      <label className="option-label-inline">{label}:</label>
      <div className="option-buttons-inline">
        {options.map((opt, index) => (
          <button
            key={index}
            className={`option-button ${selected === opt.value ? "selected" : ""}`}
            onClick={() => handleSelect(opt.value)}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default OptionSelector;