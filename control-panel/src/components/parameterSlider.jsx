
function ParameterSlider({ label, min, max, step = 1 }) {
  
  return (
    <div style={{ margin: "15px 0" }}>
      <label>{label}</label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
      />
    </div>
  );
}

export default ParameterSlider;